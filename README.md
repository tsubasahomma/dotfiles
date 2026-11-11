---
type: Guide
title: dotfiles
description: このrepoの目的と対象環境を知り、導入・日常操作・変更に必要な文書を選ぶ。
status: draft
generated:
  by: codex/gpt-6
  at: "2026-11-11T10:38:11+00:00"
---
# dotfiles

macOSとWindows 11上のWSL2（Ubuntu 24.04以降）向けの、個人用ワークステーション設定です。chezmoiのsource stateとして設定を管理し、miseのツール宣言やタスク、Git・SSHで使う1Password由来のidentity設定を含みます。

このrepoの宣言が、端末の現在の状態をすべて表しているとは限りません。手動で更新したツールや、repoの管理外にある状態もあります。導入・更新・復旧では、何を管理し、何を書き換えるかを先に確認します。

# やりたいことから読む

| やりたいこと | 参照先 |
|---|---|
| 新しい端末へ導入する | [初回導入の経路](docs/operations.md#first-install)、対象の[macOS](docs/platforms/macos.md)または[WSL・Windows](docs/platforms/wsl.md)、[identityの準備](docs/identity.md) |
| 設定を反映する・生成物の欠損を調べる | [状態の所有境界](docs/ownership.md)、[apply・repairの操作と副作用](docs/operations.md) |
| Git・SSH・1Passwordの問題を調べる | [identityのデータ契約](docs/identity.md)。Windowsとの連携は[WSL・Windows](docs/platforms/wsl.md)も参照 |
| ツールや設定を変更し、確かめる | [開発と更新](docs/development.md)、[変更に応じた検証](docs/validation.md) |
| bootstrap・apply・repair・doctorの設計を見直す | [収束設計の判断と代案](docs/decisions/convergence.md) |
| 文書を追加・整理する | [OKFの構成と記述規約](docs/decisions/okf.md) |

実機コマンドは操作文書で前提・対象・副作用を確認してから使います。読み取りhookはmiseの存在・実行属性の確認だけを行い、導入には明示的な`--install`が必要です。[旧configの移行](docs/operations.md#mise-bootstrap)とexternal/cache等の別の副作用も確認し、dry-run全体を非変更とは扱いません。

現在実行できる手順は[操作文書](docs/operations.md)、未実装の変更案は[設計判断](docs/decisions/convergence.md)に分けます。applyに管理対象生成物の欠損復旧を含める案は検討中で、現行実装の保証ではありません。

このrepoのMarkdownは、repo全体を一つのOKF bundleとして整理します。エージェント向けの常時指示は[AGENTS.md](AGENTS.md)、人間とエージェントが必要時に参照する知識は`docs/`に置きます。
