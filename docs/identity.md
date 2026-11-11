---
type: Reference
title: Git・SSH identityの入力と生成物
description: 1Passwordの入力、Gitの選択、SSH認証と署名の経路を変更・調査するときに読む。
status: draft
generated:
  by: codex/gpt-6
  at: "2026-11-11T06:40:22+00:00"
sources:
  - id: config
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoi.toml.tmpl"
    title: "ホスト入力と1Password identity取得"
  - id: git
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/git/config.tmpl"
    title: "Git共通設定とincludeIf routing"
  - id: fragment
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoitemplates/git_identity_config.tmpl"
    title: "identity別Git設定の生成fragment"
  - id: git-config
    resource: "https://git-scm.com/docs/git-config"
    title: "Git公式：条件付きincludeとSSH署名設定"
  - id: op-agent
    resource: "https://www.1password.dev/ssh/agent/config"
    title: "1Password公式：SSH agent設定と鍵の選択"
  - id: generate
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/generate/executable_identity.tmpl"
    title: "identity生成と入力空集合の扱い"
  - id: agent
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/1Password/ssh/private_agent.toml.tmpl"
    title: "1Password agentのitem/account選択"
  - id: ssh
    resource: "https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/ssh/config.tmpl"
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

以下の「現行」は2026-11-11にsourceを静的に読んだ結果である。実際の1Password item、端末の生成物、認証・署名の成否は確認していない。code参照は観測時HEADに固定した。既存実装の説明を、入力検証や安全性の保証としない。

# 現行：1Password入力

通常の非CI経路では、chezmoiのconfig生成時に`op`の発見と認証済みaccountを要求する。account一覧を取得し、各accountの`dotfiles-ssh-key`タグ付きitemを列挙して、その詳細JSONを読む。WSLではWindowsの`op.exe`を探索する。CI用の入力経路は実際のaccount検証を代替しない。[^config]

| 入力 | 現行の扱い | 注意点 |
|---|---|---|
| item/account ID | identity情報とagent設定へ保持 | accountごとの鍵選択に使う。文書には実値を載せない |
| 標準field `public key` | 公開鍵file、signing key、allowed signersへ使用 | 値全体を元に短いhashを作る。秘密鍵のfile exportは生成処理に見当たらないが、item詳細JSONを読む範囲まで公開鍵だけとは断言しない |
| 標準field `key type` | 小文字化して公開鍵file名へ使用。未指定時は`ed25519` | algorithmやfile名として安全かの包括的検証はない |
| section label `dotfiles` の `dotfiles_git_name` | Git author名 | 必須判定は非空かどうか |
| 同sectionの `dotfiles_git_email` | Git email、公開鍵file名、allowed signersへ使用 | email・path・設定値としての十分な検証は未実装 |
| 同sectionの `dotfiles_git_dirs` | comma区切りのGit routing入力 | 分割後のtrimと先頭`~/`展開。実directory作成や重複・包含関係の検査はしない |

name・email・dirs・public keyのいずれかが空のitemは、identity集合へ追加されない。入力不足をすべて明示的errorにする実装ではない。`key_hash`はpublic key文字列のSHA-256先頭8文字で、永続的な鍵IDや衝突しない識別子の保証ではない。`ssh_keys_hash`はitem一覧JSONから計算され、詳細fieldすべての正規化hashではない。入力編集を毎回確実に検知する保証としない。[^config]

# 現行：選択・署名・認証を分ける

| 経路 | 生成・参照するもの | 成功しても証明しないこと |
|---|---|---|
| Git authorの選択 | `dot_config/git/config.tmpl`が`includeIf "gitdir/i:…/**"`を生成し、XDG Git配下のidentity別configを読む | 任意の作業directoryで望むidentityが選ばれること。条件はGit directoryに対して評価される |
| Git署名 | `gpg.format=ssh`、`gpg.ssh.program`、`user.signingkey=key::<public key>`、allowed signers | Git remoteへのアクセスや、すべての署名者の信頼判断 |
| GitからのSSH認証 | identity別`core.sshCommand`が公開鍵fileを`-i`で指定し、`IdentitiesOnly=yes`を付ける | shellから直接起動したSSHも同じidentityになること |
| 1Password agentの鍵選択 | `agent.toml`にitem/accountを列挙 | Desktopの起動・unlock・agent有効化、remoteへの公開鍵登録 |

`gitdir/i`は大文字小文字を区別しない条件である。複数条件の重なりは「最適なidentityを選ぶ」仕組みではないため、具体的なrepositoryで有効設定を確かめる必要がある。`user.useConfigOnly=true`、commit/tag署名有効が共通設定にある。通常のSSH起動とGitの`core.sshCommand`、署名helperは別の経路として調べる。[^git][^fragment][^git-config][^op-agent]

生成taskはidentity別config、`~/.ssh/id_<type>_<email>_<hash>.pub`、allowed signersを作る。WSLでは公開鍵pathをWindows表記へ変換し、`core.sshCommand`を`ssh.exe`用に置き換える。agent設定は別のchezmoi templateから生成される。[^generate][^agent]

# 現行の不足と見直し候補

| 観測した挙動 | 影響・まだ確認していないこと |
|---|---|
| identity directoryを消してから再生成する。空集合でもstub生成へ進む分岐がCI限定ではない | 不完全な入力で従来の設定を失う可能性。実機で再現した結果ではない |
| 古い公開鍵fileの削除を明示的に管理していない | 鍵の入替え後に旧生成fileが残り得る |
| dirsの重複、comma分割後の空要素、name/emailのpath・設定値への使用を十分に検証していない | routingの衝突や不正な生成先・設定がないとは保証できない |
| config生成側は`data.ssh_auth_sock`、SSH template側は`.paths.ssh_auth_sock`を参照 | 読んだsourceには後者の定義がない。別入力がなければ`IdentityAgent`行が出ないと読める。renderや接続は未確認 |
| SSH共通設定に`ForwardAgent yes`と`StrictHostKeyChecking accept-new`がある | 全host向けの現在の既定値。必須要件・最善の設定と認定していない |
上記はcodeからの観測で、修正済みではない。socket値はzsh側ではrootの`.ssh_auth_sock`を読むため、この不一致だけで全認証が失敗すると断定しない。[^generate][^config][^git][^ssh][^zshenv]

# 設計変更と調査結果の扱い

入力更新・失敗保護の案と代案は[convergenceのidentity節](decisions/convergence.md#identity-input)、schema・socket・SSH既定値の見直し候補は[同文書の未決事項](decisions/convergence.md#identity-constraints)を参照する。ここでは現行入力と観測した制約を正本として維持する。

WSLの認証経路は[WSL文書](platforms/wsl.md)と1Password公式の対応条件を確認する。[^op-wsl]

調査結果にはschema・件数・不一致の種類だけを残し、item JSON、実email、公開鍵と個人の対応表、認証情報を共有文書へ転記しない。検査の対象と副作用は[validation](validation.md)で選ぶ。そこで説明する検査を、文書閲覧だけで実行する必要はない。

[^config]: [ホスト入力と1Password identity取得](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoi.toml.tmpl)。
[^git]: [Git共通設定とincludeIf routing](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/git/config.tmpl)。
[^fragment]: [identity別Git設定の生成fragment](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/.chezmoitemplates/git_identity_config.tmpl)。
[^git-config]: [Git公式：条件付きincludeとSSH署名設定](https://git-scm.com/docs/git-config)。
[^op-agent]: [1Password公式：SSH agent設定と鍵の選択](https://www.1password.dev/ssh/agent/config)。
[^generate]: [identity生成と入力空集合の扱い](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/mise/repo-tasks/generate/executable_identity.tmpl)。
[^agent]: [1Password agentのitem/account選択](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/1Password/ssh/private_agent.toml.tmpl)。
[^ssh]: [SSH共通設定とsocket値の参照](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_config/ssh/config.tmpl)。
[^zshenv]: [XDG・認証用環境変数とWSLENV](https://github.com/tsubasahomma/dotfiles/blob/f4fe1fac3e0722b173b5291a06e98e1e066786f1/dot_zshenv.tmpl)。
[^op-wsl]: [1Password公式：Windows OpenSSHとWSL署名](https://www.1password.dev/ssh/integrations/wsl)。
