# dotfiles

[![Compliance](https://github.com/tsubasahomma/dotfiles/actions/workflows/compliance.yml/badge.svg)](https://github.com/tsubasahomma/dotfiles/actions/workflows/compliance.yml)
[![Built with chezmoi](https://img.shields.io/badge/built%20with-chezmoi-50b0f0.svg)](https://chezmoi.io/)
[![Managed with mise](https://img.shields.io/badge/managed%20with-mise-blue.svg)](https://mise.jdx.dev/)

This repository is a chezmoi-managed source-state repository for personal
workstation configuration.

It uses chezmoi to render host-specific dotfiles, mise to install declared
runtime tools, and 1Password to provide identity metadata for Git, SSH signing,
and SSH agent routing.

## Overview

Use this repository to bootstrap and maintain a converged workstation on macOS
or Windows 11 with Windows Subsystem for Linux 2 (WSL2) Ubuntu 24.04+.

The README is the first-run entry point. It explains the supported bootstrap
path and links to focused contract documents for behavior details.

## Bootstrap model

First-run bootstrap has two separate prerequisite tracks:

- `GITHUB_TOKEN` covers bootstrap-time GitHub access for mise tool resolution
  and GitHub-hosted metadata or downloads.
- 1Password identity preparation covers full identity, Git, SSH signing, SSH
  agent, and identity-routing convergence.

You can supply `GITHUB_TOKEN` manually. You don't need to source it from
1Password, and it doesn't replace the required 1Password identity prerequisites.

## Bootstrap a new machine

### Before you start

Prepare these generic requirements before running the bootstrap command:

- A shell with `sh` and `curl` available.
- A GitHub token for bootstrap-time access.
- 1Password Desktop installed and signed in.
- 1Password CLI integration enabled.
- Required 1Password SSH Key items created with the repository-defined tags and
  fields.
- Pre-existing unmanaged dotfiles reviewed, backed up, or removed.
- Any host-specific prerequisites for the supported host path you are
  bootstrapping.

> [!IMPORTANT]
> This repository doesn't automatically move or back up pre-existing unmanaged
> dotfiles during first apply. Review, back up, or remove conflicting regular
> files before running `chezmoi init --apply`. In particular, an existing
> regular `~/.ssh/config` may conflict with the managed compatibility symlink
> that routes SSH configuration through the XDG config path.

### Create a GitHub token

Create a token by following GitHub's official
[fine-grained personal access token documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token).

Use the minimum access needed for this repository and the GitHub-hosted resources
that mise resolves during bootstrap. Keep the token value available for the
first-run command.

> [!IMPORTANT]
> Treat the token as a secret. Don't paste a real token into issue comments,
> pull request descriptions, logs, or shared validation output.

### Prepare 1Password

Full identity, Git, SSH signing, and SSH agent convergence requires prepared
1Password identity prerequisites:

- Install 1Password Desktop and sign in.
- Enable 1Password CLI integration.
- Create the required SSH Key items in 1Password.

Each repository-managed identity comes from a 1Password SSH Key item with the
`dotfiles-ssh-key` tag. The item must include the standard SSH Key public key
metadata and these repository-defined fields:

| Location | Name                 | Purpose                                                          |
| -------- | -------------------- | ---------------------------------------------------------------- |
| Tag      | `dotfiles-ssh-key`   | Marks SSH Key items for identity discovery.                      |
| Section  | `dotfiles`           | Groups repository-specific identity metadata.                    |
| Field    | `dotfiles_git_name`  | Git author name for the identity.                                |
| Field    | `dotfiles_git_email` | Git author email for the identity.                               |
| Field    | `dotfiles_git_dirs`  | Comma-separated directory globs for scoped Git identity routing. |

For identity boundaries, use the
[Surface operating contract](./docs/context/surfaces.md) and the
[Repository operating contract](./docs/context/repo.md).

### Prepare your host

Host-specific prerequisites are separate from the generic first-run command.
Prepare only the supported path that applies to the host you are bootstrapping.

> [!NOTE]
> This README documents only macOS and Windows 11 with WSL2 Ubuntu 24.04+.
> Other Linux distributions aren't currently supported first-run targets.

#### macOS

Grant Full Disk Access to the terminal emulator when the host needs to provision
or inspect protected directories.

#### Windows 11 with WSL2 Ubuntu 24.04+

Prepare Windows 11 with WSL2 Ubuntu 24.04+ as a WSL-to-Windows bridge path,
not as generic Linux.

WSL2 convergence requires:

- Windows 11 as the host operating system.
- Ubuntu 24.04 or later as the WSL2 distribution.
- Windows interop commands available from WSL2, including `cmd.exe`,
  `powershell.exe`, `wslpath`, and `winget.exe`.
- Windows-side 1Password Desktop installed and signed in.
- 1Password CLI integration enabled on the Windows side.
- `op.exe` discoverable from WSL2.
- `npiperelay.exe` installed and discoverable from WSL2.
- User-level systemd available for the 1Password bridge service path.
- Non-interactive `sudo` configured in WSL2 for Ubuntu package provisioning.

Install `npiperelay.exe` on the Windows side when it isn't already available:

```zsh
winget.exe install albertony.npiperelay
```

Configure non-interactive `sudo` before first-run package provisioning. The
WSL2 Ubuntu provisioning path checks `sudo -n true` before installing system
packages.

Use `sudo visudo` and add a rule for the target WSL2 Ubuntu user:

```sudoers
<linux-username> ALL=(ALL) NOPASSWD:ALL
```

Replace `<linux-username>` with the WSL2 Ubuntu user that runs
`chezmoi init --apply`.

For WSL2 validation boundaries, use the
[Surface operating contract](./docs/context/surfaces.md) and the
[Repository operating contract](./docs/context/repo.md).

### Run chezmoi init

Run the supported first-run bootstrap command:

```zsh
GITHUB_TOKEN=<token> sh -c "$(curl -fsLS https://get.chezmoi.io)" -- init --apply <github-username>
```

Replace `<token>` with the GitHub token value and `<github-username>` with the
GitHub account that owns this dotfiles repository.

### Verify convergence

After bootstrap completes, run the repository health check:

```zsh
mise run doctor
```

If the check fails, follow the task output and the focused contract documents
linked below.

## Maintain this repository

After bootstrap completes, use these commands:

```zsh
mise run doctor
chezmoi verify
mise run integrate:nvim
mise run update:lazy-lock
```

Use focused issues and pull requests for behavior changes. Keep documentation
changes scoped to the issue that authorizes them.

## Troubleshoot first-run failures

Use the failing surface to choose the next check:

- GitHub access or download failures: recreate the GitHub token with the minimum
  required read access and retry the bootstrap command.
- 1Password missing or locked: sign in to 1Password Desktop, enable
  1Password CLI integration, and confirm the required SSH Key item metadata
  exists.
- WSL2 Ubuntu package provisioning failures: confirm non-interactive `sudo`
  with `sudo -n true`, then rerun `chezmoi apply`.
- WSL2 bridge failures: review Windows interop, `op.exe`, `npiperelay.exe`, user
  systemd, and SSH agent bridge state with the WSL2 contract document.
- Post-bootstrap drift: run `mise run doctor` and use the focused contract
  documents to route the failure.

## Reference documentation

Use these focused documents when the README isn't enough:

| Document | Use it for |
| --- | --- |
| [Context architecture](./docs/context/README.md) | Repository context architecture and routing. |
| [Repository operating contract](./docs/context/repo.md) | Source-state boundaries, behavior-sensitive repository boundaries, supported host posture, and validation baseline. |
| [Surface operating contract](./docs/context/surfaces.md) | Chezmoi, mise, WSL2, identity, Neovim, and GitHub Actions surface routing, evidence, and validation boundaries. |

External references:

- [chezmoi documentation](https://www.chezmoi.io/user-guide/command-overview/)
- [mise documentation](https://mise.jdx.dev/)
- [1Password CLI documentation](https://developer.1password.com/docs/cli/)

## Safety boundaries

This README is documentation only. It doesn't change provisioning, identity,
1Password, SSH, WSL2, shell startup, Neovim, WezTerm, Starship, Git, Homebrew,
mise, GitHub Actions, CI, package lists, tool versions, runtime versions,
dependencies, or lockfiles.

Don't edit generated `repomix-*.xml` files or Repomix output under
`.context/repomix/**`. Treat Repomix snapshots as read-only repository evidence.

Don't treat GitHub Actions CI as proof of local WSL2 convergence. Local
Windows 11 and WSL2 health depends on interactive Windows interop, 1Password
Desktop state, SSH agent bridge state, user systemd behavior, and host runtime
state.
