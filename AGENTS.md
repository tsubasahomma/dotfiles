---
type: Policy
title: このdotfilesで作業するエージェントへ
description: 変更と実機操作の境界を確認し、作業に必要な文書へ進む。
status: draft
generated:
  by: codex/gpt-6
  at: "2026-11-11T05:19:46+00:00"
---
# 作業の境界

このrepoはchezmoiのsource stateです。継続して再現したい変更はsourceへ反映します。実機への操作は依頼された対象範囲と、確認できた状態の所有境界に従って行います。

- 宣言と実機の一致を前提にしない。手動のmise・brew更新や管理外の状態を、未宣言という理由だけで巻き戻したり削除したりしない。
- 文書の確認だけを理由にbootstrap・apply・repair・doctorを実行しない。読み取りやdry-runという名前だけで非変更と判断せず、実行前に該当する操作の副作用を確認する。
- 秘密鍵・認証情報・生成identityの個人情報を文書や共有出力に載せない。
- 検査結果は実行した対象と環境の範囲で述べる。CI合格を実機のWSL・認証・正常動作の証拠に置き換えない。
- 現行コード、利用者からの報告、採用した方針、未実装の案を区別する。既存の判断も前提が崩れていれば見直し、推奨には一次資料と代案・不確実性を添える。

# 必要なときに読む

作業に関係する文書・節だけを開き、必要なコードと照合します。以下は全文の必読リストではありません。

| 作業 | 参照先 |
|---|---|
| 文書の作成・再編 | [OKFの構成と記述規約](docs/decisions/okf.md) |
| chezmoi・mise、bootstrap・apply・repairの調査や操作 | [状態の所有境界](docs/ownership.md)、[操作と副作用](docs/operations.md) |
| apply等の責務・成功条件の変更 | 上記に加え、[収束設計の判断](docs/decisions/convergence.md) |
| Git identity・SSH・1Password | [identityのデータ契約](docs/identity.md) |
| macOSまたはWSL固有の作業 | 該当する[macOS](docs/platforms/macos.md)または[WSL・Windows](docs/platforms/wsl.md) |
| 変更の検証・doctorの実行 | [検証の範囲](docs/validation.md)、実機コマンドは[操作と副作用](docs/operations.md)も確認 |
| ツール更新・CI・変更レビュー | [開発と更新](docs/development.md) |
