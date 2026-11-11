---
type: Guide
title: WSL・Windowsの前提と認証境界
description: WSLのLinux側とWindows側で異なる設定・認証・copy先・検査を切り分ける。
status: draft
generated:
  by: codex/gpt-6
  at: "2026-11-11T15:42:39+00:00"
sources:
  - id: config
    resource: "../../.chezmoi.toml.tmpl"
    title: "ホスト入力と1Password identity取得"
  - id: wezterm
    resource: "../../dot_config/wezterm/wezterm.lua.tmpl"
    title: "WezTermのWSL domainとmux認証環境"
  - id: wezterm-link
    resource: "../../dot_local/bin/symlink_wezterm.tmpl"
    title: "macOS/WSLのWezTerm実体探索"
  - id: linux-script
    resource: "../../.chezmoiscripts/run_onchange_before_00-provision-linux-packages.sh.tmpl"
    title: "Linux package導入とsudo要件"
  - id: order
    resource: "https://www.chezmoi.io/reference/application-order/"
    title: "chezmoi公式：target計算とbefore/afterの順序"
  - id: op-wsl
    resource: "https://www.1password.dev/ssh/integrations/wsl"
    title: "1Password公式：Windows OpenSSHとWSL署名"
  - id: agent-sync
    resource: "../../dot_config/mise/repo-tasks/sync/executable_1password-agent.tmpl"
    title: "Windows側agent設定へのcopy"
  - id: wezterm-sync
    resource: "../../dot_config/mise/repo-tasks/sync/executable_wezterm.tmpl"
    title: "Windows側WezTerm設定へのcopy"
  - id: wsl-sync
    resource: "../../.chezmoiscripts/run_after_50-wsl-sync-services.sh.tmpl"
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
    resource: "../../.chezmoiscripts/run_onchange_before_provision-windows-packages.sh.tmpl"
    title: "Windows packageの完全一致照会とhash検証"
  - id: packages
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoidata/packages.yaml"
    title: "OS別package宣言"
  - id: docker-wsl
    resource: "https://docs.docker.com/desktop/features/wsl/"
    title: "Docker公式：WSL 2統合とbackendの差"
  - id: winget-list
    resource: "https://learn.microsoft.com/en-us/windows/package-manager/winget/list"
    title: "Microsoft — WinGet list options"
  - id: winget-install
    resource: "https://learn.microsoft.com/en-us/windows/package-manager/winget/install"
    title: "Microsoft — WinGet install options and hash check"
  - id: winget-list-code
    resource: "https://github.com/microsoft/winget-cli/blob/v1.12.350/src/AppInstallerCLICore/Commands/ListCommand.cpp"
    title: "WinGet v1.12.350 — list warning policy"
  - id: winget-flow
    resource: "https://github.com/microsoft/winget-cli/blob/v1.12.350/src/AppInstallerCLICore/Workflows/WorkflowBase.cpp"
    title: "WinGet v1.12.350 — source/search/output flow"
  - id: winget-reporter
    resource: "https://github.com/microsoft/winget-cli/blob/v1.12.350/src/AppInstallerCLICore/ExecutionReporter.cpp"
    title: "WinGet v1.12.350 — warnings use stdout"
  - id: winget-errors
    resource: "https://github.com/microsoft/winget-cli/blob/v1.12.350/src/AppInstallerSharedLib/Public/AppInstallerErrors.h"
    title: "WinGet v1.12.350 — HRESULT constants"
  - id: powershell-exe
    resource: "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_powershell_exe?view=powershell-5.1"
    title: "Microsoft — Windows PowerShell EncodedCommand"
  - id: process-arguments
    resource: "https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.processstartinfo.arguments?view=netframework-4.8.1"
    title: "Microsoft — ProcessStartInfo.Arguments"
  - id: process-exit
    resource: "https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.process.exitcode?view=netframework-4.8.1"
    title: "Microsoft — Process.ExitCode Int32"
  - id: process-read
    resource: "https://learn.microsoft.com/en-us/dotnet/api/system.io.streamreader.readtoendasync?view=netframework-4.8.1"
    title: "Microsoft — asynchronous stream reads"
  - id: posix-wait
    resource: "https://man7.org/linux/man-pages/man2/wait.2.html"
    title: "Linux man-pages — WEXITSTATUS lower eight bits"
  - id: winget-install-code
    resource: "https://github.com/microsoft/winget-cli/blob/v1.12.350/src/AppInstallerCLICore/Commands/InstallCommand.cpp"
    title: "WinGet v1.12.350 — install source open order"
  - id: winget-install-flow
    resource: "https://github.com/microsoft/winget-cli/blob/v1.12.350/src/AppInstallerCLICore/Workflows/InstallFlow.cpp"
    title: "WinGet v1.12.350 — identity and installer flow"
  - id: winget-dependencies
    resource: "https://github.com/microsoft/winget-cli/blob/v1.12.350/src/AppInstallerCLICore/Workflows/DependenciesFlow.cpp"
    title: "WinGet v1.12.350 — dependency source reuse"
  - id: winget-dependency-node
    resource: "https://github.com/microsoft/winget-cli/blob/v1.12.350/src/AppInstallerCLICore/Workflows/DependencyNodeProcessor.cpp"
    title: "WinGet v1.12.350 — dependency search result handling"
  - id: agent-config
    resource: "https://www.1password.dev/ssh/agent/config"
    title: "1Password: SSH agent config location"
  - id: wez-files
    resource: "https://wezterm.org/config/files.html#configuration-files"
    title: "WezTerm: configuration search order"
  - id: wslpath
    resource: "https://github.com/microsoft/WSL/blob/master/localization/strings/en-US/Resources.resw"
    title: "Microsoft WSL: wslpath usage"
  - id: wsl-permissions
    resource: "https://learn.microsoft.com/en-us/windows/wsl/file-permissions"
    title: "Microsoft: WSL file permissions"
---
# 対象と確認範囲

対象はWindows 11上のWSL2、Ubuntu 24.04以降というrepoの導入方針である。package dataに他のLinux分岐があることやUbuntu CIが通ることを、他環境やWSL実機の対応確認とはしない。以下の「現行」は2026-11-11のsource静的観測であり、この端末のWindows側や実認証は検査していない。

共通の操作は[operations](../operations.md)、鍵の入力とGit routingは[identity](../identity.md)、検査と副作用は[validation](../validation.md)を参照する。この文書はOS間の境界を扱い、それらの手順全文を複製しない。

# 現行：初期化・apply前に必要なもの

| 対象 | sourceの期待 | 注意点 |
|---|---|---|
| interop | Microsoft kernelの判定、`cmd.exe`・`powershell.exe`・`wslpath`等 | 通常のLinuxだけでは代替できない |
| Windows package導入 | WSL側のPython 3.9+、`powershell.exe` interop、Windows PowerShell 5.1から解決できる`winget.exe`が必要 | WinGet自身の導入処理はない。未導入・PATH不備ではWindows package段階で失敗し、先行するLinux package導入等の変更が残り得る[^win-script] |
| Windows 1Password | PowerShellで`op.exe`と署名helperを探索。非CIのconfig生成でaccount認証を要求 | 後段WinGetでの導入だけでは、この先行条件を満たさない |
| 署名helper | `op-ssh-sign-wsl.exe`、fallbackとして`op-ssh-sign.exe`を探索 | app配布形式でpathが変わり得る。過去の絶対pathへ固定しない |
| WezTerm | `C:\Program Files\WezTerm\wezterm.exe`を変換し存在確認。template評価時に`WSL_DISTRO_NAME`も必要 | 実体がなければsymlink templateがfailする。GUIが起動できるかは別の確認 |
| Linux側package導入 | 非対話sudoを使い、package managerのDBやsystem packageを変更する | sudo権限の設計は未解決。無制限の`NOPASSWD: ALL`を必須解として採用しない |

初回はLinux側のGit・Python 3.9+・ssh-keygenに加え、config生成用のinterop/op/helperとtarget計算用のWezTerm/distro名を手動で先行準備する。op/helperのconfig生成前提は後段WinGetだけで補えない。WezTermはtemplate評価で実体を要求するが、chezmoi 2.70.4ではその評価より先にbeforeが走り得る。先行準備は初回の採用手順であり、WinGetより必ず先にrenderが失敗するという保証ではない。実体欠損時の停止順は[隔離fixture](../validation.md#first-install-order)の対象であり、実WSLのinterop・クリーン環境の再現結果ではない。手順と不足時の行動は[operations](../operations.md#first-install)、採用理由と代案は[convergence](../decisions/convergence.md#bootstrap-prerequisites)を参照する。[^config][^wezterm][^wezterm-link][^linux-script][^order]

Linux package処理はidentity beforeより先に走るため、Python不足が実行時に見つかると先行package変更が残り得る。sudoのエラーでは無制限の権限設定を追加せず、選択package managerと後段のshell登録・変更に必要な権限、現在の認証を確認する。`sudo -n true`の合格は後段全commandの権限や認証維持の保証ではない。

1Password公式のWSL署名手順はWindows側のhelperを使用し、対応条件としてGit 2.34以上とx64 Windowsを挙げ、Arm版Windowsは未対応としている。repoのWindows 11という対象記述だけで、全architectureの署名対応を保証しない。[^op-wsl]

# LinuxとWindowsの設定を分ける

| 対象 | 現行の場所・処理 | 境界 |
|---|---|---|
| Git設定 | WSLのXDG Git設定からidentityを選ぶ | Git authorの選択、署名helper、remote認証は別の経路 |
| Git remoteのSSH | 生成した`core.sshCommand`でWindowsの`ssh.exe`を指定。公開鍵pathをWindows形式へ変換し、ControlPath=noneと明示したWindows IdentityAgentを付ける | WSLの`ssh`を直接起動した場合と同一ではない |
| SSH client設定 | WSLの`~/.ssh/config`はXDG SSH設定へのsymlink。一方、Windows OpenSSHはWindows側のSSH設定を使う | 1Password公式のWSL手順では`%USERPROFILE%/.ssh/config`を扱う。WSLのSSH設定を自動copyするtaskは、この同期処理にはない |
| 1Password agent設定 | 実`%LOCALAPPDATA%/1Password/config/ssh/agent.toml`へ照合同期 | 前回生成内容と手動編集を区別。agent起動・unlockは別 |
| WezTerm設定 | 実`%USERPROFILE%/.wezterm.lua`へ照合同期 | 他の優先設定を所有しない。GUIがこのfileを採用したかは別検査 |

同期は毎applyに配置後のsourceとtarget/receiptを照合する。欠損を復旧し、同一bytesなら無書換、手動変更や未所有の相違は保持停止する。[操作と失敗保持](../operations.md#windows-settings-sync)・[所有範囲](../ownership.md#windows-settings-sync)を参照。[^agent-sync][^wezterm-sync][^wsl-sync]

1Passwordの公式保存先はLOCALAPPDATAであり、USERPROFILE/AppData/Localと合成しない。WezTermの公式探索順はCLI指定、WEZTERM_CONFIG_FILE、Windowsのexe隣、XDG、HOME/.config、HOME/.wezterm.luaを含む。同期file以外の優先候補を移動・変更せず、同期成功をGUIの実効設定採用とみなさない。[^agent-config][^wez-files]

Windows PowerShell 5.1へ固定codeをUTF-16LE Base64のEncodedCommandとして渡し、process環境を読み取る。Get-Item -LiteralPathで存在する祖先と固定管理pathのReparsePoint属性を拒否し、結果はUTF-8 JSONをBase64化して返す。Linux側でschema/pathを検証し、wslpath -uで変換する。stderr・異常exit・不正応答・到達不能rootは停止する。実際のPowerShell評価、mount/ACL/別distro間排他はmacOSのstubで実証していない。[^powershell-exe][^wslpath][^wsl-permissions]

# WSLENV・pipe・WezTerm

zshenvは`SSH_AUTH_SOCK`をWindows OpenSSHのnamed pipe `\\.\pipe\openssh-ssh-agent`へ向け、`OP_BIOMETRIC_UNLOCK_ENABLED=true`とともに`WSLENV`へ`/w`付きで登録する。同名の古いentryを除き、他のentryは保持する。Microsoftの定義で`/w`はWSLから起動するWin32 processへの受渡し、`/p`はpath変換である。pipe文字列をLinux socket pathと混同しない。R04の生成Git commandはpipeを直接指定するため、この環境変数配送に依存しない。Linux側SSHはIdentityAgent noneを既定とする。詳細は[identity](../identity.md#現行ssh接続の分離とagent契約)を参照。[^zshenv][^wsl-env]

WezTermのWindows向け分岐は`WSL:<distro>`をdefault domainにし、`mux_enable_ssh_agent=false`と、mux環境から`SSH_AUTH_SOCK`・`SSH_CLIENT`・`SSH_CONNECTION`を除く設定を持つ。公式仕様ではmuxがSSH_AUTH_SOCKを設定する動作を無効化でき、指定した変数をmux serverの環境から除去できる。repoはWSL shellのzshenv側で認証環境を作り直す設計と読めるが、GUI起動から子processまでの実効値は未検査である。[^wezterm][^wez-mux][^wez-remove]

この経路を変えるときは、Windows SSH、署名helper、WSLの対話shell、WezTermからの起動を分けて確認する。以前使っていたbridgeを、必要性を確かめずに再導入しない。

# package・containerの範囲

<a id="windows-packages"></a>
## WinGetの識別・失敗分類

R11のbefore scriptは、WSLだけでheadless一覧、非CIではGUI一覧も順に処理する。`run_onchange_`を維持するため、source不変の毎applyでpackage欠損を再検査する契約ではない。list/installの両方へ`--id <ID> --exact --source winget --accept-source-agreements --disable-interactivity --authentication-mode silent`を渡す。listが完全一致の一件を返したIDはinstallしない。`AgileBits.1Password`と`.CLI`は別IDであり、CLIだけの導入をGUI導入済みとは判定しない。[^win-script][^winget-list][^winget-install]

installにはさらに`--silent --accept-package-agreements --no-upgrade`を渡す。既存確認後の競合で導入済みになった場合にもupgradeを要求しないが、その際の非zeroを成功へ読み替えない。nightly宣言は維持し、`--ignore-security-hash`を撤去した。hash不一致や他の導入失敗は停止する。独立した`source update || true`も撤去したが、list/install自身のsource自動更新・cache/log書込・通信はあり得る。明示sourceは設定済みの名前`winget`であり、sourceの追加・resetやURLの上書きは行わない。[^win-script][^winget-install][^winget-flow]

採用したCLI/出力の基準は公式`microsoft/winget-cli` **v1.12.350**の実装（2026-11-11閲覧）で、端末の導入版をpin・更新したという意味ではない。listは検索失敗を警告としてstdoutへ出し、未導入と同じ終了値や成功を返し得る。stderrが空、既知の出力構造、全32bit終了値の三つで判定し、英語メッセージの一致だけでは分岐しない。[^winget-list-code][^winget-flow][^winget-reporter]

| 照会結果 | 処理 |
|---|---|
| `0`かつ見出し・罫線・完全IDを含む一行の表だけ | 導入済みとして次のIDへ |
| `0x8A150014`（signed Int32では`-1978335212`）かつ単一の非空メッセージだけ | 正常な未導入としてそのIDをinstall |
| 追加の警告・複数行の候補・stderr・未知の表形式・空出力 | 判定不能として非zero。そのIDはinstallしない |
| その他の終了値 | 非zero。source・認証・曖昧照合・引数未対応を未導入へ変換しない |

`0x8A150016`は複数候補、`0x8A150011`はinstaller hash不一致、`0x8A150012`はsource名不存在、`0x8A150045`はsource open失敗、`0x8A150075`/`076`は認証失敗/対話要求である。実装は未導入の一値だけを特例にし、他を網羅的に成功へ分類しない。エラー値は公式headerを根拠とする。[^winget-errors]

installも終了値0だけでは成功としない。stderrが空で、最初の非progress行が対象`[ID]`とversionを含むidentity表示の形であることを要求する。採用版の通常ID installでは、source open/updateの警告と認証通知はidentity表示より前に出るため、前置きがあれば非zeroとする。依存解決はpackage versionのsourceを再利用し、別sourceをopenするmanifest installは使用しない。これは公式処理順序からの判定であり、任意のinstallerが後段に出す全警告の分類ではない。WinGet内部の依存照会は検索結果のMatchesを使い、partial failureを個別に伝播しない経路もある。出力にも終了値にも現れない内部障害まで検出する保証はない。検査はprocess終了後なので、警告で失敗とした時点でpackageが既に導入されている場合もある。先行packageやWindowsの変更をrollbackする契約ではない。[^winget-install-code][^winget-install-flow][^winget-dependencies][^winget-dependency-node][^winget-flow]

この出力検査はrepo固有の保守的な制約であり、WinGetが機械可読の安定schemaとして保証したものではない。ANSI表示制御と単独spinnerは除くが、source更新の進捗・初回agreement表示・認証通知・IDの省略・将来の表示変更も判定不能として止まり得る。installのidentity前に正常な追加表示が出る版や設定も停止対象になる。複数の導入scope/versionが複数行になる場合も自動採用しない。対応optionを持たない版は失敗させる。source問題や出力を確認して再試行し、未知形式を低8bitや文言推測で通さない。実Windowsでの出力確認後、必要な形式だけをfixtureとともに拡張する。[^winget-list-code][^winget-flow]

## WSLとWindowsの引数・終了値

[Python helper](../../.chezmoitemplates/windows_packages.py)を実templateへ埋め込み、package一覧はBase64化したJSONとして渡す。IDは非空のASCII英数字から始まる英数字・dot・underscore・hyphenだけに制限し、全IDをWindows起動前に検証する。PowerShellへは`-NoLogo -NoProfile -NonInteractive -EncodedCommand <UTF-16LEのBase64>`だけを渡す。codeを通常の`-Command`引数やstdinの逐次解釈へ流さず、WSLの引用境界を一つのBase64 tokenに限定する。[^win-script][^powershell-exe]

Windows側では`Get-Command -CommandType Application`の実体を`.NET ProcessStartInfo.FileName`へ入れ、固定optionと検証済みASCII tokenを空白で結合して`Arguments`へ設定する。空白・引用符を含む汎用argvをこの方式で扱う設計ではない。`UseShellExecute=false`、標準入力を閉じ、stdout/stderrを両方非同期に読み、終了後の`Process.ExitCode`（signed Int32）と出力をJSONで返す。bridge自身は0/1で終了し、PythonはJSONの型・範囲も検証する。[^process-arguments][^process-exit][^process-read]

POSIX wait statusからWindowsの32bitエラー値を復元することはできない。例えば未導入と同じ低8bitの別エラー、低8bitが0の失敗もあるため、WSLで直接起動した`winget.exe`の`$?`を未導入判定に使わない。bridgeが異常終了した場合は非zero、低8bitが0でも有効JSONがなければ失敗になる。実WSLでのinteropの具体的な戻り値は未観測であり、この境界をstub結果から実証したとはしない。[^process-exit][^posix-wait]

代案はWinGetのCOM API等で構造化結果を扱う方式だが、追加の対応条件・実Windows検証が必要になる。通常`list`の終了値だけを使う案は上記の警告経路を見逃すため採らない。nightlyの配布hashが変わる場合は、manifest修正を待つか、利用目的を確認してstableや検証できるartifactへ変更する。恒久的なhash検証迂回は代案にしない。非対話flagは採用した要求であり、installer固有の挙動・UAC・policyで停止せず完走する保証ではない。今回の証拠は[隔離検査](../validation.md#windows-packages)に限り、実WinGet・PowerShell・WSLでの導入・認証は未確認である。

package宣言にはWindowsの1Password・CLI・WezTerm nightlyがあるが、Docker Desktopはない。Linuxの対象packageにもDocker engine/CLIは宣言されていない。Dockerが必要な場合に別途Windows側で導入し、使うbackendと対象distributionへの統合を決める。必須のbootstrap成果物には追加しない。[^packages]

Docker公式ではWSL2 engineで対象distributionへの統合を設定する。Docker VMMなどbackendによってsocketや統合の範囲が異なるため、「Windowsに入れればWSLから同じように使える」と一般化しない。これは必要な人向けの選択肢で、既存端末へDockerを導入・変更する決定ではない。[^docker-wsl]

# 設計変更と検査の参照先

Windowsの限定2file管理を採用した理由と代案は[convergenceのWindows所有節](../decisions/convergence.md#windows-ownership)、入力更新は[identity節](../decisions/convergence.md#identity-input)を正本とする。ここではOS間の現行経路と制約を扱う。

認証調査に使う`dotfiles-diagnose --probe wsl-openssh`は外部通信と一時署名commitを含み、doctorの構成要素でもない。[validation](../validation.md)で範囲を確認してから必要なprobeを選ぶ。全identityやGit directory routingの検証を、この一つの成功結果で代替しない。

[^config]: [ホスト入力と1Password identity取得](../../.chezmoi.toml.tmpl)。
[^wezterm]: [WezTermのWSL domainとmux認証環境](../../dot_config/wezterm/wezterm.lua.tmpl)。
[^wezterm-link]: [macOS/WSLのWezTerm実体探索](../../dot_local/bin/symlink_wezterm.tmpl)。
[^linux-script]: [Linux package導入とsudo要件](../../.chezmoiscripts/run_onchange_before_00-provision-linux-packages.sh.tmpl)。
[^order]: [chezmoi公式：target計算とbefore/afterの順序](https://www.chezmoi.io/reference/application-order/)。
[^op-wsl]: [1Password公式：Windows OpenSSHとWSL署名](https://www.1password.dev/ssh/integrations/wsl)。
[^agent-sync]: [Windows側agent設定へのcopy](../../dot_config/mise/repo-tasks/sync/executable_1password-agent.tmpl)。
[^wezterm-sync]: [Windows側WezTerm設定へのcopy](../../dot_config/mise/repo-tasks/sync/executable_wezterm.tmpl)。
[^wsl-sync]: [WSL Windows sync起動条件](../../.chezmoiscripts/run_after_50-wsl-sync-services.sh.tmpl)。
[^zshenv]: [XDG・認証用環境変数とWSLENV](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_zshenv.tmpl)。
[^wsl-env]: [Microsoft公式：WSL interopとWSLENV](https://learn.microsoft.com/en-us/windows/wsl/filesystems)。
[^wez-mux]: [WezTerm公式：muxによるSSH_AUTH_SOCK設定](https://wezterm.org/config/lua/config/mux_enable_ssh_agent.html)。
[^wez-remove]: [WezTerm公式：mux環境変数の除去](https://wezterm.org/config/lua/config/mux_env_remove.html)。
[^win-script]: [Windows packageの完全一致照会とhash検証](../../.chezmoiscripts/run_onchange_before_provision-windows-packages.sh.tmpl)。
[^packages]: [OS別package宣言](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoidata/packages.yaml)。
[^docker-wsl]: [Docker公式：WSL 2統合とbackendの差](https://docs.docker.com/desktop/features/wsl/)。

[^winget-list]: [Microsoft — WinGet list options](https://learn.microsoft.com/en-us/windows/package-manager/winget/list)。2026-11-11閲覧。

[^winget-install]: [Microsoft — WinGet install options and hash check](https://learn.microsoft.com/en-us/windows/package-manager/winget/install)。2026-11-11閲覧。

[^winget-list-code]: [WinGet v1.12.350 — list warning policy](https://github.com/microsoft/winget-cli/blob/v1.12.350/src/AppInstallerCLICore/Commands/ListCommand.cpp)。2026-11-11閲覧。

[^winget-flow]: [WinGet v1.12.350 — source/search/output flow](https://github.com/microsoft/winget-cli/blob/v1.12.350/src/AppInstallerCLICore/Workflows/WorkflowBase.cpp)。2026-11-11閲覧。

[^winget-reporter]: [WinGet v1.12.350 — warnings use stdout](https://github.com/microsoft/winget-cli/blob/v1.12.350/src/AppInstallerCLICore/ExecutionReporter.cpp)。2026-11-11閲覧。

[^winget-errors]: [WinGet v1.12.350 — HRESULT constants](https://github.com/microsoft/winget-cli/blob/v1.12.350/src/AppInstallerSharedLib/Public/AppInstallerErrors.h)。2026-11-11閲覧。

[^powershell-exe]: [Microsoft — Windows PowerShell EncodedCommand](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_powershell_exe?view=powershell-5.1)。2026-11-11閲覧。

[^process-arguments]: [Microsoft — ProcessStartInfo.Arguments](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.processstartinfo.arguments?view=netframework-4.8.1)。2026-11-11閲覧。

[^process-exit]: [Microsoft — Process.ExitCode Int32](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.process.exitcode?view=netframework-4.8.1)。2026-11-11閲覧。

[^process-read]: [Microsoft — asynchronous stream reads](https://learn.microsoft.com/en-us/dotnet/api/system.io.streamreader.readtoendasync?view=netframework-4.8.1)。2026-11-11閲覧。

[^posix-wait]: [Linux man-pages — WEXITSTATUS lower eight bits](https://man7.org/linux/man-pages/man2/wait.2.html)。2026-11-11閲覧。

[^winget-install-code]: [WinGet v1.12.350 — install source open order](https://github.com/microsoft/winget-cli/blob/v1.12.350/src/AppInstallerCLICore/Commands/InstallCommand.cpp)。2026-11-11閲覧。

[^winget-install-flow]: [WinGet v1.12.350 — identity and installer flow](https://github.com/microsoft/winget-cli/blob/v1.12.350/src/AppInstallerCLICore/Workflows/InstallFlow.cpp)。2026-11-11閲覧。

[^winget-dependencies]: [WinGet v1.12.350 — dependency source reuse](https://github.com/microsoft/winget-cli/blob/v1.12.350/src/AppInstallerCLICore/Workflows/DependenciesFlow.cpp)。2026-11-11閲覧。

[^winget-dependency-node]: [WinGet v1.12.350 — dependency search result handling](https://github.com/microsoft/winget-cli/blob/v1.12.350/src/AppInstallerCLICore/Workflows/DependencyNodeProcessor.cpp)。2026-11-11閲覧。

[^agent-config]: [1Password: SSH agent config location](https://www.1password.dev/ssh/agent/config)。2026-11-11閲覧。

[^wez-files]: [WezTerm: configuration search order](https://wezterm.org/config/files.html#configuration-files)。2026-11-11閲覧。

[^wslpath]: [Microsoft WSL: wslpath usage](https://github.com/microsoft/WSL/blob/master/localization/strings/en-US/Resources.resw)。2026-11-11閲覧。

[^wsl-permissions]: [Microsoft: WSL file permissions](https://learn.microsoft.com/en-us/windows/wsl/file-permissions)。2026-11-11閲覧。
