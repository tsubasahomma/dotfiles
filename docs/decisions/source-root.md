---
type: Decision
title: source stateをhome/に分け、repoの管理ファイルと場所で区別する
description: 配備されるファイルとrepoを維持するファイルの置き場所、templateからrepo rootとsource stateを指す規則を変えるときに、理由・代案・再検討条件を確認する。
status: stable
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-16T09:07:35+00:00"
sources:
  - id: maintainer
    resource: "Maintainer decision on the refactoring proposal, decision 3"
    title: "判断3「.chezmoiroot を導入する」の承認"
  - id: chezmoiroot
    resource: https://www.chezmoi.io/reference/special-files/chezmoiroot/
    title: chezmoi — .chezmoiroot
  - id: template-vars
    resource: https://www.chezmoi.io/reference/templates/variables/
    title: chezmoi — Template variables
---
# 決定

repo直下の`.chezmoiroot`に`home`と書き、chezmoiのsource stateを`home/`に置く。端末へ届くものは`home/`の中だけにあり、repoを維持するもの（文書・テスト・CI・lint設定・mise本体の導入script）は`home/`の外に置く。利用者が提案の判断3として採用した。[^maintainer]

# 理由

**事実。** chezmoiは`.chezmoiroot`があると、その中身が指すdirectoryからsource stateを読む。`.chezmoi.toml.tmpl`などroot系のfileもそこへ移す必要がある。[^chezmoiroot]

**推論。** source stateとrepoの管理ファイルが同じ階層にあると、どれが端末へ届くかを名前と`.chezmoiignore`の列挙から判断することになる。場所で分ければ、`home/`の外のfileは配備されないので、repo管理ファイルを配備から外す列挙が要らない。人もエージェントも、置き場所だけで配備の有無が分かる。

# 規則と保つもの

- templateでsource state内のfileを指すときは`.chezmoi.sourceDir`を使う。`.chezmoiroot`があると、この値は`home/`を指す。[^template-vars]
- templateでrepo直下のfile（`.bootstrap-mise.sh`、`.mise-version`）やGitの作業ツリーを指すときは`.chezmoi.workingTree`を使う。この値はrepo rootを指す。[^template-vars]
- 生成するchezmoi configの`sourceDir`は`.chezmoi.workingTree`、つまりrepo rootにする。`home/`を直接指すと`.chezmoiroot`を経由しなくなる。repo rootを指せば、生成されるconfigの値はsource stateの置き場所に左右されない。
- `include`と`includeTemplate`の相対pathは、source state（`home/`）を起点に書く。
- Git treeをpathで読む処理（`update:lazy-lock`）は、repo rootを起点に`home/`を含むpathで読む。生成するpatchをrepo rootで`git apply`できるようにするためである。
- `home/`の外に、chezmoiの属性prefixを持つ名前・`.chezmoi*`（`.chezmoiroot`を除く）・`Library`を置かない。`home/`の中に`tests`・`docs`・`.github`を置かない。[規約検査](../../tests/test_repo_rules.py)がこの2つを確かめる。

# repo直下に残すもの

- `.chezmoiroot`。chezmoiがsource stateより先に読む。[^chezmoiroot]
- `.bootstrap-mise.sh`と`.mise-version`。mise本体の明示導入と読込hookが使い、端末へ配備するものではない。hookはconfigに書いた絶対pathで呼ばれる。
- `.mise.toml`。repo側のmise設定が使えるようになる前に使うchezmoiの版の宣言で、端末のmise設定（`home/dot_config/mise/`）とは別のもの。
- 文書（`AGENTS.md`・`README.md`・`docs/`など）、`tests/`、`.github/`、`renovate.json5`、lintとeditorの設定。

# 代案と再検討の条件

- rootにsource stateを置いたまま、`.chezmoiignore`でrepo管理ファイルを列挙して外す。追加のたびに列挙を直す必要があり、漏れると管理ファイルが端末へ届く。
- source stateを別のrepoに分ける。分離は最も明確になるが、設定と検査・文書の変更を1つのPRで扱えなくなる。

chezmoiが`.chezmoiroot`の扱いを変えた場合や、repo直下のfileを端末へ配備する必要が出た場合は見直す。

[^maintainer]: リファクタリング提案の判断3に対する利用者の採用。実装の細部や実機の状態を承認するものではない。
[^chezmoiroot]: [chezmoi: .chezmoiroot](https://www.chezmoi.io/reference/special-files/chezmoiroot/)。source stateを読むdirectoryと、移すべきroot file。
[^template-vars]: [chezmoi: Template variables](https://www.chezmoi.io/reference/templates/variables/)。`.chezmoi.sourceDir`と`.chezmoi.workingTree`。
