---
type: Reference
title: Git・SSH identityの入力と生成物
description: 1Passwordの入力、Gitの選択、SSH認証と署名の経路を変更・調査するときに読む。
status: draft
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-13T06:49:36+00:00"
sources:
  - id: identity-after
    resource: "../.chezmoiscripts/run_after_10-identity.sh.tmpl"
    title: "毎回のidentity専用after入口"
  - id: identity-link
    resource: "https://docs.python.org/3/library/os.html#os.link"
    title: "Python os.link：検証済みfileへのlink作成"
  - id: transaction
    resource: "../.chezmoitemplates/identity_transaction.py"
    title: "identity世代の生成と参照切替"
  - id: prepare
    resource: "../.chezmoiscripts/run_before_05-identity-dispatch.sh.tmpl"
    title: "target前のlegacy routing保存"
  - id: application-order
    resource: "https://www.chezmoi.io/reference/application-order/"
    title: "chezmoi application order"
  - id: win-pipe
    resource: "https://github.com/PowerShell/openssh-portable/blob/v9.5.0.0/contrib/win32/win32compat/fileio.c"
    title: "Windows OpenSSH：named pipe接続"
  - id: win-ssh
    resource: "https://github.com/PowerShell/openssh-portable/blob/v9.5.0.0/ssh.c"
    title: "Windows OpenSSH：muxとIdentityAgentのconsumer"
  - id: win-readconf
    resource: "https://github.com/PowerShell/openssh-portable/blob/v9.5.0.0/readconf.c"
    title: "Windows OpenSSH：設定parserとControlPath none"
  - id: win-scope
    resource: "https://github.com/PowerShell/Win32-OpenSSH/wiki/Project-Scope"
    title: "Windows OpenSSH：未対応機能"
  - id: ssh-options
    resource: "https://man.openbsd.org/ssh_config"
    title: "OpenSSH：ControlPath・ControlMaster・IdentityAgent"
  - id: ssh-paths
    resource: "https://man.openbsd.org/ssh_config#IdentityFile"
    title: "OpenSSH：IdentityFileのtoken・環境変数展開"
  - id: windows-names
    resource: "https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file"
    title: "Windows：filenameの予約文字"
  - id: validation
    resource: "../.chezmoitemplates/validated_identities.tmpl"
    title: "identity集合・routing・公開鍵の共通検証"
  - id: quote
    resource: "../.chezmoitemplates/posix_shell_quote.tmpl"
    title: "POSIX shell単語の互換引用helper"
  - id: signers
    resource: "https://man.openbsd.org/ssh-keygen#ALLOWED_SIGNERS"
    title: "OpenSSH：allowed signersのprincipalと公開鍵形式"
  - id: config
    resource: "../.chezmoi.toml.tmpl"
    title: "ホスト入力と1Password identity取得"
  - id: git
    resource: "../dot_config/git/config.tmpl"
    title: "Git共通設定とincludeIf routing"
  - id: fragment
    resource: "../.chezmoitemplates/git_identity_config.tmpl"
    title: "identity別Git設定の生成fragment"
  - id: git-config
    resource: "https://git-scm.com/docs/git-config"
    title: "Git公式：条件付きincludeとSSH署名設定"
  - id: op-agent
    resource: "https://www.1password.dev/ssh/agent/config"
    title: "1Password公式：SSH agent設定と鍵の選択"
  - id: generate
    resource: "../dot_config/mise/repo-tasks/generate/executable_identity.tmpl"
    title: "identity生成と入力空集合の扱い"
  - id: agent
    resource: "../dot_config/1Password/ssh/private_agent.toml.tmpl"
    title: "1Password agentのitem/account選択"
  - id: ssh
    resource: "../dot_config/ssh/config.tmpl"
    title: "SSH共通設定とsocket値の参照"
  - id: zshenv
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_zshenv.tmpl"
    title: "XDG・認証用環境変数とWSLENV"
  - id: op-wsl
    resource: "https://www.1password.dev/ssh/integrations/wsl"
    title: "1Password公式：Windows OpenSSHとWSL署名"
---
# この文書の範囲

1Passwordから何を読み、Git・SSH・agentの設定へどう変換するかを扱う。正本・生成物の所有は[ownership](ownership.md)、生成処理の実行と副作用は[operations](operations.md)、Windowsとの境界は[WSL](platforms/wsl.md)を参照する。

以下の「現行」は2026-11-11にsourceを静的に読んだ結果である。実際の1Password item、端末の生成物、認証・署名の成否は確認していない。入力検証・引用はR02の現行sourceを参照する。実機の入力や配置済みscriptが更新済みとは扱わない。

# 現行：1Password入力

通常の非CI経路では、chezmoiのconfig生成時に`op`の発見と認証済みaccountを要求する。account一覧を取得し、各accountの`dotfiles-ssh-key`タグ付きitemを列挙して、その詳細JSONを読む。WSLではWindowsの`op.exe`を探索する。CI用の入力経路は実際のaccount検証を代替しない。[^config]

| 入力 | 現行の扱い | 制約 |
|---|---|---|
| item/account ID | identity情報とagent設定へ保持 | 非空の単一行文字列。実値を文書に載せない |
| 標準field `public key` | 公開鍵file、signing key、allowed signersへ使用 | 単一行のOpenSSH公開鍵。Ed25519 / RSA / ECDSA nistp256・384・521を許可し、`ssh-keygen -lf /dev/stdin`で実体も検査。commentの記号は保持 |
| 標準field `key type` | 小文字化して公開鍵file名へ使用。未指定時は`ed25519` | 先頭は英小文字または数字、以降はそれらと`-`。32 byte以内 |
| section label `dotfiles` の `dotfiles_git_name` | Git author名 | 空・空白のみ・制御文字を拒否。引用符、日本語、shell記号はそのまま保持 |
| 同sectionの `dotfiles_git_email` | Git email、公開鍵file名、allowed signersの単一principal | ASCIIの限定したaddr-spec、180 byte以内。先頭は英数字。local部は英数字と`.!#$&'+=^_`、backtick、`{}`、`~`、`-`。domain部は英数字から始まり英数字・`.`・`-`。完全なRFC email検証ではない |
| 同sectionの `dotfiles_git_dirs` | comma区切りのGit routing入力 | 下記のliteral directory契約。取得した文字列は保持し、consumerで検証・展開 |

account/item一覧とitem fieldsはJSON配列を要求し、`null`・object・空応答を正常な空集合とみなさない。保存済みconfigのidentitiesも配列を要求する。タグ付きitemに必須fieldの欠落・空値・制御文字（改行、tab等）があれば集合全体を拒否し、黙ってitemを落とさない。emailはallowed signersのpattern構文も考慮し、`*`・`?`・`,`・先頭`!`、空白、path区切りを許可しない。filenameの移行を避けるため、OpenSSHがpath内で展開する`%`・`${…}`とWindowsでfilenameに使えない縦棒もemailでは拒否する。quoted local部や国際化emailは未対応なので、該当入力が必要なら契約と全consumerを先に変更する。[^config][^validation][^signers]

`key_hash`はpublic key文字列のSHA-256先頭8文字で、consumerでも一致を確認する。basenameは維持し、生成先は下記の世代directoryへ移す。同じ生成config名になるidentityは大文字小文字を無視して拒否する。短いhashが衝突しない保証はない。[^config][^validation]

# routingと各出力の境界

`dirs`は各要素の周囲をtrimし、先頭`~/`をhomeへ展開し、末尾の`/`一つを除く。絶対pathまたは`~/`で始まるliteral directoryだけを受け付ける。空要素（末尾・連続commaを含む）、空白のみ、root `/`、相対path、`.`・`..`要素、重複slash、backslash、glob文字`* ? [ ]`を拒否する。directory内部の空白、引用符、`$()`、backtickはliteralとして保持する。commaを含むdirectory名は現行の区切り形式では表せない。[^validation]

全identityのdirectoryを大文字小文字を無視して比較し、同一・祖先子孫関係を拒否する。同じidentity内の重複もエラーとし、「後勝ち」や空要素の全repoへの展開に依存しない。検証は文字列の関係で、filesystemのsymlink alias・mount aliasは解決しない。Gitが最終的に照合するGit directory、worktreeやsymlink経由の選択は対象repoで別途確認する。directoryの存在は要求せず、作成も行わない。[^validation][^git-config]

共通検証はconfig取得時、およびGit routing・identity generator・identity check・agent設定のrender時に集合全体へ適用する。既存chezmoi configに保存された未検証入力も拒否対象になる。公開鍵検査はshellの固定programへ引数と標準入力で渡し、認証・通信・file書込をしない。ただし、空でないidentityのrenderにはPATH上の`sh`と`ssh-keygen`が新たに必要になる。エラーはitemの番号とfield/制約を示し、実値を診断に出さない。[^validation]

shellの単語はPOSIX単一引用（apostropheを引用の外で連結）、Git文字列はGit専用のescapeで生成する。chezmoi 2.70.4に`shellQuote`関数がないため互換helperを使用する。metadataをshellコメントやheredocのprogramへ直接補間せず、検証済みJSONを引用したargvでPython generatorへ渡す。Gitの`signingkey`全体とinclude条件も引用する。home内の`%`・`${`も未対応として拒否する。WSLでは非公開のstaging directoryを作ってから`wslpath -w`で変換し、変換失敗・制御文字・`%`・`${`を切替前に拒否する。`home`に加えて公開鍵を置く`xdg_config`にもOpenSSHの展開文字を許可しない。変換先とbasenameを連結したpathをPOSIX単一引用し、`git config`へargvとして渡す。OpenSSHの`-i`は展開前にもfile存在検査するため、`%`を`%%`へ置き換える案は採用していない。[^ssh-paths][^windows-names]これらはshell、Git config、filename、allowed signersそれぞれの境界を保つための実装である。[^quote][^fragment][^generate][^git-config]

直接のpost-apply wrapper・repair依存・WSL agent配送・identity checkも同じshell引用を使う。SSH共通設定のpathはSSH構文で引用し、Includeのprefixはliteralとしてglob escapeする。他のlifecycle task全体の特殊home対応は対象外である。SSH接続共有とagent契約は下記のR04の現行仕様に従う。

不正入力はconfig生成・対象templateのrenderで拒否し、生成出力を書き始めない。WSL変換先と生成形式は実行時に非公開世代で検査する。失敗時の参照保持は下記の切替契約に従う。既に配置された古いtaskはsourceの変更だけでは置き換わらない。実入力を取得せずに契約だけを変更したため、実機移行時には現在の入力の適合と生成物を確認する。[^generate]

# 現行：選択・署名・認証を分ける

| 経路 | 生成・参照するもの | 成功しても証明しないこと |
|---|---|---|
| Git authorの選択 | `dot_config/git/config.tmpl`が固定の`identity.inc`を読み、採用世代のdispatchにある`includeIf "gitdir/i:…/**"`から同じ世代のidentity別configを読む | 任意の作業directoryで望むidentityが選ばれること。条件はGit directoryに対して評価される |
| Git署名 | `gpg.format=ssh`、`gpg.ssh.program`、`user.signingkey=key::<public key>`、allowed signers | Git remoteへのアクセスや、すべての署名者の信頼判断 |
| GitからのSSH認証 | identity別`core.sshCommand`が公開鍵fileを`-i`で指定し、`IdentitiesOnly=yes`と`ControlPath=none`を付ける | shellから直接起動したSSHも同じidentityになること |
| 1Password agentの鍵選択 | `agent.toml`にitem/accountを列挙 | Desktopの起動・unlock・agent有効化、remoteへの公開鍵登録 |

`gitdir/i`は大文字小文字を区別しない条件である。複数条件の重なりは「最適なidentityを選ぶ」仕組みではないため、具体的なrepositoryで有効設定を確かめる必要がある。`user.useConfigOnly=true`、commit/tag署名有効が共通設定にある。通常のSSH起動とGitの`core.sshCommand`、署名helperは別の経路として調べる。[^git][^fragment][^git-config][^op-agent]

生成taskは同一世代directory内にidentity別config、`id_<type>_<email>_<hash>.pub`、allowed signersを作る。旧`~/.ssh/id_*.pub`は触らない。WSLでは公開鍵pathをWindows表記へ変換し、`core.sshCommand`を`ssh.exe`用に置き換える。agent設定は別のchezmoi templateから生成される。[^generate][^agent]

# 生成の切替と既存配置からの移行

`generate:identity`は全入力をtemplateで検証し、XDG Git配下の固有名`.identity-generation-*`へ公開鍵0600・Git fragment0600・allowed_signers0644・dispatchを生成する。Git parser、`ssh-keygen -lf`、allowed signersのprincipal照合を通してから、固定file`identity.inc`を一回の`os.replace`で切り替える。各参照は固有世代への絶対pathで、可変の`current`配下を使わない。Gitが旧設定を読んだ直後に切替が起きても、旧公開鍵とsignersを引き続き参照できる。[^transaction]

旧世代・失敗した未参照世代は自動削除しない。生成directoryとfileのhash manifest、およびentry内容を照合し、変更済み・未知のentry、symlink、手動変更した採用世代では上書きせず失敗する。欠損の扱いは下記のR10a契約に従う。未知fileの名前から所有を推定しない。directory lockでrepoのwriterを直列化し、SIGKILL等で残ったlockは自動除去しない。再実行前にwriterが終了していることと状態を確認する。悪意ある同一ユーザーの同時改変への防御や停電耐久性の保証ではない。[^transaction]

静的Git設定はgeneratorより先に配置されるため、`run_before_05-identity-dispatch`が旧Git設定のroutingとallowed_signersの参照を初回だけ読み取り、同じ固定entryから参照できるlegacy世代へ保存する。旧fileは移動・削除・書換しない。beforeの途中失敗ではtargetへ進まず、再実行は残った非公開世代を無視する。既存entryがあれば所有照合を行い、所有を確認できる世代内欠損をtarget前に復旧する。target前に中断した場合は、保存した旧Git configのhashも再実行時に照合し、途中の手動変更を黙って捨てない。初回導入では旧正常identityが存在しないため空の世代から始め、生成成功で初めてidentityが利用可能になる。[^prepare][^application-order]

移行で受け付ける旧設定は、このrepoが生成していた絶対`gitdir/i:`条件と存在する絶対または`~/`include先・allowed_signers参照である。他種のinclude、相対参照、globalの個人identity、欠落した旧参照は推定せず停止する。独自設定を採用する移行は内容を確認して別途行う。generator単独実行は、新しい静的consumerが配置済みであることを要求し、未移行のconsumerのまま成功を返さない。初回移行はbefore scriptを含む通常のapplyが対象で、scriptsを除外したGit config単体の配置や手動copyではこの保護を得られない。[^prepare]

通常の空入力は失敗し、CI用の偽公開鍵は生成しない。CIでの空入力成功は初回の空世代だけで、既存identityを空へ置換しない。意図的にすべてのroutingを解除する場合は、採用入力を明示的に`[]`へ変更し、配置済みtaskに`mise run generate:identity -- --clear`を渡す。空のsignersとroutingへ切り替え、旧fileは保持する。所有検証済みのclear採用世代では、その後も同じ空入力なら通常呼出しをno-op成功として扱う。欠落・不正入力の代用品として`--clear`を使わない。[^generate]

この切替はGit identityの参照単位である。chezmoi apply全体、1Password agent設定、package導入のtransactionではない。切替前のエラー・中断は旧参照を保持する。切替完了直後の中断では終了表示が出なくても新しい検証済み世代が採用済みの場合がある。実機WSLのinterop・1Password認証は未確認である。

# 現行：SSH接続の分離とagent契約

identity別の`core.sshCommand`は`ssh`／`ssh.exe`ともに`ControlPath=none`を指定する。同じhost/user/portで別鍵の既存masterを再利用しないための設定で、共通SSHの`ControlMaster auto`は維持する。`ControlMaster=no`単独でも既存masterを利用でき、`%C`は鍵を識別しない。identityを含むControlPathを設計する代案もあるが、今回は接続共有を無効にする最小の分離を採った。Git環境変数やrepo-local設定でこのcommandを上書きした場合、または別のIdentityFileをhost設定で追加した場合の鍵選択まで固定する保証ではない。[^ssh-options][^fragment]

agent値の正本はconfig producerの`data.ssh_auth_sock`（templateではrootの`.ssh_auth_sock`）である。[^config]

| consumer | 現行の解釈 |
|---|---|
| macOSの共通SSH設定 | 非空のroot値を`IdentityAgent`へSSH構文で引用する。絶対POSIX pathだけを受け付け、制御文字・`%`・`${`展開を拒否する。`SSH_AUTH_SOCK`未設定／別値でも設定値を使う |
| WSLのLinux側SSH設定 | `IdentityAgent none`を既定にし、Windows pipeをPOSIX socketとして開かない。必要なLinux agentは先行するhost別設定で指定できる |
| WSLからのGit `ssh.exe` | producerの標準pipe `\\.\pipe\openssh-ssh-agent`を検証し、`-o IdentityAgent=…`へSSH構文とshell構文の二段で引用する。Gitからの呼出しは環境変数によるpipe配送を必要としない |
| その他のLinuxで空／未定義の値 | 明示的な`IdentityAgent`は生成しない。agent未導入を修復せず、通常のOpenSSHの設定／環境解決を維持する |

Windows公式はControlMasterを未対応機能に挙げる。一方、PowerShell/openssh-portable `v9.5.0.0`の`readconf.c`では両optionをparseし、`ControlPath=none`をNULLへ変換する。`ssh.c`はその場合mux接続を呼ばず、明示したIdentityAgentでagent環境値を設定する。Windows互換層はAF_UNIXの接続をnamed pipeの`CreateFileW`へ渡す。これは公式コードからの静的な根拠であり、このrepoの実Windowsクライアントの版・interop・認証を検証した結果ではない。Windows設定fileはWindows側にあり、WSL側SSH設定をcopyして代用しない。[^win-scope][^win-readconf][^win-ssh][^win-pipe][^op-wsl]

[隔離検証](validation.md#ssh-identity-isolation)はGit argv、公開鍵の読込、既存master用socketに接続しない挙動を確認する。実serverでの認証成功や1Passwordの実鍵選択は未確認である。sourceを更新しても配置済みtask・生成Git fragmentは変わらないため、実機移行では通常の操作境界に沿って配置とidentity再生成を行い、有効commandを確認する。今回、実機apply・repair・doctorは行っていない。

# 現行の不足と見直し候補

| 観測した挙動 | 影響・まだ確認していないこと |
|---|---|
| 旧世代・旧公開鍵fileを自動回収しない | 既存readerと未知fileを保持するための意図的な制約。容量整理は参照・所有確認後の別操作 |
| SSH共通設定に`StrictHostKeyChecking accept-new`がある | 全host向けの現在の既定値。必須要件・最善の設定と認定していない |
| agent転送（`ForwardAgent`）は全host向けの既定で無効 | 転送が必要なhostは`conf.d`のhost別設定で有効にする。`conf.d`は共通設定より先に読まれるので、host別の値が優先される。どのhostで必要かは未調査 |

上記は現行codeの制約である。R05では生成と参照切替を変更した。socket契約とGit接続の分離はR04で修正した。[^generate][^config][^git][^ssh][^zshenv]

# 設計変更と調査結果の扱い

入力更新・失敗保護の案と代案は[convergenceのidentity節](decisions/convergence.md#identity-input)、schema・socket・SSH既定値の見直し候補は[同文書の未決事項](decisions/convergence.md#identity-constraints)を参照する。ここでは現行入力と観測した制約を正本として維持する。

WSLの認証経路は[WSL文書](platforms/wsl.md)と1Password公式の対応条件を確認する。[^op-wsl]

調査結果にはschema・件数・不一致の種類だけを残し、item JSON、実email、公開鍵と個人の対応表、認証情報を共有文書へ転記しない。検査の対象と副作用は[validation](validation.md)で選ぶ。そこで説明する検査を、文書閲覧だけで実行する必要はない。

[^config]: [ホスト入力と1Password identity取得](../.chezmoi.toml.tmpl)。
[^git]: [Git共通設定とincludeIf routing](../dot_config/git/config.tmpl)。
[^fragment]: [identity別Git設定の生成fragment](../.chezmoitemplates/git_identity_config.tmpl)。
[^git-config]: [Git公式：条件付きincludeとSSH署名設定](https://git-scm.com/docs/git-config)。
[^op-agent]: [1Password公式：SSH agent設定と鍵の選択](https://www.1password.dev/ssh/agent/config)。
[^generate]: [identity生成と入力空集合の扱い](../dot_config/mise/repo-tasks/generate/executable_identity.tmpl)。
[^agent]: [1Password agentのitem/account選択](../dot_config/1Password/ssh/private_agent.toml.tmpl)。
[^ssh]: [SSH共通設定とsocket値の参照](../dot_config/ssh/config.tmpl)。
[^zshenv]: [XDG・認証用環境変数とWSLENV](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_zshenv.tmpl)。
[^op-wsl]: [1Password公式：Windows OpenSSHとWSL署名](https://www.1password.dev/ssh/integrations/wsl)。

[^validation]: [identity集合の共通検証](../.chezmoitemplates/validated_identities.tmpl)。
[^quote]: [POSIX単語引用helper](../.chezmoitemplates/posix_shell_quote.tmpl)。
[^signers]: [OpenSSH allowed signers](https://man.openbsd.org/ssh-keygen#ALLOWED_SIGNERS)。

[^ssh-paths]: [OpenSSH IdentityFile](https://man.openbsd.org/ssh_config#IdentityFile)。
[^windows-names]: [Windows filename conventions](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file)。

[^ssh-options]: [OpenSSH：ControlPath・ControlMaster・IdentityAgent](https://man.openbsd.org/ssh_config)。2026-11-11参照。

[^win-scope]: [Windows OpenSSH：未対応機能](https://github.com/PowerShell/Win32-OpenSSH/wiki/Project-Scope)。2026-11-11参照。

[^win-readconf]: [Windows OpenSSH：設定parserとControlPath none](https://github.com/PowerShell/openssh-portable/blob/v9.5.0.0/readconf.c)。2026-11-11参照。

[^win-ssh]: [Windows OpenSSH：muxとIdentityAgentのconsumer](https://github.com/PowerShell/openssh-portable/blob/v9.5.0.0/ssh.c)。2026-11-11参照。

[^win-pipe]: [Windows OpenSSH：named pipe接続](https://github.com/PowerShell/openssh-portable/blob/v9.5.0.0/contrib/win32/win32compat/fileio.c)。2026-11-11参照。

[^transaction]: [identity transaction実装](../.chezmoitemplates/identity_transaction.py)。
[^prepare]: [target反映前のlegacy参照保存](../.chezmoiscripts/run_before_05-identity-dispatch.sh.tmpl)。
[^application-order]: [chezmoi application order](https://www.chezmoi.io/reference/application-order/)。target計算後にbefore scripts、target反映、after scriptsの順。

<a id="identity-convergence"></a>
# R10a：再適用と世代内欠損の復旧

`run_after_10-identity`は毎回applyから直接Python engineを呼ぶ。共通の`run_onchange_after_20`やmise task省略に依存しない。identityはmise graphから外し、明示`generate:identity`も同じengineを使う。beforeは移行・所有検証と既存世代の復旧、afterは配置済みGit consumerの確認と必要な新世代生成を担当する。補完・bat・Vale・pbfile・Windows adapterの起動契約はこの変更に含めない。[^identity-after][^transaction]

正常世代では全fileのhashとmode、entry、manifestを検査し、採用入力のdigestが一致すればfileも世代も作り直さない。digestは検証済みJSON（render済みshared fragment/SSH option・pathを含む）、engine source、実行するGitの版、WSLでは`wslpath -w`の実変換結果を含む。Windows pathの世代basenameだけを正規化し、distroやmount mappingの変更を検出する。mise本体の版はこれらの出力に使わないため依存にしない。`WSL_DISTRO_NAME`だけが変わっても実変換先が同じならidentityの再生成は不要。公開鍵・signersの内容にdistroは関係しないが、fragmentのSSH鍵pathが変わるため参照一式は同じ新世代へ切り替える。Git版はfragmentを整形する実依存である。Python・OpenSSHは実行／検証の前提であり版文字列そのものを出力入力にしない。[^transaction]

| 欠損・競合 | 復旧または停止の契約 |
|---|---|
| 採用世代の公開鍵、各fragment、allowed_signers、dispatch、世代内entry | v2 manifestの保存内容・hash・modeを照合し、欠損fileだけを同一pathへ復旧する。新入力で旧fileを作り直さない |
| 固定`identity.inc`、採用世代directory、`manifest.json` | 採用世代や所有の根拠を失った場合は非zero停止する。残存世代から推測して選択せず、確認済みbackup等による明示復旧が必要 |
| 既存fileの内容/mode変更、symlink・非通常file、採用世代内の未知file | 全件を先に照合して拒否する。欠損が混在しても復旧を始めず、未知file・link先を保持する |
| R05のv1 manifest | 正常なら次の生成でv2へ切替。欠損時は現在の入力から旧絶対path向けに隔離生成し、file集合と全hashが旧manifestに完全一致する場合だけ復旧する。入力/template/変換先が変わり旧内容を再現できなければ停止する |
| 旧世代・失敗世代・世代外の管理外file | 自動回収・書換をしない。旧consumerの参照を保持する |

v2 manifestは生成時に検証した公開出力の内容を0600で保存する。秘密鍵は含まないが個人情報なので共有ログへ出さない。復旧は全不足分を一時directoryへ用意してから、上書きしないhardlinkで公開する。既存の正常fileは変更せず、旧dispatchを読んでいたconsumerも同じpath・同じ内容を利用する。復旧のpublish途中にI/O失敗やsignalが来た場合は、一部の欠損だけが復旧済みになり得る。非zeroで返し、正常fileを消さず、次回は残る欠損を再検査する。通常の競合検出・staging失敗では復旧を開始しない。これは複数fileの原子的復旧や同一ユーザーの悪意ある同時改変への保証ではない。[^transaction][^identity-link]

空入力の拒否・明示clear、初回CI空集合の例外はR05と同じ。所有根拠の喪失を含めた「全必須出力の自動復旧」は未達であり、R10全体の完了ではない。実WSLや実認証は未確認。[隔離検証](validation.md#identity-convergence)を参照。

[^identity-after]: [毎回のidentity専用after入口](../.chezmoiscripts/run_after_10-identity.sh.tmpl)。[chezmoi scripts](https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/)の毎回実行／onchangeの区別に基づく。2026-11-11閲覧。
[^identity-link]: [Python os.link](https://docs.python.org/3/library/os.html#os.link)。同一filesystemで検証済みfileへのlinkを作成する。2026-11-11閲覧。
