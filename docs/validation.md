---
type: Playbook
title: 変更に応じた検証と結果の限界
description: 文書・template・tool更新・認証の変更に対して、必要な検査と副作用を選ぶ。
status: draft
generated:
  by: codex/gpt-6
  at: "2026-11-11T06:41:10+00:00"
sources:
  - id: evals
    resource: "https://www.anthropic.com/research/demystifying-evals-for-ai-agents"
    title: "Anthropic, 2026-01-09：結果状態と評価範囲"
  - id: doctor
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/doctor/executable__default.tmpl"
    title: "doctorの検査集合とCI分岐"
  - id: checks
    resource: "https://github.com/tsubasahomma/dotfiles/tree/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/check"
    title: "現行check taskの集合"
  - id: hooks
    resource: "https://www.chezmoi.io/reference/configuration-file/hooks/"
    title: "chezmoi公式：dry-runでもhookが動く"
  - id: wsl-check
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/check/executable_wsl-openssh.tmpl"
    title: "WSL認証・通信・一時署名probe"
  - id: precommit
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.pre-commit-config.yaml"
    title: "変更を伴う整形hookと対象filter"
  - id: precommit-docs
    resource: "https://pre-commit.com/"
    title: "pre-commit公式：対象指定とhook環境の導入"
  - id: ci
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.github/workflows/compliance.yml"
    title: "CIの対象・実行段階・validator版"
  - id: renovate-docs
    resource: "https://docs.renovatebot.com/config-validation/"
    title: "Renovate公式：repository configの検証とstrict mode"
---
# 検証を選ぶ

検査は変更した対象と期待する結果に合わせて選ぶ。文書の修正に実機doctorを要求しない。以下のcommandは現行コードを説明するためのもので、この文書を読むだけで一括実行する手順ではない。[operations](operations.md)で前提と書込範囲を確認する。

「現行」は2026-11-11のsource静的観測である。この文案作成では各task・CI・render・実機probeを実行していない。文書検査と実機動作の証拠は分ける。

| 変更対象 | まず確かめること | 必要な場合に追加する検査 |
|---|---|---|
| Markdownだけ | [OKF規約](decisions/okf.md)のfrontmatter、相対リンク、参照先、現行と案の区別、差分と`git diff --check` | 読者の作業例で必要な情報へ到達できるかを読む。関連しないdoctor・Renovate・Repomixは要件にしない |
| chezmoi template・hook・task | sourceだけでなく対象OS/CI分岐のrender結果と起動順・変更先 | 影響する構文検査、対象を絞ったtask、結果fileと保持対象の確認。実機を使う前に入力を管理した隔離環境で扱う |
| identity・Git・SSH | [identity](identity.md)の入力schema、生成先、routing、署名と認証の別 | 対象identityごとの有効Git設定、必要な認証・署名probe。[WSL](platforms/wsl.md)ならWindows側経路も区別する |
| mise/tool・Neovim | [ownership](ownership.md)の正本、採用版、実行実体、生成物 | 変更したtoolの起動、該当check、再適用・欠損復旧・保持対象。現行doctor一回で代用しない |
| package・OS統合 | 対象OSの宣言、更新やcopyの副作用 | 該当hostで存在・実体・利用可能性を確認。CIの省略分を実機成功と扱わない |
| Renovate / CI | 設定、runtime、対象job、変更した分岐 | 以下のvalidator経路と該当CI結果。全実機への外挿をしない |

この選び方はrepo向けの文案であり、現在の旧文書が要求する全検査の移植ではない。成功をcommandの終了だけでなく結果状態で評価する考え方は、Anthropicのagent評価の解説を参考にした。このdotfilesの検査一覧の有効性が研究で実証されたわけではない。[^evals]

# 現行のcheckと保証しない範囲

`mise run doctor`は下表のcheckを束ねる。常にsecurity・identity・nvim・vale・toolchainを含み、非CIではnpm-backend・hubspot・completionを追加する。`check:wsl-openssh`はdoctorに含まれない。[^doctor]

| check | 主に調べるもの | 成功・警告の限界 |
|---|---|---|
| `check:security` | `.ssh`とXDG stateのSSH directoryのmode 0700 | 欠損directoryはwarnしてskip。すべての鍵やfile権限の検査ではない |
| `check:identity` | op認証、生成configのemail、WSL command形状・環境、agent応答 | identityなしはwarn。CI用の省略もある。全repositoryのincludeIf選択、全鍵の認証・署名を試さない |
| `check:nvim` | lock存在とchezmoi verify、headless起動、provider | nvim欠損時はwarn/skip。通常configの起動でlazy導入が起こり得る。verifyもchezmoi hookの影響を受ける |
| `check:vale` | Vale configを読めることとGoogle style directoryの存在 | Markdown本文のlintでも、全style fileの健全性検査でもない |
| `check:toolchain` | 固定pathのmiseとpinの整合、usage補完probe、PATHの一部 | 全toolの採用版や全command実体は調べない。temp fileを書き、PATH判定にはwarnがある |
| `check:npm-backend` | `npm:@hubspot/cli`の宣言・install directory・package.json | npm tool全体の検査ではない |
| `check:hubspot` | 上記の配置と`hs --version` | HubSpot accountやSaaS側の状態は確認しない |
| `check:completion` | HubSpot completionの生成probeとzshでの読込 | temp fileを作る。cacheの`_hs`欠損はwarn。全補完fileの欠損検出ではない |

いずれも現行task本文から読める範囲である。exit 0でもwarn・skip・対象外が残り得る。miseの自動導入設定、アプリの通常起動、chezmoiのread hookを経由するため、doctor全体を非変更検査とは呼ばない。[^checks][^doctor][^hooks]

# WSL OpenSSH probeを使う前に

`mise run check:wsl-openssh`は非WSLではskipする。WSLではinterop、Windows SSH command、pipe形状、agent鍵一覧、GitHub SSH認証を調べる。さらに、最初のidentity configを使ってGit remoteを参照し、一時Git repositoryで署名付きcommitを作り、その署名表示を確認する。[^wsl-check]

| 操作 | 副作用・範囲 |
|---|---|
| `ssh.exe -T git@github.com` | 外部通信・認証。Windows側known_hostsの更新や認証promptが起こり得る |
| `git ls-remote` | 認証を伴うremote参照。既定の対象はこのrepo。`DOTFILES_WSL_OPENSSH_AUTH_TARGET`で変更できるが、前段のGitHub probeは残る |
| 一時repositoryで`git commit -S` | temp file・Git履歴の作成と署名helper/agentの呼出し。実repoへのcommitではない |
| 最初のconfigを選ぶ | 全identity、Git directory routing、他hostの認証成功は保証しない |

一時領域のcleanupがあっても、外部通信やWindows側の状態まで非変更になるわけではない。timeout utilityがなければ時間制限なしで進む箇所もある。このtaskを静的棚卸しや汎用doctorの代わりに実行しない。認証経路は[WSL文書](platforms/wsl.md)で切り分ける。[^wsl-check]

# 整形・Renovate・CI

現行pre-commitには末尾空白・最終改行の修正、YAML/大file検査、`shfmt -w`、StyLuaがある。local hookは`language: system`で実行pathに依存する。拡張子filterはtemplateを包括的には扱わず、専用のOKF frontmatter検査・Markdownリンク検査も定義されていない。初回実行ではhook環境の取得・導入もあり得る。必要なhookとfileを選び、変更された差分を確認する。`pre-commit run --all-files`を非変更検査と呼ばない。[^precommit][^precommit-docs]

Renovateを変更する場合は、repo rootでCIと同じvalidator版・Node runtimeを使う。版の正本はworkflowの`RENOVATE_VERSION`と参照先のtool宣言とし、この文書に別の固定版を増やさない。以下はその版を環境変数へ設定した後の現行相当の検査であり、`npx`は取得・cache書込を伴い得る。[^ci]

```sh
test -f renovate.json5
node --version
npx --version
npx --yes --package "renovate@${RENOVATE_VERSION:?CIと同じ版を設定}" -- renovate-config-validator --version
npx --yes --package "renovate@${RENOVATE_VERSION:?CIと同じ版を設定}" -- renovate-config-validator --strict
```

位置引数なしでrepositoryの既定場所を検査する。file名だけを位置引数に加えるとglobal configとして扱われるため、安易に同等のcommandへ書き換えない。`--strict`はmigrationの警告も失敗にする。validator合格は、botが全依存を抽出し望むPRを作ることの検証ではない。[^renovate-docs]

現行CIの収束jobはUbuntu/macOSで、古いmiseのfixture、bootstrap、tool install、CI用init/apply、activation guard、verify、Neovim repair、doctorを扱う。二回目のapplyによる無変更性や生成物欠損からの復旧、実1Password、Windows/WSL、GUI状態の証拠ではない。workflowを読んだことと、対象commitのrunが合格したことも区別する。[^ci]

# 結果を残す／まだ実装しないこと

検査結果には、対象commit・変更範囲、環境、行った操作、実際の結果、skip/warnと残る限界を短く記す。認証関連では秘密や個人情報を残さず、不一致の種類や件数を記録する。固定の大きなチェック表は要求しない。

非変更doctor、必須生成物の欠損を失敗にする検査、同じ入力での再適用と保護対象の比較は[convergence](decisions/convergence.md)の未実装案である。doctorの代案比較も同Decisionで扱う。文書の構造検査を実機成功の代替にしない。

[^evals]: [Anthropic, 2026-01-09：結果状態と評価範囲](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)。
[^doctor]: [doctorの検査集合とCI分岐](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/doctor/executable__default.tmpl)。
[^checks]: [現行check taskの集合](https://github.com/tsubasahomma/dotfiles/tree/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/check)。
[^hooks]: [chezmoi公式：dry-runでもhookが動く](https://www.chezmoi.io/reference/configuration-file/hooks/)。
[^wsl-check]: [WSL認証・通信・一時署名probe](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/check/executable_wsl-openssh.tmpl)。
[^precommit]: [変更を伴う整形hookと対象filter](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.pre-commit-config.yaml)。
[^precommit-docs]: [pre-commit公式：対象指定とhook環境の導入](https://pre-commit.com/)。
[^ci]: [CIの対象・実行段階・validator版](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.github/workflows/compliance.yml)。
[^renovate-docs]: [Renovate公式：repository configの検証とstrict mode](https://docs.renovatebot.com/config-validation/)。
