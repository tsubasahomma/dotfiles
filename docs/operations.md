---
type: Playbook
title: 現行のbootstrap・apply・修復・診断
description: 現行の入口、実行前提、副作用、失敗時の扱いを確認し、将来の成功条件と区別する。
status: draft
generated:
  by: codex/gpt-6
  at: "2026-11-11T06:48:33+00:00"
sources:
  - id: install
    resource: https://www.chezmoi.io/install/
    title: chezmoi公式の導入方法
  - id: mise-pin
    resource: https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.mise-version
    title: 観測時のmise本体pin
  - id: bootstrap
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.bootstrap-mise.sh"
    title: "mise本体の導入先検査・pinとの差替え"
  - id: config
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoi.toml.tmpl"
    title: "identity入力・ホスト情報の取得とread-source-state hook"
  - id: hooks
    resource: "https://www.chezmoi.io/reference/configuration-file/hooks/"
    title: "chezmoi Hooks：dry-runでもhookは動く"
  - id: mise-config
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/config.toml.tmpl"
    title: "mise task discovery・自動導入設定"
  - id: tools
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/conf.d/10-tools.toml"
    title: "観測時のmise tool宣言"
  - id: linux-script
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_before_00-provision-linux-packages.sh.tmpl"
    title: "Linuxのsudo・package導入"
  - id: brew-script
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_before_provision-macos-homebrew.sh.tmpl"
    title: "brew updateとbundle install"
  - id: win-script
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_before_provision-windows-packages.sh.tmpl"
    title: "WinGetによるWindows package導入"
  - id: wrapper
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl"
    title: "post-applyの起動条件・mise install・認証の受け渡し"
  - id: init
    resource: "https://www.chezmoi.io/reference/commands/init/"
    title: "chezmoi init"
  - id: scripts
    resource: "https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/"
    title: "chezmoi scripts：onchangeの成功済み内容による再実行判定"
  - id: verify
    resource: "https://www.chezmoi.io/reference/commands/verify/"
    title: "chezmoi verifyの確認範囲"
  - id: doctor
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/doctor/executable__default.tmpl"
    title: "doctorが呼ぶ検査とCI分岐"
  - id: check-nvim
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/check/executable_nvim.tmpl"
    title: "chezmoi verifyと通常Neovim起動を含む検査"
  - id: lazy
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/nvim/lua/config/lazy.lua"
    title: "Neovim起動時のlazy.nvim取得"
  - id: repair-nvim
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/repair/executable_nvim.tmpl"
    title: "採用lockからのLazy restore"
  - id: security
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/repair/executable_security.tmpl"
    title: "SSHファイルに対するchmod範囲"
  - id: identity
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/generate/executable_identity.tmpl"
    title: "identity生成の先行削除と直接書き込み"
  - id: mise-tasks
    resource: "https://github.com/jdx/mise/blob/v2026.6.11/docs/tasks/running-tasks.md"
    title: "mise v2026.6.11：task省略と依存順序"
  - id: update-nvim
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/update/executable_lazy-lock.tmpl"
    title: "Neovim更新・source反映・commit・push・PR"
  - id: tasks
    resource: "https://github.com/tsubasahomma/dotfiles/tree/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks"
    title: "repo所有taskの実装"
  - id: order
    resource: "https://www.chezmoi.io/reference/application-order/"
    title: "chezmoi application order"
  - id: ignore
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiignore.tmpl"
    title: "chezmoiによる配置の除外"
  - id: remove
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiremove.tmpl"
    title: "旧管理対象の除去指定"
  - id: externals
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiexternal.toml.tmpl"
    title: "外部assetとrefresh指定"
  - id: lifecycle
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/lifecycle/executable_post-apply.tmpl"
    title: "OS別post-apply依存graph"
  - id: completions
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/generate/executable_completions.tmpl"
    title: "補完生成・warn処理・cache削除"
  - id: wsl-wrapper
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_after_wsl-sync-services.sh.tmpl"
    title: "WSL syncの起動条件とCI除外"
  - id: ci
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.github/workflows/compliance.yml"
    title: "Ubuntu/macOSでのinit apply・verify・repair・doctor"
  - id: mise-install
    resource: "https://github.com/jdx/mise/blob/v2026.6.11/docs/cli/install.md"
    title: "mise v2026.6.11 install：導入と有効化は別"
  - id: mise-upgrade
    resource: "https://github.com/jdx/mise/blob/v2026.6.11/docs/cli/upgrade.md"
    title: "mise v2026.6.11 upgrade：更新とbump"
  - id: brew-bundle
    resource: "https://docs.brew.sh/Brew-Bundle-and-Brewfile"
    title: "Homebrew Bundle：既定upgrade・no-upgrade・lock非対応"
  - id: brew-man
    resource: "https://docs.brew.sh/Manpage"
    title: "Homebrew brew(1)：導入に伴う依存変更と自動cleanup"
  - id: user
    resource: "Maintainer report in the repository OKF design conversation, 2026-11-11"
    title: "端末構築後にmise関連・brewを直接更新したとの利用者報告。実機観測ではない"
---
# 現在の操作と、その限界

この文書は2026-11-11に読んだ現行コードの説明です。基準HEADは`f4fe1fac3e0722b173b5291a06e98e1e066786f1`。実機の配置・実行版・認証状態は未確認です。ここにあるコマンドを今回実行したわけではありません。

実行対象の正本と所有者は[ownership](ownership.md)で確認します。欠損を必ず復旧するapply、対象限定の共通repair、変更しないdoctorは[convergence](decisions/convergence.md)の**未実装案**です。現行コマンドの保証として読まないでください。

# 実行前に確認すること

- **手動更新のある端末**：mise本体の実体・版、tool宣言と有効版、brew項目、手動編集したtargetの扱いを先に決める。現行hookはその判断を待たず、`~/.local/bin/mise`をrepoのpinへ戻し得る。取得済みのコードや通常のファイル読取から調べ始め、未監査のchezmoi dry-runを初手の「安全な棚卸し」としない。[^bootstrap][^config][^hooks]
- **初回config生成**：通常環境ではopが利用・認証可能であることが必要。WSLはWindows interop、cmd.exe、PowerShell、op.exe、署名helperの探索も先に通る必要がある。後段のpackage scriptがこの初期条件をすべて整えるわけではない。[^config]
- **実際の実行環境**：PATH上のchezmoi / mise、configで固定されたmiseのパス、読み込む設定scope、レンダリング済みrepo-tasksを区別する。古い配置物やlocal overrideの影響は今回未確認。source内のGo templateをそのままshellで実行しない。[^config][^mise-config][^tools]
- **必要な権限・入力**：Linux scriptは非対話sudoを要求し、macOSはHomebrew導入・更新、WSLはWindows側への導入・copyを含む。既存scriptが示す広いsudo設定例を、そのまま推奨するものではない。GitHub取得用の認証と1Passwordのidentity準備は別の前提である。[^linux-script][^brew-script][^win-script][^wrapper]

OS固有の先行条件は[macOS](platforms/macos.md)・[WSL](platforms/wsl.md)、1Password入力は[identity](identity.md)を参照します。特にWSLのWezTermはtarget計算時に実体の存在を要求するため、before scriptでの導入だけに依存できません。

これらは操作者が行う確認です。現行コードに、全対象を変更前に検査して停止する包括的なpreflightが実装されているという意味ではありません。

<a id="first-install"></a>
# 初回導入の経路

これは新しい端末向けに、現行の個別操作をつないだ手順案です。クリーンなmacOS/WSLでの通し検証は未実施で、一括bootstrapが完成しているという意味ではありません。既に管理中の端末を再初期化する手順には使わず、手動更新がある場合は上の前提確認へ戻ります。

| 順序 | 準備・操作 | 次へ進む条件と副作用 |
|---|---|---|
| 1. 初期toolを用意 | 対象OSのGit、POSIX shell、curlと、chezmoiを用意する。chezmoiは公式のpackageまたは配布binaryの導入方法を選ぶ | 未配置のrepo-tasksや未導入miseに依存しない。使用するchezmoiの版・実体を決める。OS packageやbinaryの導入自体が変更操作[^install][^bootstrap] |
| 2. sourceを取得 | 下の例のようにHTTPSでrepoをcloneし、適用するcommit・branchとsourceの差分を確認する | 取得先が既存repoならcloneを重ねず、そのsourceを確認する。新規取得はdirectory・Git履歴の作成と通信。まだinit/applyしない |
| 3. 認証とOS前提を準備 | [identity](identity.md)の1Password item・認証、対象の[macOS](platforms/macos.md)または[WSL](platforms/wsl.md)の先行条件を揃える | macOSの署名helper・開発tool、WSLのinterop・Windows op/署名helper・WezTerm・distro名などを後段install任せにしない。GitHub取得用認証と1Password identityは別経路[^config][^wrapper] |
| 4. 既存状態と変更先を確認 | `.chezmoiignore.tmpl`、`.chezmoiremove.tmpl`、package宣言、下のapply段階表を確認し、既存fileとの衝突を整理する | 特に既存の`~/.ssh/config`と管理symlink、Windows copy先を確認する。自動backup/mergeは前提にしない。必要な退避は対象を決めて行う[^ignore][^remove][^tasks] |
| 5. configを初期化 | `chezmoi init --source "$DOTFILES_SOURCE"`を実行する | op/host照会とconfig書込を伴う。ここでは`--apply`を付けず、失敗した前提を解決してから次へ進む。initを無副作用の確認とは扱わない[^init][^config] |
| 6. 採用したsourceを反映 | `chezmoi apply --source "$DOTFILES_SOURCE"`を実行する | 下の段階表のmise差替え、package更新、配置・生成・Windows copyが起こり得る。diff/dry-runを挟む場合もread hookの副作用がある[^bootstrap][^hooks][^wrapper] |
| 7. 結果を確認 | [validation](validation.md)から対象の確認を選び、静的配置、必要な生成物、実行実体、必要な認証経路を分けて確認する | `verify`だけで全生成物を保証しない。doctorやWSL probeには副作用がある。Neovim restoreなど通常applyにない操作は必要性と範囲を定めて別途扱う[^verify][^doctor][^lifecycle] |

source取得の例です。Gitが利用可能で、取得先がまだ存在しない場合に限ります。HTTPS取得には、これから生成するSSH identityを前提にしません。

```sh
DOTFILES_SOURCE="$HOME/.local/share/chezmoi"
git clone https://github.com/tsubasahomma/dotfiles.git "$DOTFILES_SOURCE"
git -C "$DOTFILES_SOURCE" status --short
git -C "$DOTFILES_SOURCE" rev-parse HEAD
```

この変数は後続commandでも同じsourceを指定するためのものです。source取得は設定の適用ではありません。取得後、選んだ版と内容を確認してから上表の準備を進めます。

**未整備の点**：初期chezmoiの導入方法・採用版から、repoが宣言するchezmoiへ移る際の実体/PATHの扱いは統一されていません。Linuxの非対話sudoは現行の前提ですが、最小権限で準備する手順は未確定です。初回の1Password・WezTerm先行導入も自動化された段階ではありません。これらを解決せずに後段へ進める手順にはせず、実装方式の比較は[bootstrapの判断](decisions/convergence.md#bootstrap-prerequisites)で扱います。

GitHub tokenは常時必須という旧記述を引き継ぎません。source取得とtool取得で必要な認証を分け、対象resource・取得方法に応じて準備します。現行post-applyにはtoken系環境変数がなければop由来の認証をmise installへ渡す経路があり、1Password準備だけで全取得が成功するという保証でもありません。秘密値をcommand例や共有ログへ埋め込みません。[^wrapper]

# 現行の入口

以下は用途を選ぶための既存入口です。順に全部実行する手順ではありません。

| 入口 | 現在行うこと | 成功の読み方・副作用 |
|---|---|---|
| `chezmoi init --source=<source-directory>` | sourceを指定しconfig生成を行う。通常環境ではop / host情報を参照 | 認証・外部照会・config更新を含む。`--apply`を付けると続けてapplyへ進む[^config][^init] |
| `chezmoi apply` | 下記のhook・OS別scripts・配置・post-applyを実行条件に従って処理 | 全生成物の欠損復旧や全アプリの正常性を保証しない[^scripts][^wrapper] |
| `chezmoi diff` / `chezmoi verify` / `--dry-run`を使う操作 | 差分表示・管理targetの照合・予定表示 | source読込hookの副作用が残る。verifyの成功は任意の生成物や認証までの保証ではない[^hooks][^verify] |
| `mise run doctor` | repoのcheck taskを順に呼び、非zeroがあれば失敗を返す | CIで検査集合が変わる。Neovim起動・chezmoi verify等を含み、非変更とは保証できない[^doctor][^check-nvim][^lazy] |
| `mise run repair:nvim` | Lazy restoreを呼ぶ | pluginの取得・変更、通常Neovim初期化を伴い得る。repoの版を最新版へ進める入口とは別[^repair-nvim] |
| `mise run repair:security` | `.ssh`配下の`id_*`通常ファイル（`.pub`以外）をchmod | 所有を識別せず利用者の鍵にも及ぶ。特定鍵だけを修復する共通APIではない[^security] |
| `mise run generate:identity`等の個別task | 対象taskとその依存を実行する | 再実行の省略条件がある。「名前を指定すれば欠損だけ直す」とは限らない[^identity][^mise-tasks] |
| `mise run update:lazy-lock` | plugin更新、lockのsource取込、branch・commit・push・PR作成 | 外部への書込まで含む更新workflow。診断や通常の復旧に含めない[^update-nvim] |

checkごとの保証範囲は[validation](validation.md)、Neovim更新の詳細は[development](development.md)を正本にします。WSL専用の`check:wsl-openssh`はdoctorに含まれず、外部通信・認証・一時署名commitを伴います。検査名だけで非変更と判断しないでください。

現行に単一の汎用`repair`コマンドはありません。bootstrapも独立した統一CLIではなく、初期導入・config生成・read hook・package scriptに分散しています。タスクが実際にどのコードを実行するかは、sourceとレンダリング済み配置物を照合して判断します。[^tasks][^config]

# applyで通る段階

`run_onchange_`は、レンダリング後のscript内容が最後の成功時から変わった場合などに実行されます。下表の各scriptが毎回すべて動くわけではありません。before / target / afterの区分と、同区分内の順序を区別します。[^scripts][^order]

| 段階 | 現行の処理 | 書き込み・外部依存・省略条件 |
|---|---|---|
| config生成（init等） | ホスト判定、op項目取得、identity入力とパスを設定へ保存 | 認証・Windows照会・config更新。通常applyのたびに最新identityへ更新する段階ではない[^config] |
| source読込 | read-source-state.pre → `.bootstrap-mise.sh` | `.mise-version`は現在`2026.6.11`。[^mise-pin]`~/.local/bin/mise`の不一致・欠損で取得・置換。新しい版も差替え対象。導入先の型検査と導入後の版確認はあるが、installer自体は可変URL[^bootstrap] |
| before scripts | OS別package導入 | Linuxのpackage DB・sudo、macOSのbrew updateとbundle install、WSLのWinGet。task配置前に必要な依存を用意する経路。WinGetのnightly判定にはhash検証回避があり、維持すべき安全性とは扱わない[^linux-script][^brew-script][^win-script] |
| target反映 | chezmoiの静的配置・symlink・external・remove | ホーム配下への配置と指定旧パスの除去。externalには固定版とfloating参照が混在[^ignore][^remove][^externals] |
| afterの共通wrapper | XDG / PATHを設定し、固定パスのmise install → lifecycle:post-apply | tool導入・通信。GitHub token系環境変数がなければop読取コマンドをinstallの環境に渡す経路がある。毎回認証が発生するとの断定ではない[^wrapper] |
| post-apply graph | identity・権限・補完・bat・Vale・pnpm、Linux shell、macOS pbfile等 | 依存graphなので全taskが表記順に直列実行されるわけではない。repair:security → generate:identity、provision:pnpm → generate:completions等の依存がある[^lifecycle][^identity][^completions][^mise-tasks] |
| WSL用after wrapper | lifecycle:wsl-post-apply → Windowsへの2設定copy | 共通wrapperの後。CI・非WSLでは実行しない。copy元欠落は成功扱いでskipし、Windows側の独自変更はmergeしない[^wsl-wrapper][^tasks] |

通常applyのgraphにはdoctorとrepair:nvimは含まれません。CIはinit --applyの後にverify、repair:nvim、doctorを別に呼んでいます。この追加段階の成功を通常apply単体の保証へ移しません。[^lifecycle][^ci]

# 手動更新されたmise・brewへ起こり得ること

| 状態 | 現行経路が行うこと | 実行前の扱い |
|---|---|---|
| `~/.local/bin/mise`がpinより新しい | source読込hookがpinへ差替え得る | まず実体・版・導入元を確認。PATH上の別miseが新しくても、hookがそれを使うとは限らない[^bootstrap] |
| mise toolを直接install / upgradeした | sourceのtarget反映とmise installは、採用済み宣言の明示的な移行判断とは別に動く | 宣言・導入済み・有効版を分ける。upgradeの`--bump`等がどのconfigを変えたかは未確認。手動版の保持・採用は[設計案](decisions/convergence.md)で判断[^mise-install][^mise-upgrade] |
| targetのmise configを直接編集した | chezmoiのtarget反映で差分が出る | 差分をsourceへ採用するか、置換するか、別scopeへ分けるかを決める。自動の逆輸入は実装されていない |
| brewで既存項目を更新・追加した | macOS before scriptが実行されるとbrew update後にbundle install | 既定で宣言項目をupgradeし得る。宣言外の一括削除は明示していないが、installに伴うcleanup・依存変更を含めて保持を保証することはできない[^brew-script][^brew-bundle][^brew-man] |

上表は現行の可能な経路です。この端末で実際にdowngrade・cleanupが起きたという観測ではありません。手動更新の詳細は利用者報告の範囲に留まります。[^user]

# 終了コードだけでは分からないこと

- **欠損の見逃し**：外側onchange wrapperが省略されれば、内側miseのoutputs判定にも到達しない。directory単位のoutputsも個別ファイルの妥当性とは別。bat themeなど一部targetは外側hashにも含まれるため、すべての欠損が必ず見逃されるとは断定しない。[^wrapper][^mise-tasks]
- **生成失敗の扱い**：補完の一部は失敗をwarnへ変換し、リダイレクト先が空でも処理を続け得る。pbfileのソース欠落、Vale config欠落、Windows copy元欠落は、現在のtaskでは成功終了になり得る。[^completions][^tasks]
- **identityの途中失敗**：Git identitiesの先行削除・公開鍵とsignersへの直接書込がある。旧正常状態を保持するtransactionではなく、失敗後も一部変更が残り得る。identity入力が空の場合のCI fallback stub生成は、CIフラグ自体で限定された分岐ではない。空入力での成功を実機認証の正常性と扱わない。[^identity]
- **doctorの範囲**：check:nvimはchezmoi verifyと通常Neovim configを使う。lazy.nvimの取得経路に入り得るほか、miseには自動導入設定がある。各probeを監査せず非変更を約束しない。「Zero Drift」という出力は端末全体の一致を証明しない。[^check-nvim][^lazy][^mise-config][^doctor]
- **CIの限界**：Ubuntu/macOSのCI分岐を使う。2回のapply比較、実1Password、手元の手動更新、Windows側copyの成功はこのworkflowだけでは分からない。[^ci]

# 失敗したとき

失敗した段階、すでに反映した対象、残った出力を確認します。全体rollbackは現行にありません。エラーを直して同じ入口を再実行しても、成功済みscriptやtaskの省略条件によって処理範囲は変わり得ます。[^scripts][^mise-tasks]

一括の履歴消去、生成directory全削除、全tool更新を通常の再試行にしません。個別taskを使う場合も依存・出力範囲・省略条件を確認します。特にidentity生成やrepair:securityは、対象名以上に広い変更を行います。対象だけを復旧できるようにする変更は[convergence](decisions/convergence.md)に残します。[^identity][^security]

ログを共有する際は鍵・アカウント識別子・生成identityの個人情報を除き、対象の種類、段階、成否、未確認事項を残します。未実行の検査を成功として記録しません。

[^bootstrap]: [mise本体の導入先検査・pinとの差替え](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.bootstrap-mise.sh).
[^config]: [identity入力・ホスト情報の取得とread-source-state hook](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoi.toml.tmpl).
[^hooks]: [chezmoi Hooks：dry-runでもhookは動く](https://www.chezmoi.io/reference/configuration-file/hooks/).
[^mise-config]: [mise task discovery・自動導入設定](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/config.toml.tmpl).
[^tools]: [観測時のmise tool宣言](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/conf.d/10-tools.toml).
[^linux-script]: [Linuxのsudo・package導入](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_before_00-provision-linux-packages.sh.tmpl).
[^brew-script]: [brew updateとbundle install](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_before_provision-macos-homebrew.sh.tmpl).
[^win-script]: [WinGetによるWindows package導入](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_before_provision-windows-packages.sh.tmpl).
[^wrapper]: [post-applyの起動条件・mise install・認証の受け渡し](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl).
[^init]: [chezmoi init](https://www.chezmoi.io/reference/commands/init/).
[^scripts]: [chezmoi scripts：onchangeの成功済み内容による再実行判定](https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/).
[^verify]: [chezmoi verifyの確認範囲](https://www.chezmoi.io/reference/commands/verify/).
[^doctor]: [doctorが呼ぶ検査とCI分岐](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/doctor/executable__default.tmpl).
[^check-nvim]: [chezmoi verifyと通常Neovim起動を含む検査](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/check/executable_nvim.tmpl).
[^lazy]: [Neovim起動時のlazy.nvim取得](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/nvim/lua/config/lazy.lua).
[^repair-nvim]: [採用lockからのLazy restore](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/repair/executable_nvim.tmpl).
[^security]: [SSHファイルに対するchmod範囲](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/repair/executable_security.tmpl).
[^identity]: [identity生成の先行削除と直接書き込み](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/generate/executable_identity.tmpl).
[^mise-tasks]: [mise v2026.6.11：task省略と依存順序](https://github.com/jdx/mise/blob/v2026.6.11/docs/tasks/running-tasks.md).
[^update-nvim]: [Neovim更新・source反映・commit・push・PR](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/update/executable_lazy-lock.tmpl).
[^tasks]: [repo所有taskの実装](https://github.com/tsubasahomma/dotfiles/tree/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks).
[^order]: [chezmoi application order](https://www.chezmoi.io/reference/application-order/).
[^ignore]: [chezmoiによる配置の除外](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiignore.tmpl).
[^remove]: [旧管理対象の除去指定](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiremove.tmpl).
[^externals]: [外部assetとrefresh指定](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiexternal.toml.tmpl).
[^lifecycle]: [OS別post-apply依存graph](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/lifecycle/executable_post-apply.tmpl).
[^completions]: [補完生成・warn処理・cache削除](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/generate/executable_completions.tmpl).
[^wsl-wrapper]: [WSL syncの起動条件とCI除外](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_after_wsl-sync-services.sh.tmpl).
[^ci]: [Ubuntu/macOSでのinit apply・verify・repair・doctor](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.github/workflows/compliance.yml).
[^mise-install]: [mise v2026.6.11 install：導入と有効化は別](https://github.com/jdx/mise/blob/v2026.6.11/docs/cli/install.md).
[^mise-upgrade]: [mise v2026.6.11 upgrade：更新とbump](https://github.com/jdx/mise/blob/v2026.6.11/docs/cli/upgrade.md).
[^brew-bundle]: [Homebrew Bundle：既定upgrade・no-upgrade・lock非対応](https://docs.brew.sh/Brew-Bundle-and-Brewfile).
[^brew-man]: [Homebrew brew(1)：導入に伴う依存変更と自動cleanup](https://docs.brew.sh/Manpage).
[^user]: 端末構築後にmise関連・brewを直接更新したとの利用者報告。実機観測ではない.

[^mise-pin]: [観測時のmise本体pin](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.mise-version).

[^install]: [chezmoi: Install](https://www.chezmoi.io/install/)。公式の導入方法であり、このrepoの初回通し試験の証拠ではない。
