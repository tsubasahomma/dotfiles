---
type: Decision
title: リポジトリ全体を一つのOKF bundleにする
description: 文書の配置・読み分け・最小メタデータを変更するときに、判断理由と代案を確認する。
status: draft
generated:
  by: codex/gpt-6
  at: "2026-11-11T06:48:33+00:00"
sources:
  - id: maintainer
    resource: "Maintainer direction in the repository OKF design conversation, 2026-11-11"
    title: "One repository-wide bundle; retire PR template; keep model provenance; temporary drafts only"
  - id: okf
    resource: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
    title: Open Knowledge Format v0.2
  - id: agents
    resource: https://learn.chatgpt.com/docs/agent-configuration/agents-md
    title: OpenAI — Custom instructions with AGENTS.md
  - id: context
    resource: https://www.anthropic.com/research/effective-context-engineering-for-ai-agents
    title: Anthropic — Effective context engineering for AI agents, 2025-09-29
  - id: agents-study
    resource: https://arxiv.org/abs/2602.11988v3
    title: Evaluating AGENTS.md, v3, 2026-09-29
  - id: hooks
    resource: https://www.chezmoi.io/reference/configuration-file/hooks/
    title: chezmoi — Hooks
  - id: repo-hook
    resource: https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoi.toml.tmpl#L203
    title: Observed read-source-state hook
  - id: repo-bootstrap
    resource: https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.bootstrap-mise.sh#L46
    title: Observed mise bootstrap implementation
---
# 判断と反映状況

repo全体を一つのOKF bundleにし、PRテンプレートを廃止する。共通契約の上流同期を終了し、重要な知識だけを救出してrepo固有の文書へ書き直す方針も維持する。既存の文書構成は保存要件にしない。[^maintainer]

この文書は文書構成と記述規約を定める。bootstrap・apply等の実装変更は別の判断であり、文書の移行や`status`を実装完了・実機検証の証拠にはしない。

# Bundleの境界と読み方

対象はversion管理されたリポジトリの木全体。残すMarkdownには、rootのREADME・AGENTSと、隠しdirectory内の文書や使用するvendor入口も含める。`docs/`・`docs/platforms/`・`docs/decisions/`は同じbundle内の通常のsubdirectoryとし、独立したbundleにはしない。`.git`内部や未追跡の端末cacheを文書として取り込まない。[^okf]

bundleの範囲は、エージェントが毎回読む範囲ではない。AGENTSを認識する実行環境では、その入口に常時必要な制約と直接の参照先を置く。CodexにはAGENTSの探索規則があるが、OKFの`type`や`status`で指示の読込を制御できるとは想定しない。`status: draft`も指示の無効化にはならない。[^agents]

| 文書 | 役割 | 開く場面 |
|---|---|---|
| [AGENTS.md](../../AGENTS.md) | Policy。依頼範囲、実機への副作用、秘密、証拠の扱いと作業別リンク | エージェントの作業入口。設計理由や手順全文は置かない |
| [README.md](../../README.md) | Guide。目的・対象環境と人間向けの行き先 | このrepoを知る、導入・操作・変更の文書を探す |
| [ownership](../ownership.md) | Reference。正本・書込主体・管理外の境界 | 設定、生成物、手動更新を扱う |
| [operations](../operations.md) | Playbook。現行の前提・手順・副作用・結果の確認 | bootstrap・apply・repair・doctorを調べる、実行する |
| [identity](../identity.md) | Reference。1Password・Git・SSHのデータ契約 | 入力や認証経路を変更・調査する |
| [validation](../validation.md) | Playbook。変更対象ごとの検査と証拠の限界 | 何を確認し、どこまで保証できるか判断する |
| [development](../development.md) | Guide。ツール更新、CI、変更レビューの注意 | repoを変更する。PRの説明もここに短く記す |
| [macOS](../platforms/macos.md) / [WSL・Windows](../platforms/wsl.md) | Guide。環境固有の前提と操作境界 | 該当する環境の作業だけで参照する |
| この文書 | Decision。OKFの規約・理由・代案 | 文書を作成・再編する |
| [convergence](convergence.md) | Decision。収束設計の案、判断理由、未決事項 | 責務・所有境界・成功条件を見直す |

AGENTSから上の知識へ直接進めるようにし、全員にREADMEや全docsの通読を求めない。nested AGENTSや各階層の索引も初期構成には追加しない。人間も操作時の危険を見落とさないよう、READMEに限り短い副作用の注意を再掲する。詳細な所有・手順・設計理由は各文書を正本とする。

常時文脈を小さくし必要時に情報を取る方針は、Anthropicのcontext engineeringの実践を参考にした。AGENTS.md評価研究も、説明や制約の追加が一律に性能を改善するという前提を支持しない。ただし、この11文書の配置や今回のモデルへの効果が実証されたわけではない。作業で必要な知識へ到達できるかを見て調整する。[^context][^agents-study]

# 現行の知識と変更案を混ぜない

operationsには現在のコードで実行できる手順と限界を書く。管理対象生成物の欠損復旧をapplyの成功条件へ含める案は、convergenceで扱う。採用判断と実装・検証の完了は別々に記す。

AGENTSとREADMEに残した副作用の注意には具体的な根拠がある。現行コードはsource state読込前にmiseのbootstrapを起動し、その処理は宣言版との不一致でmiseを置き換え得る。chezmoiはdry-runでもhookを実行する。通常の確認コマンドだから安全とする判断を避けるため、この注意だけは入口にも置く。これは現状を維持すべきという決定ではない。[^repo-hook][^repo-bootstrap][^hooks]

利用者が報告した端末状態は、実機を確認した観測と区別する。提案を繰り返し記載しても採用済みにはしない。判断が変わったら本文・代案・実装予定を書き直し、古い版はGit履歴に残す。会話を追記し続ける台帳は作らない。

# 最小メタデータ

OKF v0.2を対象にする。標準の常時必須項目は`type`だけだが、このrepoでは通常Markdownに次の5項目を置く。`generated`の必須化は利用者の指定である。[^okf][^maintainer]

| 項目 | このrepoでの使い方 |
|---|---|
| `type` | Guide / Policy / Reference / Playbook / Decisionで文書の役割を表す |
| `title` | 内容が分かる名前 |
| `description` | どの作業で読むかが分かる一文 |
| `status` | draft / stable / deprecatedを明示。文書の扱いであり、実装状態や操作許可ではない |
| `generated` | `by`に実際の執筆主体・モデル、`at`に意味のある最終編集時刻を記録 |

`generated.by`の`codex/gpt-6`は開示されたモデル系列であり、正確な配備snapshot IDではない。判明していないモデル名・版を補わない。後の改訂ではその改訂を行った主体を記録し、過去の版はGitで辿る。人間が執筆した場合はOKFの`human:<id>`形式を使う。救出した旧文書の初稿モデルを、現在の執筆モデルと同一視しない。[^okf]

必要なときだけ、次の項目を加える。[^okf]

- `tags`：複数の文書を横断して探す用途がある場合。
- `sources`：判断を支える公式資料、コード、利用者の決定。主張ごとの脚注IDと`sources[].id`を対応させる。
- `resource`：文書が説明する特定の資産がある場合。参考文献の一覧は`sources[].resource`に置く。
- `verified`：内容を実際に確認した場合だけ。確認対象・方法・限界も本文に残す。本文執筆やYAML検査だけで内容を確認済みにしない。

`audience`・`priority`・`must_read`・独自のversion等は追加しない。現在の役割分担とリンクで足りない具体的な用途が生じたら検討する。常時読まれるAGENTSには研究紹介や大きな出典一覧を置かず、その判断理由をこの文書に集める。

# リンク・履歴・移行

通常のREADMEを人間向けの索引として使い、任意の`index.md`と`log.md`は作らない。更新差分はGit、現在の理由と代案はDecisionで辿る。repo内リンクは相対パスを使い、移動時に参照元も更新する。[^okf]

PRテンプレートは廃止する。変更内容・検証結果・残る制約を簡潔に説明するという用途はdevelopmentに残し、固定のチェック表は移植しない。共通契約を上流installerで上書きする運用と、Repomixを必須とする文書・設定を退役させる。repo内に同期jobは見当たらず、repo外で設定された同期の有無は未確認。Repomixのtool宣言の削除は別の依存整理として残す。[^maintainer]

既存文書からは、コードと照合できる所有境界、identity schema、環境固有の前提、副作用、検証範囲、判断理由を救出する。汎用契約の重複、未記入のpolicy表、固定の多段承認・全検査手順は移植しない。既存の[Claude](../../CLAUDE.md)・[Gemini](../../GEMINI.md)・[Copilot](../../.github/copilot-instructions.md)入口は、利用実態が未確認のため互換用の薄い案内として残す。独自の規約を追加しない。実際のconsumerによるfrontmatter・参照の読込は未検証であり、使わない入口は利用実態を確認して削除できる。

参照先の本文が揃ってから入口を切り替える。旧文書を外すときは非Markdown設定の参照とchezmoiの除外設定も確認する。参照先が揃わない途中の文書だけを先にrepoへ適用しない。文書整理に実機apply・repairは伴わせない。

# 代案と再検討する条件

| 代案 | 今回選ばない理由 | 再検討する条件 |
|---|---|---|
| docsだけをbundleにする | 利用者がrepo全体を一つにすると決定した | 使用するconsumerにMarkdown frontmatterとの実際の非互換が判明した |
| 領域ごとに複数bundleにする | 独立した所有・配布の必要がまだない | 別repoへの再利用や別々の更新周期が必要になった |
| AGENTSに手順も集約する | 無関係な作業にも手順が入り、知識との二重管理になる | 常時知るべき制約の見落としが具体的な作業で発生した場合、その制約だけ追加する |
| index/logを追加する | 現在はREADMEとGitで必要な入口・履歴を持てる | 対象consumerが索引を必要とする、またはGit外の配布で履歴が必要になった |
| PRテンプレートを維持する | 廃止が選ばれた。OKFの形式統一だけを削除理由にはしない | 自由記述で繰り返し欠ける情報が生じ、テンプレートで改善できる根拠が得られた |

この判断を固定化するための新しい承認フローは設けない。構造の検査に加え、文書だけの修正、手動mise更新後のapply相談、生成物欠損、WSL認証の調査を題材に、必要な情報へ進めるか・未実装案を保証と誤読しないかを確かめる。実行しない読み合わせと、実機を使った検証の結果は区別する。

[^maintainer]: 2026-11-11の文書再編相談で明示された方針。実機の状態や全本文の承認を証明するものではない。
[^okf]: [Open Knowledge Format SPEC v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md)。閲覧日2026-11-11。
[^agents]: [OpenAI: Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。Codexの仕様を他の実行環境へ外挿しない。
[^context]: [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)。特定の文書構成の比較試験ではない。
[^agents-study]: [Evaluating AGENTS.md v3](https://arxiv.org/abs/2602.11988v3)。対象repo・モデル・taskを限定した研究であり、このdotfilesへの効果量は不明。
[^hooks]: [chezmoi: Hooks](https://www.chezmoi.io/reference/configuration-file/hooks/)。
[^repo-hook]: [read-source-state hook](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoi.toml.tmpl#L203)。観測時の固定HEAD。
[^repo-bootstrap]: [mise bootstrap](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.bootstrap-mise.sh#L46)。観測時の固定HEAD。
