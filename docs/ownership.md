---
type: Reference
title: 状態の正本と書き込み主体
description: 設定・生成物・手動管理状態について、現行の所有境界と未決の引受け範囲を確認する。
status: draft
generated:
  by: codex/gpt-6
  at: "2026-11-11T16:02:49+00:00"
sources:
  - id: config
    resource: "../.chezmoi.toml.tmpl"
    title: "identity入力・ホスト情報の取得とread-source-state hook"
  - id: bootstrap
    resource: "../.bootstrap-mise.sh"
    title: "mise本体の読込検査・明示導入"
  - id: ignore
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiignore.tmpl"
    title: "chezmoiによる配置の除外"
  - id: remove
    resource: "../.chezmoiremove.tmpl"
    title: "旧パスの恒久削除を停止したremove定義"
  - id: externals
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiexternal.toml.tmpl"
    title: "外部assetとrefresh指定"
  - id: tools
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/conf.d/10-tools.toml"
    title: "観測時のmise tool宣言"
  - id: mise-config
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/config.toml.tmpl"
    title: "mise task discovery・自動導入設定"
  - id: wrapper
    resource: "../.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl"
    title: "post-applyの起動条件・mise install・認証の受け渡し"
  - id: mise-install
    resource: "https://github.com/jdx/mise/blob/v2026.6.11/docs/cli/install.md"
    title: "mise v2026.6.11 install：導入と有効化は別"
  - id: packages
    resource: "../.chezmoidata/packages.yaml"
    title: "OS別packageの宣言"
  - id: brewfile
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/homebrew/Brewfile.tmpl"
    title: "macOS Brewfileの生成とCI分岐"
  - id: brew-bundle
    resource: "https://docs.brew.sh/Brew-Bundle-and-Brewfile"
    title: "Homebrew Bundle：既定upgrade・no-upgrade・lock非対応"
  - id: identity
    resource: "../dot_config/mise/repo-tasks/generate/executable_identity.tmpl"
    title: "identity入力の検証と世代切替"
  - id: security
    resource: "../dot_config/mise/repo-tasks/repair/executable_security.tmpl"
    title: "権限変更を行わない互換task"
  - id: completions
    resource: "../dot_config/mise/repo-tasks/generate/executable_completions.tmpl"
    title: "補完・initの個別検証と切替"
  - id: tasks
    resource: "https://github.com/tsubasahomma/dotfiles/tree/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks"
    title: "repo所有taskの実装"
  - id: repair-nvim
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/repair/executable_nvim.tmpl"
    title: "採用lockからのLazy restore"
  - id: lifecycle
    resource: "../dot_config/mise/repo-tasks/lifecycle/executable_post-apply.tmpl"
    title: "OS別post-apply依存graph"
  - id: update-nvim
    resource: "../dot_config/mise/repo-tasks/update/executable_lazy-lock.tmpl"
    title: "選択revisionからの隔離lock候補生成"
  - id: scripts
    resource: "https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/"
    title: "chezmoi scripts：onchangeの成功済み内容による再実行判定"
  - id: mise-tasks
    resource: "https://github.com/jdx/mise/blob/v2026.6.11/docs/tasks/running-tasks.md"
    title: "mise v2026.6.11：task省略と依存順序"
  - id: user
    resource: "Maintainer report in the repository OKF design conversation, 2026-11-11"
    title: "端末構築後にmise関連・brewを直接更新したとの利用者報告。実機観測ではない"
---
# 現行の所有境界を読む

ここでいう「所有」は、宣言の正本・実際に書く主体・変更してよい範囲を分けて考えるための言葉です。現在のtaskが触る範囲を、そのまま望ましい管理範囲とは認めません。操作の順序と副作用は[operations](operations.md)、変更したい境界は[convergence](decisions/convergence.md)で扱います。identityの入力schemaは[identity](identity.md)、toolやlockの更新作業は[development](development.md)を正本とします。

以下は2026-11-11のコードの静的観測です。基準HEADは`f4fe1fac3e0722b173b5291a06e98e1e066786f1`。固定HEADは観測の根拠であり、端末へ適用すべき版を指定するものではありません。実機の有効版・PATH・配置状態は未確認です。mise読込・明示導入の境界はR01の現行sourceに更新しており、固定HEAD時点の動作とは異なります。

R02ではidentity集合を取得・render時に検証し、不正入力を出力書込前に拒否する。空でないidentityのrenderは`ssh-keygen`へ公開鍵を標準入力で渡して検査する（認証・通信・file書込なし）。[入力契約](identity.md#routingと各出力の境界)と[隔離検証](validation.md#identity-boundary)を参照。R05の生成・空集合・所有照合・切替契約は[identity](identity.md#生成の切替と既存配置からの移行)を参照する。

# 状態・正本・書き込み主体

パスの`~`は対象ホストのhomeを表します。XDGの値は現行config templateでhome配下へ設定されます。[^config]

| 状態 | 現行の正本・入力 | 実際に書く主体と範囲 | 境界の注意 |
|---|---|---|---|
| mise本体 | `.mise-version`とbootstrap実装 | `.bootstrap-mise.sh --install`が不在時だけ`~/.local/bin/mise`へ導入 | 読込hookと引数なし呼出しは存在・実行属性のみ検査。既存の旧版・新版は保持し、明示導入でも版不一致・symlink・非通常fileを置換しない。PATH上のmiseとは別の実体になり得る[^bootstrap][^config] |
| chezmoiのホスト設定・identity入力 | `.chezmoi.toml.tmpl`、ホスト情報、1Password | config生成時に外部入力を取得し、chezmoi設定へ保持 | 1Passwordが入力の出所、生成済みconfigは取得時点の値。通常applyを毎回の再取得とみなさない[^config] |
| 静的設定・symlink・外部asset | source、ignore、remove、external定義 | chezmoiがtargetへ配置・削除・外部取得 | ignoreはchezmoiの境界。後段shell taskの書込権限を制限しない[^ignore][^remove][^externals] |
| miseで使うCLI/runtime | `dot_config/mise/conf.d/10-tools.toml`、動的config、実行時に読まれる他の設定 | post-applyのmise install、mise exec等 | 宣言・導入済み版・有効版・実行パスは別。repo宣言だけから端末の実行版を断定しない[^tools][^mise-config][^wrapper][^mise-install] |
| OS package・アプリ | `packages.yaml`、macOSは生成Brewfile | OS別before script → brew / Linux package manager / WinGet | repoの宣言一覧は端末全体の所有一覧ではない。brewは[不足導入と明示更新](operations.md#homebrew-packages)を分離。依存変更までは禁止しない[^packages][^brewfile][^brew-bundle] |
| Git identity includes・公開鍵・allowed_signers | config内のidentity入力と生成template | identity専用after入口 / generate:identity → XDG Git配下の固有`.identity-generation-*`と固定`identity.inc` | 新入力は新しい世代へ書き、manifestとentry照合後に参照を切替。所有照合済み世代の欠損は元の内容だけを復旧する（[R10a契約](identity.md#identity-convergence)）。before scriptは旧routing参照を保存する。旧identities・signers・SSH公開鍵と未知fileは変更・削除しない。旧世代の回収は行わない[^identity] |
| SSH秘密鍵・known_hosts | 利用者・SSH・認証システム側の状態 | chezmoiは鍵等を除外し、repair:securityは変更しない互換入口 | ファイル名から所有を推定しない。公開鍵とallowed_signersのmodeはgenerate:identityが出力時に設定する[^ignore][^security][^identity] |
| 補完・init・cache・styles・pbfile | tool宣言、補完定義、外部asset、Swiftソース | generate:completions、cache:bat、sync:vale、build:pbfile | `.cache/zsh`、`.cache/bat`、`.config/zsh/completions`のzwc、`.local/share/vale`、`.local/bin/pbfile`等。補完の切替対象は[個別出力と対応cache](operations.md#completion-generation)に限定。bat/Vale/pbfileの所有は[個別出力receipt](operations.md#generated-assets)に限定。cacheという分類だけで全内容を所有しない[^completions][^tasks] |
| login shell・pnpm設定 | provision task内の期待値 | `/etc/shells`とユーザーshellの変更、`pnpm config set global-bin-dir` | ホスト設定への変更。pnpmの設定保存先は実行環境に依存し、今回未確認[^tasks] |
| Windows側1Password / WezTerm設定 | WSLへ配置したagent.toml / wezterm.lua | 専用after_50 → 2個のsync taskが実LOCALAPPDATA / USERPROFILEへ同期 | target隣のreceipt・lockで前回bytesを照合。初回相違・手動編集・不明なpathは保持停止。同一既存fileだけ無書換で採用。限定契約は[操作](operations.md#windows-settings-sync)を参照 |
| Neovimのlock・plugins | repoのlockとNeovim設定 | repair:nvimはLazy restore、通常起動も初期化し得る。update:lazy-lockは選択local revisionから一時HOME/XDG内で候補・差分を生成し保持する | 通常source/branch/index/config/plugin/cacheへの反映と公開は別の明示操作。lazy.nvim実行版・build等の[更新範囲](development.md#neovimrestoreと更新を混同しない)を確認する。plugin復元は通常applyに含めない[^repair-nvim][^lifecycle][^update-nvim] |
| script実行履歴・taskの省略状態 | chezmoiの成功済みscript内容、miseのsources/outputs | 各ツールが再実行の要否を判断 | 出力の妥当性や1ファイル欠損の完全な検査とは別。履歴消去を一般的な修復手順にしない[^scripts][^mise-tasks] |

同じ領域に異なる所有者が混在します。例えば`.config/zsh/completions`の取得済み補完本体はchezmoi externalです。R07以降、生成taskはその隣の既存zwcには触れず、cache配下の明示した生成出力と対応zwcだけを切り替えます。`.ssh`のdirectory管理、利用者の鍵、旧生成公開鍵も同一の所有範囲ではありません。directoryごとの再帰削除で一括管理しない設計が必要ですが、まだ全出力の境界を実装した状態ではありません。[^externals][^completions][^ignore][^security]

# 旧パスと管理外ファイルの保持

R06では`repair:security`の再帰chmodを撤去し、`.chezmoiremove.tmpl`のパス名だけによる削除も全件停止した。docker-cliのinstall directory・shimに加え、旧Vale・補完・Neovim・Git設定・旧task・WSL bridgeの各パスも、現在の内容が旧管理状態であると確実に識別できないため保持する。旧ファイルが残ることは不要と判断した証拠ではない。自動の所有manifestや回収処理は導入していない。[^security][^remove]

旧状態を整理する場合は、対象の内容・導入元・現在の参照と利用意図を個別に確認してから採否を決める。この変更は過去の削除やmode変更を復元しない。source実装の境界であり、配置済みの古いrepair taskは更新するまで旧挙動を持つ。[操作上の注意](operations.md#ownership-preservation)と[検証範囲](validation.md#ownership-preservation)を参照。

# 手動更新されたmise・brew

端末はこのrepoで構築した後、mise関連のupgradeやbrew操作を直接行ったものがある、と利用者から共有されています。「mise関連」が本体・tool・設定のどれを含むか、実行版・導入元・手動追加packageは未調査です。これは利用者報告で、実機の観測ではありません。[^user]

| 区別する状態 | 確認する情報 | この情報だけでは決められないこと |
|---|---|---|
| mise本体 | 実体のパス、symlink、版、導入・更新を担当する仕組み | repoのpinが古いとも、最新の実機版が互換とも断定しない |
| miseが扱うtool | source宣言、target側config・local override、導入版、選択版、実行パス | install済みを利用中と同一視しない[^mise-install] |
| brew項目 | formula/cask/tap、導入済み項目、必要性、mise等との重複、利用パス | 未宣言を不要と決めない。同名でもWindowsとWSLなど実行環境が違えば重複とは限らない |
| 手動編集したtarget | sourceとの差分、編集目的、他の利用者・toolとの共有範囲 | 全ファイルの取り込みや上書きを自動で選ばない |

macOSのjust・atuin・duckdb・deno・AWS CLIは、2026-11-11の利用者決定でmiseを主担当とし、Homebrew側の宣言5件を除去した。既存brew実体のuninstall/cleanupは行わず、Windows native宣言も保持する。このプロセスのPATHでmiseが先、Homebrew receiptsに他formulaからのruntime依存なしという事前読取観測は、全consumerや対話shellでの選択の証明ではない。採用理由と代案は[Decision](decisions/convergence.md#manual-updates)を参照する。

# 今後の方針との境界

利用者は今後コード管理へ寄せる意向ですが、どの手動差分を取り込むかは未決です。差分ごとに「宣言へ採用」「理由を確認して宣言へ戻す」「管理外として保持」を選ぶ手順を[convergence](decisions/convergence.md)で提案しています。ここで示した現行の書込主体が、その選択を自動的に決めるわけではありません。[^user]

維持候補はsourceとtargetの区別、toolの明示的な要求、repo taskの分離、導入先の型検査です。読み取り時のmise差替えは分離済みです。未所有鍵へのchmodと旧パスの恒久削除は停止した。identity先行削除はR05で世代切替へ変更した。Windows設定の無条件copyはR14で2fileのreceipt照合へ変更した。OS/miseの担当整理は採用した範囲に限る。採否と理由・代案は[convergence](decisions/convergence.md)を正本とし、この文書に将来の成功保証を混ぜません。

[^config]: [identity入力・ホスト情報の取得とread-source-state hook](../.chezmoi.toml.tmpl).
[^bootstrap]: [mise本体の読込検査・明示導入](../.bootstrap-mise.sh).
[^ignore]: [chezmoiによる配置の除外](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiignore.tmpl).
[^remove]: [旧パスの恒久削除を停止したremove定義](../.chezmoiremove.tmpl).
[^externals]: [外部assetとrefresh指定](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiexternal.toml.tmpl).
[^tools]: [観測時のmise tool宣言](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/conf.d/10-tools.toml).
[^mise-config]: [mise task discovery・自動導入設定](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/config.toml.tmpl).
[^wrapper]: [post-applyの起動条件・mise install・認証の受け渡し](../.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl).
[^mise-install]: [mise v2026.6.11 install：導入と有効化は別](https://github.com/jdx/mise/blob/v2026.6.11/docs/cli/install.md).
[^packages]: [OS別packageの宣言](../.chezmoidata/packages.yaml).
[^brewfile]: [macOS Brewfileの生成とCI分岐](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/homebrew/Brewfile.tmpl).
[^brew-bundle]: [Homebrew Bundle：既定upgrade・no-upgrade・lock非対応](https://docs.brew.sh/Brew-Bundle-and-Brewfile).
[^identity]: [identityの検証・世代切替](../dot_config/mise/repo-tasks/generate/executable_identity.tmpl).
[^security]: [権限変更を行わない互換task](../dot_config/mise/repo-tasks/repair/executable_security.tmpl).
[^completions]: [補完・initの個別検証と切替](../dot_config/mise/repo-tasks/generate/executable_completions.tmpl).
[^tasks]: [repo所有taskの実装](https://github.com/tsubasahomma/dotfiles/tree/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks).
[^repair-nvim]: [採用lockからのLazy restore](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/repair/executable_nvim.tmpl).
[^lifecycle]: [OS別post-apply依存graph](../dot_config/mise/repo-tasks/lifecycle/executable_post-apply.tmpl).
[^update-nvim]: [選択revisionからの隔離lock候補生成](../dot_config/mise/repo-tasks/update/executable_lazy-lock.tmpl).
[^scripts]: [chezmoi scripts：onchangeの成功済み内容による再実行判定](https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/).
[^mise-tasks]: [mise v2026.6.11：task省略と依存順序](https://github.com/jdx/mise/blob/v2026.6.11/docs/tasks/running-tasks.md).
[^user]: 端末構築後にmise関連・brewを直接更新したとの利用者報告。実機観測ではない.


# R10b補完の依存とcache所有

補完・initは[専用after_30](../.chezmoiscripts/run_after_30-completions.sh.tmpl)が毎apply直接検査する。R07の個別source/zwc/dumpに加え、各出力の隠し`.<basename>.generation.json`を成功内容の照合用に生成する。未知schemaやsymlinkのreceiptは保持して停止する。これは外部fileを所有認定するmanifestではない。管理外cacheやSDKの変更・削除範囲を増やさず、入力として実体を読むだけである。[詳細契約](operations.md#completion-convergence)を参照。

<a id="windows-settings-sync"></a>
# Windows同期の所有範囲

利用者がrepo管理を選択した対象は`%USERPROFILE%/.wezterm.lua`と`%LOCALAPPDATA%/1Password/config/ssh/agent.toml`だけ。隣接する`<filename>.dotfiles-sync.json`はversion・kind・Windows destination・前回SHA256を持ち、`<filename>.dotfiles-sync.lock`は同じWindows targetを使うrepo writer間の排他用。Windows user環境全体・app本体・別探索先・旧誤path・未知fileは所有しない。receiptはidentity本文を含めない。

初回またはreceipt喪失時は、target欠損か現在の期待bytesと完全同一の場合だけ採用する。これは利用者決定と内容照合を根拠とし、旧copy実装やfile名を根拠にしない。有効receiptがあってtargetの前回hashと異なる場合は、新しい期待bytesと偶然同じでも停止する。receipt破損・別destination・symlink/reparse・hardlink・非通常fileは黙って初期化しない。具体的な失敗保持と移行手順は[operations](operations.md#windows-settings-sync)、判断理由は[Decision](decisions/convergence.md#windows-ownership)を正本とする。
