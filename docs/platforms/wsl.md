---
type: Guide
title: WSL・Windowsの前提と認証境界
description: WSLのLinux側とWindows側で異なる設定・認証・copy先・検査を切り分ける。
status: draft
generated:
  by: codex/gpt-6
  at: "2026-11-11T07:15:07+00:00"
sources:
  - id: config
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoi.toml.tmpl"
    title: "ホスト入力と1Password identity取得"
  - id: wezterm
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/wezterm/wezterm.lua.tmpl"
    title: "WezTermのWSL domainとmux認証環境"
  - id: wezterm-link
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_local/bin/symlink_wezterm.tmpl"
    title: "macOS/WSLのWezTerm実体探索"
  - id: linux-script
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_before_00-provision-linux-packages.sh.tmpl"
    title: "Linux package導入とsudo要件"
  - id: order
    resource: "https://www.chezmoi.io/reference/application-order/"
    title: "chezmoi公式：target計算とbefore/afterの順序"
  - id: op-wsl
    resource: "https://www.1password.dev/ssh/integrations/wsl"
    title: "1Password公式：Windows OpenSSHとWSL署名"
  - id: agent-sync
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/sync/executable_1password-agent.tmpl"
    title: "Windows側agent設定へのcopy"
  - id: wezterm-sync
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/sync/executable_wezterm.tmpl"
    title: "Windows側WezTerm設定へのcopy"
  - id: wsl-sync
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_after_wsl-sync-services.sh.tmpl"
    title: "WSL Windows sync起動条件"
  - id: zshenv
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_zshenv.tmpl"
    title: "XDG・認証用環境変数とWSLENV"
  - id: wsl-env
    resource: "https://learn.microsoft.com/en-us/windows/wsl/filesystems"
    title: "Microsoft公式：WSL interopとWSLENV"
  - id: wez-mux
    resource: "https://wezterm.org/config/lua/config/mux_enable_ssh_agent.html"
    title: "WezTerm公式：muxによるSSH_AUTH_SOCK設定"
  - id: wez-remove
    resource: "https://wezterm.org/config/lua/config/mux_env_remove.html"
    title: "WezTerm公式：mux環境変数の除去"
  - id: win-script
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_before_provision-windows-packages.sh.tmpl"
    title: "Windows package導入とnightlyのhash回避"
  - id: packages
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoidata/packages.yaml"
    title: "OS別package宣言"
  - id: docker-wsl
    resource: "https://docs.docker.com/desktop/features/wsl/"
    title: "Docker公式：WSL 2統合とbackendの差"
---
# 対象と確認範囲

対象はWindows 11上のWSL2、Ubuntu 24.04以降というrepoの導入方針である。package dataに他のLinux分岐があることやUbuntu CIが通ることを、他環境やWSL実機の対応確認とはしない。以下の「現行」は2026-11-11のsource静的観測であり、この端末のWindows側や実認証は検査していない。

共通の操作は[operations](../operations.md)、鍵の入力とGit routingは[identity](../identity.md)、検査と副作用は[validation](../validation.md)を参照する。この文書はOS間の境界を扱い、それらの手順全文を複製しない。

# 現行：初期化・apply前に必要なもの

| 対象 | sourceの期待 | 注意点 |
|---|---|---|
| interop | Microsoft kernelの判定、`cmd.exe`・`powershell.exe`・`wslpath`等 | 通常のLinuxだけでは代替できない |
| Windows package導入 | apply前に、WSLから`winget.exe`を実行可能にしておく | WinGet自身の導入処理はない。未導入・PATH不備ではWindows package段階で失敗し、先行するLinux package導入等の変更が残り得る[^win-script] |
| Windows 1Password | PowerShellで`op.exe`と署名helperを探索。非CIのconfig生成でaccount認証を要求 | 後段WinGetでの導入だけでは、この先行条件を満たさない |
| 署名helper | `op-ssh-sign-wsl.exe`、fallbackとして`op-ssh-sign.exe`を探索 | app配布形式でpathが変わり得る。過去の絶対pathへ固定しない |
| WezTerm | `C:\Program Files\WezTerm\wezterm.exe`を変換し存在確認。template評価時に`WSL_DISTRO_NAME`も必要 | 実体がなければsymlink templateがfailする。GUIが起動できるかは別の確認 |
| Linux側package導入 | 非対話sudoを使い、package managerのDBやsystem packageを変更する | sudo権限の設計は未解決。無制限の`NOPASSWD: ALL`を必須解として採用しない |

chezmoiはtarget計算後にbefore scriptを実行するため、WezTermやopの先行要求とWindows packageの自動導入には順序上の課題がある。これはcodeと公式の適用順からの推論で、クリーンなWSLで再現した結果ではない。初回導入の手順は[operations](../operations.md#first-install)、変更方式の比較は[convergence](../decisions/convergence.md#bootstrap-prerequisites)を参照する。[^config][^wezterm][^wezterm-link][^linux-script][^order]

1Password公式のWSL署名手順はWindows側のhelperを使用し、対応条件としてGit 2.34以上とx64 Windowsを挙げ、Arm版Windowsは未対応としている。repoのWindows 11という対象記述だけで、全architectureの署名対応を保証しない。[^op-wsl]

# LinuxとWindowsの設定を分ける

| 対象 | 現行の場所・処理 | 境界 |
|---|---|---|
| Git設定 | WSLのXDG Git設定からidentityを選ぶ | Git authorの選択、署名helper、remote認証は別の経路 |
| Git remoteのSSH | 生成した`core.sshCommand`でWindowsの`ssh.exe`を指定。公開鍵pathをWindows形式へ変換 | WSLの`ssh`を直接起動した場合と同一ではない |
| SSH client設定 | WSLの`~/.ssh/config`はXDG SSH設定へのsymlink。一方、Windows OpenSSHはWindows側のSSH設定を使う | 1Password公式のWSL手順では`%USERPROFILE%/.ssh/config`を扱う。WSLのSSH設定を自動copyするtaskは、この同期処理にはない |
| 1Password agent設定 | WSLの生成fileを`%USERPROFILE%/AppData/Local/1Password/config/ssh/agent.toml`へcopy | Windows側の既存fileをmergeせず上書きする。agent起動・unlockは別 |
| WezTerm設定 | WSLの生成fileを`%USERPROFILE%/.wezterm.lua`へcopy | Windows GUI側の設定を書き換える。導入先の別profileとの整合は未確認 |

同期taskはWSL・非CIの経路で動き、copy元がないと成功skipする。target directory作成と`cp -f`を使い、Windows側の手動変更を自動的に取り込む設計ではない。二つのcopy先をrepoの管理へ引き受ける範囲は、[ownership](../ownership.md)と[convergence](../decisions/convergence.md)で確認する。[^agent-sync][^wezterm-sync][^wsl-sync][^op-wsl]

# WSLENV・pipe・WezTerm

zshenvは`SSH_AUTH_SOCK`をWindows OpenSSHのnamed pipe `\\.\pipe\openssh-ssh-agent`へ向け、`OP_BIOMETRIC_UNLOCK_ENABLED=true`とともに`WSLENV`へ`/w`付きで登録する。同名の古いentryを除き、他のentryは保持する。Microsoftの定義で`/w`はWSLから起動するWin32 processへの受渡し、`/p`はpath変換である。pipe文字列をLinux socket pathと混同しない。[^zshenv][^wsl-env]

WezTermのWindows向け分岐は`WSL:<distro>`をdefault domainにし、`mux_enable_ssh_agent=false`と、mux環境から`SSH_AUTH_SOCK`・`SSH_CLIENT`・`SSH_CONNECTION`を除く設定を持つ。公式仕様ではmuxがSSH_AUTH_SOCKを設定する動作を無効化でき、指定した変数をmux serverの環境から除去できる。repoはWSL shellのzshenv側で認証環境を作り直す設計と読めるが、GUI起動から子processまでの実効値は未検査である。[^wezterm][^wez-mux][^wez-remove]

この経路を変えるときは、Windows SSH、署名helper、WSLの対話shell、WezTermからの起動を分けて確認する。以前使っていたbridgeを、必要性を確かめずに再導入しない。

# package・containerの範囲

WinGet scriptはsource更新を試み、既存判定後に未導入packageをsilent installする。source更新の失敗を無視する箇所と、nightly packageに`--ignore-security-hash`を付ける経路がある。後者は現行の挙動として記録し、維持を推奨しない。nightlyの必要性と取得物の検証方法は見直し候補である。[^win-script]

package宣言にはWindowsの1Password・CLI・WezTerm nightlyがあるが、Docker Desktopはない。Linuxの対象packageにもDocker engine/CLIは宣言されていない。Dockerが必要な場合に別途Windows側で導入し、使うbackendと対象distributionへの統合を決める。必須のbootstrap成果物には追加しない。[^packages]

Docker公式ではWSL2 engineで対象distributionへの統合を設定する。Docker VMMなどbackendによってsocketや統合の範囲が異なるため、「Windowsに入れればWSLから同じように使える」と一般化しない。これは必要な人向けの選択肢で、既存端末へDockerを導入・変更する決定ではない。[^docker-wsl]

# 設計変更と検査の参照先

Windows copy先を管理へ引き受けるかの比較は[convergenceのWindows所有節](../decisions/convergence.md#windows-ownership)、入力更新は[identity節](../decisions/convergence.md#identity-input)を正本とする。ここではOS間の現行経路と制約を扱う。

認証調査に使う`check:wsl-openssh`は外部通信と一時署名commitを含み、doctorの構成要素でもない。[validation](../validation.md)で範囲を確認してから必要なprobeを選ぶ。全identityやGit directory routingの検証を、この一つの成功結果で代替しない。

[^config]: [ホスト入力と1Password identity取得](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoi.toml.tmpl)。
[^wezterm]: [WezTermのWSL domainとmux認証環境](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/wezterm/wezterm.lua.tmpl)。
[^wezterm-link]: [macOS/WSLのWezTerm実体探索](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_local/bin/symlink_wezterm.tmpl)。
[^linux-script]: [Linux package導入とsudo要件](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_before_00-provision-linux-packages.sh.tmpl)。
[^order]: [chezmoi公式：target計算とbefore/afterの順序](https://www.chezmoi.io/reference/application-order/)。
[^op-wsl]: [1Password公式：Windows OpenSSHとWSL署名](https://www.1password.dev/ssh/integrations/wsl)。
[^agent-sync]: [Windows側agent設定へのcopy](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/sync/executable_1password-agent.tmpl)。
[^wezterm-sync]: [Windows側WezTerm設定へのcopy](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/sync/executable_wezterm.tmpl)。
[^wsl-sync]: [WSL Windows sync起動条件](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_after_wsl-sync-services.sh.tmpl)。
[^zshenv]: [XDG・認証用環境変数とWSLENV](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_zshenv.tmpl)。
[^wsl-env]: [Microsoft公式：WSL interopとWSLENV](https://learn.microsoft.com/en-us/windows/wsl/filesystems)。
[^wez-mux]: [WezTerm公式：muxによるSSH_AUTH_SOCK設定](https://wezterm.org/config/lua/config/mux_enable_ssh_agent.html)。
[^wez-remove]: [WezTerm公式：mux環境変数の除去](https://wezterm.org/config/lua/config/mux_env_remove.html)。
[^win-script]: [Windows package導入とnightlyのhash回避](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoiscripts/run_onchange_before_provision-windows-packages.sh.tmpl)。
[^packages]: [OS別package宣言](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoidata/packages.yaml)。
[^docker-wsl]: [Docker公式：WSL 2統合とbackendの差](https://docs.docker.com/desktop/features/wsl/)。
