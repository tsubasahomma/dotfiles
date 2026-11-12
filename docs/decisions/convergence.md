---
type: Decision
title: 欠損復旧を含むapplyと操作の責務分離
description: 採用した検討方針と未実装案を分け、成功条件・手動更新の扱い・代案・反証条件を確認する。
status: draft
generated:
  by: codex/gpt-6
  at: "2026-11-12T00:24:47+00:00"
sources:
  - id: order
    resource: "https://www.chezmoi.io/reference/application-order/"
    title: "chezmoiの概略適用順。遅延評価は採用版実装と照合する"
  - id: zsh-files
    resource: "https://github.com/zsh-users/zsh/blob/zsh-5.9/Src/Modules/files.c"
    title: "Zsh 5.9 files moduleのatomic rename実装（ローカルmanも確認）"
  - id: zsh-system
    resource: "https://github.com/zsh-users/zsh/blob/master/Doc/Zsh/mod_system.yo"
    title: "Zsh system moduleのadvisory lockとprocess終了時解除"
  - id: zsh-compile
    resource: "https://zsh.sourceforge.io/Doc/Release/Shell-Builtin-Commands.html"
    title: "Zsh sourceとzcompile"
  - id: zsh-autoload
    resource: "https://zsh.sourceforge.io/Doc/Release/Functions.html"
    title: "Zsh autoloadとcompiled fileの優先順位"
  - id: identity-transaction
    resource: "../../.chezmoitemplates/identity_transaction.py"
    title: "identity世代の生成と参照切替"
  - id: identity-prepare
    resource: "../../.chezmoiscripts/run_before_05-identity-dispatch.sh.tmpl"
    title: "target前のlegacy routing保存"
  - id: python-replace
    resource: "https://docs.python.org/3/library/os.html#os.replace"
    title: "Python os.replaceの原子性とfilesystem境界"
  - id: direction
    resource: "Maintainer direction in the repository OKF design conversation, 2026-11-11"
    title: "applyに管理対象生成物の欠損復旧を含める案を主軸に検討する。詳細方式は未承認"
  - id: user
    resource: "Maintainer report in the repository OKF design conversation, 2026-11-11"
    title: "端末構築後にmise関連・brewを直接更新したとの利用者報告。実機観測ではない"
  - id: tools
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/conf.d/10-tools.toml"
    title: "観測時のmise tool宣言"
  - id: mise-config
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/config.toml.tmpl"
    title: "mise task discovery・自動導入設定"
  - id: bootstrap
    resource: "../../.bootstrap-mise.sh"
    title: "mise本体の読込検査・明示導入"
  - id: config
    resource: "../../.chezmoi.toml.tmpl"
    title: "identity入力・ホスト情報の取得とread-source-state hook"
  - id: hooks
    resource: "https://www.chezmoi.io/reference/configuration-file/hooks/"
    title: "chezmoi Hooks：dry-runでもhookは動く"
  - id: wrapper
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl"
    title: "post-applyの起動条件・mise install・認証の受け渡し"
  - id: tasks
    resource: "https://github.com/tsubasahomma/dotfiles/tree/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks"
    title: "repo所有taskの実装"
  - id: scripts
    resource: "https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/"
    title: "chezmoi scripts：onchangeの成功済み内容による再実行判定"
  - id: mise-tasks
    resource: "https://github.com/jdx/mise/blob/v2026.6.11/docs/tasks/running-tasks.md"
    title: "mise v2026.6.11：task省略と依存順序"
  - id: identity
    resource: "../../dot_config/mise/repo-tasks/generate/executable_identity.tmpl"
    title: "identity入力の検証と世代切替"
  - id: security
    resource: "../../dot_config/mise/repo-tasks/repair/executable_security.tmpl"
    title: "権限変更を行わない互換task"
  - id: doctor
    resource: "../../dot_config/mise/repo-tasks/doctor/executable__default.tmpl"
    title: "doctorの共通検査集合"
  - id: check-nvim
    resource: "../../dot_config/mise/repo-tasks/check/executable_nvim.tmpl"
    title: "Neovim lockの直接比較と実体の存在検査"
  - id: lazy
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/nvim/lua/config/lazy.lua"
    title: "Neovim起動時のlazy.nvim取得"
  - id: evals
    resource: "https://www.anthropic.com/research/demystifying-evals-for-ai-agents"
    title: "Anthropic, 2026-01-09：結果状態に基づくagent評価"
  - id: mise-install
    resource: "https://github.com/jdx/mise/blob/v2026.6.11/docs/cli/install.md"
    title: "mise v2026.6.11 install：導入と有効化は別"
  - id: verify
    resource: "https://www.chezmoi.io/reference/commands/verify/"
    title: "chezmoi verifyの確認範囲"
  - id: completions
    resource: "../../dot_config/mise/repo-tasks/generate/executable_completions.tmpl"
    title: "補完・initの個別検証と切替"
  - id: mise-upgrade
    resource: "https://github.com/jdx/mise/blob/v2026.6.11/docs/cli/upgrade.md"
    title: "mise v2026.6.11 upgrade：更新とbump"
  - id: brew-bundle
    resource: "https://docs.brew.sh/Brew-Bundle-and-Brewfile"
    title: "Homebrew Bundle：既定upgrade・no-upgrade・lock非対応"
  - id: brew-man
    resource: "https://docs.brew.sh/Manpage"
    title: "Homebrew brew(1)：導入に伴う依存変更と自動cleanup"
  - id: mise-run-diagnostics
    resource: https://github.com/jdx/mise/blob/v2026.6.11/src/cli/run.rs
    title: mise task開始前のtool導入
  - id: mise-settings-diagnostics
    resource: https://github.com/jdx/mise/blob/v2026.6.11/settings.toml
    title: 採用miseの自動導入・offline設定
  - id: nvim-diagnostics
    resource: https://neovim.io/doc/user/starting/
    title: Neovimの初期化抑制option
  - id: git-diagnostics
    resource: https://git-scm.com/docs/git-config#Documentation/git-config.txt-gpgsshallowedSignersFile
    title: SSH署名の信頼判定
  - id: ssh-diagnostics
    resource: https://man.openbsd.org/ssh-keygen#ALLOWED_SIGNERS
    title: OpenSSH allowed signers
  - id: mise-version-startup
    resource: https://github.com/jdx/mise/blob/v2026.6.11/src/cli/mod.rs
    title: 版表示後も実行される起動処理
  - id: mise-cache-prune
    resource: https://github.com/jdx/mise/blob/v2026.6.11/src/cache.rs
    title: 確率的cache pruneと早期return
  - id: mise-version-command
    resource: https://github.com/jdx/mise/blob/v2026.6.11/src/cli/version.rs
    title: 最新版照会とcache書込
  - id: mise-migrations
    resource: https://github.com/jdx/mise/blob/v2026.6.11/src/migrate.rs
    title: 起動時の移動・削除
  - id: mise-miserc
    resource: https://github.com/jdx/mise/blob/v2026.6.11/src/config/miserc.rs
    title: 早期設定探索とceiling
  - id: mise-directories
    resource: https://github.com/jdx/mise/blob/v2026.6.11/src/dirs.rs
    title: mise directoryの参照先
  - id: mise-environment
    resource: https://github.com/jdx/mise/blob/v2026.6.11/src/env.rs
    title: system dataと共有installの既定path
  - id: mise-runtime-migration
    resource: https://github.com/jdx/mise/blob/v2026.6.11/src/runtime_symlinks.rs
    title: 共有installを含むruntime symlink移行
---
# 採用した検討方針と、まだ実装していないこと

applyの成功条件に、管理対象生成物の欠損復旧まで含める案を主軸に検討する。これは利用者が選んだ検討方針である。現在の`chezmoi apply`がその条件を満たすという意味ではない。[^direction]

| 区分 | 現在の扱い |
|---|---|
| 採用した方向 | 文書を先に整理し、chezmoi・miseの責務とbootstrap / applyを見直す。既存コードを無条件の正解とせず、欠損復旧を含むapplyを主案にする |
| 利用者からの報告 | 端末構築後にmise関連・brewを直接更新したものがある。今後コード管理へ寄せたい。実機の差分内容・版・導入元は未調査[^user] |
| 本文で提案する詳細 | 以下の成功条件、生成物の対象、版管理、全体収束、identity入力更新の分離、実装方式 |
| 未決 | 手動差分の採用先、生成物の衝突（Windows2設定は下記で採用済み）、必須／任意の生成物、各probe、既存入口での実現可否 |
| 実装・実機検証 | R08の診断専用入口・明示probeはsource実装済み（下記）。実機未適用。R01のmise読込／明示導入分離はsource実装・隔離検証済み。実機未適用。R06の未所有鍵chmod・旧パス恒久削除の停止もsource実装済み。R10aのidentity、R10bの補完、R10cのbat/Vale/pbfile、R14のWindows2設定同期は下記の限定契約でsource実装済み・実機未適用。下記で採用済みと明記した範囲以外の詳細案は未実装で、host操作の許可や全項目の承認を意味しない |

現状の正本と書込主体は[ownership](../ownership.md)、既存入口の動作は[operations](../operations.md)を参照する。identityのschema・現行の不一致は[identity](../identity.md)、checkの実際の範囲と副作用は[validation](../validation.md)を正本とする。ここに現行手順の全一覧を複製せず、変更する理由と満たしたい結果を残す。

# 維持する候補と、変える候補

| 論点 | 維持する価値 | 見直す理由と主案 |
|---|---|---|
| source / target、明示的なtool宣言、repo-tasksの分離 | 継続する変更の正本と実行対象を追える | 手動更新を採用する判断まで自動化されてはいない。実機との差分を宣言へ取り込む段階を先に設ける[^tools][^mise-config] |
| mise本体のpinと導入先検査 | 要求版と配置先を明示でき、symlink等を誤って置換しない | 旧実装はsource読込で新版もpinへ戻した。R01では読込を存在・実行属性の検査、導入を--installへ分離した。既存不一致も保持する[^bootstrap][^config][^hooks] |
| before scriptでの依存導入 | 初回にrepo-tasksが未配置という制約に対応する | 毎回の更新や広いホスト設定変更まで一緒にしない。必要な順序は残し、対象・副作用を限定する[^wrapper][^tasks] |
| 生成をmise taskへ分ける | 同じ生成処理を再利用できる | 外側onchangeが内側の欠損確認を遮る。毎回軽い確認へ到達し、必要な生成だけ実行する[^wrapper][^scripts][^mise-tasks] |
| identity・Windows反映 | 入力から出力を再生成できる | 未所有鍵のchmodはR06で撤去した。identityの先行削除・直接書込はR05で世代切替へ変更した。Windowsは下記の限定2file管理へ変更し、既存相違と手動編集を停止する[^identity][^security][^tasks] |
| doctorとrepairの入口 | 調査と修復の目的を分けて呼べる | R08で直接診断入口と明示probeへ分離した。従来mise入口のtask開始前導入は残る。repair全体の対象共有は後続[^doctor][^check-nvim][^lazy] |

# R01で採用した境界

読込からmise取得・差替えを外し、引数なしの旧hook呼出しも検査として扱う。templateだけの変更では既存configに旧入口が残るため、scriptの既定動作も変えた。`--install`は不在時にpin版を導入し、既存不一致を失敗として保持する。[操作と移行](../operations.md#mise-bootstrap)、[隔離検証](../validation.md#mise-read-boundary)が現行契約である。

代案はhookの完全撤去、または読込時に版一致を必須とする方式。今回は不足時に明示操作を説明する入口を残し、既存版の互換性を未確認のままdowngradeも読込拒否もしない。pin廃止・manager統一・初回導入全体・check全体の非変更化はこの変更に含めない。存在検査は互換性の保証にならず、明示導入の可変installerと途中失敗の扱いにも限界がある。実機への移行は未実施である。

# R06で採用した保持の境界

現在のidentity generatorは秘密鍵を生成せず、出力する公開鍵とallowed_signersのmodeを自身で設定している。`repair:security`の再帰chmodは不要であり、互換入口として非変更にする。名前で対象を狭める代案でも所有を証明できず、今回のための汎用manifest導入も必要ない。[所有境界](../ownership.md)を現行の正本とする。[^identity][^security]

旧パスを列挙した`.chezmoiremove.tmpl`も、手動再導入物や同名の利用者ファイルを旧管理状態から区別できないため、恒久削除を全件停止する。代案は旧内容を確実に識別する限定移行だが、現時点でその証拠を持たない。旧ファイル・task・serviceの残存を許容し、必要な整理は内容と現在の参照を確認して行う。過去の被害復元や、generatorの既存出力との衝突・transactionまで解決した判断ではない。[移行上の注意](../operations.md#ownership-preservation)を参照。

# applyの成功条件案

採用した宣言・入力・ホスト条件に対し、選択した管理範囲が期待する状態へ到達したことを成功とする。ログや終了コードだけでなく結果の状態を確かめる、という評価の考え方を用いる。これはこのrepoへの設計上の適用であり、以下の方式が研究で実証されたという意味ではない。[^evals]

1. **対象と入力が決まっている**：OS、有効な機能、採用するsource、外部入力、必須／任意を開始時に特定する。失敗後に必須項目を対象外へ変更しない。
2. **静的状態が合う**：管理する内容・mode・symlinkが採用targetと一致する。未解決の手動編集との衝突は成功扱いしない。
3. **必要な依存を使える**：miseは要求版とその処理の実行パス、brewは採用した項目の存在・利用可能性を確認する。単にinstall済みという判定では足りない。[^mise-install]
4. **必須生成物を個別に確認・復旧する**：欠損・切れたリンク・既知の不正状態を確認する。親directoryや成功stampだけで済ませず、各出力に必要な軽い検査を設ける。
5. **保護対象を保つ**：利用者の鍵・独自設定・未宣言packageを勝手に削除・権限変更・一括更新しない。必要な共有依存の変更は開始前に対象と副作用へ含める。所有出力も生成失敗で直前の正常内容を失わない。
6. **未達を成功にしない**：必須対象の復旧失敗・検査不能は非zero。任意の未実施・OS上の非該当・対象限定の成功を区別する。

全アプリの無故障、全packageの最新版、常時の認証解除、あらゆる破損の検出は保証しない。chezmoi verifyは静的target確認の材料であり、任意の生成物までの保証に拡張しない。doctor全部の無条件実行をapplyの成功条件にする必要もない。[^verify]

# 四つの責務と副作用の案

以下は論理的な責務名であり、新しい同名CLIを作る決定ではない。

| 責務 | 成功時の状態 | 許容する副作用 | 含めないもの・失敗時 |
|---|---|---|---|
| bootstrap | 選択ホストでapplyを始められる基盤と初期入力が揃う | 定めた最小依存の不足導入、初期config生成、明示的な認証準備 | 既存miseの未整理な差替え、日常の全package更新。初回は未配置taskや未導入mise自身に依存しない |
| apply | 上の成功条件を選択範囲で満たす | 静的配置、採用要求の不足導入、必要asset取得、欠損復旧・生成 | sourceや要求版の自動bump、全体upgrade / cleanup、未所有鍵のchmod。必須未達は失敗 |
| repair | 指定対象を同じ採用入力の状態へ戻す | applyと同じ生成・検査処理を対象指定で再評価し、必要ならその対象の再取得・再生成 | 別実装のrepair-all、版更新、認証方針変更。成功は指定した範囲に限定 |
| doctor | 指定範囲の状態・差分・検査不能を報告する | 出力と片付ける一時作業領域。監査した既存環境でのprobe | 導入・生成・sudo・source変更・暗黙の認証開始・通常アプリ起動からの初期化。必須検査不能は失敗 |

<a id="diagnostic-boundary"></a>
# R08で採用した診断境界

通常診断は配置済み`dotfiles-diagnose`からcheck scriptを直接呼ぶ。CIと端末で必須欠損・lock driftの失敗条件を揃え、任意のWezTerm/HubSpot補完は警告、非WSLのWindows probeは対象外とする。identityは公開鍵を含む必須参照とrender済み入力（name/email/signingkey/signers/routing）を直接照合する。固定entry・dispatch・fragmentはR05の生成形式にキー集合を限定し、追加includeや署名設定での上書きも失敗にする。R05の生成済み世代をfixtureにし、存在だけを満たす不完全な世代を合格例にしない。WSL鍵pathの実directory変換はWindowsを起動せず判定できないため、形状・option・filenameまでに限定して明示する。未実施のアプリ動作・認証を成功表示へ含めない。現在の対象と入口は[validation](../validation.md#diagnostic-boundary)と[operations](../operations.md#diagnostic-entry)を正本にする。

採用mise v2026.6.11は`task.run_auto_install`と`auto_install`が既定trueで、run.rsはtask実行前にtoolsetとtask専用toolを準備する。check本体のexportは遅い。local/private設定を巻き戻さず、通常診断からmise task runnerを外す方式を採った。直接入口でもauto-install関連環境変数をfalseにするが、未知binaryを隔離するsandboxとは扱わない。[^mise-run-diagnostics][^mise-settings-diagnostics]

代案は起動前に環境変数を付けてmise run/execを使う方式。task discoveryとPATH解決を再利用できる一方で、利用者の動的configやhook、別版miseの挙動まで通常診断へ持ち込むため既定入口には選ばない。CIは管理されたconfigと導入済みtoolのPATHを使う必要があるため、起動前にauto-installを無効化したmise execを別段階で使う。診断のためにglobalな自動導入方針を変更する代案も選ばない。

<a id="diagnostic-version-isolation"></a>
版照会だけは一時HOME/XDG・専用mise領域と空の環境へ分離する。採用v2026.6.11では`--version`の表示後もbackend初期化・migration・確率的cache pruneを通り、終了前に非CIの最新版照会も行う。旧診断は隔離fixture内でも古いcacheの削除と`.auto_prune`作成を起こし得た。通常テストの偶然の合格では非変更性を証明できない。[^mise-version-startup][^mise-cache-prune][^mise-version-command][^mise-migrations]

`MISE_CACHE_PRUNE_AGE=0s`はageをNoneにし、marker作成より前にpruneからreturnする。ただし、この設定だけの代案ではmigrationのrename/削除や最新版cache書込が残るため採らない。子processに0s・offline・CI・設定/環境/hookの読込禁止を指定し、全mise directoryとcwdを一時領域へ向ける。system dataは既定で`/usr/local/share/mise`となり、共有installもruntime symlink移行の削除対象に含まれるため、`MISE_SYSTEM_DATA_DIR`も明示する。[^mise-environment][^mise-runtime-migration]早期のmiserc探索もceilingとsystem config directoryで切る。ceilingとcwdはpath文字列で比較されるため、一時directoryは物理pathへ揃える。親の環境overrideを選択的に残す方式より、版文字列取得に不要な値を`env -i`で全て外す方が参照先を限定できる。実体と版の一致判定は維持し、検査不能をskipへ変えない。[^mise-settings-diagnostics][^mise-cache-prune][^mise-version-command][^mise-miserc][^mise-directories]

一時領域の書込・cleanupは許容するが、利用者のcache/config/dataは変更しない。これは採用版のコードに基づくdirectory/settings上の隔離であり、未知版・改変binary・任意wrapperの任意pathアクセスを禁止するsandboxではない。版更新時には起動順・環境変数・directory契約を再確認する。native実験はmacOSの隔離環境に限り、全ホストや未知設定の実動作を保証しない。明示probeの実行副作用と、CIのmise execによるPATH準備はこの版照会の外側にある。

Neovim lockは非templateのsource fileとtargetを直接cmpする。chezmoi verifyを使う代案にはsource hook・external/cacheの境界があり、この一fileのbyte比較には不要である。providerを通常configで試す代案はLazy初期化へ入るため、明示probeだけで`-u NONE --noplugin -i NONE -n`を使う。これは通常設定でのprovider選択・Node RPCやplugin動作の保証を失うため、検査結果に限界を示す。[^nvim-diagnostics]

署名の暗号学的妥当性と信頼する鍵の集合を分ける。GitのSSH署名ではallowedSignersFile内の鍵はfully、未登録鍵はundefinedとしてverify-commitが失敗する。`gpg.minTrustLevel=fully`も明示し、表示文言のgrepは使わない。使い捨て鍵による隔離回帰は信頼集合の判定を検証するが、実1Password helper・Windows interopの成功は未確認である。[^git-diagnostics][^ssh-diagnostics]

今回の対象は診断境界であり、全生成物の再適用・欠損復旧やCI全体の再設計は含めない。既存配置からの移行、実toolの未知wrapper・runtime副作用は実機で別途確認する。

login shellや`/etc/shells`の変更は明示的なホスト準備へ分ける案とする。pnpmの設定をapplyへ残すなら、管理するキー・保存先・同じファイルの他のキーの保持を定める。Windows設定は下記の限定2file管理を採用し、無条件copyを撤去した。[^tasks]

# 管理対象生成物の初期案

現在taskが触る全パスを自動的に所有しない。対象を有効にしたホストについて、既存入力から期待する出力を導く。別の巨大な一覧を手作業で二重管理する方式は前提にしない。

| 対象候補 | 復旧・確認の案 | 別判断・対象外 |
|---|---|---|
| identity includes、生成公開鍵、allowed_signers | 採用入力から個別出力と参照関係を確認し、一時生成・検査後に置換 | 秘密鍵の抽出・再生成、任意のid_* chmod、識別できない旧公開鍵のglob削除 |
| Zsh init・必須補完 | 期待する個々のファイルとリンクを確認。1つの欠損でも再生成へ到達 | 任意補完は事前定義。zwcを必須にするかは元ファイルからのfallback要件で決める |
| bat cache・Vale styles | 選択theme / styleに対応する欠損・確認可能な不整合を復旧 | 全cacheの所有、取得のたびの無条件最新版化。floating入力はbyte再現性を保証しない |
| macOS pbfile | 対象OSでソースとcompilerを確認し、欠損・必要な変更時にbuild | ソースやcompilerの欠落を成功skipしない。他OSは非該当 |
| Neovim plugins | Neovimを対象に含めるなら、採用lockに沿って不足をrestore | lock更新・最新化・commit / push / PR。必須profileに含めるかは未決 |
| Windowsへ複製する設定 | 所有すると決めた範囲だけ期待内容・競合を確認して反映 | Windows独自変更の黙った上書き、copy元欠落の成功skip |

この対象選択は現行の生成処理と欠損判定の弱点から導いたローカル案である。補完・initについては下記R07の契約を採用した。bat・Vale・pbfileは下記R10cの限定契約を採用した。その他の必要な正常性検査と必須／任意の区分はまだ決定していない。[^identity][^completions][^tasks]

<a id="manual-updates"></a>
# 手動更新を宣言へ引き受ける

手動操作は、故障の原因にも採用すべき改善にもなり得る。repoの古い宣言へ戻すことを自動的に「復旧」と呼ばない。一度の移行判断として差分を整理し、同じ差分について毎回承認を求める儀式は追加しない。[^user]

| 差分 | 推奨案 | 代案・採用条件 |
|---|---|---|
| mise本体 | 実体・版・導入元と互換性を確認し、採用版または基盤要件を宣言する。更新担当は一つにする | repo pinを維持して戻すのは理由・影響を確認した場合。Homebrew等の別管理に任せるならbootstrapが同じ実体を差し替えない設計にする |
| mise tool | 宣言・導入済み・有効版・PATH・config scopeを照合し、必要な手動更新をsourceへ取り込む。日常applyは採用要求の不足を導入する | 旧要求へ戻すか、local overrideを管理外として保持するかも選べる。installとuse / upgradeは同一操作ではない。余剰版のpruneやsource bumpは別操作[^mise-install][^mise-upgrade] |
| brewで更新した宣言項目 | 存在・利用可能性を管理し、実機の新版をそれだけで不一致としない。通常applyでの一括upgradeをR12で除去 | 更新もapplyに含める代案は、保守の手間が減る一方で欠損復旧の変更範囲が広がる。明示的な更新作業との分離を採用した[^brew-bundle] |
| brewの手動追加項目 | 必要ならpackage宣言へ取り込む。管理外として残す選択も持つ | 未宣言だけを理由にcleanup / uninstallしない。不要と判断して除去する作業は別に扱う |
| 手動編集したtarget | 必要な差分だけsourceへ採用、宣言へ置換、別scopeで管理のいずれかを選ぶ | target全体の自動chezmoi add、実機全体の自動dumpを正本へ無差別に取り込む方式は採らない |

mise本体とmiseが扱うtoolは別に決める。R12では利用者がjust・atuin・duckdb・deno・AWS CLIの主担当をmiseと決定した。macOSのbrew宣言だけを外し、既存brew実体とWindows native宣言を保持する。両管理元を維持する代案は今回選ばない。事前読取でこのプロセスではmiseのPATHが先、brew receiptsに他formulaからのruntime依存なしと観測したが、全consumer・対話shell・共有依存の不在までは証明していない。削除やPATH一括変更は別の作業である。

R12は`brew bundle install --no-upgrade`と自動update/cleanup抑制を採用した。Homebrew不在時は明示準備を案内して停止し、通常applyからinstallerを起動しない。これは版固定でも完全な非変更保証でもない。Homebrew Bundleはlockによる任意旧版の再現を提供しない。厳密版が必要な項目だけ管理手段を再検討する。[^brew-bundle]

不足導入の必要な依存解決・link・post-installは許容し、`--ignore-dependencies`等では抑えない。既存dependentsの追随upgrade/reinstallは`HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1`で通常経路から外す。これには既存consumerの互換性修復が自動で行われない代償があるため、成功を全consumerの正常性とはしない。依存変更自体も禁止する代案では不足導入を満たせない場合があり、今回は選ばない。失敗は非zeroで停止する。具体的な入口は[operations](../operations.md#homebrew-packages)、採用実装と検査限界は[macOS](../platforms/macos.md#homebrew-policy)に記す。[^brew-man]

<a id="identity-input"></a>
# identity入力の更新と失敗時の保護

通常applyは採用済みidentity入力から復旧し、最新入力の取得は明示的な更新段階へ分ける案を主とする。初回op準備がconfig生成より先に必要という現行制約を踏まえる。採用入力が不明な場合や取得が必要な場面で、取得不能を空identityへ置き換えて正常出力を消さない。[^config]

代案はapply前に毎回opから再取得する方式。最新性を上げられる一方、認証・通信依存が増える。採用済み入力からの復旧案には、遠隔の失効・変更をapplyだけでは検知できない限界があり、指定した認証probeと入力更新が別途必要になる。入力更新方式・鮮度の要件は未決である。

R05ではGit identityの切替単位として、固有世代の公開鍵・fragment・allowed_signers・routingと、それを選ぶ単一のentryを採用した。全入力検証→非公開世代生成→Git/OpenSSH形式検証→entry置換の順とし、静的Git targetの先行変更にはbefore scriptによる旧routing保存で対応する。現行の契約と移行の制約は[identity](../identity.md#生成の切替と既存配置からの移行)を正本とする。[^identity-transaction][^identity-prepare]

代案のファイル別renameでは、複数fileを横断するreaderに混在が見える。可変の`current`symlink配下へ鍵とsignersを向ける案も、Gitが設定を読んだ後の切替で別世代を開き得るため選ばない。固有世代へ固定参照し、単一entryの同一filesystemでの`os.replace`を利用する。Pythonの仕様は成功時のrenameの原子性を述べるが、停電耐久性やapply全体のtransactionを保証する根拠ではない。旧世代は既存readerのため回収しない。[^python-replace]

beforeでPython 3.9+が必要になる費用を受け入れ、不足時はtarget前に明示的に停止する。mise installより前に必要なので、初回のPATH準備を[operations](../operations.md#first-install)へ加える。shellだけで同じ状態・JSON・file検証を実装する代案は引用・失敗処理を複雑にする。初回bootstrap全体の自動化はこの変更には含めない。

<a id="bootstrap-prerequisites"></a>
# 初回準備の方式と未決事項

R13では、必要な前提を手動で先行準備する方式を採用する。最小tool、OS固有前提・認証、config生成、配置の順を[operations](../operations.md#first-install)に定め、OS別の詳細は[macOS](../platforms/macos.md)・[WSL](../platforms/wsl.md)を正本とする。既存の手動準備方針を具体化する変更であり、完全自動bootstrapの保証を撤回する変更ではない。[^config]

| 方式 | 利点 | 費用・採用条件 |
|---|---|---|
| 必要な前提を手動で先行準備（採用） | 既存templateを大きく変えず、依存順と不足時の行動を明示できる | tool・認証・GUIの準備は操作者が担う。局所guardと隔離順序検査を備えるが、クリーンOSの通し検証は未実施 |
| bootstrapを前提導入とconfig生成へ分割 | 初回依存の順序をcodeで表現できる | 未導入miseや未配置repo-tasksへの循環依存を避ける。既存端末の手動版を勝手に戻さない |
| 必要な探索・生成を後段へ遅らせる | WSL WezTermなどの先行要求を減らせる可能性 | 不完全なtargetを成功扱いしない設計と失敗伝播が必要。1Password入力の鮮度・config生成との関係は別途検討 |

初期chezmoiの導入方法・採用版とrepo宣言への移行、PATH上の実体、Linuxの非対話sudoの最小権限設計は未決。GUI app・container runtime・OS権限をすべてapplyの管理対象にする決定ではない。公式資料はcommandの意味を支えるもので、この方式比較の優劣を証明しない。

config生成のop認証はapplyのbefore package導入では補えない。WezTermも初回手順では手動先行準備とする。ただし公式の概略順だけから全templateがbefore前に評価済みとは断定しない。chezmoi 2.70.4の実装と隔離fixtureでは、WezTerm実体/distro不足より前にbeforeが走る遅延評価を確認した（[操作上の限界](../operations.md#applyで通る段階)）。Python 3.9+とGitもidentityのbefore段階で必要になり、afterのmise installには依存できない。準備を手動で分けることでこの循環を避ける。新たな汎用bootstrapや探索の後段移動は、手動手順で解決できない具体的な障害が出た場合に再検討する。[^order]

局所guardの失敗は後段の配置・生成を止めるが、先行beforeでの変更は残り得る。Linux sudoの案内は必要commandの権限確認へ限定し、無制限のpasswordless設定を勧めない。fixture合格を実WSL・実認証・クリーン端末の成功に置き換えない。

# Neovim restoreの成功条件

CIで通常startupのmissing installが採用pinを失い、checkout失敗でも終了0になることを確認したため、`repair:nvim`を専用sessionでのinstall/restoreへ変更した。入力lockを保持し、task/process失敗と最終active pluginのcheckout/originを検査する。通常applyに含めない境界は維持する。具体的な対応範囲と副作用は[development](../development.md#neovimrestoreと更新を混同しない)、検証入口は[validation](../validation.md#neovim-restoreの検証)を正本とする。

CIから復元を削除する案、診断のlock driftを警告へ落とす案、終了後にlockだけを書き戻す案では実checkout失敗が隠れるため採らない。submoduleの一律無効化も既存機能が使う依存を欠くため採らない。上流managerの非公開境界へ触れるadapterには版制約を置き、engine更新時は失敗fixtureと隔離native復元で再確認する。

[^order]: [chezmoi application order](https://www.chezmoi.io/reference/application-order/)。全templateの評価時刻までこの概略から推測せず、[採用版実装とfixture](../validation.md#first-install-order)を照合する。

<a id="windows-ownership"></a>
# Windowsの2設定管理を採用する

利用者は2026-11-11にrepo管理を選択した。R14ではWezTermと1Password agent設定だけを欠損・前回bytesで照合し、既存相違と手動編集を保持停止する。旧writerの存在を所有承認には使わず、初回は欠損または現在の期待bytesと完全同一の場合に限り登録する。[操作契約](../operations.md#windows-settings-sync)と[所有境界](../ownership.md#windows-settings-sync)を正本とする。

代案のWindows手動管理はOS間書込を減らせるが、欠損復旧と入力変更の同期を利用者が別途担うため今回は選ばない。receiptをWSL側だけに置く案は複数distroから同じtargetを扱う際に所有記録が分岐するため、target隣のreceipt/lockを採用する。別distroの採用入力が違う場合、順次applyは最後の正常入力へ更新する。特定distroへ永久固定する契約ではない。

R10 Windows部分は専用の毎回after_50で2taskだけを呼ぶ。実targetのbytesを配置後に読むため、Windows target単独欠損とWSL_DISTRO_NAME等のrender依存変更をその回で扱う。共通mise graphの毎回化は不要なtool導入・他のprovisionを増やすため採らない。R10cの共有generator frameworkへWindows処理を追加せず、2file用のhelperに留める。

stage検証後のfile別replaceと捕捉可能なI/O失敗のrollbackに限定する。全file/receiptの一括原子性、強制中断の自動回復、外部Windows editorとの完全排他、実Windows ACLの保持は保証しない。receipt喪失時の異なるtarget、未知path、reparse/非通常fileは安全側に停止する。配置先rootが変われば新rootを初回規則で扱い、旧場所は削除しない。実Windows互換性は[検証の限界](../validation.md#windows-settings-sync)として残す。

<a id="identity-constraints"></a>
# identityの未決事項

現行のschema・生成経路・不一致は[identity](../identity.md)を参照する。socket参照階層とGit接続の分離はR04でsourceへ反映した（実機未適用）。次の項目は採否を決めていない改善候補である。[^config][^identity]

| 論点 | 検討する変更・比較条件 |
|---|---|
| 空集合・不完全入力 | 入力検証後に生成する。空集合を許可する条件と失敗時の既存出力保持を定める |
| 古い公開鍵 | 所有を識別できる生成物だけを対象にする。保持による残存と、削除時の誤判定の両方を評価する |
| schemaとrouting | 空要素・重複・包含、path/設定値としての妥当性を検査し、複数identityのfixtureで確かめる |
| SSH既定値 | agent forwardingが必要なhostとhost keyの扱いを用途ごとに決める。現行の全host既定値を必須要件としない |

# 実装方式の代案

| 方式 | 評価 | 選び直す条件 |
|---|---|---|
| 既存apply入口に毎回の軽い確認を組み込む | 第一候補。必要な生成だけ行い、同じ処理を対象repairからも使う。read hookの非変更化と失敗伝播が必要 | preflight・段階間の制御・部分対象の意味を既存入口で明確にできなければ次案へ |
| sourceから使う専用のapply入口 | 配置・生成・検査の順序を制御しやすい | 入口増加、二重実行・再帰、未導入miseへの依存を防げる場合。独自frameworkは必要条件にしない |
| onchangeを維持し欠損はrepairのみ | 通常applyは軽いが、主案の欠損復旧条件を満たさない | applyを静的配置に限定する方針へ見直した場合 |
| 常に全生成・全導入 | 欠損確認の抜けを減らせるが、不要な通信・認証・buildが増える | 測って十分安価な処理だけ部分採用する場合 |

chezmoiのscript起動条件とmiseのsources/outputsは方式選択の制約を説明するが、最適な方式を決定してはくれない。省略条件は「入力不変、かつ必要な出力が妥当」を目指し、mtimeやstampは最適化の材料として使う。[^scripts][^mise-tasks]

# 実装前後に確かめること

R01のmise読込分離は上記の隔離検証を行った。以下の収束設計全体のケースは未実行であり、変更に対応するケースを選び、出力と保護対象の実状態を確認する。常設の全検査儀式にしない。[^evals]

| ケース | 主案が満たすべき結果 |
|---|---|
| source不変、親directoryを残して補完1ファイルだけ欠損 | applyが検出して復旧する |
| identityの一部欠損・生成途中失敗・容量不足 | 旧正常出力を不必要に失わず、未達は非zero。再実行で復旧できる |
| 手動mise新版、targetの直接編集、未宣言brew項目 | 自動downgrade・上書き・削除せず採用先を決める。移行後は採用宣言で処理する |
| 不足package導入が共有依存を変える | 影響が選択範囲内に収まり、無関係なcleanup・更新をしない |
| 管理外鍵やWindows独自設定が存在する | 内容・modeを保持し、競合を成功skipしない |
| tool / pluginがない状態でdoctor | 導入や初期化をせず不足を報告し、永続状態が変わらない |
| 入出力が正常な再apply、または対象指定repair | 正常な再applyは重い再生成を省く。repairは対象の同じpostconditionを満たす |
| identity fragment / 外部assetだけ変更、認証locked | 関係する生成が新しい入力を使う。入力が必要な処理の取得不能を空入力で代用しない |

# 進める順序と再検討条件

文書の変更と実機挙動の変更を分ける。手動差分を変更なしで調べられる方法を確立する。その後、状態の引受け先と必須出力を決め、失敗保護・診断の非変更性・毎回の欠損確認を小さい単位で実装する。実機applyは、その対象と副作用が具体化した段階で行う。今回の作業範囲には含めない。

主案を支持する材料だけで判断しない。欠損検査の維持費が過大、毎回確認が著しく遅い、共有依存の変更を制御できない、認証の鮮度要件を満たせない、既存入口では成功範囲が説明できない場合には、上の代案へ戻る。この比較によるバイアス低減効果は未測定で、初稿は履歴を共有しない3担当の静的レビューを受けたが、実機試験やこの構成の効果測定は行っていない。

公式資料は2026-11-11に確認した。miseはrepoのpinと同じv2026.6.11の文書を参照し、手動更新された端末の実版まで同じと仮定しない。Homebrewは現行公式資料の説明であり、端末固有の挙動は別途確認する。

[^direction]: applyに管理対象生成物の欠損復旧を含める案を主軸に検討する。詳細方式は未承認.
[^user]: 端末構築後にmise関連・brewを直接更新したとの利用者報告。実機観測ではない.
[^tools]: [観測時のmise tool宣言](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/conf.d/10-tools.toml).
[^mise-config]: [mise task discovery・自動導入設定](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/config.toml.tmpl).
[^bootstrap]: [mise本体の読込検査・明示導入](../../.bootstrap-mise.sh).
[^config]: [identity入力・ホスト情報の取得とread-source-state hook](../../.chezmoi.toml.tmpl).
[^hooks]: [chezmoi Hooks：dry-runでもhookは動く](https://www.chezmoi.io/reference/configuration-file/hooks/).
[^wrapper]: [post-applyの起動条件・mise install・認証の受け渡し](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl).
[^tasks]: [repo所有taskの実装](https://github.com/tsubasahomma/dotfiles/tree/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks).
[^scripts]: [chezmoi scripts：onchangeの成功済み内容による再実行判定](https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/).
[^mise-tasks]: [mise v2026.6.11：task省略と依存順序](https://github.com/jdx/mise/blob/v2026.6.11/docs/tasks/running-tasks.md).
[^identity]: [identity入力の検証と世代切替](../../dot_config/mise/repo-tasks/generate/executable_identity.tmpl).
[^security]: [権限変更を行わない互換task](../../dot_config/mise/repo-tasks/repair/executable_security.tmpl).
[^doctor]: [doctorの共通検査集合](../../dot_config/mise/repo-tasks/doctor/executable__default.tmpl).
[^check-nvim]: [Neovim lockの直接比較と実体の存在検査](../../dot_config/mise/repo-tasks/check/executable_nvim.tmpl).
[^lazy]: [Neovim起動時のlazy.nvim取得](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/nvim/lua/config/lazy.lua).
[^evals]: [Anthropic, 2026-01-09：結果状態に基づくagent評価](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).
[^mise-install]: [mise v2026.6.11 install：導入と有効化は別](https://github.com/jdx/mise/blob/v2026.6.11/docs/cli/install.md).
[^verify]: [chezmoi verifyの確認範囲](https://www.chezmoi.io/reference/commands/verify/).
[^completions]: [補完・initの個別検証と切替](../../dot_config/mise/repo-tasks/generate/executable_completions.tmpl).
[^mise-upgrade]: [mise v2026.6.11 upgrade：更新とbump](https://github.com/jdx/mise/blob/v2026.6.11/docs/cli/upgrade.md).
[^brew-bundle]: [Homebrew Bundle：既定upgrade・no-upgrade・lock非対応](https://docs.brew.sh/Brew-Bundle-and-Brewfile).
[^brew-man]: [Homebrew brew(1)：導入に伴う依存変更と自動cleanup](https://docs.brew.sh/Manpage).

[^identity-transaction]: [identity世代生成と単一entry切替](../../.chezmoitemplates/identity_transaction.py)。
[^identity-prepare]: [before scriptの移行入口](../../.chezmoiscripts/run_before_05-identity-dispatch.sh.tmpl)。[chezmoi application order](https://www.chezmoi.io/reference/application-order/)に従いtarget前に保存する。
[^python-replace]: [Python os.replace](https://docs.python.org/3/library/os.html#os.replace)。同一filesystemでの成功したrenameの原子性を参照。

# 補完・initの失敗時保持で採用した契約

R07では現行tool宣言とZshのsource/fpath consumerに基づき、生成対象の宣言済みCLI・mise・chezmoi・gcloud・2つのinitを必須、PATHから検出するWezTermだけを任意とした。pnpm・deltaの従来の失敗無視は採用しない。個別sourceの正常生成後renameで十分であり、一式transactionのframeworkは導入しない。[操作契約](../operations.md#completion-generation)と[隔離検査](../validation.md#completion-generation)を参照。[^completions]

Zshはsourceやautoload時に新しいcompiled fileを優先し、directory単位digestも探索する。そこで`zcompile -U`を非実行の構文検査に使い、生成sourceとzwcを二段階で配布する代案を避け、成功時にはsourceだけを配置する。旧対象zwcとconsumer dumpは検証後・source切替前に退避・無効化する。task shell自身がpublishとsignal trapを持ち、task PIDだけへのTERMで子publisherが残らないようにする。新sourceが旧compiled内容に隠れないことを優先し、起動/補完のparse時間が増える可能性は未測定である。未知のdirectory digestは自動削除せず拒否する。並行generatorがrollback時に別の新sourceへ古いcacheを戻さないよう、Zshの`zsystem flock`で排他する。mkdir lockの取得/解除とshellの所有flag更新の間に中断が入る代案は避け、process終了で解除されるkernel lockを採用した。file inodeは削除しない。module非対応なら非zeroで止まる。[^zsh-system]

backup・source commit・復元は`zsh/files`の`zf_mv` builtinを使う。外部mvを使う代案ではtask PIDだけへのSIGKILL後に子mvが残り、lock解除後の次の生成を上書きできるため採らない。builtinならrename syscallとlock所有processが同じであり、別filesystemへのcopy fallbackも行わない。[^zsh-files][^zsh-compile][^zsh-autoload]

全生成codeをsourceして検証する代案は、initが実tool起動やshell状態変更を行い得るため採らない。構文正常なエラーメッセージ等の意味的不正や実CLIの互換性を、この構文検査だけでは検出できない。fixtureでloadabilityを検証し、実toolでの全体動作保証とは分ける。gcloudはlink先が後で変わり検証を迂回する方式から、検証したincludeのsnapshotへ変更した。次のSDK更新はR10bの毎apply検査で検出し、includeを再生成する。

[^zsh-compile]: [Zsh: Shell Builtin Commands — sourceとzcompile](https://zsh.sourceforge.io/Doc/Release/Shell-Builtin-Commands.html)。2026-11-11閲覧。
[^zsh-autoload]: [Zsh: Functions — Autoloading Functions](https://zsh.sourceforge.io/Doc/Release/Functions.html)。2026-11-11閲覧。

[^zsh-system]: [Zsh公式source: system module — zsystem flock](https://github.com/zsh-users/zsh/blob/master/Doc/Zsh/mod_system.yo)。2026-11-11閲覧。

[^zsh-files]: [Zsh 5.9 files module source](https://github.com/zsh-users/zsh/blob/zsh-5.9/Src/Modules/files.c)。`mv`はrenameとMV_ATOMICを選ぶ。ローカルZsh 5.9 `man zshmodules`のTHE ZSH/FILES MODULEも確認。

[^mise-run-diagnostics]: [mise v2026.6.11 run.rs](https://github.com/jdx/mise/blob/v2026.6.11/src/cli/run.rs)。task実行前のinstall_missing_versionsとinstall_task_tools。2026-11-11参照。
[^mise-settings-diagnostics]: [mise v2026.6.11 settings.toml](https://github.com/jdx/mise/blob/v2026.6.11/settings.toml)。auto_install・task.run_auto_install・offlineの定義。
[^nvim-diagnostics]: [Neovim起動option](https://neovim.io/doc/user/starting/)。導入済み0.12.3のruntime/doc/starting.txtとも照合。
[^git-diagnostics]: [Git SSH allowedSignersFileとtrust level](https://git-scm.com/docs/git-config#Documentation/git-config.txt-gpgsshallowedSignersFile)、[verify-commit](https://git-scm.com/docs/git-verify-commit)。
[^ssh-diagnostics]: [OpenSSH allowed signers](https://man.openbsd.org/ssh-keygen#ALLOWED_SIGNERS)。

# R10aで採用したidentityの収束範囲

identityだけを毎回動く小さいafter scriptへ分離し、所有・全出力・render済み入力の一致をengineで一度判定する方式を採る。共通onchange wrapperを毎回実行する代案は、R10a時点で未整備だった補完・bat・Vale・pbfile等の生成やpackage操作まで起動するため採らなかった。単に入力hashをwrapperへ増やす代案では、個別欠損の検査が遮られたままになる。chezmoiの毎回scriptとbefore/target/after順序に従い、beforeでは既存世代の検査・復旧、afterでは新入力への切替を行う。[^scripts][^identity-prepare][^identity-transaction]

新世代へ切り替えるだけの欠損復旧は、旧dispatchをすでに読んだconsumerの欠損pathを救えない。v2 manifestへ検証済み公開出力の内容とmodeを保存し、欠損だけを旧pathへ戻す方式を採った。新入力から旧世代を上書きする方式は採らない。v1は全hashが一致する場合だけ復旧でき、不一致なら停止する。固定entry／manifest自体の喪失は採用・所有が曖昧なので、別の可変pointerを増やして推測復旧することはしない。このためR10の「全必須出力一個の削除で自動復旧」は全面達成ではない。詳細な出力別契約は[identity](../identity.md#identity-convergence)、証拠の範囲は[validation](../validation.md#identity-convergence)を正本とする。

入力依存はshared templateのrender結果とengine source、Git formatter版、実WSL path変換へ限定する。mise版だけやWSL環境名だけでの無用な世代生成を避けつつ、実際のWindows鍵pathが変わる場合は再生成する。実WSLの変換とconsumerは未確認で、stubは実機保証ではない。他のR10出力契約は後続へ残す。


# R10bで採用した補完の収束範囲

補完専用after_30からR07の安全なtaskへ毎回到達させ、task内の個別照合だけを生成省略の判断にする。共通onchange graphを毎回動かす代案は、tool install・pnpm設定・Linux shell・未整備generatorへ責務を広げるため採らない。補完だけをmise sources/outputsへ列挙し直す代案も、実CLI・SDKの変化と正常sourceの内容を十分に表さず、二重判定になるため採らない。after_20から補完を外し、その終了後に動かすので初回の準備順を保つ。[操作契約](../operations.md#completion-convergence)を正本とする。

小さい隠しreceiptで成功時の入力/出力hashを記録し、欠損と入力変化を区別する。R07の出力所有・失敗保持契約を変えず、入力検査やreceipt生成のPythonにはpublishさせない。すべての入力を毎回再生成して比較する代案よりCLI起動とzcompileを減らす。mtimeだけの永続cacheは同一mtimeの内容変更を見逃すため採らず、一回の実行内でのみfile/tree hashを共有する。新しい汎用task frameworkは導入しない。

採用pathとbytesを使い、単なるtool宣言の文面・directory markerを正常性の根拠にしない。`mise which --tool`と実行先を揃え、Node系はlauncherの外のpackage実装も入力に含める。SDKは実際にcopyするincludeだけを読む。mise内部のusage依存は同じtool環境で解決し、有無とbytesを追うがfallbackの必須性は変えない。共通generatorのrender変更は全出力を再生成する保守的な判定とし、通常の個別依存変更は関係する出力に限る。採用版の`exec --no-deps`と自動導入抑止は[公式実装](https://github.com/jdx/mise/blob/v2026.6.11/src/cli/exec.rs)および隔離したv2026.6.11 helpで確認した。

未知receiptの上書き、外部SDK/外部補完/未知cacheの回収、tool更新との同時transactionは引き受けない。toolとlib/configの全環境を閉包する保証もない。実機全CLI互換性・実WSLは後続の確認とする。R10aのidentityの所有根拠喪失時停止はそのまま残る。bat/Vale/pbfileの後続契約は下記R10c、Windowsは[別契約](#windows-ownership)で扱う。


<a id="generated-assets"></a>
# R10cで採用したbat・Vale・pbfileの収束範囲

外側onchangeとdirectory outputsを外して専用afterから個別checkerへ到達させる。配置後のthemeを処理時に読むため、配置前targetをtemplate hashへ埋めて次回まで遅れる問題も避ける。共通graph自体を毎apply化する代案はtool準備・pnpm・Linux shellまで広げるため採らない。実装は[bat](../../.chezmoitemplates/bat_cache.py)、[Vale](../../.chezmoitemplates/vale_styles.py)、[pbfile](../../.chezmoitemplates/pbfile_build.py)を分け、共有部分をlock・file照合・限定publishに留める。receiptは各系統に一つ、固定entryや世代pointerは追加しない。

batは[公式build実装](https://github.com/sharkdp/bat/blob/v0.26.1/src/assets/build_assets.rs)と[CLI](https://github.com/sharkdp/bat/blob/v0.26.1/src/bin/bat/clap_app.rs)にある別source/target指定を使う。default cacheへの直書きや`cache --clear`は必要ない。themes/syntaxesの利用者追加も入力として含める。cache形式依存は選択binaryと版、三つの出力で扱う。[metadata実装](https://github.com/sharkdp/bat/blob/v0.26.1/src/assets/assets_metadata.rs)が生成時刻を含むため、既存cacheのbyte再生成比較による自動所有認定は採らない。input内symlinkは追跡範囲を拡張せず停止する制約がある。

Valeの[採用版sync実装](https://github.com/errata-ai/vale/blob/v3.14.2/cmd/vale/sync.go)は同名出力の削除・copyと設定pipeline変更を行うため、稼働中StylesPathへ直接syncする代案を採らない。今回の出力契約はGoogleのstyle-only packageへ限定する。許す指定は裸のGoogle、HTTPSのGoogle.zip、絶対pathのlocal Google directory/zip。取得物は全ruleとvocab補助fileを検証・記録し、無関係なstyleや設定bundleは引き受けない。package数や再帰依存まで自動一般化するframeworkは追加しない。

[公式Google package案内](https://vale.sh/explorer/google)は裸の名前がsync時にlatest releaseを選ぶことと固定release URLの代案を示す。今回は既存の裸の`Google`を維持し、正常同一入力では通信せず、必要時にだけsyncする。この保存方式では欠損復旧時にremoteが更新されていればstyleも更新され得る。version固定URLは選ぶ版を明示できるがremote assetのbytes不変性まで保証しない。digestを検証する固定artifactや検証済みpackageのlocal保存なら、毎回通信せずに旧bytesを復元できる。今回は採用版・digestを新たに決定したりartifact保管/回収機構を追加したりせず、URL/local入力の変更を検出するところまでとする。厳密再現が必要になった場合は固定artifactを採用する小さな別変更が候補となる。

pbfileは[Appleのxcrun説明](https://developer.apple.com/library/archive/technotes/tn2339/_index.html)に沿って選択されたcompiler/SDKを問い合わせ、そのcompilerへSDKと一時出力を指定する。sourceだけのmtime判定や常時compileより、実compiler・SDKの代表入力を含むdigest判定を採る。compiler driverのbytes/versionとSDKSettingsは検出対象だが、toolchain全dylib・SDK全header・OS loader等の完全な閉包ではない。bat/Valeも動的library・任意のwrapper runtimeまで閉包しない。

移行時に既存出力を無条件採用する方式と、全directoryを置換する方式は採らない。空いた対象だけを初期化し、以後はreceiptで所有とbytes/modeを照合する。未知・競合を保持して停止することは、すべての欠損や不整合を自動修復する契約ではない。staging検証後のfile単位publishと捕捉可能なエラーのrollbackを提供するが、全host・複数fileの原子性や停電耐久性は名乗らない。詳細な運用境界は[operations](../operations.md#generated-assets)、証拠の範囲は[validation](../validation.md#generated-assets)を参照。R10aの所有根拠喪失時停止、R10bの補完契約を変更せず、Windows部分は[別契約](#windows-ownership)と別fixtureで扱う。このR10c検査だけでR10全体完了とはしない。

[^mise-version-startup]: [mise v2026.6.11 — 版表示後も実行される起動処理](https://github.com/jdx/mise/blob/v2026.6.11/src/cli/mod.rs)。2026-11-12参照。

[^mise-cache-prune]: [mise v2026.6.11 — 確率的cache pruneと早期return](https://github.com/jdx/mise/blob/v2026.6.11/src/cache.rs)。2026-11-12参照。

[^mise-version-command]: [mise v2026.6.11 — 最新版照会とcache書込](https://github.com/jdx/mise/blob/v2026.6.11/src/cli/version.rs)。2026-11-12参照。

[^mise-migrations]: [mise v2026.6.11 — 起動時の移動・削除](https://github.com/jdx/mise/blob/v2026.6.11/src/migrate.rs)。2026-11-12参照。

[^mise-miserc]: [mise v2026.6.11 — 早期設定探索とceiling](https://github.com/jdx/mise/blob/v2026.6.11/src/config/miserc.rs)。2026-11-12参照。

[^mise-directories]: [mise v2026.6.11 — mise directoryの参照先](https://github.com/jdx/mise/blob/v2026.6.11/src/dirs.rs)。2026-11-12参照。

[^mise-environment]: [mise v2026.6.11 — system dataと共有installの既定path](https://github.com/jdx/mise/blob/v2026.6.11/src/env.rs)。2026-11-12参照。

[^mise-runtime-migration]: [mise v2026.6.11 — 共有installを含むruntime symlink移行](https://github.com/jdx/mise/blob/v2026.6.11/src/runtime_symlinks.rs)。2026-11-12参照。
