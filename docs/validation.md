---
type: Playbook
title: 変更に応じた検証と結果の限界
description: 文書・template・tool更新・認証の変更に対して、必要な検査と副作用を選ぶ。
status: draft
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-13T14:12:12+00:00"
sources:
  - id: evals
    resource: "https://www.anthropic.com/research/demystifying-evals-for-ai-agents"
    title: "Anthropic, 2026-01-09：結果状態と評価範囲"
  - id: doctor
    resource: "../dot_config/mise/repo-tasks/doctor/executable__default.tmpl"
    title: "doctorの共通検査集合"
  - id: checks
    resource: "../dot_config/mise/repo-tasks/check"
    title: "現行check taskの集合"
  - id: hooks
    resource: "https://www.chezmoi.io/reference/configuration-file/hooks/"
    title: "chezmoi公式：dry-runでもhookが動く"
  - id: wsl-check
    resource: "../dot_config/mise/repo-tasks/check/executable_wsl-openssh.tmpl"
    title: "WSL認証・通信・一時署名probe"
  - id: precommit
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.pre-commit-config.yaml"
    title: "変更を伴う整形hookと対象filter"
  - id: precommit-docs
    resource: "https://pre-commit.com/"
    title: "pre-commit公式：対象指定とhook環境の導入"
  - id: ci
    resource: "../.github/workflows/compliance.yml"
    title: "CIの対象・実行段階・validator版"
  - id: renovate-docs
    resource: "https://docs.renovatebot.com/config-validation/"
    title: "Renovate公式：repository configの検証とstrict mode"
  - id: render-command
    resource: "https://www.chezmoi.io/reference/commands/execute-template/"
    title: "chezmoiのtemplate単独評価"
  - id: mise-action
    resource: "https://github.com/jdx/mise-action/blob/dba19683ed58901619b14f395a24841710cb4925/action.yml"
    title: "採用mise-actionの導入入力"
  - id: actions-needs
    resource: "https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idneeds"
    title: "GitHub Actionsのjob依存と失敗伝播"
  - id: vale-lint-test
    resource: "../tests/test_vale_lint.py"
    title: "Vale診断の隔離native検査"
  - id: vale-lint-upstream
    resource: "https://github.com/mfussenegger/nvim-lint/blob/5259819fe849c978935281d1cab4bd26b375ab0f/lua/lint/linters/vale.lua"
    title: "採用nvim-lintのVale parser・stdin・severity"
  - id: vale-lazyvim
    resource: "https://github.com/LazyVim/LazyVim/blob/c10948c50b18fae7f256433afdef09e432410480/lua/lazyvim/plugins/linting.lua"
    title: "採用LazyVimのlinter mergeと引数追加"
  - id: vale-utf8
    resource: "https://neovim.io/doc/user/lua/#vim.str_utf_start()"
    title: "Neovim公式：UTF-8開始byte境界"
  - id: vale-cli
    resource: "https://docs.vale.sh/topics/cli"
    title: "Vale公式：stdin・config探索・JSON出力"
---
# 検証を選ぶ

検査は変更した対象と期待する結果に合わせて選ぶ。文書の修正に実機doctorを要求しない。以下のcommandは現行コードを説明するためのもので、この文書を読むだけで一括実行する手順ではない。[operations](operations.md)で前提と書込範囲を確認する。

「現行」はsourceの実装を指す。以下に隔離検査の対象と限界を記す。fixtureの成功は、CIの統合jobや実機probeの成功を意味しない。文書検査と実機動作の証拠は分ける。

| 変更対象 | まず確かめること | 必要な場合に追加する検査 |
|---|---|---|
| Markdownだけ | [OKF規約](decisions/okf.md)のfrontmatter、相対リンク、参照先、現行と案の区別、差分と`git diff --check` | 読者の作業例で必要な情報へ到達できるかを読む。関連しないdoctor・Renovate・Repomixは要件にしない |
| chezmoi template・hook・task | sourceだけでなく対象OS/CI分岐のrender結果と起動順・変更先 | 影響する構文検査、対象を絞ったtask、結果fileと保持対象の確認。実機を使う前に入力を管理した隔離環境で扱う |
| identity・Git・SSH | [identity](identity.md)の入力schema、生成先、routing、署名と認証の別 | 対象identityごとの有効Git設定、必要な認証・署名probe。[WSL](platforms/wsl.md)ならWindows側経路も区別する |
| mise/tool・Neovim | [ownership](ownership.md)の正本、採用版、実行実体、生成物 | 変更したtoolの起動、該当check、再適用・欠損復旧・保持対象。現行doctor一回で代用しない |
| package・OS統合 | 対象OSの宣言、更新やcopyの副作用 | 該当hostで存在・実体・利用可能性を確認。CIの省略分を実機成功と扱わない |
| Renovate / CI | 設定、runtime、対象job、変更した分岐 | 以下のvalidator経路と該当CI結果。全実機への外挿をしない |

この選び方はrepo向けの文案であり、現在の旧文書が要求する全検査の移植ではない。成功をcommandの終了だけでなく結果状態で評価する考え方は、Anthropicのagent評価の解説を参考にした。このdotfilesの検査一覧の有効性が研究で実証されたわけではない。[^evals]

<a id="isolated-regression"></a>
# 隔離回帰・render・統合の入口

repo rootから次を実行する。runner自身はtoolを導入しない。不足・shimだけ・版違いを検出したら検査前に非zeroで停止する。

```sh
python3 tests/run_checks.py lint            # 全言語のlintと整形の確認
python3 tests/run_checks.py fast            # applyを伴わないtest
python3 tests/run_checks.py full            # lintと全test（fastとslow）
python3 tests/run_checks.py test_git_fetch  # module・class・test単位（複数可）
```

chezmoi・Neovim・Zsh・Git/OpenSSHとOS utilityが必要で、render検査以外にはmise実体も要る。各実体は`CHEZMOI_BIN`・`NVIM_BIN`・`MISE_BIN`・`ZSH_BIN`等の環境変数、PATH上の実体、repoが宣言した版のmise install（chezmoiは`.mise.toml`、NeovimとPythonは`dot_config/mise/conf.d/10-tools.toml`）の順に探す。PATHの先頭がmiseのshimなら宣言版のinstallを使う。miseは`~/.local/bin/mise`を候補にし、版が`.mise-version`と一致しなければ停止する。Python 3.11未満で起動した場合は宣言版のPythonで起動し直す。fixture内の一部stubと本番scriptは`/usr/bin/python3`・`/bin/zsh`・`/usr/bin/ssh`等も使うため、任意OSへの可搬性を保証する入口ではない。macOS/Ubuntuを対象にする。

[runner](../tests/run_checks.py)はmoduleごとに一時HOME/XDGと限定PATHの子processを起動し、CPU数まで並列に実行する。実ユーザーのGit/mise設定override、SSH agent、OP環境変数、tokenを引き継がない。各fixtureも自身の一時HOME/XDGと明示configを使う。moduleごとの件数・所要時間と遅いtestを表示し、失敗したmoduleの出力だけを表示する（`-v`で全出力）。`slow`は同runnerの`SLOW`に列挙した、縮小sourceへchezmoi applyを（`--dry-run`・`init --apply`も含めて）実行するtestである。`fast`はそれ以外の全testで、chezmoiを`apply`・`--apply`・`update`を拒否するwrapperに差し替えて実行する。applyを始めたtestは`SLOW`へ移すまでfastで失敗する。`full`は`lint`・`fast`・`slow`の和で、Windows設定同期とlazy-lock候補生成の検査も含む。CIは移行まで旧名の`render`（render検査だけ）と`regression`（render以外の全module）を使う。R17のVale native検査は[別入口](#vale-lint)である。R05は既存`load_tests`で自身の12件を選択する。失敗・例外・skip・expected failure・空suiteは非zeroになる。

R01とR13のinit検査は実config template・読込hook・bootstrapを保持し、取得/認証をstubに置き換える。R02のconfig生成fixtureは入力検証を保持してhook部分をsourceコピーから除き、生成configにhookがないことを検査する。他はhookなしconfigを使い、external取得を空定義または最小sourceで除外する。縮小sourceへのapply、使い捨て鍵の署名、ローカルbare remoteのfetch、UNIX socketのmux検査を含むが、実機applyや実認証は行わない。socket bindが許されない環境は失敗となり、skipで代替しない。

[render検査](../tests/test_render_syntax.py)はmacOS arm64・Linux amd64・WSL amd64のdata/builtin値とCI有無を模擬して、config取得以外のstandalone templateをrenderする。共通templateはconsumer経由で扱う。config取得はR01/R02に任せる。shellは`-n`、Luaは初期化を無効にしたNeovimの`loadfile`で構文だけを調べる。external宣言は文字列としてrenderし、取得しない。WSL path変換はstubである。模擬OS上での実行、全設定形式の妥当性、補完やpluginの実動作は証明しない。[^render-command]

| CI job表示 | 前提を用意する順序・実施範囲 | 成功が示さないこと |
|---|---|---|
| Isolated render / regression（Ubuntu/macOSそれぞれ） | checkout → runnerのPythonで一時mise manifest作成 → mise-actionでpin版miseと宣言から抽出したPython/chezmoi/Neovimを導入 → LinuxのZsh/Git/OpenSSH導入 → 上記command | fixture実行自体の前に通信・tool導入はある。端末のinit/apply・認証・全tool導入は前提にしない |
| Network Integration - One Apply and Selected Diagnostics（Ubuntu/macOS） | 隔離jobの成功後、明示bootstrap → CI用init/apply一回 → 配置済みZsh起動検査 → managed target verify（`--exclude=scripts`） → Neovim restore → 配置済み入口のlocal診断 | 二回適用の無変更性、生成物欠損復旧、実1Password、Windows/WSL・GUIの動作 |
| Renovate Config Validation | Node準備 → 固定版validatorの取得・実行 | 依存更新の動作や端末の正常性 |

Neovim restoreのCI stepだけでMasonのDEBUG logを有効にし、一時XDG stateへ保存する。step失敗時は`mason.log`だけを収集し、環境に渡されたtoken・secret・passwordの値とAuthorization headerを除去して、OS・run・attempt別の`mason-failure-*` artifactに7日間保存する。ログ未生成時もその旨を記した`status.txt`を保存する。収集・uploadは失敗を成功へ変えず、後続診断や自動マージを通さない。通常実機のrestoreではDEBUGを有効にしない。artifactには外部commandや取得URLが含まれ得るため、環境に渡されていない任意の秘密まで自動除去する保証ではない。

毎apply scriptは次回も実行予定なので、統合jobの静的target検査は`chezmoi verify --exclude=scripts`を使う。scriptの失敗は直前のapply終了値で判定する。[隔離検査](../tests/test_ci_verify.py)はscriptのみ実行予定ならこのverifyが成功し、管理fileのdriftは非zeroになること、verify自体がscriptを実行しないことを確認する。

`Required CI`は上の3 job ID（matrixを含む）の結果を集約する固定名のcheckである。`always()`で上流失敗後にも実行し、すべての結果が`success`の場合だけ成功する。failure/cancelled/skippedを合格へ変えない。runner版をcheck名に含めず、runner更新でGitHub側の必須check名が失われることを避ける。検証jobを追加したら`needs`も更新する。[^actions-needs]

`tests/check_shell_startup.py --home <使い捨てCI HOME>`は、配置済み`.zshenv`・`.zshrc`と生成済みzoxide/starship initを実Zshで読み込み、miseのhookによるtool選択を確認する。通常端末のHOMEへ向けない。起動前に環境を限定し、token/agentを引き継がず、mise自動導入を無効化し、認証commandを失敗stubへ向ける。30秒timeout、stderr、認証呼出し、関数/PATH不成立を失敗とする。cache書込は使い捨てHOMEに許容する。`-d`でsystem rcを外し、prompt表示・Tab補完・実認証・WSLは検証しない。`test_shell_startup`は一時HOMEとCLI doubleでactivation失敗の握りつぶし、空init、認証失敗の握りつぶし、stderr、hangを検査し、regressionへ含める。

全jobはworkflow既存のpush/PR（main/master）、手動、週次triggerで動く。統合jobは隔離jobに依存し、失敗時は実行されない。その未実行を統合合格とは表示しない。fixtureの検査結果が統合applyの成否に依存する方向にはしない。tool準備にはpin済みmise-actionの`working_directory`と`install`を使い、一時manifestを明示的にtrustする。actionがPATHへ公開した導入済み実体をrunnerが検査し、fixtureにはactionの認証環境を渡さない。[^ci][^mise-action][^actions-needs]

これはこのrepoでの設計判断である。代案は同一job内でfixtureをapply前へ移す方法だが、job表示と失敗範囲が混ざるため分離した。専用container/VM imageへ全依存を封じる方式もあり得るが、macOSを含む別imageの維持は追加していない。runner付属OS utility・配布物取得・GitHub ActionsサービスはCI実行時の依存であり、この設計だけで再現性や無通信を完全保証しない。

localの隔離試験とworkflow構文検査は、実際のGitHub Actions runや他OSの合格とは区別して記録する。R10aのidentity、R10bの補完、R10cのbat/Vale/pbfileは下記の限定した復旧契約を持つ。Windows同期の隔離契約は[専用検査](#windows-settings-sync)で扱い、このjobの成功を実Windowsの証拠にはしない。

<a id="mise-read-boundary"></a>
# mise読込境界の隔離検証

導入済みのchezmoiとPython 3を指定して`python3 tests/test_mise_read_boundary.py`を実行する。`CHEZMOI_BIN`でchezmoi実体を指定できる。検査自体はmiseによるtool自動導入を起動しない。[検査コード](../tests/test_mise_read_boundary.py)はsourceコピーと一時HOME/XDGを使い、実config templateから`chezmoi init`でconfigを生成する。opはstub、external定義はコピー内で空にし、hookとbootstrapは実sourceを使う。

新configと旧config相当の引数なしhookで、旧版・pin一致・新版・不在のmiseに対し実chezmoiの`diff`/`verify`とその`--dry-run`を実行する。取得stubとmiseの呼出し記録、既存fileの内容・mode、不在時のdirectory未作成、非zeroと導入案内を確認する。非実行file・directory・symlinkとリンク切れも保持を検査する。明示`--install`は不在時の導入・版確認をinstaller stubで検査し、既存版不一致の保持と一致版の無変更も確認する。

macOSでchezmoi 2.70.4を用いた隔離検証は成功した。CIにも同じ検査を接続したが、workflow全体やUbuntu/WSL実機、実installerの通信・配布物・実認証は今回未検証。対象はmise取得・差替えの境界であり、chezmoi external/cacheまで無通信・無書込とする証拠ではない。

<a id="identity-boundary"></a>
# identity入力境界の隔離検証

`python3 tests/test_identity_boundary.py`はPython 3.11以降、導入済みchezmoi・zsh・Git・ssh-keygenを使う。`CHEZMOI_BIN`でchezmoiを指定できる。sourceコピーと仮HOME/XDG、使い捨てEd25519鍵、op・wslpath・SSH stubでproducerからGit consumerまで調べる。実機のop参照・認証・apply・repair・doctorは実行しない。repair依存とagent同期はコピーを仮HOME内で実行し、post-apply wrapperはmise stubからこの対象だけへdispatchする。CIではLinux上のzsh不在時に明示導入してから検査する。

`$()`・backtick・引用符・backslash・空白・非ASCIIを含む正当な値の保持、Gitの対象内外repoでのname/email/signingkey/sshCommand、SSH stubへ渡る公開鍵path、signers principalを確認する。不正入力を各consumerがrender時に拒否し、旧出力とconfigを保持することも検査する。末尾・連続comma、空要素、root・相対path・glob・dot要素・重複slash、同一・包含routing、改行/heredoc終端、filename逸脱、壊れた公開鍵、JSON集合の誤型、OpenSSH path展開も対象である。実OpenSSHは`ProxyCommand=/bin/false`・agent/known_hosts無効の無通信probeで公開鍵の読込まで確認する。共通SSH設定は`ssh -G`で構文とIncludeの実効値を確認する。

macOS・chezmoi 2.70.4で隔離検証とR01の回帰検証が成功した。CIに接続したが、workflow全体、Ubuntu、WSL実機・実認証は未検証。WSLは既存directoryだけを変換できるstub、変換先の拒否、argvとagent configの仮Windows directoryへの配送を確認し、実Windows OpenSSHや接続共有の正しさは保証しない。symlink alias、Git worktreeのrouting、複数出力のtransactionはこの検査の保証外である。

# Git fetchの隔離検証

`python3 tests/test_git_fetch.py`は導入済みPython 3・chezmoi・Gitを使い、実global config templateを仮HOMEにrenderする。2つのローカルbare remoteとclientで通常の`git fetch origin`を実行し、local-only tag・別remote由来tagのobject ID保持、新しいbranch先端・tagの取得、削除済みremote-tracking branchのpruneを確認する。実repoへのfetch・tag操作、署名helper、実機applyは実行しない。

globalの`fetch.pruneTags`は設定せず、`fetch.prune = true`は保持する。Git公式の[pruning仕様](https://git-scm.com/docs/git-fetch#_pruning)では、tagの明示refspecやpruneTagsとpruneの併用はremoteに存在しないlocal tagも削除対象にする。repo/remote側の明示設定・`--prune-tags`・tag refspecまで無効化する変更ではない。必要なtag削除はその範囲で意図を確認して選ぶ。

macOSで隔離検証に成功し、Ubuntu/macOSのCI stepへ接続した。workflow全体とUbuntu/WSL実機は未検証。実機の生成済みglobal configは未変更なので、source変更だけで端末のfetch挙動が変わったとは扱わない。

<a id="ssh-identity-isolation"></a>
# SSH identity分離の隔離検証

`python3 tests/test_identity_boundary.py`はR02に加えR04を扱う。明示config・仮HOME・異なる使い捨て公開鍵A/Bを使い、Gitから実OpenSSHへ渡すargvと鍵fileの読込をA→B／B→Aの両順で確かめる。専用UNIX socketをlistenし、修正前のcommandおよび`ControlMaster=no`だけのcommandからmux helloを受信する正の対照を置く。`ControlPath=none`を持つ生成commandからは接続が来ないことを観測する。`ProxyCommand /bin/false`で外部接続を止め、agent・known_hosts・実ユーザーのSSH設定を使わない。socket bindを禁止するsandboxではその検査は失敗し、skipで合格へ置き換えない。

`ssh -G`はrootのagent値が環境変数未設定／別値でも解決されること、WSLのLinux側が`IdentityAgent none`になることの検査に限る。Windows branchはwslpath／ssh.exeのstubでGit argv・引用・二つのcheck consumerの判定を検査する。macOSの実OpenSSHでのsocket非接続probeと、Windowsソースの静的確認を、Windows実行・SSH serverでの認証成功・1Passwordの鍵選択の証拠に置き換えない。実Windows/WSLとUbuntu、CI workflow全体は未実行である。

<a id="ownership-preservation"></a>
# 管理外ファイル保持の隔離検証

`python3 tests/test_ownership_boundary.py`はPython 3と導入済みchezmoiを使用する。`CHEZMOI_BIN`で実体を指定できる。repair templateを仮HOMEでrender・実行し、ダミーの管理外鍵・同名file・nested file・symlinkについて内容・mode・存在・リンク先の保持を比較する。旧削除対象49パスを通常file、directory、symlinkで用意し、手動再導入docker-cliとshimも含める。

削除計算はremove templateと共通templateだけの隔離source、hookのない明示config、仮HOME/XDGで実chezmoiのdiff・dry-run・applyを行う。WSL条件のtrue/falseを両方確認するが、Windows実機検証ではない。削除対象を一つだけ仮sourceへ戻す正の対照でdiffが検出することも確認する。`private_`属性による管理対象mode設定と、既存`tests/test_identity_boundary.py`によるgeneratorの公開鍵0600・allowed_signers 0644、R02/R04の引用・依存経路は別途確認する。

実ユーザーの鍵・認証・設定、実機apply・repair・doctorは対象にしない。CIにこのfixture検査を接続するが、workflow全体・Ubuntu/WSL実機・過去の削除やmode変更の復元を保証しない。既存generatorの失敗時保持・同名出力との衝突は別の課題として残る。

<a id="diagnostic-boundary"></a>
# 現行のcheckと保証しない範囲

`~/.local/bin/dotfiles-diagnose`は配置済みcheckを直接呼ぶ。security・identity・nvim・vale・toolchain・npm-backend・hubspot・completionの集合と必須判定はCIでも同じ。従来の`mise run doctor`はtask開始前に自動導入し得るため、非変更入口ではない。[入口と移行](operations.md#diagnostic-entry)を参照。[^doctor]

| check | 必須として失敗させる条件 | 警告・未確認の範囲 |
|---|---|---|
| security | `.ssh`とXDG stateのSSH directory欠損、modeが0700以外、stat不能 | 個々の鍵の権限・所有者までは検査しない |
| identity | render済み入力が非空の場合、Git consumer/entry/dispatch/公開鍵/signers/fragment/manifest欠損、世代内entryの不一致、公開鍵・name/email/signingkey・signers・routingの入力不一致、entry/dispatch/fragmentの生成形式外の設定、SSH鍵参照不一致 | 入力が空の場合は警告。manifestは存在検査で、全digest照合はR05 generator側。POSIX鍵pathは全文一致、WSLはcommand形状・option・鍵filenameまで。Windows側directory変換、別global config・repo-local・Git環境override、実認証・署名は未確認 |
| nvim | source/target lock欠損またはbyte不一致、非shim PATHにnvim不在 | plugin revision・provider動作は未確認。chezmoi verifyも通常configも呼ばない |
| vale | config・Google style directory・vale実体欠損 | config解釈や全ruleの健全性は未確認 |
| toolchain | mise実体・pin・配置config欠損/空/読取不能、版表示失敗・版不一致、配置path不一致、config内credential_command | 一時HOME/XDG・専用mise領域で`--version`を実行する。全tool inventory・local override・補完互換性は未確認 |
| npm-backend / hubspot | node/npm/hs実体が非shim PATHにない | package layout・実行動作は未確認。mise where/execで補わない |
| completion | R07必須の18補完と3 init/include fileの欠損・空file | WezTerm/HubSpot補完欠損は任意警告。出力の鮮度・構文・実行正常性は未確認 |

成功表示は選択したlocal検査の合格に限定する。警告が残る結果を端末全体のZero Driftとしない。CLIの存在を調べることと実行することは区別する。通常診断もOS utility・Git config・mise版表示を起動するので、任意のPATH wrapperや置換済みbinaryまで無副作用と保証するものではない。[^checks]

# 明示probeの副作用と保証範囲

`dotfiles-diagnose --probe NAME`で一つずつ選ぶ。通常doctorはこれらを呼ばない。probeは利用者のPATH上の既存CLIを直接起動し、mise execによる自動導入を使わない。

| NAME | 実行するもの・確認すること | 限界・副作用 |
|---|---|---|
| nvim | `nvim --headless -u NONE --noplugin -i NONE -n`によるPython provider検出、Node hostの`--version` | user config/Lazy bootstrap/通常pluginを読まない。provider codeは実行する。cache/log書込はあり得る。通常configでのprovider選択、Node RPC、編集機能の成功ではない |
| completion | `hs --help`、`hs completion`の一時出力と`zsh -f -n` | CLI起動・一時書込。出力自体はsource/autoload/実行しない。Zsh構文合格は補完の意味的正常性ではない |
| hubspot / vale | `hs --version` / `vale ls-config` | CLIの設定読込・cache等が起こり得る。外部サービスの認証成功ではない |
| toolchain | mise usageの生成とusage complete-word | CLI実行・一時書込・動的completionの実行があり得る。全toolの互換性ではない |
| identity | op account、agent一覧、WSL環境照会、生成binding | 認証prompt・agent/Windowsプロセス起動が起こり得る。CIでも実行不能を成功へ変えない |
| wsl-openssh | 下記のWindows認証・署名probe | 非WSLでは`[N/A]`、WSLで明示flagなしは`[NOT RUN]`と非zero |

# WSL OpenSSH probeを使う前に

`dotfiles-diagnose --probe wsl-openssh`はinterop、Windows SSH command、pipe形状、agent鍵一覧、GitHub SSH認証を調べる。最初のidentity configを使ってGit remoteを参照し、一時repositoryで署名commitを作る。`git -c gpg.minTrustLevel=fully verify-commit HEAD`の終了結果でallowed signersの信頼判定を行う。署名表示文字列の一致だけでは合格にしない。[^wsl-check]

| 操作 | 副作用・範囲 |
|---|---|
| `ssh.exe -T git@github.com` | 外部通信・認証。Windows側known_hostsの更新や認証promptが起こり得る |
| `git ls-remote` | 認証を伴うremote参照。既定はこのrepo。`DOTFILES_WSL_OPENSSH_AUTH_TARGET`を変えても前段のGitHub probeは残る |
| 一時repositoryの`git commit -S` / `verify-commit` | temp file・Git履歴と署名helper/agent呼出し。初期templateとcommit hookは無効化する |
| 最初のconfigを選ぶ | 全identity、directory routing、他hostの認証成功は保証しない |

cleanupで外部通信やWindows側の状態まで元に戻るわけではない。timeout utility不在では時間制限なしの箇所もある。静的棚卸しの代わりに実行しない。[^wsl-check]

# 診断境界の隔離検証

`python3 tests/test_diagnostic_boundary.py`は導入済みchezmoi・mise・Neovim・Git/OpenSSH・Zshを使う。`CHEZMOI_BIN`・`MISE_BIN`・`NVIM_BIN`で実体を指定できる。仮HOME/XDG、hookなし明示config、CLI stubでrenderした直接入口を実行し、CI true/false双方の欠損・lock drift・任意警告・対象外を確認する。通常診断がアプリ/認証/補完生成stubを起動しないことと、file内容/mode・directory・symlink先を比較する。identityはR05の実before script・Git config・generatorで完全な世代を作り、公開鍵を含む各file欠損と、署名鍵・SSH鍵path・signers・routing・consumer参照のずれをCI true/falseで検出する。診断は欠損を修復しない。R02/R04の特殊文字入りpath・複数identity・WSL変換stubにも完全なcheckを通す。

採用mise 2026.6.11では、欠損toolを宣言した明示configとローカルのasdf fixtureを使う。直接入口はmiseの版表示以外を呼ばず保持する。正の対照として従来のmise runはtask本体のexportより先にfixtureのdownload段階へ進み、markerを作って即失敗する。実package取得・導入は行わず、mise HTTPをoffline設定で無効化する。CLI自体の独自通信を遮断する汎用sandboxではない。

版照会の回帰には、毎回cache削除・marker作成・最新版cache書込・trust移動・旧plugin削除・system側install移行を起こすstubを使う。prune無効化設定も意図的に無視するため、設定抑制とは独立にdirectory隔離を試せる。正の対照は同じstubを隔離なしでfixtureへ実行し、実際の削除・移動を確認する。成功・非zero終了・版不一致のすべてで、外側HOME/明示mise領域の内容・mode・directory・symlink先の保持と一時領域cleanupを確認する。親のprune age、log path、plugin/install path、credential command等のoverrideが子へ漏れないことも確認する。system dataの既定pathはfixtureへ置き換えて、子の専用path指定が欠けた場合も必ず検出する。TMPDIRをsymlink経由にし、物理cwdと探索上限の一致、親に置いた不正misercをnativeが読まないことも確かめる。

native検査は初回版照会の前からsnapshotを取り、古いcache・移行対象に似たdirectory・未知設定を置いた隔離HOME/XDGを比較する。利用者側CI false/trueで採用版2026.6.11を各一回実行するが、その成功回数をprune停止の証明にはしない。採用コードの0s時早期return、最新版照会のCI条件、migrationの参照directoryと、上記の決定的stub検査を組み合わせる。事前warmup、cacheの比較除外、失敗が消えるまでのretryは行わない。[起動経路と限界](decisions/convergence.md#diagnostic-version-isolation)を参照。

使い捨て鍵Aで実Gitの署名commitを作り、Bだけを信頼する場合に失敗、Aを信頼する場合に合格することを実装の署名関数で検査する。実1Password/WSL/network関数は呼ばない。実Neovimに対しては通常initのmarker/Lazy directoryが作られないことを確認する。providerの実環境での正常動作は検証しない。生成completion内のmarkerが構文検査で実行されないことも確認する。

CI stepへ接続するが、local実行結果はmacOSの隔離fixtureに限る。実機apply・doctor・repair・認証、Ubuntu/WSL、workflow全体は未確認。identityの所有確認済み世代内欠損は下記R10a、補完はR10b、bat/Vale/pbfileはR10c検査で扱う。Windows等の残る生成欠損からの自動復旧や全inventoryの比較は後続の収束設計で扱う。

# identity世代切替の隔離検査

`python3 tests/test_identity_transaction.py`は一時HOME・明示config・ダミー公開鍵を使い、二個目の出力失敗、WSL path変換失敗、欠落/空入力、SIGTERM/SIGINT/SIGKILL、旧配置の移行途中失敗・再実行・途中の手動変更、未移行consumerの拒否、clear採用後の再実行、未知entryとsymlink・変更済み世代の拒否を検査する。対象repo内外の実Gitによるname/email/signingkey/SSH鍵/allowed_signersの参照と、切替前に読んだ旧参照の生存を照合する。

縮小したsourceでbefore script・Git target・identity after scriptだけを通すchezmoi applyも含む。実repoのhooks、package導入、externals、mise graph全体、実1Passwordは実行しない。CIのUbuntu/macOS jobに接続するが、local合格はCI runの合格ではない。WSLはwslpath/ssh.exe stubであり、実Windowsのfile共有・interop・認証、停電耐久性は対象外。既存R02/R04の入力・引用・routing・SSH分離検査とR06の未知file保持検査も併用する。

# 整形・Renovate・CI

`python3 tests/run_checks.py lint`（[実装](../tests/test_lint.py)）はファイルを書き換えない。Pythonは[Ruff](../.ruff.toml)のlintと`format --check`、Luaは`.lua`の全件にStyLuaの`--check`（`.editorconfig`）、shellは`.tmpl`でないsh/bash scriptにshfmtの`-d`とShellCheck、templateは[render検査](../tests/render_fixture.py)と同じ6分岐でrenderしたsh/bashの各出力にShellCheck（`-S warning`）をかける。workflowはactionlint（`run:`のShellCheckを含む）とzizmorを`--offline`で実行する。zshはShellCheckの対象外で、render検査の`zsh -n`だけである。除外は設定か[実装](../tests/test_lint.py)の定数に理由と並べて置き、配備されるファイルの整形・修正を利用者の承認待ちにしているものは`PENDING`と書く。Ruff・zizmor・actionlintの版は[lint tool一覧](../tests/lint-tools.toml)、StyLua・ShellCheck・shfmtは`10-tools.toml`を正本にし、CIの`Lint` jobはこの版だけを一時manifestで導入する。zizmorのoffline実行はGitHubへの照会が要るaudit（既知の脆弱なaction等）を含まない。

現行pre-commitには末尾空白・最終改行の修正、YAML/大file検査、`shfmt -w`、StyLuaがある。local hookは`language: unsupported`（pre-commit 4.4.0より前の名称は`system`）で実行pathに依存する。拡張子filterはtemplateを包括的には扱わず、専用のOKF frontmatter検査・Markdownリンク検査も定義されていない。初回実行ではhook環境の取得・導入もあり得る。必要なhookとfileを選び、変更された差分を確認する。`pre-commit run --all-files`を非変更検査と呼ばない。[^precommit][^precommit-docs]

Renovateを変更する場合は、repo rootでCIと同じvalidator版・Node runtimeを使う。版の正本はworkflowの`RENOVATE_VERSION`と参照先のtool宣言とし、この文書に別の固定版を増やさない。以下はその版を環境変数へ設定した後の現行相当の検査であり、`npx`は取得・cache書込を伴い得る。[^ci]

```sh
test -f renovate.json5
node --version
npx --version
npx --yes --package "renovate@${RENOVATE_VERSION:?CIと同じ版を設定}" -- renovate-config-validator --version
npx --yes --package "renovate@${RENOVATE_VERSION:?CIと同じ版を設定}" -- renovate-config-validator --strict
```

位置引数なしでrepositoryの既定場所を検査する。file名だけを位置引数に加えるとglobal configとして扱われるため、安易に同等のcommandへ書き換えない。`--strict`はmigrationの警告も失敗にする。validator合格は、botが全依存を抽出し望むPRを作ることの検証ではない。[^renovate-docs]

CIのjob分離・tool準備順・実施範囲は[隔離回帰の入口](#isolated-regression)を参照する。workflowを読んだことと、対象commitのrunが合格したことは区別する。[^ci]

# 結果を残す／まだ実装しないこと

検査結果には、対象commit・変更範囲、環境、行った操作、実際の結果、skip/warnと残る限界を短く記す。認証関連では秘密や個人情報を残さず、不一致の種類や件数を記録する。固定の大きなチェック表は要求しない。

identityのR10a・補完のR10b・bat/Vale/pbfileのR10c・Windows2設定のR14範囲を除き、全生成物の欠損復旧、同じ入力での再適用と保護対象の比較は[convergence](decisions/convergence.md)の未実装案である。診断専用入口の採用理由・代案は同Decisionで扱う。文書の構造検査を実機成功の代替にしない。

[^evals]: [Anthropic, 2026-01-09：結果状態と評価範囲](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)。
[^doctor]: [doctorの共通検査集合](../dot_config/mise/repo-tasks/doctor/executable__default.tmpl)。
[^checks]: [現行check taskの集合](../dot_config/mise/repo-tasks/check)。
[^hooks]: [chezmoi公式：dry-runでもhookが動く](https://www.chezmoi.io/reference/configuration-file/hooks/)。
[^wsl-check]: [WSL認証・通信・一時署名probe](../dot_config/mise/repo-tasks/check/executable_wsl-openssh.tmpl)。
[^precommit]: [変更を伴う整形hookと対象filter](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.pre-commit-config.yaml)。
[^precommit-docs]: [pre-commit公式：対象指定とhook環境の導入](https://pre-commit.com/)。
[^ci]: [CIの対象・実行段階・validator版](../.github/workflows/compliance.yml)。
[^renovate-docs]: [Renovate公式：repository configの検証とstrict mode](https://docs.renovatebot.com/config-validation/)。

<a id="completion-generation"></a>
# 補完・initの失敗時保持検査

`python3 tests/test_completion_transaction.py`は導入済みchezmoi・ZshとPython 3を使い、hookのない明示config、仮HOME/XDG、mise/WezTerm stubでtemplateをrender・実行する。chezmoi自身の補完出力だけは導入済み実体を使う。実mise・認証・tool install・実機apply/repair/doctorは実行しない。

必須generatorの非zero/空/構文不正、任意WezTermの失敗、gcloud include欠損/不正と旧link、process groupへのTERM/INT/KILL、task PID単独へのTERM/KILL後にgeneratorが成功する場合、render済みfixtureだけに注入したrename失敗・直前/直後のTERM、二つ目のwriterの拒否とTERM/INT/KILL後のretryを検査する。旧sourceの内容/modeと旧zwcを比較し、成功時は実Zshでinitのsource、全補完のautoload、代表補完とgcloud wrapperの呼出しを確認する。未来mtimeの旧zwcが新sourceを隠さないこと、実compinit dumpを作り、切替直後の中断でも実consumerの判定で新しい登録を取得すること、未知cache・外部path・symlink先の保持、固定親directory/lockのsymlink・非通常lockとdirectory digestの拒否も対象とする。

Ubuntu/macOS CI stepへ接続するが、local実行はmacOS隔離fixtureの証拠に限る。全toolの採用版による補完の意味的正常性、実WSL、generator以外による同時編集や稼働中shellのcompdump書込、停電耐久性、CI workflow全体は未確認。補完のdirectory単位outputsとonchange依存はR10bで撤去し、欠損復旧・SDK更新を下記で検査する。診断判定は上記R08の範囲で扱う。

[^render-command]: [chezmoi execute-template](https://www.chezmoi.io/reference/commands/execute-template/)、[明示config/source/destination/cacheのflags](https://www.chezmoi.io/reference/command-line-flags/global/)。renderはtemplate内のoutputを無効にしないため、fixture入力とstubを別途制御する。
[^mise-action]: [採用mise-actionのinputs](https://github.com/jdx/mise-action/blob/dba19683ed58901619b14f395a24841710cb4925/action.yml)と[導入・環境export実装](https://github.com/jdx/mise-action/blob/dba19683ed58901619b14f395a24841710cb4925/src/index.ts)。2026-11-11参照。最新READMEだけでは採用revisionの仕様を断定しない。
[^actions-needs]: [GitHub Actions workflow syntax: jobs.needs](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idneeds)。依存jobの成功後に動く条件と、失敗/skip時の伝播。

<a id="identity-convergence"></a>
# R10a identityの再適用・欠損検査

`python3 tests/test_identity_convergence.py`は、一時HOME/XDG・ダミーidentity・明示configで、実before/after/Git consumerと共通onchange wrapperを含む縮小sourceへapplyする。miseはinstall/runの呼出記録だけを行うstubで、package導入・認証・externals・実repo hookは起動しない。`tests/run_checks.py regression`と既存CIの隔離jobにも接続する。

同一入力二回適用のfile内容・mode・mtime・inode・世代数、各公開鍵/fragment/signers/dispatch/世代内entryの単独削除と同じpathへの復旧、shared templateだけ／engineだけの変更が同じapplyで反映されることを確認する。identityの欠損・変更だけで共通wrapperが再起動しないこと、不要な生成commandを呼ばないこと、R08 checkと実Git consumerが復旧後の参照を読めることを確かめる。

欠損と手動変更・symlink・未知file・mode変更の混在はbeforeで全件拒否し、部分復旧しない。復旧staging失敗は非zeroで残存fileを保持する。新入力の生成失敗時にも、欠損した旧世代fileを元の内容で復旧して旧consumerを保持する。固定entry／manifest喪失は非zero停止・無変更であり、自動復旧の合格例に数えない。v1 manifestの完全hash一致での復旧・v2移行と、不一致時の保持を検査する。R05の既存失敗／signal／空入力／旧参照保持検査も継続する。

WSLでは実変換結果を模す`wslpath` stubのdistro変更、変換失敗、環境名だけの変更、mise pin変更、Git formatter版変更を検査する。実WSL・Windows共有・認証の証拠ではない。macOSの隔離fixture結果は実機applyやCI workflow全体の合格とは区別する。固定entry／manifest等の所有根拠喪失と、v1で旧内容を再現できない欠損は明示復旧が必要であり、R10の全必須出力復旧や他generatorの完了を主張しない。


<a id="completion-convergence"></a>
# R10b 補完の再適用・依存変更検査

`test_completion_convergence.py`をR09の`python3 tests/run_checks.py regression`へ接続した。hookなしの明示config・隔離HOME/XDG・reduced source・実chezmoiを使い、before → target配置 → 実after_20 wrapper → 実after_30の順序を検査する。外部取得定義はfixtureで空にし、tool準備と共通graphの実処理はmise stubに置換する。初回導入・実graphの副作用の成功証拠ではない。

二回applyで全補完source/receipt/lockのhash・mode・mtime・inodeを比較し、CLI生成の呼出増加がないことを検査する。21個の必須補完/init/includeを一つずつ削除し、同回applyの復旧と他出力の保持を比較する。補完定義と共通checker template、mise本体bytes、代表CLI bytes/採用path、Node、package内実装、usageの実体と有無、SDK include変更を検査する。生成失敗・receipt競合・未知fileの保持を検査し、R07の旧source/zwc保持・親PID signal・並行lock・builtin rename・symlink親拒否も継続する。R08存在診断の成功と非変更性を確認する。

共通依存のhashは実行内で共有し、次のapplyでは再読する。代表既存mise 80,785,120 bytesとpnpm 11.6.0 treeを使った21回checkerの隔離測定は約0.85秒、読取約243MB（同一inodeのhardlinkを重複読取しない）だった。CLI生成・実tool環境解決を含む通常applyの所要時間ではなく、このmacOS環境の一例である。全tool採用版の意味的正常性・実CI・実WSL・実認証・実機applyは未実施。bat/Vale/pbfileは下記R10cで扱う。WindowsのR10契約を完了扱いにしない。


<a id="generated-assets"></a>
# R10c bat・Vale・pbfileの隔離検査

[test_generated_convergence.py](../tests/test_generated_convergence.py)をR09のregression runnerへ登録する。hookなし明示config・一時HOME/XDG・実chezmoiの縮小applyを用い、before → target → 実after_20 wrapper（mise準備/graphのみstub）→ 実after_40/41/42を検査する。R10a/R10bの全処理を重複fixtureへ組み込まず、それぞれ既存試験で保持する。

bat/Vale/compilerは決定的なstubを使い、同一入力の二回applyで生成・通信相当呼出し・出力/receiptの書換がないこと、各必須fileの単独欠損、その回でのtheme反映、Vale config/local package更新、Swift source/compiler/SDK代表入力変更を検査する。生成途中と検証での失敗、batの成功終了に隠れたtheme parse warning、未知file/独自style/手動tool保持、receipt喪失・不正・symlink・出力先redirect・手動変更の拒否、source/config欠落と他OSの非該当を区別する。共有publishには通常I/O例外のrollbackと再試行、rollback自体の失敗・receipt再読失敗時のbackup保持、publish途中のSIGKILLで部分反映が残り次回は競合停止する検査、receipt切替直後のSIGINTでは新出力と新receiptを保持する検査を追加する。これらを「すべての失敗で旧正常状態」とまとめない。native通信やcompiler互換性の証拠にstubを代用しない。

既存bat 0.26.1、Vale 3.14.2、macOSの選択Swift compiler/SDKを使う一時環境の検査は別に記録する。batの実theme load、Valeの実Google package（rule・vocab.txt・meta.json）、pbfileのcompileと引数なし起動の確認範囲に限る。hostへの導入・更新、実機apply/doctor、pasteboard操作、実認証、Ubuntu/WSL、実GitHub Actions全体は実行しない。floating Googleの欠損再syncはbyte再現検査とは呼ばない。receiptに記録した全fileのhash/modeを毎回確認するが、稼働中consumerの全動作、SDK全依存、generator外の並行編集、SIGKILL/停電時の復旧は保証しない。


<a id="windows-packages"></a>
# R11 Windows packageの識別・失敗分類の隔離検査

[test_windows_packages.py](../tests/test_windows_packages.py)をR09のregression runnerへ接続した。一時HOME/XDG、hookなし明示configと縮小sourceで実chezmoiにbefore templateをrenderさせ、実shell/Python helperを起動する。`powershell.exe`はfixtureであり、渡されたUTF-16LE Base64をdecodeし、Windows側で意図する引数を照合して全32bit終了値・stdout・stderrのJSONを返す。実package導入、source更新、PowerShellの評価は行わない。

CLIだけ導入済みのGUI不足、完全一致一件の再installなし、多言語の正常未導入、nightly hash不一致、source/認証/曖昧照合/引数/導入失敗、未導入と同じ低8bit・低8bitが0の別エラー、警告を伴うlist成功/未導入、install終了値0にsource警告やstderrが併存する場合、install identity表示の多言語・ID一致、複数行・省略ID・不正JSON・bridge不在を検査する。list/installのsource・exact・非対話/認証mode・installのsilent/agreements/no-upgrade、ID入力の拒否、実package宣言、非WSLの空出力とCIのheadless限定も確認する。hash迂回flagやsource更新失敗の握りつぶしを追加しない。

stubはPowerShellの構文・`.NET ProcessStartInfo`による実Windows argv分割・App Execution Alias解決・WSLの終了値変換・WinGetの実出力を実行検証しない。bridgeのAPIとCLIの基準は[公式資料と採用範囲](platforms/wsl.md#windows-packages)を静的照合する。macOSのfixture合格は実Windows/WSL、installer/UAC、認証、GitHub Actions runの成功ではない。表示形式の厳格な検査は安全側に停止し得るため、実Windowsでの多言語/初回source/更新/複数scopeの確認は残る。R10/R14のWindows設定copy・欠損復旧とは別の検査である。

<a id="homebrew-packages"></a>
# R12 Homebrew不足導入の隔離検査

[test_homebrew_packages.py](../tests/test_homebrew_packages.py)を`python3 tests/run_checks.py regression`へ接続した。一時HOME/XDGとhookなし明示configで実chezmoiに実package宣言・Brewfile・before scriptをrenderさせ、実Zshで実行する。brewは状態を持つstubだけをPATHへ置き、curl/bashはinstaller禁止のguardとする。実Homebrewやinstallerを実行しない。

旧版の宣言項目と未宣言項目の保持要求、不足formula/caskの追加、導入失敗の終了値伝播と成功表示なし、一時Brewfileの後始末、Homebrew不在時の停止、CI/headlessと非CI/media/GUI、macOS重複5件だけの除去とWindows native一覧保持、宣言変更がonchange入力へ反映されることを確認する。継承されたcleanup/skip設定の解除とauto-update/cleanup/dependents抑制も引数・環境の境界で照合する。

stubはHomebrewの依存解決、link、cask installer、brew.env読込、失敗途中の実package状態を再現しない。実Homebrewが既存項目を必ず不変にするという試験ではなく、scriptが要求したpolicyと制御フローの検査である。[公式資料・採用実装の静的照合](platforms/macos.md#homebrew-policy)で実装側の根拠を補う。実機apply・brew install/update/upgrade/cleanup、実CI runは未実施である。

<a id="first-install-order"></a>
# R13 初回段階と不足時停止の隔離検査

`python3 tests/test_first_install_order.py`は、導入済みchezmoi・Python・GitとOS shellを使用する。[検査実装](../tests/test_first_install_order.py)は空HOME/XDG、限定PATH、最小source、明示config/cacheを使い、regression runnerにも登録する。実installer・package manager・op・Windows tool・認証は使わない。init検査だけ実config templateと実read hookを維持し、mise実体・opをstubにする。その他はhookなしconfigを使う。

検査は、op不在/account失敗でinitが停止すること、成功init単独ではtargetやscriptsを適用しないこと、WSLのWezTerm/distro不足時に後続targetとafterが実行されないこと、Python/Git不足でbefore05がidentity出力を書く前に停止すること、Linux package/shellのsudo拒否時の案内と後続未実行を確認する。成功する対照も置き、単にfixture全体が壊れているための失敗を区別する。Python/Git不足時には先行before markerが残る。

使用したchezmoi **2.70.4**では、WezTermのtarget templateがbeforeより後に評価されることを観測した。失敗時にもbefore markerが残り、beforeがdestination外の仮Windows実体を作る正の対照では、その回のsymlink配置が成功する。したがって「beforeの導入ではWezTerm欠損を補えない」とは一般化しない。これは[同版の逐次apply](https://github.com/twpayne/chezmoi/blob/v2.70.4/internal/cmd/config.go#L750)と[遅延symlink評価](https://github.com/twpayne/chezmoi/blob/v2.70.4/internal/chezmoi/sourcestate.go#L2169)に整合する。config生成のop前提はapplyより先という別の境界である。`--keep-going`を使わない条件で、停止箇所より後だけを検査する。

macOSのWezTermは固定pathのrenderのみを確認し、存在確認とはしない。WSL分岐はLinux/Windows実環境ではなく明示dataとwslpath stubである。実クリーンOS、Windows interop・WinGet、sudo policy/認証有効期間、1Password認証、GUI起動、tool導入、実CI runは未確認。手動先行準備は[採用した手順](operations.md#first-install)であり、包括的な無変更preflightを追加したものではない。

<a id="windows-settings-sync"></a>
# R14・R10 Windows同期の隔離検査

[test_windows_config_sync.py](../tests/test_windows_config_sync.py)をregression runnerへ登録する。隔離HOME/XDG・ダミーidentity・hookなし明示config・縮小sourceで、実chezmoiと実Python helperを実行する。実after_20のmise準備/graphはstub、PowerShell/wslpathはWindows境界stub。before marker→target配置→after_20→after_50という観測順と、その回のtarget bytes配送を検査する。R13の訂正を維持し、全templateがbefore前に評価されるとは仮定しない。

同一入力2applyでtarget/receiptのbytes・mtime・inodeが不変であることを検査する。各targetの単独削除は同回に復旧し、distroやshared identity templateの変更で期待bytesが変わる場合はその回に更新する。一方、mise宣言・mise pin・実体・adapter/helperだけが変わり期待bytesが同じ場合は、同期出力を再書込しないことを検査する。初回欠損/同一採用/相違、手動編集、receipt喪失/破損/別destination、別distroの共有receiptとlock、redirected LOCALAPPDATA、旧誤pathと未知file保持、source欠損、query/変換失敗、POSIX symlink/非通常file/hardlink、Windows reparse拒否応答、CI/非WSLの対象外を分ける。

stage書込・target replace・receipt publishの失敗、通常rollback、rollback失敗時のbackup保持、公開前/後の外部編集、公開直後SIGKILLで新target・旧receipt・lock/backupが残り次回停止することを故障注入する。後続設定の失敗で先行設定が反映済みになるcaseも確認し、全applyのtransactionとは呼ばない。既存identity配送fixtureもLOCALAPPDATAと新taskへ更新する。

Windows stubはEncodedCommandをdecodeして固定queryと引数を照合するが、PowerShell 5.1の評価、Windowsのreparse/DrvFs lock/rename/ACL、別distroの共有filesystem、アプリ導入検出、GUI設定探索・reload、1Password unlock/認証、実CI runは検証しない。macOSでの隔離合格は実Windows互換性の証拠ではない。アプリ未導入の前提と順序はR11/R13の別検査、設定source欠損はこの検査の非zero条件であり、アプリの状態をsource欠損から推定しない。R10cの出力条件を再受入したという意味でもない。


# Neovim restoreの検証

`python3 tests/test_lazy_restore.py`は一時HOME/XDGのnative Neovimとmodule doubleで、lockの入力と出力の分離、silent process失敗、Neovimが終了0でも`v:errmsg`に残る非同期callbackエラー、submodule/build/spec/taskエラー、異なるorigin・engine・local変更、未採用plugin、最終checkout不一致を検査する。submoduleは採用親commitのcheckout後に初期化する。通常startupを起動せず、成功・失敗とも採用lockのbyteが変わらないことを確認する。

このfixtureは上流取得・実buildを代替しない。CIの独立したnetwork integration jobが、配置された`repair:nvim`を実際の採用lockで実行し、後続のlocal診断でsourceとのlock byte一致を確認する。復元成功はactive pluginのrevision一致とmanagerが観測するtaskの成功を指す。Mason pluginのconfigはsetupのみとし、`:MasonUpdate` buildを維持する。LazyVimのMason configにある`ensure_installed`は開始しないが、Treesitter等の別buildからMasonを使う導入は残る。これらの背景処理完了や、editor・provider・Mason/parserの動作証明ではない。未適用の実機や既存の破損pluginを自動修復できる保証も含まない。

# Neovim lock候補の隔離検証

`python3 tests/test_lazy_lock_update.py`は実Gitの一時repoとCLI stubで、A/B revisionと配置config Cの不一致、HEADとstagedの分離、dirty/index/untracked保持、literal options、取得前の入力拒否、非zero/成功report欠落/不正候補とartifact保持、literal lockのsource名、末尾改行なし/CRLFのpatchを別checkoutへ実Gitで適用して検査する。native Neovimでmodule doubleを用い、実Lua driverのsilent process・task・spec失敗gate、最終origin/target不一致も通す。上流取得はstubなので、これだけでupstream互換を証明しない。`tests/run_checks.py regression`にも接続する。

別のmacOS隔離native試験ではNeovim 0.12.3、lazy.nvim `85c7ff3`と選択HEAD `7dabf575`の実spec/lockを用い、public pluginの取得→更新→fresh process補完→最終照合まで成功した。50 active plugin、51 lock entry、34 entry差分を観測した。staged lockは入力外。lazy.nvimを保持し、通常plugin init/config・build・submodule取得は停止した。終了0でもbuild内部例外がtask ERRORになる経路と、無出力fetch失敗がtask ERRORにすらならない経路を採用版の別fixtureで再現し、process観測の必要性を確認した。

成功はこの入力revision・実行版・macOS・取得時点に限る。選択revisionのtool宣言版との一致を一般に保証せず、engine更新、全将来spec、通常editor動作・Mason/parser/provider、実CI・Linux/WSL・実機適用・公開は未検証。候補の採用条件とartifactの扱いは[development](development.md#neovimrestoreと更新を混同しない)を参照する。

<a id="vale-lint"></a>
# Vale診断の隔離検証

`NVIM_LINT_DIR=/path/to/nvim-lint LAZYVIM_DIR=/path/to/LazyVim python3 tests/test_vale_lint.py`は、導入済みNeovim・Vale・Gitと、source lockに一致する既存のplugin checkoutを使う。`NVIM_BIN`・`VALE_BIN`で既存実体を指定できる。関連Luaの変更があるcheckoutやshimを拒否し、pluginを一時領域へコピーする。取得・導入は行わず、不足時は失敗する。plugin依存のない一括regression入口とは別の検査であり、現時点のCIへは接続していない。[^vale-lint-test]

仮HOME/XDG、ローカルVale ruleと未保存bufferで、採用LazyVimの実mergeとnvim-lintの実行を確認する。ASCII・日本語・emojiのseverity、開始・終端byte範囲、拡張子なし`COMMIT_EDITMSG`、空白・Unicode path、`VALE_CONFIG_PATH`設定時と未設定時のconfig選択、診断の消去を検査する。parser境界では明示buffer番号、空出力、空行への文書全体の診断、不正JSON・範囲外行・不正Spanの解析失敗表示を確かめる。通常Neovim初期化・plugin manager・実Google styleの取得・認証・実機applyは行わない。

nvim-lint採用版のstdin・severity変換・parserを使い、Markdown stdin名の対応とNeovimのUTF-8境界APIによる開始byte位置だけを補正する。[^vale-lint-upstream][^vale-utf8]採用LazyVimは`prepend_args`を末尾へ追加するため、最後の`--ext .md`が有効になる。[^vale-lazyvim]configはVale自身の`VALE_CONFIG_PATH`／通常探索に任せる。[^vale-cli]

macOS・Neovim 0.12.3・Vale 3.14.2の隔離検証に成功した。実機適用・通常UIのtrigger・Windows/WSL・実CIの成功を示さない。採用Vale 3.14.2では複数行の反復語に不正な位置が返る再現例が残る。buffer外の行番号を含む場合、その回のVale診断は解析失敗のERROR表示へ置き換わり、個々の指摘を利用できない。Neovim側のbyte境界補正では直せず、Vale更新の別検証対象とする。現在のfixtureはこの失敗伝播も検査するため、Vale更新時は同じ再現入力で改善を確認して期待結果を見直す。文字列検索で位置を推測したり、失敗を空の診断集合へ変えたりしない。

[^vale-lint-test]: [Vale診断の隔離native検査](../tests/test_vale_lint.py)。
[^vale-lint-upstream]: [採用nvim-lintのVale parser・stdin・severity](https://github.com/mfussenegger/nvim-lint/blob/5259819fe849c978935281d1cab4bd26b375ab0f/lua/lint/linters/vale.lua)。
[^vale-lazyvim]: [採用LazyVimのlinter mergeと引数追加](https://github.com/LazyVim/LazyVim/blob/c10948c50b18fae7f256433afdef09e432410480/lua/lazyvim/plugins/linting.lua)。
[^vale-utf8]: [Neovim公式：UTF-8開始byte境界](https://neovim.io/doc/user/lua/#vim.str_utf_start())。
[^vale-cli]: [Vale公式：stdin・config探索・JSON出力](https://docs.vale.sh/topics/cli)。
