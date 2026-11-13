---
type: Guide
title: sourceの変更・ツール更新・レビュー
description: 設定や依存を変更するときに正本、更新taskの副作用、必要なレビュー情報を確認する。
status: draft
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-13T06:49:21+00:00"
sources:
  - id: pin
    resource: "../.mise-version"
    title: "bootstrapが採用するmise本体版"
  - id: bootstrap
    resource: "../.bootstrap-mise.sh"
    title: "mise本体の読込検査・明示導入"
  - id: mise-root
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.mise.toml"
    title: "repo内tool要求"
  - id: tools
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/conf.d/10-tools.toml"
    title: "観測時のmise tool宣言"
  - id: packages
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoidata/packages.yaml"
    title: "OS別package宣言"
  - id: repair-nvim
    resource: "../dot_config/mise/repo-tasks/repair/executable_nvim.tmpl"
    title: "採用lockによるLazy restore"
  - id: update-nvim
    resource: "../dot_config/mise/repo-tasks/update/executable_lazy-lock.tmpl"
    title: "選択revisionからの隔離lock候補生成"
  - id: wrapper
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl"
    title: "post-apply wrapperのhash入力と起動条件"
  - id: scripts
    resource: "https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/"
    title: "chezmoi公式：render後のscript内容によるonchange判定"
  - id: renovate
    resource: "../renovate.json5"
    title: "Renovateのmanagerと更新単位"
  - id: ci
    resource: "../.github/workflows/compliance.yml"
    title: "CIの対象・実行段階・validator版"
  - id: user
    resource: "Maintainer decisions in the repository OKF design conversation, 2026-11-11"
    title: "単一bundle、PR template廃止、上流同期終了・Repomix退役の方向。文書移行の方針。実機操作は別"
  - id: lazy-source
    resource: "https://www.chezmoi.io/reference/source-state-attributes/"
    title: "chezmoi source state attributes"
  - id: lazy-usage
    resource: "https://lazy.folke.io/usage"
    title: "lazy.nvim Usage：waitと更新API"
  - id: lazy-task
    resource: "https://github.com/folke/lazy.nvim/blob/85c7ff3711b730b4030d03144f6db6375044ae82/lua/lazy/manage/task/init.lua"
    title: "採用版のtaskとprocess失敗処理"
  - id: lazy-restore
    resource: "../.chezmoitemplates/lazy_restore.lua"
    title: "採用lockを保持するrestore adapter"
  - id: git-clone
    resource: "https://git-scm.com/docs/git-clone"
    title: "Git clone：no-checkoutとsubmodule"
  - id: git-submodule
    resource: "https://git-scm.com/docs/git-submodule"
    title: "Git submodule update：親commitが指す版の初期化"
  - id: lazyvim-mason
    resource: "https://github.com/LazyVim/LazyVim/blob/83d90f339defdb109a6ede333865a66ffc7ef6aa/lua/lazyvim/plugins/lsp/init.lua"
    title: "採用LazyVimのMason setup・背景導入"
  - id: nvim-errmsg
    resource: "https://neovim.io/doc/user/vvars.html#v:errmsg"
    title: "Neovim v:errmsg：直近のエラーメッセージ"
  - id: merge-methods
    resource: "https://docs.github.com/en/pull-requests/reference/pull-request-merges"
    title: "GitHubのsquash/rebaseと元SHAの扱い"
  - id: protected-branches
    resource: "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches"
    title: "必須check・strict・linear history・admin適用"
  - id: automerge
    resource: "https://docs.renovatebot.com/key-concepts/automerge/"
    title: "Renovate automergeの前提と限界"
  - id: kubectl-skew
    resource: "https://kubernetes.io/releases/version-skew-policy/#kubectl"
    title: "kubectlとAPI serverの対応範囲"
---
# 変更する場所を決める

継続して再現したい変更はchezmoiのsource stateへ反映する。生成済みのtargetを直しただけで管理完了とはしない。一方、手動更新された実機をsourceに合わせて直ちに戻すこともしない。正本とwriterの一覧は[ownership](ownership.md)、実機への反映は[operations](operations.md)を参照する。

この文書の「現行」はsourceの実装を指し、実機への適用やCIの成功を意味しない。固定HEADは観測の根拠であり、そのまま採用すべき版とは扱わない。採用済みの更新方式と未実装の提案を分け、検証範囲は[validation](validation.md)に記す。

# 宣言と更新単位

| 変更したいもの | 現行の主なsource | 先に確認する境界 |
|---|---|---|
| mise本体の採用版 | `.mise-version`と`.bootstrap-mise.sh` | pinは明示導入とcheck:toolchainの基準。読込hookは版を強制せず、--installも既存不一致を保持して停止する。版変更時は実体の所有者と採用・置換を決める |
| repo内および端末のtool要求 | `.mise.toml`、`dot_config/mise/conf.d/10-tools.toml`等 | どのconfigが有効か、PATH上の実体とinstall済み版を分ける。version要求の編集とupgrade実行を同じものとしない |
| OS package・GUI app | `.chezmoidata/packages.yaml`、Brewfile template、OS別script | Homebrew・Linux・WinGet・miseで同名toolが重なる場合、どれを使うかを先に決める |
| 生成・修復・検査の処理 | `dot_config/mise/repo-tasks/**`、chezmoi script/hook | source/output指定・task依存・実行順・skip条件と、実際の書込先を一緒に確認する |
| Neovim pluginの採用状態 | `dot_config/nvim/lazy-lock.json`とNeovim設定 | 既定lockへのrestoreか、lockを更新する作業かを分ける |
| 文書・入口 | [OKF Decision](decisions/okf.md)の11文書構成 | 常時ルールをAGENTSへ増やす前に、必要時知識の正本で足りるかを見る |

最初の三行は現在の宣言位置の説明であり、現行の重複所有を維持する決定ではない。手動mise・brew更新を採用宣言へ取り込む手順案は[convergence](decisions/convergence.md)に集める。端末ごとの採用／戻す／管理外の分類はまだ済んでいない。[^pin][^bootstrap][^mise-root][^tools][^packages]

# Neovim：restoreと更新を混同しない

`repair:nvim`は配置済みlockを入力として、通常editor startupを止めたsessionで上流のinstall/restoreを実行する。lock writerの出力は一時copyに限定し、restore前に入力pinを戻す。active pluginの採用lock欠損、spec/task/processエラー、検査時点のNeovim callback/commandエラー、最終checkout/origin不一致は非zeroにする。source・配置済みlockは更新せず、既存のplugin directory、submodule、build/cacheには書き込む。[^repair-nvim][^lazy-restore]

採用engineは更新taskと同じ`85c7ff3711b730b4030d03144f6db6375044ae82`に限定する。欠損したlazy.nvim/LazyVimは採用pinを取得するが、既存engineの別版、bootstrap先のlocal変更・異なるoriginは停止する。local/dev/virtual plugin、custom root/lockfile、rocksは対応外。project `.lazy.lua`は読み込まない。信頼する配置済みLuaを実行するので、任意Luaへのsandboxではない。

新規cloneでは現在のbranchを展開せず、採用親commitのcheckout後にその版のsubmoduleを初期化する。kulalaのfmt等を省略して成功扱いにしない。通常startupは止めるが、plugin managerのbuild taskは実行する。Masonに限り、このsessionのconfigを`mason.setup(opts)`へ限定し、LazyVimによる並行registry refresh・`ensure_installed`導入・FileType再triggerを実行しない。`:MasonUpdate` buildは維持する。その他のbuildがplugin configやparser等の背景処理を起動する可能性は残る。例えばTreesitterのbuildがMason経由でtree-sitter-cliを導入する経路は維持する。成功条件はactive pluginのrevision一致、managerが観測するtaskの成功と検査時点のNeovimエラー不在であり、背景処理の完了やeditor/provider/Mason/parserの正常動作を保証しない。失敗時は非zeroで止まり、途中まで変更されたpluginを自動rollback・削除しない。失敗したdirectoryやlocal変更は内容を確認してから個別に扱う。[^lazy-restore][^git-clone][^git-submodule][^lazyvim-mason][^nvim-errmsg]

`update:lazy-lock`は、既存local revision（既定`HEAD`）の`dot_config/nvim`をGit objectから一時directoryへ展開し、lock候補だけを作る。staged・unstaged・untrackedは入力外で、通常branch/index/sourceや配置済みNeovimには書かない。remote branchのfetch、checkout切替、`chezmoi add`、commit/push/PR作成は行わない。plugin取得・更新は一時HOME/XDG内で通信を伴う。[^update-nvim]

導入済みPython 3.9+、Git、Neovim 0.12以上が必要。miseの自動導入を避ける場合は、更新済みの配置taskを直接呼ぶ。source変更だけでは古い配置taskは更新されない。実機反映は別操作として[operations](operations.md)の境界を確認する。

```sh
"$HOME/.config/mise/repo-tasks/update/lazy-lock" --revision HEAD --nvim /absolute/path/to/nvim
```

`--git`も導入済み実体を指定できる。mise shimを指定しない。manifestは実際のNeovim版を記録するが、選択revisionのtool宣言版との一致は検査しない。Neovim版やOSでspec条件が変わるため、その環境もレビュー対象にする。

対応入力は通常のLua/JSON fileとGo template delimiterを含まないliteral `.tmpl`だけ。optionsも同じrevisionから使う。symlink/submodule、chezmoiの属性prefix（`dot_`・`create_`等を含む）、実template、project `.lazy.lua`、local/dev/virtual plugin、custom root/runtimepathや解決できないimportは停止する。chezmoiの全target計算を再実装せず、選択treeのtrusted Luaを実行する方式であり、悪意あるLuaに対するOS sandboxではない。[^lazy-source]

上流setup/install/updateとlock writerを使う。startup/buildの2箇所だけを止め、無出力process失敗をtask ERRORへ伝えるadapterを加える。初回install/update、fresh processで追加依存のinstall、さらにfresh processの読取照合の3段階で、spec/task/processエラー、取得漏れ、lock/checkout不一致、最終specのorigin・branch・commit/tag/version制約との不一致を失敗とする。追加の未解決importが残ればartifactを保持して止まり、一般的な再収束loopは行わない。`Lazy!`のwaitやNeovim終了0、lockの存在だけでは成功にしない。[^lazy-usage][^lazy-task]

**更新範囲からlazy.nvim自身を除く。** adapterを確認した`85c7ff3711b730b4030d03144f6db6375044ae82`を入力・実行・出力で保持し、他のactive pluginを更新する。未確認engineへ更新して次回必ず失敗する状態を作らないための制約で、起動表示とmanifestにも記す。engineを更新する場合はadapterの上流APIを再確認し、失敗fixtureと隔離native更新を通して対応commitを改訂する。全更新を無条件に認める代案は内部API互換を保証できず、独自plugin managerへ置換する代案は管理範囲が大きいため採らない。

build・通常plugin init/config・editor event・submodule取得は行わない。lockはplugin repositoryのcommitを記録し、build済み実行環境を証明しない。native試験では旧kulala lockへのsubmodule checkoutが失敗したため、lock生成で不要なsubmoduleは上流の`submodules=false`で分離した。event依存でspec自体を変える独自configは対応範囲外。Mason/provider/parserやplugin動作確認は、候補の採用後に必要範囲を定めて別途行う。

成功・失敗とも開始時に表示した固有artifact directoryを自動削除しない。`status.json`が`success`の候補だけをレビューする。`failed`、`incomplete`、status欠損は成功ではない。成功時は`before.json`、`candidate.json`、一fileの`lazy-lock.patch`、入力OID/blob一覧と実行版の`manifest.json`、phase report、ログが残る。無更新でもartifactは残る。一時領域はOS清掃対象なので必要なら別の保存先へコピーし、不要になったdirectoryだけを利用者が明示削除する。

採用・公開は次の別工程とする。まずmanifestのrevisionと更新範囲、before/candidate/patchを確認し、採用先のspecが入力revisionと一致することを確かめる。既存staged lockを候補で上書きしない。必要なら別checkoutを用意して、その採用先で`git apply --check /path/to/artifact/lazy-lock.patch`、差分確認後に`git apply /path/to/artifact/lazy-lock.patch`を行う。specが変わった場合はそのrevisionから生成し直す。内容をレビューしてから明示的に`git add`・commit・push・PR作成を行う。公開失敗でもartifactは保持され、生成成功と公開成功を混同しない。原子性や自動rollbackは名乗らない。

# RenovateとCIの現行

Renovateはrootの`.mise.toml`と`dot_config/mise/conf.d/*.toml`をnative mise managerで扱い、`.mise-version`にはmise release向けのcustom regexを使う。CI workflowの`RENOVATE_VERSION`は直前行の`# renovate:`注釈を公式preset `customManagers:githubActionsVersions`で読み、pre-commit hookの`rev`は既定で無効のpre-commit managerを有効にして追う。mise・GitHub Actions・custom regex・pre-commitの通常更新を、majorを含めて一つのPRにまとめる。作成枠は日本時間の月曜で、同時PR上限は1件。月曜の枠内にbotが実行され、対象の更新があるときに作成する。対応lockfileがないためweekly lock maintenanceは無効にする。[^renovate]

`Required CI`に合格したPRはsquashで自動マージする。既存のPRが最新mainに追随するためのrebaseとCI完了後のマージは、月曜の作成枠外でも進む。失敗した場合はログを調べ、原因の更新を特定して分離する。

2026-11-12の利用者決定により、Renovate PRには元SHAを保持する純粋なFFに代えてsquashを許可する。merge commitは禁止する。GitHub rebaseも元SHAを保持せず、Renovateの`fast-forward` enumはGitHub対応の根拠にならない。実機への取り込みは利用者が都合のよい時点で開始する。[^merge-methods]

GitHub側はmainに`Required CI`を必須とし、発行元をGitHub Actionsに限定、最新baseへの追随とlinear historyを要求する。adminにも適用し、恒常bypass・force-push・deleteを許可しない。required reviewやPR経由の一律必須化は加えないが、必須checkはdirect pushにも作用する。GitHub設定はrepo内のJSONだけでは反映されない。導入・修復時は[固定gateの検証](validation.md#isolated-regression)と保護設定を先に確認してからautomergeを有効にする。runner版で変わる内部job名を必須名にしない。[^protected-branches][^automerge]

`config:best-practices`は設定の土台であり、全toolの互換性保証ではない。npm向けrelease-ageの待機を維持するが、minor/patchも破壊変更がないとはみなさない。実際に不具合が確認された版だけ理由と解除条件を付けて除外する。切り戻す場合は次回の自動再更新も抑える。仕事固有のtool制約はプロジェクト側mise設定へ分離する。例えばkubectlはAPI serverの±1 minorが公式範囲であり、globalの最新CLIをすべてのclusterへ使えるとは限らない。[^automerge][^kubectl-skew]

Homebrew/WinGet/OS package、Neovim plugin lock・Mason・parser、Vale stylesはこの設定の版更新対象ではない。chezmoi externalはURLにcommit SHAを含めて固定し、直前行の`# renovate:`注釈とURL中のSHAをcustom regexで追う。tagのある取得元はtagとそのcommit、tagのない`catppuccin/bat`はbranch先頭のcommitを追う。release添付の`win32yank`は版をURLに固定して`checksum.sha256`で照合し、Renovateの追跡対象にしない。raw fileにchecksumを付けないのは、内容がcommit SHAで決まり、Renovateがchecksumを更新できないためである。botが実際に検出・更新することはmerge後のDashboardで確かめる。gcloudは2026-11-12のDashboard検出一覧にない。workflowのvalidator env pinとpre-commit hookは2026-11-13に追跡設定を加えた。設定がpresetの正規表現に一致することは確認したが、botによる実際の検出はmerge後のDashboardで確かめる。同日のRenovate 43.150.0によるnative抽出ではgcloudに`unsupported-datasource`が返った。gcloudの既存「manual review」コメントは承認ruleではなく、検出がない間は別途明示更新する。bot側の対応が変われば実抽出を確認してnative managerを優先する。mise pin更新でも既存mise本体は自動置換されず、Git revertはbinary・DB・remote stateのrollbackではない。実機更新と復旧の範囲は[操作](operations.md#mise-bootstrap)・[所有境界](ownership.md)に従う。

Renovate validatorの版はCI workflow、Nodeの要求はworkflowが読むtool宣言を正本にする。変更時のcommandと結果の限界は[validation](validation.md)を参照する。workflowで指定したつもりのruntimeと、実際の`node --version`は分けて記録する。診断の入口は[operations](operations.md#diagnostic-entry)に従い、CIも必須driftを成功へ変えない。登録済みmoduleの隔離回帰は`python3 tests/run_checks.py regression`、OS分岐のrender/構文検査は`python3 tests/run_checks.py render`で再現する。tool準備と通常applyを前提にしないfixture実行、通信・導入を伴う統合jobの違いは[検証の入口](validation.md#isolated-regression)を参照する。通常Neovim初期化や実認証を使わない診断fixtureもこの回帰集合に含める。現行CIがUbuntu/macOSで合格しても、WSL・Windows・実認証の成功とはしない。[^ci]

# 採用済みの文書方針と移行時の確認

repo全体を一つのOKF bundleにすること、PR templateを廃止することは利用者の決定である。共通契約の上流同期を終了し、Repomixを必須とする経路を退役する。旧文書を保存するための同型移植や、新しいpacking手順は作らない。[^user]

入口や文書を変更するときは、[chezmoi除外](../.chezmoiignore.tmpl)、[Issue Form](../.github/ISSUE_TEMPLATE/change-request.yml)、[更新taskの採用案内](../dot_config/mise/repo-tasks/update/executable_lazy-lock.tmpl)も確認する。Issue Formは問題・範囲・確認方法・参照の短い入力を残す。Repomix設定は撤去し、既存生成packのignoreは誤配置・誤追跡を避けるため維持する。`npm:repomix`のtool宣言は別の依存整理で退役する。[^tools]

更新taskはPR本文を生成しない。配置taskの更新とlifecycleの再実行条件は別であり、実機への反映時は[operations](operations.md)で起動範囲を確認する。

文書確認ではsourceと出典を読み、実機コマンドを検査の名目で起動しない。bootstrap・apply・repairの意味を変える実装は、[convergence](decisions/convergence.md)の対象と成功条件を具体化してから行う。旧文書の削除と実機の掃除・resetを結びつけない。

# 変更をレビュー可能にする

変更説明は、何が問題でどう変わるか、確認した対象と結果、未確認の範囲・運用上の影響を必要な長さで記す。実行したCIの状態はそのrun/checkへの参照で示し、固定のPR本文へ結果を転記し続けない。親子Issueや大きなチェック表を、変更の大小に関係なく必須にする案は採らない。検査の選択は[validation](validation.md)に任せる。

PR templateの廃止理由と再検討条件は[OKF Decision](decisions/okf.md)を正本とする。

[^pin]: [bootstrapが採用するmise本体版](../.mise-version)。
[^bootstrap]: [mise本体の読込検査・明示導入](../.bootstrap-mise.sh)。
[^mise-root]: [repo内tool要求](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.mise.toml)。
[^tools]: [観測時のmise tool宣言](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/conf.d/10-tools.toml)。
[^packages]: [OS別package宣言](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoidata/packages.yaml)。
[^repair-nvim]: [採用lockによるLazy restore](../dot_config/mise/repo-tasks/repair/executable_nvim.tmpl)。
[^update-nvim]: [選択revisionからの隔離lock候補生成](../dot_config/mise/repo-tasks/update/executable_lazy-lock.tmpl)。
[^wrapper]: [post-apply wrapperのhash入力と起動条件](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl)。
[^scripts]: [chezmoi公式：render後のscript内容によるonchange判定](https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/)。
[^renovate]: [Renovateのmanagerと更新単位](../renovate.json5)。
[^ci]: [CIの対象・実行段階・validator版](../.github/workflows/compliance.yml)。
[^user]: 単一bundle、PR template廃止、上流同期終了・Repomix退役の方向。文書移行の方針。実機操作は別。


[^lazy-source]: [chezmoi source state attributes](https://www.chezmoi.io/reference/source-state-attributes/)。

[^lazy-usage]: [lazy.nvim Usage：waitと更新API](https://lazy.folke.io/usage)。

[^lazy-task]: [採用版のtaskとprocess失敗処理](https://github.com/folke/lazy.nvim/blob/85c7ff3711b730b4030d03144f6db6375044ae82/lua/lazy/manage/task/init.lua)。

[^lazy-restore]: [採用lockを保持するrestore adapter](../.chezmoitemplates/lazy_restore.lua)。

[^git-clone]: [Git clone：no-checkoutとsubmodule](https://git-scm.com/docs/git-clone)。

[^git-submodule]: [Git submodule update：親commitが指す版の初期化](https://git-scm.com/docs/git-submodule)。

[^lazyvim-mason]: [採用LazyVimのMason setup・背景導入](https://github.com/LazyVim/LazyVim/blob/83d90f339defdb109a6ede333865a66ffc7ef6aa/lua/lazyvim/plugins/lsp/init.lua)。

[^nvim-errmsg]: [Neovim v:errmsg：直近のエラーメッセージ](https://neovim.io/doc/user/vvars.html#v:errmsg)。

[^merge-methods]: [GitHubのsquash/rebaseと元SHAの扱い](https://docs.github.com/en/pull-requests/reference/pull-request-merges)。
[^protected-branches]: [必須check・strict・linear history・admin適用](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)。
[^automerge]: [Renovate automergeの前提と限界](https://docs.renovatebot.com/key-concepts/automerge/)。
[^kubectl-skew]: [kubectlとAPI serverの対応範囲](https://kubernetes.io/releases/version-skew-policy/#kubectl)。
