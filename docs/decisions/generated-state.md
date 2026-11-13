---
type: Decision
title: 生成物を専用ディレクトリ単位で所有し、作り直して直す
description: 生成物の配置・所有・復旧の方式を変えるときに、前提とする脅威、規則、受け入れたトレードオフと再検討条件を確認する。
status: stable
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-13T13:50:15+00:00"
sources:
  - id: maintainer
    resource: "Maintainer decision on the refactoring proposal, decision 1, 2026-11-13"
    title: "生成物の扱いを「簡素化する」"
  - id: measure
    resource: https://github.com/tsubasahomma/dotfiles/tree/79db166c1d9ec062c27c9b46f059561757efb215
    title: 行数の計測対象commit
  - id: chezmoi-scripts
    resource: https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/
    title: chezmoi — Use scripts to perform actions
  - id: chezmoi-order
    resource: https://www.chezmoi.io/reference/application-order/
    title: chezmoi — Application order
---
# 決定

生成物ごとの専用機構（receipt・lock・世代・manifest・rollback）をやめ、専用ディレクトリ単位の所有と再生成に置き換える。対象はbat cache、Vale styles、pbfile、補完、Windowsの設定同期、identityの生成部、Neovimのlock更新とrestore。利用者が2026-11-13に「簡素化する」と決めた。[^maintainer]

方針の決定であり、実装ではない。置き換えが入るまでは、現行コードと[収束設計の判断](convergence.md)の契約が動作の正本である。

# 前提とする脅威

利用者1人の端末を想定し、警戒する相手は供給網の側とする。同じHOMEの中でのsymlinkのすり替えや並行writerは対象にしない。

# 規則と保つもの

- 生成物は専用ディレクトリに閉じ込め、所有の単位はディレクトリとする。
- 作り直せるものにtransactionを求めない。欠損や不整合は作り直して直す。
- 専用ディレクトリの外へは書かない。Windowsの2設定のように外へ置く出力は、既存の相違があれば上書きせず停止する性質を残す。
- 「欠損したらapplyで直る」と「管理外の状態を壊さない」は保つ。
- 1Passwordの値をshell・Git・SSHの構文へ渡す前の入力検証は残す。identityの入力元はこの決定に含めない。

**受け入れるトレードオフ。** 生成中の強制終了や、手で置いた同名ファイルを検出せず、次のapplyでの作り直しで済ませる。

**予算（目安）。** 仕組みの行数は設定の行数以下、全検査は90秒以内。

# 根拠

**事実。** `79db166`で、端末に届く設定1,817行に対し、仕組みは4,121行、テストは5,204行だった（区分は計測者の分類）。[^measure] chezmoi公式はscriptを控えめに使うよう求め、実行中にsourceやdestinationが変わる場合の動作を未定義とする。[^chezmoi-scripts][^chezmoi-order] [収束設計の判断](convergence.md#進める順序と再検討条件)は、欠損検査の維持費が過大なら代案へ戻ると書いている。

**推論。** 守っている対象の多くは作り直せるcacheで、上の脅威の前提では専用機構の維持費が見合わない。再検討条件に当たる。

# 代案と再検討の条件

- 現行機構を通常のPythonパッケージへ移し、lintと型検査をかける。品質は上がるが、仕組みとテストの量は減らない。
- 現状維持。変更のたびに仕組み・stub・文書を直す負担が続く。

簡素化した生成が実機で実害を出したら、その生成物だけを元の方式へ戻す。

# 収束設計の判断との関係

[収束設計の判断](convergence.md)の採用済み範囲のうち、次を各生成物の実装時に置き換える。欠損復旧をapplyの成功条件に含める方向と、管理外の状態を保持する境界は置き換えない。

- identityの世代切替（固有世代・単一entry・before scriptでの旧routing保存）とmanifestによる復旧。入力検証は残す。
- 補完・initのreceiptによる収束と段階的な公開。
- bat・Vale・pbfileのreceipt・lock・限定publish・rollback。
- Windowsの2設定のreceipt・lock・rollback。既存相違での停止は残す。
- Neovimのlock更新とrestoreのadapter。

[^maintainer]: リファクタリング提案の判断1に対する利用者の決定。実装の細部や実機の状態を承認するものではない。
[^measure]: [計測対象のcommit](https://github.com/tsubasahomma/dotfiles/tree/79db166c1d9ec062c27c9b46f059561757efb215)。計測時点の値。
[^chezmoi-scripts]: [chezmoi: Use scripts to perform actions](https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/)。抜粋：「Scripts break chezmoi's declarative approach and should be used sparingly.」。閲覧日2026-11-13。
[^chezmoi-order]: [chezmoi: Application order](https://www.chezmoi.io/reference/application-order/)。閲覧日2026-11-13。
