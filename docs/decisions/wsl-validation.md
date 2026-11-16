---
type: Decision
title: WSLは手動で確認し、CIでは代用品を使って通さない
description: WSLの検証方法を見直すときに、CIで自動化しない理由、採らなかった代案、守る条件と再検討の条件を確認する。
status: stable
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-16T10:12:07+00:00"
sources:
  - id: config
    resource: "../../home/.chezmoi.toml.tmpl"
    title: "chezmoi config template（WSLのop.exe探索）"
  - id: runner-image
    resource: "https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-Readme.md"
    title: "GitHub windows-2025 runner imageの内容"
---
# 決定

WSLの動作は、利用者が実機のWSL2 Ubuntuで手順どおりに確認する。GitHubのWindows runnerでWSLを動かすCI jobは置かない。手順と頻度は[検証の範囲](../validation.md#wsl-manual)にある。

# 理由

GitHubの`windows-2025` runnerはWSL2を備え、Ubuntuを導入して起動でき、WSLからWindowsのcommandも呼べる。[^runner-image] しかし、このrepoのconfig templateはWSLで、CIであってもWindows側の1Password CLI（`op.exe`）をPowerShell経由で探し、見つからなければinitを止める。[^config] runnerには1Password・WezTerm・その設定が無いので、先へ進めるには代用品を置くしかない。

代用品で通しても、WSLで確かめたい部分は検査から外れる。1Passwordとの連携、Windows側のSSH agentと署名、interop越しのpath変換と設定の同期である。残るのはLinux側の配置だけで、それはUbuntuのCIがすでに確かめている。

# 採らなかった代案

- **templateにWSLのCI分岐を足す。** 配備するtemplateの分岐が増え、検査できる範囲は上と同じくLinux側の配置に留まる。
- **代用品のop.exe・WezTermをrunnerに置く。** 検査が通っても、実機で壊れる経路を見逃す。合格の意味が誤解されやすい。

# 守る条件

- CIの合格を、WSL・Windows・1Passwordでの成功として扱わない。
- WSLに関わる変更を取り込んだら手動確認を行い、行っていない変更は「WSL未確認」と記録する。

# 再検討する条件

- hosted runnerで、1Password CLIのサービス用認証などの、実物の連携をsecretなしで検査できる手段が出たとき。
- config templateのWSL経路が、Windows側のtoolを必須としない形に変わったとき。

[^config]: [chezmoi config template](../../home/.chezmoi.toml.tmpl)のWSL分岐。`op.exe`の探索に失敗するとinitを止める。
[^runner-image]: [windows-2025 runner imageの内容](https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-Readme.md)。WSL（既定はWSL2）が入っている。
