---
type: Reference
title: 状態の正本と書き込み主体
description: 設定・生成物・手動管理状態について、現行の所有境界と未決の引受け範囲を確認する。
status: draft
generated:
  by: codex/gpt-6
  at: "2026-11-11T06:48:33+00:00"
sources:
  - id: config
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoi.toml.tmpl"
    title: "identity入力・ホスト情報の取得とread-source-state hook"
  - id: bootstrap
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.bootstrap-mise.sh"
    title: "mise本体の導入先検査・pinとの差替え"
  - id: ignore
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiignore.tmpl"
    title: "chezmoiによる配置の除外"
  - id: remove
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiremove.tmpl"
    title: "旧管理対象の除去指定"
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
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl"
    title: "post-applyの起動条件・mise install・認証の受け渡し"
  - id: mise-install
    resource: "https://github.com/jdx/mise/blob/v2026.6.11/docs/cli/install.md"
    title: "mise v2026.6.11 install：導入と有効化は別"
  - id: packages
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoidata/packages.yaml"
    title: "OS別packageの宣言"
  - id: brewfile
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/homebrew/Brewfile.tmpl"
    title: "macOS Brewfileの生成とCI分岐"
  - id: brew-bundle
    resource: "https://docs.brew.sh/Brew-Bundle-and-Brewfile"
    title: "Homebrew Bundle：既定upgrade・no-upgrade・lock非対応"
  - id: identity
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/generate/executable_identity.tmpl"
    title: "identity生成の先行削除と直接書き込み"
  - id: security
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/repair/executable_security.tmpl"
    title: "SSHファイルに対するchmod範囲"
  - id: completions
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/generate/executable_completions.tmpl"
    title: "補完生成・warn処理・cache削除"
  - id: tasks
    resource: "https://github.com/tsubasahomma/dotfiles/tree/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks"
    title: "repo所有taskの実装"
  - id: repair-nvim
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/repair/executable_nvim.tmpl"
    title: "採用lockからのLazy restore"
  - id: lifecycle
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/lifecycle/executable_post-apply.tmpl"
    title: "OS別post-apply依存graph"
  - id: update-nvim
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/update/executable_lazy-lock.tmpl"
    title: "Neovim更新・source反映・commit・push・PR"
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

以下は2026-11-11のコードの静的観測です。基準HEADは`f4fe1fac3e0722b173b5291a06e98e1e066786f1`。固定HEADは観測の根拠であり、端末へ適用すべき版を指定するものではありません。実機の有効版・PATH・配置状態は未確認です。

# 状態・正本・書き込み主体

パスの`~`は対象ホストのhomeを表します。XDGの値は現行config templateでhome配下へ設定されます。[^config]

| 状態 | 現行の正本・入力 | 実際に書く主体と範囲 | 境界の注意 |
|---|---|---|---|
| mise本体 | `.mise-version`とbootstrap実装 | read-source-state hook → `.bootstrap-mise.sh` → `~/.local/bin/mise` | PATH上のmiseとは別の実体になり得る。pinと異なれば新しい版も差替え対象。symlink・非通常ファイルは拒否する[^bootstrap][^config] |
| chezmoiのホスト設定・identity入力 | `.chezmoi.toml.tmpl`、ホスト情報、1Password | config生成時に外部入力を取得し、chezmoi設定へ保持 | 1Passwordが入力の出所、生成済みconfigは取得時点の値。通常applyを毎回の再取得とみなさない[^config] |
| 静的設定・symlink・外部asset | source、ignore、remove、external定義 | chezmoiがtargetへ配置・削除・外部取得 | ignoreはchezmoiの境界。後段shell taskの書込権限を制限しない[^ignore][^remove][^externals] |
| miseで使うCLI/runtime | `dot_config/mise/conf.d/10-tools.toml`、動的config、実行時に読まれる他の設定 | post-applyのmise install、mise exec等 | 宣言・導入済み版・有効版・実行パスは別。repo宣言だけから端末の実行版を断定しない[^tools][^mise-config][^wrapper][^mise-install] |
| OS package・アプリ | `packages.yaml`、macOSは生成Brewfile | OS別before script → brew / Linux package manager / WinGet | repoの宣言一覧は端末全体の所有一覧ではない。brewは導入時に更新も行い得る[^packages][^brewfile][^brew-bundle] |
| Git identity includes・公開鍵・allowed_signers | config内のidentity入力と生成template | generate:identity → `~/.config/git/identities`、`allowed_signers`、`~/.ssh/id_*.pub` | identities directoryを先に削除し、出力を直接書く。古い公開鍵の回収は見当たらない。生成物一式の原子的切替は保証されない[^identity] |
| SSH秘密鍵・known_hosts | 利用者・SSH・認証システム側の状態 | chezmoiは鍵等を除外する一方、repair:securityは`.ssh`以下の`id_*`通常ファイル（`.pub`除外）を再帰的にchmodする | 除外されていても現行taskからは変更され得る。鍵の内容を取得・再生成する処理ではない[^ignore][^security] |
| 補完・init・cache・styles・pbfile | tool宣言、補完定義、外部asset、Swiftソース | generate:completions、cache:bat、sync:vale、build:pbfile | `.cache/zsh`、`.cache/bat`、`.config/zsh/completions`のzwc、`.local/share/vale`、`.local/bin/pbfile`等。cacheという分類だけで全内容を所有しない[^completions][^tasks] |
| login shell・pnpm設定 | provision task内の期待値 | `/etc/shells`とユーザーshellの変更、`pnpm config set global-bin-dir` | ホスト設定への変更。pnpmの設定保存先は実行環境に依存し、今回未確認[^tasks] |
| Windows側1Password / WezTerm設定 | WSLへ配置したagent.toml / wezterm.lua | sync taskがWindows USERPROFILEを解決し、対象ファイルを`cp -f` | Windowsの直接編集も上書き対象。競合mergeはない。所有の引受け方は未決[^tasks] |
| Neovimのlock・plugins | repoのlockとNeovim設定 | repair:nvimはLazy restore、通常起動も初期化し得る。update:lazy-lockはlockをsourceへ取り込み、公開操作まで進む | restoreと版更新は別。plugin復元を通常applyが完了させる構成にはなっていない[^repair-nvim][^lifecycle][^update-nvim] |
| script実行履歴・taskの省略状態 | chezmoiの成功済みscript内容、miseのsources/outputs | 各ツールが再実行の要否を判断 | 出力の妥当性や1ファイル欠損の完全な検査とは別。履歴消去を一般的な修復手順にしない[^scripts][^mise-tasks] |

同じ領域に異なる所有者が混在します。例えば`.config/zsh/completions`の取得済み補完本体はchezmoi external、その隣のzwcは生成taskです。`.ssh`のdirectory管理、利用者の鍵、生成公開鍵も同一の所有範囲ではありません。directoryごとの再帰削除で一括管理しない設計が必要ですが、まだ全出力の境界を実装した状態ではありません。[^externals][^completions][^ignore][^security]

# 手動更新されたmise・brew

端末はこのrepoで構築した後、mise関連のupgradeやbrew操作を直接行ったものがある、と利用者から共有されています。「mise関連」が本体・tool・設定のどれを含むか、実行版・導入元・手動追加packageは未調査です。これは利用者報告で、実機の観測ではありません。[^user]

| 区別する状態 | 確認する情報 | この情報だけでは決められないこと |
|---|---|---|
| mise本体 | 実体のパス、symlink、版、導入・更新を担当する仕組み | repoのpinが古いとも、最新の実機版が互換とも断定しない |
| miseが扱うtool | source宣言、target側config・local override、導入版、選択版、実行パス | install済みを利用中と同一視しない[^mise-install] |
| brew項目 | formula/cask/tap、導入済み項目、必要性、mise等との重複、利用パス | 未宣言を不要と決めない。同名でもWindowsとWSLなど実行環境が違えば重複とは限らない |
| 手動編集したtarget | sourceとの差分、編集目的、他の利用者・toolとの共有範囲 | 全ファイルの取り込みや上書きを自動で選ばない |

macOSではjust・atuin・duckdb・deno・awscli等がmise側にもOS package側にも宣言されています。主担当を決める材料ですが、名前の重複だけを理由に片方を削除しません。実際のPATHと依存関係を確認してから判断します。[^packages][^tools]

# 今後の方針との境界

利用者は今後コード管理へ寄せる意向ですが、どの手動差分を取り込むかは未決です。差分ごとに「宣言へ採用」「理由を確認して宣言へ戻す」「管理外として保持」を選ぶ手順を[convergence](decisions/convergence.md)で提案しています。ここで示した現行の書込主体が、その選択を自動的に決めるわけではありません。[^user]

維持候補はsourceとtargetの区別、toolの明示的な要求、repo taskの分離、導入先の型検査です。見直し候補は読み取り時のmise差替え、未所有鍵へのchmod、identity先行削除、Windows設定の無条件copy、OS/miseの重複担当です。採否と理由・代案は[convergence](decisions/convergence.md)を正本とし、この文書に将来の成功保証を混ぜません。

[^config]: [identity入力・ホスト情報の取得とread-source-state hook](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoi.toml.tmpl).
[^bootstrap]: [mise本体の導入先検査・pinとの差替え](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.bootstrap-mise.sh).
[^ignore]: [chezmoiによる配置の除外](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiignore.tmpl).
[^remove]: [旧管理対象の除去指定](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiremove.tmpl).
[^externals]: [外部assetとrefresh指定](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiexternal.toml.tmpl).
[^tools]: [観測時のmise tool宣言](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/conf.d/10-tools.toml).
[^mise-config]: [mise task discovery・自動導入設定](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/config.toml.tmpl).
[^wrapper]: [post-applyの起動条件・mise install・認証の受け渡し](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl).
[^mise-install]: [mise v2026.6.11 install：導入と有効化は別](https://github.com/jdx/mise/blob/v2026.6.11/docs/cli/install.md).
[^packages]: [OS別packageの宣言](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoidata/packages.yaml).
[^brewfile]: [macOS Brewfileの生成とCI分岐](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/homebrew/Brewfile.tmpl).
[^brew-bundle]: [Homebrew Bundle：既定upgrade・no-upgrade・lock非対応](https://docs.brew.sh/Brew-Bundle-and-Brewfile).
[^identity]: [identity生成の先行削除と直接書き込み](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/generate/executable_identity.tmpl).
[^security]: [SSHファイルに対するchmod範囲](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/repair/executable_security.tmpl).
[^completions]: [補完生成・warn処理・cache削除](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/generate/executable_completions.tmpl).
[^tasks]: [repo所有taskの実装](https://github.com/tsubasahomma/dotfiles/tree/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks).
[^repair-nvim]: [採用lockからのLazy restore](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/repair/executable_nvim.tmpl).
[^lifecycle]: [OS別post-apply依存graph](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/lifecycle/executable_post-apply.tmpl).
[^update-nvim]: [Neovim更新・source反映・commit・push・PR](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/update/executable_lazy-lock.tmpl).
[^scripts]: [chezmoi scripts：onchangeの成功済み内容による再実行判定](https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/).
[^mise-tasks]: [mise v2026.6.11：task省略と依存順序](https://github.com/jdx/mise/blob/v2026.6.11/docs/tasks/running-tasks.md).
[^user]: 端末構築後にmise関連・brewを直接更新したとの利用者報告。実機観測ではない.
