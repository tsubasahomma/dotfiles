---
type: Guide
title: macOSの前提と管理境界
description: macOSでbootstrap・apply・認証・GUI app・生成物を扱う前提を確認する。
status: draft
generated:
  by: codex/gpt-6
  at: "2026-11-12T00:01:15+00:00"
sources:
  - id: config
    resource: "../../.chezmoi.toml.tmpl"
    title: "ホスト入力と1Password identity取得"
  - id: pbfile
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/build/executable_pbfile.tmpl"
    title: "macOS Swift build"
  - id: wezterm-link
    resource: "../../dot_local/bin/symlink_wezterm.tmpl"
    title: "macOS/WSLのWezTerm実体探索"
  - id: brew-script
    resource: "../../.chezmoiscripts/run_onchange_before_provision-macos-homebrew.sh.tmpl"
    title: "Homebrew不足導入と前提検査"
  - id: order
    resource: "https://www.chezmoi.io/reference/application-order/"
    title: "chezmoi公式：target計算とbefore/afterの順序"
  - id: apple-tools
    resource: "https://developer.apple.com/documentation/xcode/installing-the-command-line-tools"
    title: "Apple公式：command-line tools"
  - id: packages
    resource: "../../.chezmoidata/packages.yaml"
    title: "OS別package宣言"
  - id: brewfile
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/homebrew/Brewfile.tmpl"
    title: "macOS BrewfileとCI分岐"
  - id: brew
    resource: "https://docs.brew.sh/Brew-Bundle-and-Brewfile"
    title: "Homebrew公式：bundleの更新と版管理の限界"
  - id: brew-man
    resource: "https://docs.brew.sh/Manpage"
    title: "Homebrew：no-upgradeとupdate/cleanup/dependentsの環境変数"
  - id: brew-implementation
    resource: "https://github.com/Homebrew/brew/tree/bc63375ac3a4d6debb1ceb441ae6e22854f0909a/Library/Homebrew/bundle"
    title: "静的照合したHomebrew Bundle実装：brew/cask/installer/subcommand install"
  - id: azure-cask
    resource: "https://formulae.brew.sh/cask/azure-cli"
    title: "Homebrew公式：Azure CLIのcask配布"
  - id: azure-migration
    resource: "https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-macos"
    title: "Microsoft公式：旧formulaからの移行"
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
| 開発tool | `build:pbfile`がxcrunで選択compiler/SDKを解決し、Swift sourceをbuildする | 適切なSDK/toolchainが利用可能か。Xcodeまたは対応するCommand Line ToolsはOS側の前提 |
| WezTerm | symlink先に`/Applications/WezTerm.app/Contents/MacOS/wezterm`を使う | 別場所へのapp導入を探索することやGUI起動の成功 |
| Homebrew | 本体とPATHは初回準備。before scriptは不足packageのbundle installを担う | 初回本体導入、完全なversion固定、依存変更まで含む非変更性 |

Git・Python 3.9+・ssh-keygenは[初期tool準備](../operations.md#first-install)で先行させる。Python/Gitの不足はidentity beforeで停止するが、Homebrew不足の判定はその後なので、全前提を無変更で検査する構成ではない。WezTermのmacOS分岐は固定pathを返すだけで、WSLと異なり実体欠損をrender時に拒否しない。通常の非CI applyでは後段bundleの導入対象であり、render成功をapp存在・起動の証拠にしない。

1Passwordがpackage宣言にあることだけでは初回の認証前提を満たさない。config生成はapplyより前なので、この前提を後段のpackage installで用意できない。targetのtemplate評価はbeforeより後になる場合もあり、[適用順の限界](../operations.md#applyで通る段階)と区別する。[^config][^pbfile][^wezterm-link][^brew-script][^order]

AppleはXcodeに含まれるtoolと、単独のCommand Line Toolsを提供している。どのOS/SDKの組合せが必要かはその時点の公式対応表と実際のbuildで確認する。このrepoのために常にfull Xcodeを要求する根拠はない。[^apple-tools]

# Homebrew・mise・GUIの境界

Azure CLIは現在の配布に合わせ、headlessのcaskとして宣言する。CIでも導入対象だがGUI appを追加する変更ではない。旧formulaの実機からの移行は未検証で、このrepoは自動uninstallを追加しない。旧実体との競合がある場合は停止結果と所有・導入元を確認し、Microsoftの移行案内にある旧formulaの削除・再導入を別の明示操作として判断する。[^azure-cask][^azure-migration]

package宣言にはbrewの`colima`とGUIの`docker-desktop`が共存する。just・atuin・duckdb・deno・AWS CLIは利用者決定によりmiseを主担当とし、macOSのbrew宣言を外した。既存実体は保持する。宣言されていることを、実際に使うcommandやcontainer runtimeが決まっている証拠としない。brewの実体・miseの実体・PATH上の選択を分ける。[^packages]

<a id="homebrew-policy"></a>
通常applyは不足導入、既存項目の更新は明示保守へ分離した。[操作とflag/env](../operations.md#homebrew-packages)を正本とする。CIではheadlessだけ、非CIではmedia/GUIも導入対象である。[^brew-script][^brewfile]

2026-11-11に現行公式manpageと、この端末に存在するHomebrew checkout `bc63375ac3a4d6debb1ceb441ae6e22854f0909a`の該当fileを静的照合した（HEADとのdiffなし、brew本体は実行していない）。Bundleのbrew/cask `preinstall!`は`no_upgrade`時に既存項目を省略する。installerは不足対象をinstallへ渡すが、batch内で`HOMEBREW_NO_INSTALL_UPGRADE`を解除するので、このenvを追加しても依存更新全体を禁止した証拠にはならない。install subcommandは失敗を非zeroにし、継承した`HOMEBREW_BUNDLE_INSTALL_CLEANUP` / `HOMEBREW_BUNDLE_FORCE_INSTALL_CLEANUP`によるcleanup経路を持つため、通常scriptで両方をunsetする。brew/cask skipも解除する。[^brew-implementation]

Homebrew公式資料も`--no-upgrade`を依存まで含めた版固定とはしていない。自動update/cleanupとinstall後のdependents検査は個別envで抑えるが、不足の依存導入、link、post-install、tap移行などは残る。dependentsの追随修復を止めるため既存consumerの正常性は保証しない。古いmetadataで不足導入に失敗した場合は成功扱いにせず、明示更新で解決する。別版Homebrewや独自`brew.env`、実installerの動作は隔離stub検査の対象外である。[^brew-man][^brew]

Docker Desktopはpackageがあること、appが起動していること、目的のCLI/context/daemonが使えることを分けて確認する。公式導入手順にもapp起動の段階がある。Colimaとのどちらを使うかをこの文案で決めず、実機の利用先を調べてから所有範囲を決める。両方を自動起動する案は採用していない。[^packages][^docker-mac]

# 認証とmacOS固有の生成物

configは1Passwordのsocketを`~/Library/Group Containers/2BUA8C4S2C.com.1password/t/agent.sock`として扱う。署名helperは`/Applications/1Password.app/Contents/MacOS/op-ssh-sign`の固定pathに設定される。Git author・署名・SSH認証、明示的IdentityAgentの入力契約は[identity](../identity.md)を正本にする。このpathが実機で存在し、望む鍵を提供していることは未確認である。[^config]

`build:pbfile`はmacOSの毎apply after_42から呼ぶ。source・選択compiler・SDK代表入力と所有receiptを確認し、必要時だけ一時build/検証後に`~/.local/bin/pbfile`へ反映する。source/compiler/SDK欠落、compile/検証失敗は非zeroで旧実体を保持する。未知の既存binaryは自動採用しない。[出力・移行契約](../operations.md#generated-assets)と[検証範囲](../validation.md#generated-assets)を参照。実機未適用。

# 設計変更の参照先

brewの版管理・更新をapplyへ含めるかの比較は[convergenceの手動更新節](../decisions/convergence.md#manual-updates)、初回準備の変更案は[bootstrapの判断](../decisions/convergence.md#bootstrap-prerequisites)を正本とする。ここではmacOS固有の現行前提を扱う。

Full Disk Accessや無制限のpasswordless sudoが本repoの全操作に必要という確認はしていない。実際の操作で不足する権限が分かった場合に、その操作と対象を絞って扱う。

[^config]: [ホスト入力と1Password identity取得](../../.chezmoi.toml.tmpl)。
[^pbfile]: [macOS Swift build](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/build/executable_pbfile.tmpl)。
[^wezterm-link]: [macOS/WSLのWezTerm実体探索](../../dot_local/bin/symlink_wezterm.tmpl)。
[^brew-script]: [Homebrew不足導入と前提検査](../../.chezmoiscripts/run_onchange_before_provision-macos-homebrew.sh.tmpl)。
[^order]: [chezmoi公式：target計算とbefore/afterの順序](https://www.chezmoi.io/reference/application-order/)。
[^apple-tools]: [Apple公式：command-line tools](https://developer.apple.com/documentation/xcode/installing-the-command-line-tools)。
[^packages]: [OS別package宣言](../../.chezmoidata/packages.yaml)。
[^brewfile]: [macOS BrewfileとCI分岐](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/homebrew/Brewfile.tmpl)。
[^brew]: [Homebrew公式：bundleの更新と版管理の限界](https://docs.brew.sh/Brew-Bundle-and-Brewfile)。
[^docker-mac]: [Docker公式：Macへの導入と起動](https://docs.docker.com/desktop/setup/install/mac-install/)。

[^brew-man]: [Homebrew brew(1)](https://docs.brew.sh/Manpage)。2026-11-11閲覧。
[^brew-implementation]: [Bundle実装](https://github.com/Homebrew/brew/tree/bc63375ac3a4d6debb1ceb441ae6e22854f0909a/Library/Homebrew/bundle)。`brew.rb` / `cask.rb`の`preinstall!`、`installer.rb`の`batch_install_homebrew!`、`subcommand/install.rb`をローカルcheckoutで確認。

[^azure-cask]: [Homebrew Azure CLI cask](https://formulae.brew.sh/cask/azure-cli)。
[^azure-migration]: [Microsoft：Azure CLIのmacOS導入・旧formula移行](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-macos)。
