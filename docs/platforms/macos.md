---
type: Guide
title: macOSの前提と管理境界
description: macOSでbootstrap・apply・認証・GUI app・生成物を扱う前提を確認する。
status: draft
generated:
  by: codex/gpt-6
  at: "2026-11-11T06:40:22+00:00"
sources:
  - id: config
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoi.toml.tmpl"
    title: "ホスト入力と1Password identity取得"
  - id: pbfile
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/build/executable_pbfile.tmpl"
    title: "macOS Swift build"
  - id: wezterm-link
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_local/bin/symlink_wezterm.tmpl"
    title: "macOS/WSLのWezTerm実体探索"
  - id: brew-script
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_before_provision-macos-homebrew.sh.tmpl"
    title: "Homebrewの導入・更新・bundle実行"
  - id: order
    resource: "https://www.chezmoi.io/reference/application-order/"
    title: "chezmoi公式：target計算とbefore/afterの順序"
  - id: apple-tools
    resource: "https://developer.apple.com/documentation/xcode/installing-the-command-line-tools"
    title: "Apple公式：command-line tools"
  - id: packages
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoidata/packages.yaml"
    title: "OS別package宣言"
  - id: brewfile
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/homebrew/Brewfile.tmpl"
    title: "macOS BrewfileとCI分岐"
  - id: brew
    resource: "https://docs.brew.sh/Brew-Bundle-and-Brewfile"
    title: "Homebrew公式：bundleの更新と版管理の限界"
  - id: docker-mac
    resource: "https://docs.docker.com/desktop/setup/install/mac-install/"
    title: "Docker公式：Macへの導入と起動"
---
# 対象と確認範囲

macOSはこのrepoの対象環境である。以下は2026-11-11に読んだsourceと公式資料による説明であり、この端末の導入版・起動状態・権限を調べた結果ではない。通常の操作順は[operations](../operations.md)、共通の所有表は[ownership](../ownership.md)を参照する。

利用者から、chezmoiで構築した後にmise関連のupgradeやbrew操作を直接行ったと報告されている。何をどの版へ変更したかは未調査である。現行pinへ戻す前提でbootstrapやdoctorを実行せず、[convergence](../decisions/convergence.md)の移行案に沿って採用する状態を判断する。

# 現行の前提

| 対象 | sourceが期待する状態 | sourceだけでは用意・保証しないこと |
|---|---|---|
| 1Password | 非CIのconfig生成時に`op`が使え、accountへ認証済み。署名helperとagentを利用 | appの初回設定、unlock、SSH agentの有効化、remoteへの鍵登録 |
| 開発tool | `build:pbfile`が`xcrun -sdk macosx swiftc`でSwift sourceをbuildする | 適切なSDK/toolchainが利用可能か。Xcodeまたは対応するCommand Line ToolsはOS側の前提 |
| WezTerm | symlink先に`/Applications/WezTerm.app/Contents/MacOS/wezterm`を使う | 別場所へのapp導入を探索することやGUI起動の成功 |
| Homebrew | before scriptがbrew導入・update・bundle installを担う | 一般のapplyに完全なversion固定や非更新性があること |

1Passwordがpackage宣言にあることだけでは初回の認証前提を満たさない。chezmoiはtarget stateを計算してからbefore scriptを実行するため、config/template評価に必要なものを後段のpackage installだけで用意できるとは考えない。[^config][^pbfile][^wezterm-link][^brew-script][^order]

AppleはXcodeに含まれるtoolと、単独のCommand Line Toolsを提供している。どのOS/SDKの組合せが必要かはその時点の公式対応表と実際のbuildで確認する。このrepoのために常にfull Xcodeを要求する根拠はない。[^apple-tools]

# Homebrew・mise・GUIの境界

package宣言にはbrewの`colima`とGUIの`docker-desktop`が共存する。ほかにもmiseとbrewで重なるCLIがある。宣言されていることを、実際に使うcommandやcontainer runtimeが決まっている証拠としない。brewの実体・miseの実体・PATH上の選択を分ける。[^packages]

現行before scriptの`brew update`と`brew bundle install`は更新を伴い得る。Brewfile templateにはCIでGUI appを省く分岐がある。通常のbundle installは既存の宣言対象もupgradeし得て、`--no-upgrade`も厳密なlockfileにはならない。手動で更新したbrewの状態を維持するか、宣言へ採用するかは、applyの責務と分けて決める。[^brew-script][^brewfile][^brew]

Docker Desktopはpackageがあること、appが起動していること、目的のCLI/context/daemonが使えることを分けて確認する。公式導入手順にもapp起動の段階がある。Colimaとのどちらを使うかをこの文案で決めず、実機の利用先を調べてから所有範囲を決める。両方を自動起動する案は採用していない。[^packages][^docker-mac]

# 認証とmacOS固有の生成物

configは1Passwordのsocketを`~/Library/Group Containers/2BUA8C4S2C.com.1password/t/agent.sock`として扱う。署名helperは`/Applications/1Password.app/Contents/MacOS/op-ssh-sign`の固定pathに設定される。Git author・署名・SSH認証、socketの入力階層の不一致は[identity](../identity.md)を正本にする。このpathが実機で存在し、望む鍵を提供していることは未確認である。[^config]

`build:pbfile`はSwift sourceがあれば`~/.local/bin/pbfile`をbuildする。source不在時に明示的な欠損失敗にする実装ではない。現行taskの終了だけで全管理生成物が揃ったと解釈せず、[validation](../validation.md)の対象別確認と、[convergence](../decisions/convergence.md)の成功条件案を分けて扱う。[^pbfile]

# 設計変更の参照先

brewの版管理・更新をapplyへ含めるかの比較は[convergenceの手動更新節](../decisions/convergence.md#manual-updates)、初回準備の変更案は[bootstrapの判断](../decisions/convergence.md#bootstrap-prerequisites)を正本とする。ここではmacOS固有の現行前提を扱う。

Full Disk Accessや無制限のpasswordless sudoが本repoの全操作に必要という確認はしていない。実際の操作で不足する権限が分かった場合に、その操作と対象を絞って扱う。

[^config]: [ホスト入力と1Password identity取得](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoi.toml.tmpl)。
[^pbfile]: [macOS Swift build](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/build/executable_pbfile.tmpl)。
[^wezterm-link]: [macOS/WSLのWezTerm実体探索](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_local/bin/symlink_wezterm.tmpl)。
[^brew-script]: [Homebrewの導入・更新・bundle実行](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_before_provision-macos-homebrew.sh.tmpl)。
[^order]: [chezmoi公式：target計算とbefore/afterの順序](https://www.chezmoi.io/reference/application-order/)。
[^apple-tools]: [Apple公式：command-line tools](https://developer.apple.com/documentation/xcode/installing-the-command-line-tools)。
[^packages]: [OS別package宣言](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoidata/packages.yaml)。
[^brewfile]: [macOS BrewfileとCI分岐](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/homebrew/Brewfile.tmpl)。
[^brew]: [Homebrew公式：bundleの更新と版管理の限界](https://docs.brew.sh/Brew-Bundle-and-Brewfile)。
[^docker-mac]: [Docker公式：Macへの導入と起動](https://docs.docker.com/desktop/setup/install/mac-install/)。
