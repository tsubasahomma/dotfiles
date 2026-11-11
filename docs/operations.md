---
type: Playbook
title: 現行のbootstrap・apply・修復・診断
description: 現行の入口、実行前提、副作用、失敗時の扱いを確認し、将来の成功条件と区別する。
status: draft
generated:
  by: codex/gpt-6
  at: "2026-11-11T16:58:03+00:00"
sources:
  - id: apply-implementation
    resource: "https://github.com/twpayne/chezmoi/blob/v2.70.4/internal/cmd/config.go#L750"
    title: "chezmoi 2.70.4：entryの逐次apply"
  - id: completion-usage
    resource: "https://github.com/jdx/mise/blob/v2026.6.11/src/cli/completion.rs"
    title: "mise補完のusage呼出しとfallback"
  - id: completion-after
    resource: "../.chezmoiscripts/run_after_30-completions.sh.tmpl"
    title: "毎回補完検査"
  - id: completion-state
    resource: "../.chezmoitemplates/completion_state.py"
    title: "補完入力・出力hash"
  - id: completion-exec
    resource: "https://github.com/jdx/mise/blob/v2026.6.11/src/cli/exec.rs"
    title: "mise採用版exec"
  - id: completion-which
    resource: "https://github.com/jdx/mise/blob/v2026.6.11/src/cli/which.rs"
    title: "mise採用版which"
  - id: completion-where
    resource: "https://github.com/jdx/mise/blob/v2026.6.11/src/cli/where.rs"
    title: "mise採用版where"
  - id: legacy-bridge
    resource: "https://github.com/tsubasahomma/dotfiles/blob/9d8cbe39596177cc5ddb217d15ecade9b360ebab/dot_config/systemd/user/1password-bridge.service.tmpl"
    title: "退役前のWSL bridge unit"
  - id: legacy-fzf
    resource: "https://github.com/tsubasahomma/dotfiles/blob/41692b36e85d881d2e3d6505934cafa9c3e70f48/dot_config/nvim/lua/plugins/fzf.lua"
    title: "退役前のfzf-lua specとkeymap"
  - id: legacy-security
    resource: "https://github.com/tsubasahomma/dotfiles/blob/eac4c9e49eae7d3441a7cf7aa04ad3838ba73697/dot_config/mise/repo-tasks/setup/executable_security.tmpl"
    title: "退役前のsetup:securityと同directoryの_default依存"
  - id: install
    resource: https://www.chezmoi.io/install/
    title: chezmoi公式の導入方法
  - id: mise-pin
    resource: ../.mise-version
    title: 観測時のmise本体pin
  - id: bootstrap
    resource: "../.bootstrap-mise.sh"
    title: "mise本体の読込検査・明示導入"
  - id: config
    resource: "../.chezmoi.toml.tmpl"
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
    resource: "../.chezmoiscripts/run_onchange_before_00-provision-linux-packages.sh.tmpl"
    title: "Linuxのsudo・package導入"
  - id: brew-script
    resource: "../.chezmoiscripts/run_onchange_before_provision-macos-homebrew.sh.tmpl"
    title: "Homebrew不足導入と前提検査"
  - id: win-script
    resource: "../.chezmoiscripts/run_onchange_before_provision-windows-packages.sh.tmpl"
    title: "WinGetによるWindows package導入"
  - id: wrapper
    resource: "../.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl"
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
    resource: "../dot_config/mise/repo-tasks/doctor/executable__default.tmpl"
    title: "doctorの共通検査集合"
  - id: check-nvim
    resource: "../dot_config/mise/repo-tasks/check/executable_nvim.tmpl"
    title: "Neovim lockの直接比較と実体の存在検査"
  - id: lazy
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/nvim/lua/config/lazy.lua"
    title: "Neovim起動時のlazy.nvim取得"
  - id: repair-nvim
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/repair/executable_nvim.tmpl"
    title: "採用lockからのLazy restore"
  - id: security
    resource: "../dot_config/mise/repo-tasks/repair/executable_security.tmpl"
    title: "権限変更を行わない互換task"
  - id: identity
    resource: "../dot_config/mise/repo-tasks/generate/executable_identity.tmpl"
    title: "identity入力の検証と世代切替"
  - id: mise-tasks
    resource: "https://github.com/jdx/mise/blob/v2026.6.11/docs/tasks/running-tasks.md"
    title: "mise v2026.6.11：task省略と依存順序"
  - id: update-nvim
    resource: "../dot_config/mise/repo-tasks/update/executable_lazy-lock.tmpl"
    title: "選択revisionからの隔離lock候補生成"
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
    resource: "../.chezmoiremove.tmpl"
    title: "旧パスの恒久削除を停止したremove定義"
  - id: externals
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiexternal.toml.tmpl"
    title: "外部assetとrefresh指定"
  - id: lifecycle
    resource: "../dot_config/mise/repo-tasks/lifecycle/executable_post-apply.tmpl"
    title: "OS別post-apply依存graph"
  - id: completions
    resource: "../dot_config/mise/repo-tasks/generate/executable_completions.tmpl"
    title: "補完・initの個別検証と切替"
  - id: wsl-wrapper
    resource: "../.chezmoiscripts/run_after_50-wsl-sync-services.sh.tmpl"
    title: "WSL syncの起動条件とCI除外"
  - id: ci
    resource: "../.github/workflows/compliance.yml"
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

この文書は2026-11-11に読んだ現行コードの説明です。基準HEADは`f4fe1fac3e0722b173b5291a06e98e1e066786f1`。実機の配置・実行版・認証状態は未確認です。mise読込・明示導入はR01の現行sourceに更新しました。隔離検証の範囲は[validation](validation.md#mise-read-boundary)に記し、実機操作の完了を意味しません。

実行対象の正本と所有者は[ownership](ownership.md)で確認します。identityの所有確認済み世代内欠損は[R10a契約](identity.md#identity-convergence)で復旧します。全生成物の欠損を必ず復旧するapply、対象限定の共通repairは[convergence](decisions/convergence.md)の**未実装案**です。現行コマンドの保証として読まないでください。

R02ではidentity集合を取得・render時に検証し、不正入力を出力書込前に拒否する。空でないidentityのrenderは`ssh-keygen`へ公開鍵を標準入力で渡して検査する（認証・通信・file書込なし）。[入力契約](identity.md#routingと各出力の境界)と[隔離検証](validation.md#identity-boundary)を参照。生成途中失敗・空集合・所有範囲・transactionは[identityの現行契約](identity.md#生成の切替と既存配置からの移行)に従う。

# 実行前に確認すること

- **手動更新のある端末**：mise本体の実体・版、tool宣言と有効版、brew項目、手動編集したtargetの扱いを先に決める。更新済みhookは`~/.local/bin/mise`の版を変えない。古いconfigがどのsourceのscriptを呼ぶかを通常のファイル読取で確認し、[移行条件](#mise-bootstrap)が未確認のchezmoi dry-runを初手の「安全な棚卸し」としない。[^bootstrap][^config][^hooks]
- **初回config生成**：通常環境ではopが利用・認証可能であることが必要。WSLはWindows interop、cmd.exe、PowerShell、op.exe、署名helperの探索も先に通る必要がある。後段のpackage scriptがこの初期条件をすべて整えるわけではない。[^config]
- **実際の実行環境**：PATH上のchezmoi / mise、configで固定されたmiseのパス、読み込む設定scope、レンダリング済みrepo-tasksを区別する。古い配置物やlocal overrideの影響は今回未確認。source内のGo templateをそのままshellで実行しない。[^config][^mise-config][^tools]
- **必要な権限・入力**：Linux scriptは非対話sudoを要求し、macOSはHomebrew packageの不足導入、WSLはWindows側への導入・copyを含む。Linuxではpackage managerと後段のshell登録・変更に必要な権限を確認する。GitHub取得用の認証と1Passwordのidentity準備は別の前提である。[^linux-script][^brew-script][^win-script][^wrapper]

OS固有の先行条件は[macOS](platforms/macos.md)・[WSL](platforms/wsl.md)、1Password入力は[identity](identity.md)を参照します。WSLのWezTermはtemplate評価時に実体を要求するため、初回手順では先行準備します。ただし、この評価が必ずbefore scriptより先に終わるとは限りません（下記の適用順を参照）。

これらは操作者が行う確認です。現行コードに、全対象を変更前に検査して停止する包括的なpreflightが実装されているという意味ではありません。

<a id="first-install"></a>
# 初回導入の経路

新しい端末では、**最小tool → OS固有前提・認証 → config生成 → 配置**の順に手動準備する方針を採用します。根拠と代案は[初回準備の判断](decisions/convergence.md#bootstrap-prerequisites)を参照してください。クリーンなmacOS/WSLでの通し検証は未実施です。既に管理中の端末を再初期化する手順には使わず、手動更新がある場合は上の前提確認へ戻ります。

| 順序 | 準備・操作 | 次へ進む条件と副作用 |
|---|---|---|
| 1. 初期toolを用意 | 対象OSのGit、POSIX shell、chezmoi、Python 3.9+、OpenSSHのssh-keygenを用意する。mise本体を既存bootstrapで導入する場合はcurlも必要 | 未配置のrepo-tasksや後段mise installに依存しない。OS提供tool等の実体をPATHへ通し、選んだchezmoiの版・実体を記録する。導入自体は変更操作[^install][^bootstrap] |
| 2. sourceを取得 | 下の例のようにHTTPSでrepoをcloneし、適用するcommit・branchとsourceの差分を確認する | 取得先が既存repoならcloneを重ねず、そのsourceを確認する。新規取得はdirectory・Git履歴の作成と通信。まだinit/applyしない |
| 3. 認証とOS前提を準備 | [identity](identity.md)の1Password item・認証、対象の[macOS](platforms/macos.md)または[WSL](platforms/wsl.md)の先行条件を揃える | macOSのHomebrew/PATH・署名helper・開発tool、WSLのinterop・Windows op/署名helper・WezTerm・distro名を準備する。packageやappの導入と認証・unlockは別。config生成の不足を後段installで補えない。WezTermも初回手順では先行準備する[^config][^order] |
| 4. 既存状態と変更先を確認 | `.chezmoiignore.tmpl`、`.chezmoiremove.tmpl`、package宣言、下のapply段階表を確認し、既存fileとの衝突を整理する | 特に既存の`~/.ssh/config`と管理symlink、Windows copy先を確認する。自動backup/mergeは前提にしない。必要な退避は対象を決めて行う[^ignore][^remove][^tasks] |
| 4a. mise本体を明示導入 | `sh "$DOTFILES_SOURCE/.bootstrap-mise.sh" --install`を実行する | 不在時にpin版の取得・配置。既存不一致は保持して停止するので、所有者と採用先を整理する。初期化後の読込hookは導入しない[^bootstrap] |
| 5. configを初期化 | `chezmoi init --source "$DOTFILES_SOURCE"`を実行する | op/host照会とconfig書込を伴う。ここでは`--apply`を付けず、失敗した前提を解決してから次へ進む。initを無副作用の確認とは扱わない[^init][^config] |
| 6. 採用したsourceを反映 | `chezmoi apply --source "$DOTFILES_SOURCE"`を実行する | 下の段階表のpackage導入、配置・生成・Windows copyが起こり得る。diff/dry-runの読込hookはmiseを導入しないが、external/cache等は別の副作用として扱う[^bootstrap][^hooks][^wrapper] |
| 7. 結果を確認 | [validation](validation.md)から対象の確認を選び、静的配置、必要な生成物、実行実体、必要な認証経路を分けて確認する | `verify`だけで全生成物を保証しない。通常診断は下記の直接入口を使い、認証probeは別に選ぶ。Neovim restoreなど通常applyにない操作は必要性と範囲を定めて別途扱う[^verify][^doctor][^lifecycle] |

source取得の例です。Gitが利用可能で、取得先がまだ存在しない場合に限ります。HTTPS取得には、これから生成するSSH identityを前提にしません。

```sh
DOTFILES_SOURCE="$HOME/.local/share/chezmoi"
git clone https://github.com/tsubasahomma/dotfiles.git "$DOTFILES_SOURCE"
git -C "$DOTFILES_SOURCE" status --short
git -C "$DOTFILES_SOURCE" rev-parse HEAD
```

この変数は後続commandでも同じsourceを指定するためのものです。source取得は設定の適用ではありません。取得後、選んだ版と内容を確認してから上表の準備を進めます。

初期chezmoiからrepoの宣言版へ移る実体/PATHの運用は統一されていません。後段でmiseがchezmoiを導入しても、起動済みprocessの実体は切り替わりません。次の操作でどの実体を使うかを確認します。Linuxの最小sudo権限設計も未確定です。

不足した段階で止まり、次の行動を済ませて同じ段階から再試行します。以下は操作者の準備表であり、自動preflightではありません。停止の説明は`--keep-going`を使わない通常applyが対象です。`command -v`で選択pathを確認しても、shim経由の自動導入や実体の健全性まで検証したことにはなりません。

| 不足・失敗した条件 | 次の行動 | 実行中に判明した場合の境界 |
|---|---|---|
| Python 3.9+・Git・ssh-keygen | OS側で実体を準備しPATHを確認する。公開鍵エラーはssh-keygen不足と入力不正を切り分ける | 公開鍵検証はrender時。Python/Gitのbefore05 guardはtarget配置前だが、Linux before00のpackage操作は先行し得る |
| mise本体 | 上表4aの明示導入。不一致や壊れた既存fileは所有者・採用版を確認する | read hookは不足を補わず停止する |
| 1Password CLI・account照会 | macOSは選択したop、WSLはWindows op.exeの導入・PATH・account・app連携・認証を確認し、initを再試行する | account照会失敗はlock以外のCLI障害も含む。認証が通っても鍵登録・署名・SSH接続の成功ではない |
| WSL interop・helper・WezTerm・distro名 | configのエラーに従いWindows/WSL側を準備する。WezTermは`C:\Program Files\WezTerm\wezterm.exe`とmount/変換先を確認し、対象distributionの`WSL_DISTRO_NAME`でapplyする | WezTerm実体欠損はtemplate評価で停止するが、beforeや先行targetの変更が残り得る。macOSのsymlinkは存在検査なしの固定path |
| Homebrew・WinGet | macOSは採用したbrewをPATHへ、WSLはWindows PowerShellから解決できるwingetを準備する | OS package段階の失敗。先行beforeや導入済みpackageを巻き戻す契約はない |
| Linux sudo | 管理者とsudoの利用・認証、選択package manager（apt-get/dnf/pacman）、後段の`/etc/shells`登録と`chsh`に必要な権限を確認する | 現行guardは`sudo -n true`。それだけ通しても後続commandの権限・認証有効期間を保証しない。無制限の`NOPASSWD: ALL`を準備手順にしない |
| 配置後のtool取得・生成 | エラー対象のtool、取得用認証、compiler/SDKを確認してapplyを再試行する | after失敗時にはtarget配置や先行生成が残る。apply全体のtransactionではない |

手順の順序と限定した停止条件は[隔離検査](validation.md#first-install-order)で確認します。実OSの権限・認証・GUIの動作確認は別途必要です。

GitHub tokenは常時必須という旧記述を引き継ぎません。source取得とtool取得で必要な認証を分け、対象resource・取得方法に応じて準備します。現行post-applyにはtoken系環境変数がなければop由来の認証をmise installへ渡す経路があり、1Password準備だけで全取得が成功するという保証でもありません。秘密値をcommand例や共有ログへ埋め込みません。[^wrapper]

<a id="mise-bootstrap"></a>
# miseの明示導入と旧configの移行

[bootstrap script](../.bootstrap-mise.sh)は引数なしと`--check`で非変更の前提検査だけを行います。`.mise-version`を読まずmise自体も実行しないため、旧版・一致版・新版を区別せず保持します。実行属性の確認はbinaryの健全性やtool互換性の証明ではありません。`check:toolchain`のpin整合判定は引き続き残り、read hookの合格とは別です。

不足導入は`sh "$DOTFILES_SOURCE/.bootstrap-mise.sh" --install`で明示します。不在なら`.mise-version`（現在`2026.6.11`）の版を可変URL `https://mise.run`のinstallerで取得し、配置・実行属性設定・版確認を行います。一致する通常fileは保持し、不一致版・壊れた既存file・symlink・非通常fileは自動修復せず停止します。既存版を採用する場合は互換性を確認してsourceのpinを変更し、置換する場合は導入元・所有者を確認して別途実行します。失敗した新規導入の残骸を自動で再置換する仕組みはありません。[^mise-pin][^bootstrap]

生成済みchezmoi configはtemplateの編集だけでは更新されません。次の順序で移行します。

1. 使用するconfig fileを通常のfile読取で確認し、`hooks.read-source-state.pre.command`の絶対pathを調べます。標準は`$XDG_CONFIG_HOME/chezmoi/chezmoi.toml`（未設定時は`~/.config/chezmoi/chezmoi.toml`）ですが、`--config`指定等も確認します。共有出力にidentity情報を載せません。
2. hookが指すsourceの`.bootstrap-mise.sh`を今回の版へ更新します。従来の引数なしhookは、その時点で検査のみになります。別checkout・コピー・古いscriptを指すconfigは、現在の作業ツリーを更新しただけでは保護されません。`--source`の変更だけでもconfig内の絶対pathは直りません。
3. 既存configのidentity等を保持したまま、hookのcommandを更新済みscriptの絶対path、argsを`["--check"]`へ局所編集できます。configの再生成を選ぶ場合は、更新済みscriptを指すことを先に確認し、`chezmoi init --source "$DOTFILES_SOURCE"`を`--apply`なしで実行します。再生成はop/host照会とidentity入力・configの更新を伴うため、hookだけの移行とは区別します。[^init][^config]

今回の検証は隔離configで実施し、利用者の生成済みconfigや別sourceの更新・実機適用は行っていません。hookの分離はchezmoiのexternal取得・cache書込や他taskの自動導入を無効化するものではありません。

# 現行の入口

以下は用途を選ぶための既存入口です。順に全部実行する手順ではありません。

| 入口 | 現在行うこと | 成功の読み方・副作用 |
|---|---|---|
| `chezmoi init --source=<source-directory>` | sourceを指定しconfig生成を行う。通常環境ではop / host情報を参照 | 認証・外部照会・config更新を含む。`--apply`を付けると続けてapplyへ進む[^config][^init] |
| `chezmoi apply` | 下記のhook・OS別scripts・配置・post-applyを実行条件に従って処理 | 全生成物の欠損復旧や全アプリの正常性を保証しない[^scripts][^wrapper] |
| `chezmoi diff` / `chezmoi verify` / `--dry-run`を使う操作 | 差分表示・管理targetの照合・予定表示 | 更新済みread hookはmiseの存在・実行属性だけ確認し、不足時は停止。external/cacheまで無通信・無書込ではない。verifyの成功は任意の生成物や認証までの保証ではない[^hooks][^verify] |
| `~/.local/bin/dotfiles-diagnose` | 配置済みcheckを直接呼び、必須欠損・driftはCIでも失敗にする | mise task開始前の自動導入を迂回する。file検査、Git config読取、mise `--version`だけ。全tool・pluginの正常動作は保証しない[^doctor][^check-nvim] |
| `mise run doctor` / `mise run check:*` | 互換用task名 | task本体の前に自動導入や利用者config評価が起こり得る。非変更の診断入口として使わない |
| `mise run repair:nvim` | Lazy restoreを呼ぶ | pluginの取得・変更、通常Neovim初期化を伴い得る。repoの版を最新版へ進める入口とは別[^repair-nvim] |
| `mise run repair:security` | 変更を行わず、生成時にmodeを設定する旨を表示する互換入口 | 鍵の権限検査・修復の成功を意味しない。generate:identityへの既存依存を保持する[^security] |
| `mise run generate:identity`等の個別task | 対象taskとその依存を実行する | identityは直接呼ぶたびに所有・入力を検証し、必要時だけ世代生成・復旧する。他taskには省略条件がある。「名前を指定すれば欠損だけ直す」とは限らない[^identity][^mise-tasks] |
| 配置済み`repo-tasks/update/lazy-lock`を直接実行 | 選択local revisionの隔離plugin更新とlock候補生成 | 一時HOME/XDGへ取得・書込し、成功/失敗artifactを保持。通常sourceへの採用とGit/PR公開は別。mise run経由ではtask開始前の自動導入があり得る。[範囲と採用手順](development.md#neovimrestoreと更新を混同しない)を確認する[^update-nvim] |

checkごとの保証範囲は[validation](validation.md)、Neovim更新の詳細は[development](development.md)を正本にします。`dotfiles-diagnose --probe wsl-openssh`はdoctorに含まれず、外部通信・認証・一時署名commitを伴います。検査名だけで非変更と判断しないでください。

現行に単一の汎用`repair`コマンドはありません。mise本体には明示的な`--install`入口がありますが、初期導入全体はconfig生成・package script等に分散しています。タスクが実際にどのコードを実行するかは、sourceとレンダリング済み配置物を照合して判断します。[^tasks][^config]

<a id="diagnostic-entry"></a>
# 診断の直接入口と移行

配置後の`~/.local/bin/dotfiles-diagnose`を使用する。既存のshellで有効化済みの、信頼できるtool実体をPATHへ渡す。`*/shims`、相対・空PATH要素は除外するので、shimだけのPATHでは必須実体の不足として失敗する。自動でmise activate/execを実行して補わない。実体が存在しても採用版・provider・全toolの動作を確認したことにはならない。mise本体だけは固定pathの`--version`を下記の一時環境で実行し、pin不一致・実行失敗を報告して保持する。

版表示もmiseの起動処理を通るため、通常の利用者環境では実行しない。`check:toolchain`は版照会のsubprocessだけを`env -i`で起動し、HOME・cwd・XDG・miseのconfig/data/cache/state/system config/system dataを新しい一時directoryへ向ける。一時pathは物理pathへ揃え、TMPDIRにsymlinkがあってもcwdと探索上限を一致させる。PATHはOS utilityのみとし、利用者のmise設定・log path・認証command等の環境overrideを継承しない。`MISE_NO_CONFIG/NO_ENV/NO_HOOKS=true`、探索のceiling、auto-install禁止、`MISE_CACHE_PRUNE_AGE=0s`、`MISE_OFFLINE=true`と`CI=true`をそのsubprocessに指定する。CI指定は最新版照会の停止用で、外側checkの判定をCIへ変更しない。

この一時領域は成功・版不一致・実行失敗後に片付ける。migration/cache書込を利用者の永続状態から分離するための費用であり、無書込commandという意味ではない。SIGKILLや電源断では一時領域が残り得る。採用mise版以外や任意wrapperがこれらのdirectory/設定を無視する場合を封じるOS sandboxではない。使用する実体は信頼できるものに限り、版更新時に[根拠と検証](decisions/convergence.md#diagnostic-version-isolation)を見直す。global設定・既存cacheの書換えで抑制する方式は使わない。

個別診断は`dotfiles-diagnose check:nvim`等、実行probeは`dotfiles-diagnose --probe nvim`等で選ぶ。[検査一覧と副作用](validation.md#diagnostic-boundary)を確認する。probeはCLI実行、cache/temp書込、認証・通信を伴い得るので静的read-onlyとは呼ばない。CIも同じ必須判定を使用する。CI側の既に導入済みtoolのPATH設定には、起動前にauto-installを無効化したmise execを使うが、これはCI管理configに限定した別の段階である。

採用mise v2026.6.11のtask実行は、本体のscriptより先にtoolsetを導入する。`MISE_AUTO_INSTALL`等をcheck内でexportするだけでは従来入口を保護しない。専用入口はtask runner自体を通らず、補助的にauto-install関連環境変数もfalseへ固定する。local/private mise設定を上書きしてこの問題を解決しない。選択理由と代案は[Decision](decisions/convergence.md#diagnostic-boundary)に記す。

source更新だけでは既存taskは変わらない。入口とcheck/probe一式を同じsourceから配置する必要がある。古い配置や別checkout、利用者側のtask overrideからの呼出しを新契約と見なさず、実機適用は通常のapplyの副作用境界で扱う。このタスクでは実機適用していない。

# applyで通る段階

公式の概略順はtarget計算 → before → target反映 → afterです。ただし、使用したchezmoi 2.70.4の実装はentryを順に評価・適用し、file/symlinkのtemplate内容は遅延評価します。最小sourceでWezTerm/distro不足より先にbeforeが実行されることを確認しました。render失敗なら全before・全targetが未変更、と解釈しないでください。config生成のop照会は引き続きapplyより前です。[^order][^apply-implementation]

`run_onchange_`は、レンダリング後のscript内容が最後の成功時から変わった場合などに実行されます。下表の各scriptが毎回すべて動くわけではありません。before / target / afterの区分と、同区分内の順序を区別します。[^scripts][^order]

| 段階 | 現行の処理 | 書き込み・外部依存・省略条件 |
|---|---|---|
| config生成（init等） | ホスト判定、op項目取得、identity入力とパスを設定へ保存 | 認証・Windows照会・config更新。通常applyのたびに最新identityへ更新する段階ではない[^config] |
| source読込 | read-source-state.pre → `.bootstrap-mise.sh --check` | `~/.local/bin/mise`が実行属性を持つ通常file（symlink参照先も可）かだけを検査。mise実行・pin照合・取得・mkdir・chmodはしない。不在・非実行file等では必要な明示操作を示して停止[^bootstrap] |
| before scripts | identityのlegacy参照保存、OS別package導入 | identityのbefore_05はGit/Pythonを使い、旧routingを新しいentryへ保存する（詳細は[identity](identity.md#生成の切替と既存配置からの移行)）。Python不足・移行衝突ではtarget反映前に停止する。Linuxのpackage DB・sudo、macOSの`brew bundle install --no-upgrade`（[制御と限界](#homebrew-packages)）、WSLのWinGet。task配置前に必要な依存を用意する経路。WinGetは完全IDとsourceを指定し、正常な未導入だけをinstallする。照会障害・曖昧な出力・hash不一致は停止する（[Windows package契約](platforms/wsl.md#windows-packages)）[^linux-script][^brew-script][^win-script] |
| target反映 | chezmoiの静的配置・symlink・external・remove | ホーム配下への配置。旧パス名だけによる恒久削除は停止。externalには固定版とfloating参照が混在[^ignore][^remove][^externals] |
| identity after_10 | 毎回、所有・個別出力・入力digestを検査 | Python engineを直接起動する。正常同一入力は生成しない。所有根拠喪失は停止する。[R10a契約](identity.md#identity-convergence)を参照 |
| afterの共通wrapper | XDG / PATHを設定し、固定パスのmise install → lifecycle:post-apply | tool導入・通信。GitHub token系環境変数がなければop読取コマンドをinstallの環境に渡す経路がある。毎回認証が発生するとの断定ではない[^wrapper] |
| post-apply graph | security互換入口・pnpm、Linux shell | 依存graphなので全taskが表記順に直列実行されるわけではない。生成物はgraph終了後の専用after_30/40/41/42へ分離した[^lifecycle][^identity][^completions][^mise-tasks] |
| 生成物 after_30/40/41/42 | 補完、bat、Vale、macOS pbfileを毎apply確認 | tool準備後に配置済みtaskを直接起動。個別の正常同一入力では生成・通信・出力書換なし。[R10c契約](#generated-assets)を参照 |
| WSL用after_50 wrapper | 配置済みsync:1password-agent → sync:weztermを直接実行 | 毎applyに2fileの欠損と前回内容を照合。CI・非WSLは対象外。必須source欠損・競合は非zero。共通mise graphは再起動しない。[契約](#windows-settings-sync)[^wsl-wrapper] |

通常applyのgraphにはdoctorとrepair:nvimは含まれません。CIの通信を伴う統合jobはinit --apply一回の後にverify、repair:nvim、専用入口でのlocal診断を別に呼びます。隔離fixture・render検査は独立jobで先に実行します。この追加段階の成功を通常apply単体の保証へ移しません。[^lifecycle][^ci]

<a id="ownership-preservation"></a>
# 権限と旧ファイルの移行

`repair:security`は既存の依存graphと直接呼出しを壊さないために残すが、探索・chmod・削除は行わない。sourceの`private_`属性による管理directoryのmode設定、generatorによる生成公開鍵0600・allowed_signers 0644の設定は継続する。秘密鍵は生成しない。未知の鍵をこのtaskで「修復済み」と扱わない。[^security][^identity]

`.chezmoiremove.tmpl`による旧パスの継続削除は停止した。手動再導入されたdocker-cli/shim、同名の設定やtask、旧WSL bridgeも残る。不要物の整理が必要なら現在の所有・内容・参照を個別確認する。古いtaskやserviceが残るため、別の入口や有効なserviceから参照されていないかは移行時に確認する。この変更だけで古いserviceを停止・無効化したとは扱わない。[^remove]

保持した旧ファイルは、単なる未参照の残骸とは限らない。次はsourceから分かる到達経路であり、実機での存在・内容・有効状態は未確認である。

| 残る対象 | 現行sourceから分かる影響 |
|---|---|
| `~/.config/nvim/lua/plugins/fzf.lua` | [Lazy設定](../dot_config/nvim/lua/config/lazy.lua)が`import = "plugins"`を指定しているため、残存fileは通常起動で読まれ、plugin構成へ作用し得る。履歴上の旧specは`fzf-lua`と`<leader>ff/fg/fb`を設定するため、現行pickerと競合し得る。削除停止は旧pluginの無効化を意味しない[^legacy-fzf] |
| `~/.config/mise/repo-tasks`内の旧task | [task discovery設定](../dot_config/mise/config.toml.tmpl)のincludes配下に残る。明示呼出しや利用者側依存から実行され得る。現行の[lifecycle](../dot_config/mise/repo-tasks/lifecycle/executable_post-apply.tmpl)と[doctor](../dot_config/mise/repo-tasks/doctor/executable__default.tmpl)は新task名を参照するが、旧task自体の無害化はしない。特に履歴上の`setup:security`は未所有の`id_*`秘密鍵を再帰chmodし、旧`setup`もこれに依存する。旧実体が残る端末の`mise run setup`／`setup:security`は同じ危険へ到達し得る[^legacy-security] |
| `~/.config/mise/tasks`内の旧task | 同設定の`disable_paths`で通常の探索から外している。ただし直接path指定や別設定からの利用まで停止しない |
| WSLの旧`1password-bridge.service`と`default.target.wants`リンク | 有効なwantsリンクが残れば旧bridgeはuser serviceの自動起動候補のまま。現行[WSL lifecycle](../dot_config/mise/repo-tasks/lifecycle/executable_wsl-post-apply.tmpl)にbridgeの停止・無効化はなく、履歴上のunitは`agent.sock`の削除・relay起動と`Restart=always`を持ち、旧service taskは`enable --now`を実行する。Windows OpenSSHへの移行完了をこの保持検査で証明しない[^legacy-bridge] |

これらの自動読込・起動を確実に止める必要がある端末では、現在の内容・参照・利用意図を確認してから個別の移行を行う。未知のfileを名前だけで消す処理には戻さず、実機を調べていない今回の変更で機能面まで安全になったとは主張しない。

source更新だけでは配置済みrepair taskは変わらない。採用sourceからの配置更新時にはwrapperがrepair sourceのhashを入力に持つため、post-apply graphが再実行され得る。他の生成・tool導入の副作用は通常のapplyと同じ境界で確認する。実機適用は今回未実施であり、過去の削除・権限変更の復元も行わない。[^wrapper]

<a id="homebrew-packages"></a>
# Homebrewの不足導入と明示更新

macOSのbefore scriptはPATHで選ばれたHomebrewを使う。不在時は非zeroで初回準備を案内し、installerを起動しない。[Homebrew公式](https://brew.sh)の手順で本体とPATHを準備してからapplyへ進む。別prefixへの自動切替も行わない。R13の初回導入全体を自動化したものではない。

通常経路は一時Brewfileへrenderした宣言を`brew bundle install --no-upgrade --file=...`へ渡す。CIはheadlessのみ、非CIはmedia/GUIも対象にする。全宣言をこの呼出しの必須対象とし、非zeroはapplyへ伝播する。`run_onchange`は維持するため、成功済みscriptの内容が同じなら実行されず、削除済みpackageを毎applyで復旧する契約ではない。[^brew-script][^brew-bundle]

| 制御 | 通常経路で抑えるもの |
|---|---|
| `--no-upgrade` | Bundleによる既存の宣言項目の版更新 |
| `HOMEBREW_NO_AUTO_UPDATE=1` | command前のHomebrew/metadata自動更新。優先する`HOMEBREW_FORCE_API_AUTO_UPDATE`もunset。明示`brew update`も通常経路から除去 |
| `HOMEBREW_NO_INSTALL_CLEANUP=1` | installに伴う旧版・cache等の自動cleanup |
| `HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1` | install後の既存dependentsへの追随upgrade/reinstall |
| Bundleのcleanup設定2種とbrew/cask skip設定をunset | 継承環境による未宣言package削除、宣言の成功skip |

制御はこのscriptの子processに限定する。必要な依存は通常どおり解決するため、依存の版更新・link・post-install・caskのinstaller等の変更は残る。dependentsの自動修復を抑える分、既存consumerの互換性は別途確認が必要になる。任意のformula/cask、利用者の`brew.env`や別版Homebrewを隔離する仕組みでも、完全な版lockでもない。確認した公式実装と限界は[macOS](platforms/macos.md#homebrew-policy)を参照する。[^brew-man]

更新したい場合は対象を選び、既存のHomebrew CLIで明示する。例えば`colima`を選んだ保守作業は次の通り。**今回のsource検査では実行していない。**

```sh
brew update
HOMEBREW_NO_AUTO_UPDATE=1 HOMEBREW_NO_INSTALL_CLEANUP=1 brew upgrade --formula colima
```

`brew update`はHomebrew本体・package情報を更新する。`upgrade`は指定formula（caskなら`--cask <name>`）と必要な依存・既存dependents等へ影響し得る。引数なしの全件upgradeや`bundle cleanup`はこの手順に含めない。利用者が直接必要とするpackageを追加するときはsourceの`packages.yaml`へ反映する。Homebrewが解決する推移依存の手動列挙は求めない。版はBrewfileで厳密固定されない。mise主担当の5 CLIの版変更はmiseのsource宣言で扱う。[更新元](development.md)を参照。

# 手動更新されたmise・brewへ起こり得ること

| 状態 | 現行経路が行うこと | 実行前の扱い |
|---|---|---|
| `~/.local/bin/mise`がpinより新しい | 更新済みsource読込hookは保持。`--install`も不一致を報告して停止 | 版・導入元を確認しpinへの採用か所有者による明示置換を決める。PATH上の別miseへの自動fallbackはない[^bootstrap] |
| mise toolを直接install / upgradeした | sourceのtarget反映とmise installは、採用済み宣言の明示的な移行判断とは別に動く | 宣言・導入済み・有効版を分ける。upgradeの`--bump`等がどのconfigを変えたかは未確認。手動版の保持・採用は[設計案](decisions/convergence.md)で判断[^mise-install][^mise-upgrade] |
| targetのmise configを直接編集した | chezmoiのtarget反映で差分が出る | 差分をsourceへ採用するか、置換するか、別scopeへ分けるかを決める。自動の逆輸入は実装されていない |
| brewで既存項目を更新・追加した | macOS before scriptが実行されると不足導入用のbundle install | 宣言対象の既定upgrade・自動metadata更新・自動cleanup・既存dependentsの追随更新を抑える。必要な依存導入やlink等まで無変更とはしない（[契約](#homebrew-packages)）[^brew-script][^brew-bundle][^brew-man] |

上表は現行の可能な経路です。この端末で実際にdowngrade・cleanupが起きたという観測ではありません。手動更新の詳細は利用者報告の範囲に留まります。[^user]

# 終了コードだけでは分からないこと

- **欠損の境界**：identity・補完・bat・Vale・macOS pbfileは専用afterから毎回確認する。所有receiptや固定entryの喪失、管理外変更との競合は自動復旧せず停止する。WSL・非CIのWindows2設定も専用afterから毎回確認する（[同期契約](#windows-settings-sync)）。[^wrapper][^mise-tasks]
- **生成失敗の扱い**：補完・initは[下記契約](#completion-generation)で旧正常出力を保持し、必須生成失敗を非zeroにする。pbfileのsource・Vale config欠落はR10cで非zeroへ変更した。Windowsの必須copy元欠損もR14で非zeroへ変更した（[契約](#windows-settings-sync)）。[^completions][^tasks]
- **identityの途中失敗**：R05では検証済み世代への参照切替まで旧routingを保持する。before scriptを含む移行、空入力の拒否、意図的解除の`--clear`、中断後のlock確認は[identity](identity.md#生成の切替と既存配置からの移行)に従う。apply全体やagent設定のrollbackではない。[^identity]
- **doctorの範囲**：専用入口は通常Neovim初期化・chezmoi verify・mise run/execを呼ばない。合格表示は選択したlocal検査だけを指す。PATHの未知wrapperや実体改変まで無副作用と保証するsandboxではない。認証・provider・CLI生成は明示probeへ分ける。[^check-nvim][^doctor]
- **CIの限界**：Ubuntu/macOSのCI分岐を使う。2回のapply比較、実1Password、手元の手動更新、Windows側copyの成功はこのworkflowだけでは分からない。[^ci]

# 失敗したとき

失敗した段階、すでに反映した対象、残った出力を確認します。全体rollbackは現行にありません。エラーを直して同じ入口を再実行しても、成功済みscriptやtaskの省略条件によって処理範囲は変わり得ます。[^scripts][^mise-tasks]

一括の履歴消去、生成directory全削除、全tool更新を通常の再試行にしません。個別taskを使う場合も依存・出力範囲・省略条件を確認します。identityの欠損復旧・停止条件は[出力別契約](identity.md#identity-convergence)に従います。repair:security自体は変更しない互換入口です。対象だけを復旧できるようにする変更は[convergence](decisions/convergence.md)に残します。[^identity][^security]

ログを共有する際は鍵・アカウント識別子・生成identityの個人情報を除き、対象の種類、段階、成否、未確認事項を残します。未実行の検査を成功として記録しません。

[^bootstrap]: [mise本体の読込検査・明示導入](../.bootstrap-mise.sh).
[^config]: [identity入力・ホスト情報の取得とread-source-state hook](../.chezmoi.toml.tmpl).
[^hooks]: [chezmoi Hooks：dry-runでもhookは動く](https://www.chezmoi.io/reference/configuration-file/hooks/).
[^mise-config]: [mise task discovery・自動導入設定](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/config.toml.tmpl).
[^tools]: [観測時のmise tool宣言](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/conf.d/10-tools.toml).
[^linux-script]: [Linuxのsudo・package導入](../.chezmoiscripts/run_onchange_before_00-provision-linux-packages.sh.tmpl).
[^brew-script]: [Homebrew不足導入と前提検査](../.chezmoiscripts/run_onchange_before_provision-macos-homebrew.sh.tmpl).
[^win-script]: [WinGetによるWindows package導入](../.chezmoiscripts/run_onchange_before_provision-windows-packages.sh.tmpl).
[^wrapper]: [post-applyの起動条件・mise install・認証の受け渡し](../.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl).
[^init]: [chezmoi init](https://www.chezmoi.io/reference/commands/init/).
[^scripts]: [chezmoi scripts：onchangeの成功済み内容による再実行判定](https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/).
[^verify]: [chezmoi verifyの確認範囲](https://www.chezmoi.io/reference/commands/verify/).
[^doctor]: [doctorの共通検査集合](../dot_config/mise/repo-tasks/doctor/executable__default.tmpl).
[^check-nvim]: [Neovim lockの直接比較と実体の存在検査](../dot_config/mise/repo-tasks/check/executable_nvim.tmpl).
[^lazy]: [Neovim起動時のlazy.nvim取得](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/nvim/lua/config/lazy.lua).
[^repair-nvim]: [採用lockからのLazy restore](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/repair/executable_nvim.tmpl).
[^security]: [権限変更を行わない互換task](../dot_config/mise/repo-tasks/repair/executable_security.tmpl).
[^identity]: [identityの検証・世代切替](../dot_config/mise/repo-tasks/generate/executable_identity.tmpl).
[^mise-tasks]: [mise v2026.6.11：task省略と依存順序](https://github.com/jdx/mise/blob/v2026.6.11/docs/tasks/running-tasks.md).
[^update-nvim]: [選択revisionからの隔離lock候補生成](../dot_config/mise/repo-tasks/update/executable_lazy-lock.tmpl).
[^tasks]: [repo所有taskの実装](https://github.com/tsubasahomma/dotfiles/tree/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks).
[^order]: [chezmoi application order](https://www.chezmoi.io/reference/application-order/).
[^ignore]: [chezmoiによる配置の除外](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiignore.tmpl).
[^remove]: [旧パスの恒久削除を停止したremove定義](../.chezmoiremove.tmpl).
[^externals]: [外部assetとrefresh指定](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiexternal.toml.tmpl).
[^lifecycle]: [OS別post-apply依存graph](../dot_config/mise/repo-tasks/lifecycle/executable_post-apply.tmpl).
[^completions]: [補完・initの個別検証と切替](../dot_config/mise/repo-tasks/generate/executable_completions.tmpl).
[^wsl-wrapper]: [WSL syncの起動条件とCI除外](../.chezmoiscripts/run_after_50-wsl-sync-services.sh.tmpl).
[^ci]: [隔離検査とUbuntu/macOSの一回apply統合](../.github/workflows/compliance.yml).
[^mise-install]: [mise v2026.6.11 install：導入と有効化は別](https://github.com/jdx/mise/blob/v2026.6.11/docs/cli/install.md).
[^mise-upgrade]: [mise v2026.6.11 upgrade：更新とbump](https://github.com/jdx/mise/blob/v2026.6.11/docs/cli/upgrade.md).
[^brew-bundle]: [Homebrew Bundle：既定upgrade・no-upgrade・lock非対応](https://docs.brew.sh/Brew-Bundle-and-Brewfile).
[^brew-man]: [Homebrew brew(1)：導入に伴う依存変更と自動cleanup](https://docs.brew.sh/Manpage).
[^user]: 端末構築後にmise関連・brewを直接更新したとの利用者報告。実機観測ではない.

[^mise-pin]: [観測時のmise本体pin](../.mise-version).

[^install]: [chezmoi: Install](https://www.chezmoi.io/install/)。公式の導入方法であり、このrepoの初回通し試験の証拠ではない。

[^legacy-security]: [退役前のsetup:securityと同directoryの_default依存](https://github.com/tsubasahomma/dotfiles/blob/eac4c9e49eae7d3441a7cf7aa04ad3838ba73697/dot_config/mise/repo-tasks/setup/executable_security.tmpl)。repoの固定revisionを読取確認。実機の残存内容・稼働状態の観測ではない。

[^legacy-fzf]: [退役前のfzf-lua specとkeymap](https://github.com/tsubasahomma/dotfiles/blob/41692b36e85d881d2e3d6505934cafa9c3e70f48/dot_config/nvim/lua/plugins/fzf.lua)。repoの固定revisionを読取確認。実機の残存内容・稼働状態の観測ではない。

[^legacy-bridge]: [退役前のWSL bridge unit](https://github.com/tsubasahomma/dotfiles/blob/9d8cbe39596177cc5ddb217d15ecade9b360ebab/dot_config/systemd/user/1password-bridge.service.tmpl)。repoの固定revisionを読取確認。実機の残存内容・稼働状態の観測ではない。

<a id="completion-generation"></a>
# 補完・init生成の切替

`generate:completions`は宣言済みCLIの補完（pnpm・delta・gcloudも含む）、mise・chezmoi補完、zoxide・starship initを必須とする。PATH検出のWezTermのみ任意で、不在・生成失敗・空/構文不正は警告し旧出力を保持する。必須項目は同じ条件で非zero終了する。これは全CLIの補完を提供する契約ではなく、[現在の生成対象](../dot_config/mise/repo-tasks/generate/executable_completions.tmpl)に限る。[^completions]

出力の隣に一時directoryを作り、generator終了値・非空・`zcompile -U`の構文検査が通ったsourceだけをZshの`zf_mv` builtinでrenameする。backup/復元も同じbuiltinを使い、task終了後に外部mvだけが残ってpublishしないようにする。新しいzwcは配置せず、旧対象zwcと正確なconsumer dumpはcommit直前に退避し、rename失敗/捕捉した中断では復元する。source rename後は退避cacheを削除する。完了済みの別出力は巻き戻さない。SIGKILLや停電では一時directory・退避zwcが残り得るが、未commitの旧sourceは保持される。同じgeneratorの並行実行は`$XDG_CACHE_HOME/zsh/.completion-generation.lock`の通常fileに対する`zsystem flock`で拒否する。Zshのsystem/flock・files/zf_mv対応がない環境は非zeroで止まる。lockはprocess終了時（SIGKILLも含む）にkernelが解除する。file自体は残し、利用中writerと異なるinodeをlockしないよう削除しない。残存stageは自動回収せず、active writerがなく旧source/退避cacheの状態を確認できた場合だけ個別に整理する。[^completions]

gcloudは選択したSDKのincludeを検証済みの通常fileとして保存し、その固定pathをwrapperが読む。旧symlinkはリンク自体を置き換え、SDKのfileは変更しない。includeとwrapperは個別切替なので、後者の失敗時には更新済みincludeと旧wrapperが残り得る。wrapperの参照pathは従来どおりである。

補完sourceの検証後・rename前に、consumerが使う正確な`$XDG_CACHE_HOME/zsh/zcompdump`とその`.zwc`を退避する。これによりrename直後の中断で旧dumpが新しい`#compdef`登録を隠す窓をなくす。未知のglob一致file、`$HOME/.zcompdump*`、外部asset側の補完/zwcを削除・再compileしない。出力や対応zwcがdirectory等なら拒否し、gcloud旧include以外のsymlinkも拒否する。設定済みXDG cache root配下の固定`zsh`/`completions`/`init` directoryのsymlinkも拒否する。directory全体の`completions.zwc`は新sourceを隠し得るため、存在時は削除せずエラーにする。

構文検査はtool固有の補完動作・外部commandの存在を保証しない。実toolの出力互換性、doctor全体の意味は別途検証する。補完の再実行・欠損検知は下記R10b契約に従う。source変更を実機へapplyした状態ではない。


<a id="completion-convergence"></a>
# R10b 補完の毎apply検査

`run_after_30-completions`はafter_20のtool準備・共通graph終了後、配置済み`generate/completions`をZshで直接起動する。補完のgraph依存と`provision:pnpm`依存、miseのsources/outputs判定を外した。初回のtool installは従来のafter_20が担当し、二回目の補完確認だけでは共通graphを起動しない。補完定義・生成templateだけの変更も共通wrapperのtriggerから外した。[^completion-after]

明示的な補完のみの収束は`/bin/zsh -f "$XDG_CONFIG_HOME/mise/repo-tasks/generate/completions"`でも同じ判定へ到達する。Python 3とZshの既存前提が必要。`mise run generate:completions`も同じtaskを呼ぶが、mise run自身のtask開始前の自動導入設定は別なので、導入を避ける用途では直接入口を使う。task内では`MISE_AUTO_INSTALL=false`・`MISE_EXEC_AUTO_INSTALL=false`・`MISE_TASK_RUN_AUTO_INSTALL=false`・`MISE_OFFLINE=true`と`exec --no-deps`で導入と自動依存準備を抑止し、不足時は非zeroで止まる。採用版v2026.6.11のexec実装・実binaryのhelpと照合した。[^completion-exec]

排他中に各出力の非空・通常file・0644・内容hashを、隣の隠し`.<basename>.generation.json`に記録した前回成功値と照合する。対象zwcが存在すれば再生成する。入力hashにはrender済みgenerator（共通template結果を含む）、Zsh、実際に使うmise/chezmoi/CLIの絶対path・解決先・mode・bytesを使う。`mise which --tool`で採用した絶対pathを`mise exec`へ渡す。pnpm/Codexは選択したNodeを実行PATHの先頭へ固定し、installation treeも含める。gcloudは`mise where`で選択したSDK includeのpathと内容を検査し、SDK自体は編集しない。mise補完が内部で使う`usage`は同じmise exec環境のPATHで解決し、実体bytesと有無を検査する。不在・生成失敗時のmise組込み補完へのfallbackは維持する。WezTermとtrは実行PATHの実体を検査する。[^completion-state][^completion-which][^completion-where][^completion-usage]

同じ正常入力ならgenerator・zcompile・source/receiptのrename・dump無効化を省略する。個別欠損・内容/mode変更・採用依存変更はその出力をR07の切替手順で再生成する。generator全体のrender変更は保守的に全出力を再検証・生成する。receiptは所有manifestではなく再生成省略用で、欠損なら生成、未知schema・壊れたJSON・symlinkなら保持して停止する。source commit後にreceiptをparentのbuiltinでrenameするため、途中停止時は次回再検査される。任意WezTermの失敗は引き続き警告である。

依存hashは毎回新しいTMPDIR内のprivate directoryで実行中だけ共有する。同じfile inodeと内容識別metadata、同じpackage treeを一回のapply内で重複して読まず、apply間のmtime cacheにはしない。正常時もtemporary fileとmise自身の照会cacheは書き得るが、補完source・receipt・zwc・dumpを書き換えない。検査中のtool upgradeやgenerator外からの同時書込をtransactionに含めず、実行中は依存を固定する。強制終了のtemporary directoryは自動回収しない。

診断consumerはR08の非変更・存在検査のままで、receiptやCLIを実行しない。診断合格は鮮度保証ではない。外部assetの`_git`/`_eza`/git-completion.bashはこのgeneratorの入力でなく別consumerなので、それだけの変更による再生成はしない。tool宣言の文面・mise pinだけの変更も、採用実体が同じなら補完入力にしない（共通graphの既存triggerとは別）。gcloud本体/Python版は保存includeの内容に影響せず対象外。OSライブラリ、ユーザーCLI設定、任意環境変数全体、外部package stateを網羅するfingerprintではない。

[^completion-after]: [毎回の補完after入口](../.chezmoiscripts/run_after_30-completions.sh.tmpl)。[chezmoi application order](https://www.chezmoi.io/reference/application-order/)に従う。
[^completion-state]: [入力・出力hashの照合](../.chezmoitemplates/completion_state.py)。
[^completion-exec]: [mise v2026.6.11 exec実装](https://github.com/jdx/mise/blob/v2026.6.11/src/cli/exec.rs)。auto_installとexec_auto_install、no_deps、絶対pathの実行。2026-11-11参照。
[^completion-which]: [mise v2026.6.11 which実装](https://github.com/jdx/mise/blob/v2026.6.11/src/cli/which.rs)。tool指定・有効toolsetから実体を解決。2026-11-11参照。
[^completion-where]: [mise v2026.6.11 where実装](https://github.com/jdx/mise/blob/v2026.6.11/src/cli/where.rs)。選択した導入directoryを解決。2026-11-11参照。

[^completion-usage]: [mise v2026.6.11 completion実装](https://github.com/jdx/mise/blob/v2026.6.11/src/cli/completion.rs)。toolset.full_envのusageと組込みfallback。2026-11-11参照。


<a id="generated-assets"></a>
# R10c bat・Vale・pbfileの毎apply検査

`after_40` → `cache:bat`、`after_41` → `sync:vale`、macOSの`after_42` → `build:pbfile`を配置済みpathから直接呼ぶ。共通`after_20`のtool準備と`after_30`補完の後に進む。taskのmise `sources/outputs`判定は撤去し、各checkerだけが生成要否を決める。bat theme・Vale config・pbfile source/taskのhashも共通wrapperから撤去した。このためそれらだけの変更や出力欠損でtool install、pnpm設定、Linux shellを再起動しない。Windows同期の独立した毎回検査は[after_50](#windows-settings-sync)で行う。共通manifest等の変更で共通onchangeが起動する既存契約は残る。

| 系統 | 実行時の入力・必須出力 | 生成・検証・通信 |
|---|---|---|
| bat | 配置後の`bat/themes`と`bat/syntaxes`内file、選択されたbatの実体bytes/path/version、配置task。必須は`syntaxes.bin`・`themes.bin`・`metadata.yaml` | 公式`cache --build --source … --target …`でstaging。list-themes/list-languagesとCatppuccin MochaでのSwift描画、metadata版を確認。warningによるbuilt-in fallbackも拒否。bat 0.26.1がstdoutへ通知して成功終了するtheme parse失敗と未解決syntax contextも拒否。未知cache、acknowledgements、利用者theme/syntaxは消さない |
| Vale | 明示`vale.ini`全体、選択Vale実体、配置task、Google package指定（local packageはbytesも）。同期で採用したGoogleの各`.yml`と`vocab.txt`（空も可）・`meta.json`をreceiptへ記録し、すべてを次回の必須出力とする | 採用packageだけを指定する一時configとStylesPathで`--no-global sync`。GoogleのAcronyms/AMPM ruleを最低条件とし、取得した全ruleをValeで読み込む。config bundle・他package・未知出力は停止。同期時だけremote通信し得る。通常の同一正常入力は通信しない |
| pbfile | macOSのみ。Swift source、xcrunが選ぶcompiler実体/hash/version、SDK path/version/SDKSettings.json、architecture、deployment target、配置task。必須は実行可能な`.local/bin/pbfile` | 選択compilerへSDKを明示し一時build。生成したbinaryを引数なしで起動してloader/終了を確認（現行sourceはpasteboardへ到達せず終了）。compile/検証失敗、source/compiler/SDK欠落は非zero。module cacheも一時directory。非macOS taskは明示的な非該当 |

generatorは既存identityと同じPython 3.9+を使う（検証runnerはtomllibのため3.11+）。bat/Valeの解決は導入済みtoolへの`mise which`だけで、自動installを無効化しofflineにする。その実体を直接実行するため、native配布のbat/Valeを対象とし任意のruntime wrapperには一般化しない。BAT_/VALE_の環境overrideは生成と検証から除き、明示pathでconsumer用の出力を作る。利用者がconsumer側で別cache/configを指定した場合はこの管理対象外となる。

所有receiptは`XDG_STATE_HOME/dotfiles-generators/{bat,vale,pbfile}.json`に一つずつ置く。初期化できるのは今回生成するfile名がすべて空いている場合だけ。既存fileの名前から旧管理物と推定しない。receiptなしの既存出力、receiptの欠損・不正、hash/modeの異なる既存出力、symlinkによる出力先redirectは保持して非zero。正常なreceiptが示すfileの欠損は再生成し、他の正常fileは同じbytes/modeなら置換しない。Vale upstreamで不要になった旧ruleは、receiptと一致したfileだけを除去する。未知style・未知file・手動toolは引き取らない。

旧配置からは、所有者が既存出力を確認し、必要な独自内容を保持したうえで対象fileを別の保管先へ移し、空いた対象へ生成する移行が必要になる。receiptを手作りして上書き権限を与える手順は提供しない。bat cache metadataには生成時刻があり、pbfile binaryも同一sourceからbyte一致するとは限らないため、再生成との単純一致を自動移行条件にはしていない。実機の移行は未実施。

既存配置での具体的な移行順序は次のとおり（実施は別作業）。

1. 有効なXDG pathとconsumerのoverrideを確認し、batの三file、Valeの既存Google package全file、pbfile実体の内容・mode・導入元を別の保管先に記録する。source theme/syntax、Google以外のstyle、手動toolには触れない。
2. 既存Google内の独自ruleや変更済みruleを確認する。採用する独自ruleは別style名として保全し、必要ならsourceのBasedOnStylesへ反映する。同名独自ruleを新Googleと共用して上書きさせない。
3. 利用者が引受けを決めた旧出力だけを保管先へ移し、生成予定file名を空ける。batは三fileだけ、pbfileは当該実体だけ。Valeは取得版によって名前が変わるため、既存Googleの独自内容を保全したうえでGoogle directoryを退避するのが明確である。未判断の競合は残し、taskの停止を維持する。
4. 対象の配置済みtaskを直接bashで実行する（通常mise task実行前の自動導入を避ける）。正常な初期生成とreceipt、consumerを確認し、旧保管物は自動削除しない。別系統のtool準備や実機全体のapplyを移行コマンドに混ぜない。

検証済み候補と同一内容の既存fileだけを採用する代案はあり得るが、今回その自動採用機能はない。Valeの完全一致も取得物の出所・利用者の意図まで証明しないため、名前や一致だけから所有を拡張しない。

全候補を生成・検証し、入力と既存出力を再照合してからfileごとにrenameする。途中の生成・通信・検証失敗は旧出力とreceiptを保持する。receipt切替前に捕捉できたpublishエラーはbackupから戻す。receipt切替後の捕捉済み中断は新出力と新receiptを維持し、旧出力だけへ戻さない（終了は非zero）。同一receiptで欠損を戻す途中では、復旧済みfileは正しい内容で残り、未復旧分は次回も欠損として検知する。commit状態を調べるreceipt再読が失敗した場合やrollback自体が失敗した場合は`.publish-*`の名前付き旧fileと旧receiptを残して保管先を報告する。SIGTERM/SIGKILLでは部分反映と一時backupが残り得る。複数fileの同時可視化、SIGKILL/停電耐久性、generator外の同時編集は保証しない。各系統にkernel lockを置き、同じgeneratorの競合実行は非zeroとする。異常終了でreceiptと出力が不一致になった場合も黙って上書きせず、明示的な調整が必要。

裸の`Packages = Google`は今回維持した浮動参照である。remoteの変化は毎applyでは問い合わせず、入力変更・必須出力欠損によってsyncが必要な回に再解決する。その回に新しいstyleになる可能性があるため、旧版の同一byte復旧・同じ入力の厳密再現とは呼ばない。固定URL/local packageとartifact保存の代案、依存閉包の限界は[Decision](decisions/convergence.md#generated-assets)を参照する。

[^apply-implementation]: [chezmoi v2.70.4 applyArgsの逐次適用](https://github.com/twpayne/chezmoi/blob/v2.70.4/internal/cmd/config.go#L750)と[symlink templateの遅延評価](https://github.com/twpayne/chezmoi/blob/v2.70.4/internal/chezmoi/sourcestate.go#L2169)。版固有の実装と隔離fixtureを照合した。

<a id="windows-settings-sync"></a>
# Windowsの2設定同期

WSL・非CIでは`after_50`が配置済み2taskをbashで直接順番に呼ぶ。common `after_20`やmise taskのauto-installを毎回起動せず、Python 3.9+、Windows PowerShell interop、wslpathは準備済みの実体を使う。明示`lifecycle:wsl-post-apply`も同じ2taskへの既存入口だが、mise run自身の環境解決は専用afterとは別。同期の成功は設定fileの配送結果であり、アプリ導入・起動・GUI採用・unlock・認証の成功ではない。アプリ未導入の前提は[初回手順](#first-install)とpackage段階、同期元未配置は必須入力エラーとして区別する。同期taskはアプリを導入しない。

[helper](../.chezmoitemplates/windows_config_sync.py)はWindowsプロセスからUSERPROFILE / LOCALAPPDATAを取得し、wslpathで実際のmount先へ変換する。sourceはその回に配置されたbytesを読む。SOURCE欠損を成功skipにせず、空identity由来の有効なagent設定とは区別する。Windows設定先やreceipt・parentの不正、bridge/query/変換失敗は非zeroとなる。

| 検出状態 | 動作 |
|---|---|
| target・receiptともなし | `CREATED`。限定parentを作成し、内容とreceiptを初回配置 |
| receiptなし・targetが期待bytesと同一 | `ADOPTED`。targetのbytes/mtime/inodeを保持しreceiptだけ新設 |
| receiptなし・異なるtarget | 未所有の競合として保持停止 |
| 正常receipt・前回内容と現在入力が同一 | `UNCHANGED`。target/receiptを無書換 |
| 正常receipt・前回内容のままで入力変更 | stage検証後に`UPDATED` |
| 正常receipt・target単独欠損 | `RESTORED`。同回で現在入力から復旧。入力不変ならreceiptは無書換 |
| 手動編集・不正receipt・別destination | 内容を保持して停止。自動merge/forceはしない |

receiptを失った場合は初回規則を使う。異なる既存fileを上書きしたい場合は、差分を確認しsourceへ採用するか、必要な退避と対象を決めて別途整理する。receipt削除だけで異なる内容を採用できる仕組みにはしない。LOCALAPPDATA/USERPROFILEが別rootへ変わった場合、その新rootを初回規則で扱い、旧rootは変更・削除しない。旧`USERPROFILE/AppData/Local`への誤配置も削除しない。

targetと同じdirectoryの一時fileへ全bytesを書き検証してから、target、receiptの順にreplaceする。通常のreceipt公開失敗は自分が公開したtargetのinode/bytesと旧receiptを再確認して旧内容へrollbackする。rollbackも失敗する場合は非zeroでbackupを残す。出力単位の処理であり、2設定・receipt・apply全体の一括原子性や停電耐久性を保証しない。後続WezTermが失敗しても先行1Passwordの成功は残る。rollbackによるinode/mtimeの不変も保証しない。

lockはWindows target隣でexclusive mkdirし、自分が作った空directoryだけ除去する。他writerや中断による既存lockは盗まず停止する。強制中断後は残ったlock/stage/backup、targetとreceiptを確認し、実行中writerがないことと必要な退避を確かめて個別に復旧する。中断窓では新target・旧receiptが残り、lockを整理しても次回は競合停止になり得る。未知fileの再帰cleanupはない。

Windows editorはこのlockへ参加しないため、同期中は対象を手動編集しない。直前照合は任意の同時writerに対する完全な排他ではない。新fileのmodeと既存fileのPOSIX modeを扱うがWindows ACL保持は保証しない。UNC/device path、reparse point、redirected parent、hardlinkは対象外として停止する。別driveを指す通常のLOCALAPPDATA値は許容する。実DrvFsのrename/lock/ACL/PowerShell互換性とGUIの採用は[隔離検査](validation.md#windows-settings-sync)からは保証しない。
