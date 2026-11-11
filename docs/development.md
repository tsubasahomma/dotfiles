---
type: Guide
title: sourceの変更・ツール更新・レビュー
description: 設定や依存を変更するときに正本、更新taskの副作用、必要なレビュー情報を確認する。
status: draft
generated:
  by: codex/gpt-6
  at: "2026-11-11T07:15:07+00:00"
sources:
  - id: pin
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.mise-version"
    title: "bootstrapが採用するmise本体版"
  - id: bootstrap
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.bootstrap-mise.sh"
    title: "mise本体のpin差替え"
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
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/repair/executable_nvim.tmpl"
    title: "採用lockによるLazy restore"
  - id: update-nvim
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/update/executable_lazy-lock.tmpl"
    title: "Neovim更新からcommit・push・PRまで"
  - id: wrapper
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl"
    title: "post-apply wrapperのhash入力と起動条件"
  - id: scripts
    resource: "https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/"
    title: "chezmoi公式：render後のscript内容によるonchange判定"
  - id: renovate
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/renovate.json5"
    title: "Renovateのmanagerと更新単位"
  - id: ci
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.github/workflows/compliance.yml"
    title: "CIの対象・実行段階・validator版"
  - id: user
    resource: "Maintainer decisions in the repository OKF design conversation, 2026-11-11"
    title: "単一bundle、PR template廃止、上流同期終了・Repomix退役の方向。文書移行の方針。実機操作は別"
---
# 変更する場所を決める

継続して再現したい変更はchezmoiのsource stateへ反映する。生成済みのtargetを直しただけで管理完了とはしない。一方、手動更新された実機をsourceに合わせて直ちに戻すこともしない。正本とwriterの一覧は[ownership](ownership.md)、実機への反映は[operations](operations.md)を参照する。

この文書の「現行」は2026-11-11のsource静的観測であり、更新taskやCIを実行した結果ではない。固定HEADは観測の根拠であり、そのまま採用すべき版とは扱わない。更新方式の変更は、以下の現行説明とは別の案として扱う。

# 宣言と更新単位

| 変更したいもの | 現行の主なsource | 先に確認する境界 |
|---|---|---|
| mise本体の採用版 | `.mise-version`と`.bootstrap-mise.sh` | 読込hookで固定pathの本体が置換され得る。tool要求やbrew導入のmiseとは別に扱う |
| repo内および端末のtool要求 | `.mise.toml`、`dot_config/mise/conf.d/10-tools.toml`等 | どのconfigが有効か、PATH上の実体とinstall済み版を分ける。version要求の編集とupgrade実行を同じものとしない |
| OS package・GUI app | `.chezmoidata/packages.yaml`、Brewfile template、OS別script | Homebrew・Linux・WinGet・miseで同名toolが重なる場合、どれを使うかを先に決める |
| 生成・修復・検査の処理 | `dot_config/mise/repo-tasks/**`、chezmoi script/hook | source/output指定・task依存・実行順・skip条件と、実際の書込先を一緒に確認する |
| Neovim pluginの採用状態 | `dot_config/nvim/lazy-lock.json`とNeovim設定 | 既定lockへのrestoreか、lockを更新する作業かを分ける |
| 文書・入口 | [OKF Decision](decisions/okf.md)の11文書構成 | 常時ルールをAGENTSへ増やす前に、必要時知識の正本で足りるかを見る |

最初の三行は現在の宣言位置の説明であり、現行の重複所有を維持する決定ではない。手動mise・brew更新を採用宣言へ取り込む手順案は[convergence](decisions/convergence.md)に集める。端末ごとの採用／戻す／管理外の分類はまだ済んでいない。[^pin][^bootstrap][^mise-root][^tools][^packages]

# Neovim：restoreと更新を混同しない

`repair:nvim`は採用lockに基づく`Lazy restore`を実行する。plugin directoryやcacheに書き込み、必要なら取得を伴うため、検査ではなく修復操作として扱う。source lock自体を新しい版へ更新する目的ではない。[^repair-nvim]

`update:lazy-lock`は名前以上に広い副作用を持つ。clean worktreeとGitHub認証を要求し、originのdefault branchを取得して作業branchへ切り替え、headlessの`Lazy update`、`chezmoi add`、commit、push、PR作成まで行う。更新なしの経路はbranchを戻して削除するが、全段階をtransactionとしてrollbackする実装ではない。単に更新差分を見たい作業で無条件に起動しない。[^update-nvim]

PR本文はtask内のhere-documentから作られており、PR templateを廃止しても消えない。生成本文もこのrepoの説明方針に合わせ、更新内容と未確認の互換性、検査・復元の参照を記す。現行taskのbranch命名やPR生成方式を、この文書で新しい一般規約として採用しない。更新と公開を分ける案は検討候補で、まだ実装していない。[^update-nvim]

# RenovateとCIの現行

Renovateはrootの`.mise.toml`と`dot_config/mise/conf.d/*.toml`をnative mise managerで扱い、`.mise-version`にはmise release向けのcustom regexを使う。依存のcategory付与と、一つのPRへgroup化することは別である。現行ではchezmoiの複数宣言をまとめるgroupがある一方、各分類が一律にgroup化される設定ではない。pnpm・npm tool・GitHub Actions等も各ruleの範囲を確認する。[^renovate]

Renovate validatorの版はCI workflow、Nodeの要求はworkflowが読むtool宣言を正本にする。変更時のcommandと結果の限界は[validation](validation.md)を参照する。workflowで指定したつもりのruntimeと、実際の`node --version`は分けて記録する。現行CIがUbuntu/macOSで合格しても、WSL・Windows・実認証の成功とはしない。[^ci]

# 採用済みの文書方針と移行時の確認

repo全体を一つのOKF bundleにすること、PR templateを廃止することは利用者の決定である。共通契約の上流同期を終了し、Repomixを必須とする経路を退役する。旧文書を保存するための同型移植や、新しいpacking手順は作らない。[^user]

入口や文書を変更するときは、[chezmoi除外](../.chezmoiignore.tmpl)、[Issue Form](../.github/ISSUE_TEMPLATE/change-request.yml)、[task内の生成PR本文](../dot_config/mise/repo-tasks/update/executable_lazy-lock.tmpl)も確認する。Issue Formは問題・範囲・確認方法・参照の短い入力を残す。Repomix設定は撤去し、既存生成packのignoreは誤配置・誤追跡を避けるため維持する。`npm:repomix`のtool宣言は別の依存整理で退役する。[^tools]

生成PR本文の編集は、次回applyで配置される更新taskと、そのtaskが将来生成するPR本文を変える。一方、現行wrapperのhash入力にこの更新taskは含まれず、この編集単独では`run_onchange_`の入力は変わらない。chezmoiの再実行判定はrender後のscript内容に基づくため、配置fileの変更とlifecycleの再実行条件は分けて考える。これはsourceの静的確認であり、read hookや他の入力変化によるapply自体の副作用がなくなるという意味ではない。実機への反映時は[operations](operations.md)で起動範囲を確認する。[^wrapper][^scripts]

文書確認ではsourceと出典を読み、実機コマンドを検査の名目で起動しない。bootstrap・apply・repairの意味を変える実装は、[convergence](decisions/convergence.md)の対象と成功条件を具体化してから行う。旧文書の削除と実機の掃除・resetを結びつけない。

# 変更をレビュー可能にする

変更説明は、何が問題でどう変わるか、確認した対象と結果、未確認の範囲・運用上の影響を必要な長さで記す。実行したCIの状態はそのrun/checkへの参照で示し、固定のPR本文へ結果を転記し続けない。親子Issueや大きなチェック表を、変更の大小に関係なく必須にする案は採らない。検査の選択は[validation](validation.md)に任せる。

PR templateの廃止理由と再検討条件は[OKF Decision](decisions/okf.md)を正本とする。

[^pin]: [bootstrapが採用するmise本体版](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.mise-version)。
[^bootstrap]: [mise本体のpin差替え](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.bootstrap-mise.sh)。
[^mise-root]: [repo内tool要求](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.mise.toml)。
[^tools]: [観測時のmise tool宣言](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/conf.d/10-tools.toml)。
[^packages]: [OS別package宣言](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoidata/packages.yaml)。
[^repair-nvim]: [採用lockによるLazy restore](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/repair/executable_nvim.tmpl)。
[^update-nvim]: [Neovim更新からcommit・push・PRまで](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/update/executable_lazy-lock.tmpl)。
[^wrapper]: [post-apply wrapperのhash入力と起動条件](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl)。
[^scripts]: [chezmoi公式：render後のscript内容によるonchange判定](https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/)。
[^renovate]: [Renovateのmanagerと更新単位](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/renovate.json5)。
[^ci]: [CIの対象・実行段階・validator版](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.github/workflows/compliance.yml)。
[^user]: 単一bundle、PR template廃止、上流同期終了・Repomix退役の方向。文書移行の方針。実機操作は別。
