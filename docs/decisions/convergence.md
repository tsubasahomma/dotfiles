---
type: Decision
title: 欠損復旧を含むapplyと操作の責務分離
description: 採用した検討方針と未実装案を分け、成功条件・手動更新の扱い・代案・反証条件を確認する。
status: draft
generated:
  by: codex/gpt-6
  at: "2026-11-11T06:48:33+00:00"
sources:
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
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.bootstrap-mise.sh"
    title: "mise本体の導入先検査・pinとの差替え"
  - id: config
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoi.toml.tmpl"
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
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/generate/executable_identity.tmpl"
    title: "identity生成の先行削除と直接書き込み"
  - id: security
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/repair/executable_security.tmpl"
    title: "SSHファイルに対するchmod範囲"
  - id: doctor
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/doctor/executable__default.tmpl"
    title: "doctorが呼ぶ検査とCI分岐"
  - id: check-nvim
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/check/executable_nvim.tmpl"
    title: "chezmoi verifyと通常Neovim起動を含む検査"
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
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/generate/executable_completions.tmpl"
    title: "補完生成・warn処理・cache削除"
  - id: mise-upgrade
    resource: "https://github.com/jdx/mise/blob/v2026.6.11/docs/cli/upgrade.md"
    title: "mise v2026.6.11 upgrade：更新とbump"
  - id: brew-bundle
    resource: "https://docs.brew.sh/Brew-Bundle-and-Brewfile"
    title: "Homebrew Bundle：既定upgrade・no-upgrade・lock非対応"
  - id: brew-man
    resource: "https://docs.brew.sh/Manpage"
    title: "Homebrew brew(1)：導入に伴う依存変更と自動cleanup"
---
# 採用した検討方針と、まだ実装していないこと

applyの成功条件に、管理対象生成物の欠損復旧まで含める案を主軸に検討する。これは利用者が選んだ検討方針である。現在の`chezmoi apply`がその条件を満たすという意味ではない。[^direction]

| 区分 | 現在の扱い |
|---|---|
| 採用した方向 | 文書を先に整理し、chezmoi・miseの責務とbootstrap / applyを見直す。既存コードを無条件の正解とせず、欠損復旧を含むapplyを主案にする |
| 利用者からの報告 | 端末構築後にmise関連・brewを直接更新したものがある。今後コード管理へ寄せたい。実機の差分内容・版・導入元は未調査[^user] |
| 本文で提案する詳細 | 以下の成功条件、生成物の対象、版管理、doctorの非変更性、identity入力更新の分離、実装方式 |
| 未決 | 手動差分の採用先、SSH鍵とWindows設定の所有、必須／任意の生成物、各probe、既存入口での実現可否 |
| 実装・実機検証 | 未実施。この文案の作成もhost操作の許可や全項目の承認を意味しない |

現状の正本と書込主体は[ownership](../ownership.md)、既存入口の動作は[operations](../operations.md)を参照する。identityのschema・現行の不一致は[identity](../identity.md)、checkの実際の範囲と副作用は[validation](../validation.md)を正本とする。ここに現行手順の全一覧を複製せず、変更する理由と満たしたい結果を残す。

# 維持する候補と、変える候補

| 論点 | 維持する価値 | 見直す理由と主案 |
|---|---|---|
| source / target、明示的なtool宣言、repo-tasksの分離 | 継続する変更の正本と実行対象を追える | 手動更新を採用する判断まで自動化されてはいない。実機との差分を宣言へ取り込む段階を先に設ける[^tools][^mise-config] |
| mise本体のpinと導入先検査 | 要求版と配置先を明示でき、symlink等を誤って置換しない | source読込で新版もpinへ戻す。bootstrapを明示段階へ分け、通常の読込から導入・差替えを外す[^bootstrap][^config][^hooks] |
| before scriptでの依存導入 | 初回にrepo-tasksが未配置という制約に対応する | 毎回の更新や広いホスト設定変更まで一緒にしない。必要な順序は残し、対象・副作用を限定する[^wrapper][^tasks] |
| 生成をmise taskへ分ける | 同じ生成処理を再利用できる | 外側onchangeが内側の欠損確認を遮る。毎回軽い確認へ到達し、必要な生成だけ実行する[^wrapper][^scripts][^mise-tasks] |
| identity・Windows反映 | 入力から出力を再生成できる | 先行削除、直接書込、Windowsへの無条件copy、未所有鍵のchmodを絞る。所有を引き受ける範囲を先に決める[^identity][^security][^tasks] |
| doctorとrepairの入口 | 調査と修復の目的を分けて呼べる | 現行doctorには変更経路があり、repairの対象も広い。probeを監査し、対象別の生成と検査を共有する[^doctor][^check-nvim][^lazy] |

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

doctorの非変更性には、呼び出すtoolの自動導入・更新・cache書込も含めて確認が必要である。実機で「変更しなかった」ことはまだ試していない。副作用のない観測が用意できない項目は検査不能を報告し、別途依頼された操作へ分ける。[^mise-config][^check-nvim][^lazy]

doctorを作り直さず現行checkを対象限定で使う代案もある。その場合は副作用と対象外を個別に示し、非変更doctorという主案の条件を満たしたとは扱わない。実際のcheckの範囲は[validation](../validation.md)に残す。

login shellや`/etc/shells`の変更は明示的なホスト準備へ分ける案とする。pnpmの設定をapplyへ残すなら、管理するキー・保存先・同じファイルの他のキーの保持を定める。Windows設定も引受け範囲が決まるまで無条件copyを標準にしない。[^tasks]

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

この対象選択は現行の生成処理と欠損判定の弱点から導いたローカル案である。必要な正常性検査と必須／任意の区分はまだ決定していない。[^identity][^completions][^tasks]

<a id="manual-updates"></a>
# 手動更新を宣言へ引き受ける

手動操作は、故障の原因にも採用すべき改善にもなり得る。repoの古い宣言へ戻すことを自動的に「復旧」と呼ばない。一度の移行判断として差分を整理し、同じ差分について毎回承認を求める儀式は追加しない。[^user]

| 差分 | 推奨案 | 代案・採用条件 |
|---|---|---|
| mise本体 | 実体・版・導入元と互換性を確認し、採用版または基盤要件を宣言する。更新担当は一つにする | repo pinを維持して戻すのは理由・影響を確認した場合。Homebrew等の別管理に任せるならbootstrapが同じ実体を差し替えない設計にする |
| mise tool | 宣言・導入済み・有効版・PATH・config scopeを照合し、必要な手動更新をsourceへ取り込む。日常applyは採用要求の不足を導入する | 旧要求へ戻すか、local overrideを管理外として保持するかも選べる。installとuse / upgradeは同一操作ではない。余剰版のpruneやsource bumpは別操作[^mise-install][^mise-upgrade] |
| brewで更新した宣言項目 | 存在・利用可能性を管理し、実機の新版をそれだけで不一致としない。通常applyでの一括upgradeは外す案 | 更新もapplyに含める代案は、保守の手間が減る一方で欠損復旧の変更範囲が広がる。明示的な更新作業との分離を主案とする[^brew-bundle] |
| brewの手動追加項目 | 必要ならpackage宣言へ取り込む。管理外として残す選択も持つ | 未宣言だけを理由にcleanup / uninstallしない。不要と判断して除去する作業は別に扱う |
| 手動編集したtarget | 必要な差分だけsourceへ採用、宣言へ置換、別scopeで管理のいずれかを選ぶ | target全体の自動chezmoi add、実機全体の自動dumpを正本へ無差別に取り込む方式は採らない |

mise本体の管理と、miseが扱うtoolの管理は別に決める。同じtoolをbrewとmiseの両方で持つ必要がなければ主担当を選ぶが、異なるOSや実行用途は例外として理由を残す。実機の実行パス・共有依存が未確認なので、現時点で削除対象は決めない。

brewの候補は`brew bundle --no-upgrade`等だが、これは版固定でも完全な非変更保証でもない。Homebrew Bundleはlockによる任意旧版の再現を提供しない。厳密版が必要な項目だけ管理手段を再検討する。[^brew-bundle]

不足導入にも共有依存・link・post-install・自動cleanupの影響がある。自動cleanupを抑える設定を検討し、必要な依存変更は対象と副作用へ含める。依存整合性を壊す一律抑制で成功を装わない。影響を特定できない変更や範囲外の変更が必要なら、その項目を未達として保守・移行の判断へ戻す。これは現行scriptの挙動ではなく、実装前に確かめる制約である。[^brew-man]

<a id="identity-input"></a>
# identity入力の更新と失敗時の保護

通常applyは採用済みidentity入力から復旧し、最新入力の取得は明示的な更新段階へ分ける案を主とする。初回op準備がconfig生成より先に必要という現行制約を踏まえる。採用入力が不明な場合や取得が必要な場面で、取得不能を空identityへ置き換えて正常出力を消さない。[^config]

代案はapply前に毎回opから再取得する方式。最新性を上げられる一方、認証・通信依存が増える。採用済み入力からの復旧案には、遠隔の失効・変更をapplyだけでは検知できない限界があり、指定した認証probeと入力更新が別途必要になる。入力更新方式・鮮度の要件は未決である。

生成は可能な単位で一時生成 → 検査 → 置換へ変える。複数identityファイルの切替全体が原子的になるとは未検証で約束しない。途中失敗時は失敗対象と既に変更した範囲を示し、旧正常出力を保持して再実行できる構造を目指す。package導入まで含む全体rollbackは成功条件に含めない。[^identity]

<a id="bootstrap-prerequisites"></a>
# 初回準備の方式と未決事項

現在の初回導入経路は[operations](../operations.md#first-install)、先行条件は[macOS](../platforms/macos.md)・[WSL](../platforms/wsl.md)を正本とする。以下はその順序上の不足を解く案で、実装方式は未採用である。[^config]

| 方式 | 利点 | 費用・採用条件 |
|---|---|---|
| 現行に必要な前提を明示的に先行導入 | 既存templateを大きく変えず、最初のconfig生成へ到達できる | tool・認証・GUIの準備が残る。operationsの経路はこの方式を説明するが通し検証は未実施 |
| bootstrapを前提導入とconfig生成へ分割 | 初回依存の順序をcodeで表現できる | 未導入miseや未配置repo-tasksへの循環依存を避ける。既存端末の手動版を勝手に戻さない |
| 必要な探索・生成を後段へ遅らせる | WSL WezTermなどの先行要求を減らせる可能性 | 不完全なtargetを成功扱いしない設計と失敗伝播が必要。1Password入力の鮮度・config生成との関係は別途検討 |

初期chezmoiの導入方法・採用版とrepo宣言への移行、PATH上の実体、Linuxの非対話sudoの最小権限設計は未決。GUI app・container runtime・OS権限をすべてapplyの管理対象にする決定ではない。公式資料はcommandの意味を支えるもので、この方式比較の優劣を証明しない。

<a id="windows-ownership"></a>
# Windows設定を引き受けるか

現在の2設定copyは[WSL文書](../platforms/wsl.md)の通りで、copy元欠損のskipとcopy先の無条件上書きがある。次の比較は未決であり、現行にwriterがあることを所有承認としない。[^tasks]

| 方式 | 利点 | 費用・採用条件 |
|---|---|---|
| Windows側は手動管理し、WSL内の生成まで保証 | OSをまたぐ書込を減らせる | Windows側との整合を利用者が別途保つ。対象外を明示し、現行の自動copyをどう外すか決める |
| 指定したWindows設定を管理へ引き受ける | 対象の欠損復旧・内容確認をapplyへ含められる | 初回差分と手動変更の採用先、既存fileの保護・競合時の失敗を設計する。Windows全体を所有しない |

<a id="identity-constraints"></a>
# identityの未決事項

現行のschema・生成経路・不一致は[identity](../identity.md)を参照する。次の項目は採否を決めていない改善候補である。[^config][^identity]

| 論点 | 検討する変更・比較条件 |
|---|---|
| 空集合・不完全入力 | 入力検証後に生成する。空集合を許可する条件と失敗時の既存出力保持を定める |
| 古い公開鍵 | 所有を識別できる生成物だけを対象にする。保持による残存と、削除時の誤判定の両方を評価する |
| schemaとrouting | 空要素・重複・包含、path/設定値としての妥当性を検査し、複数identityのfixtureで確かめる |
| socket参照階層 | 入力とconsumerの階層を揃え、環境変数経由と明示的IdentityAgentの選択をrenderと実効経路で判断する |
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

すべて未実行。変更に対応するケースを選び、出力と保護対象の実状態を確認する。常設の全検査儀式にしない。[^evals]

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
[^bootstrap]: [mise本体の導入先検査・pinとの差替え](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.bootstrap-mise.sh).
[^config]: [identity入力・ホスト情報の取得とread-source-state hook](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoi.toml.tmpl).
[^hooks]: [chezmoi Hooks：dry-runでもhookは動く](https://www.chezmoi.io/reference/configuration-file/hooks/).
[^wrapper]: [post-applyの起動条件・mise install・認証の受け渡し](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl).
[^tasks]: [repo所有taskの実装](https://github.com/tsubasahomma/dotfiles/tree/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks).
[^scripts]: [chezmoi scripts：onchangeの成功済み内容による再実行判定](https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/).
[^mise-tasks]: [mise v2026.6.11：task省略と依存順序](https://github.com/jdx/mise/blob/v2026.6.11/docs/tasks/running-tasks.md).
[^identity]: [identity生成の先行削除と直接書き込み](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/generate/executable_identity.tmpl).
[^security]: [SSHファイルに対するchmod範囲](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/repair/executable_security.tmpl).
[^doctor]: [doctorが呼ぶ検査とCI分岐](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/doctor/executable__default.tmpl).
[^check-nvim]: [chezmoi verifyと通常Neovim起動を含む検査](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/check/executable_nvim.tmpl).
[^lazy]: [Neovim起動時のlazy.nvim取得](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/nvim/lua/config/lazy.lua).
[^evals]: [Anthropic, 2026-01-09：結果状態に基づくagent評価](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).
[^mise-install]: [mise v2026.6.11 install：導入と有効化は別](https://github.com/jdx/mise/blob/v2026.6.11/docs/cli/install.md).
[^verify]: [chezmoi verifyの確認範囲](https://www.chezmoi.io/reference/commands/verify/).
[^completions]: [補完生成・warn処理・cache削除](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/generate/executable_completions.tmpl).
[^mise-upgrade]: [mise v2026.6.11 upgrade：更新とbump](https://github.com/jdx/mise/blob/v2026.6.11/docs/cli/upgrade.md).
[^brew-bundle]: [Homebrew Bundle：既定upgrade・no-upgrade・lock非対応](https://docs.brew.sh/Brew-Bundle-and-Brewfile).
[^brew-man]: [Homebrew brew(1)：導入に伴う依存変更と自動cleanup](https://docs.brew.sh/Manpage).
