# Chezmoi script trigger audit

## Purpose

This document audits the current trigger-contract status of every
`.chezmoiscripts/*` entry in this dotfiles source-state repository.

The audit is read-only. It does not change script behavior, add trigger hashes,
remove trigger hashes, normalize trigger comments, or claim that inspection
output proves convergence or idempotency.

The current script-contract baseline is
[Chezmoi action graph](./action-graph.md). The evidence collection workflow is
[Chezmoi script contract inspection](./script-contract-inspection.md). The
bootstrap, 1Password, identity, SSH, and WSL2 bridge boundary is documented in
[Bootstrap and identity boundary](./bootstrap-identity-boundary.md).

## Scope and non-goals

This audit covers trigger-contract status only.

It classifies current scripts by:

- explicit trigger comments
- checksum content rendered into `run_onchange_` scripts
- other rendered content that can affect `run_onchange_` behavior
- `run_once_` content contracts
- follow-up candidates
- scripts where no action is recommended

This audit does not duplicate the full action graph table. It intentionally
omits phase, purpose, idempotency, hard-fail, soft-fallback, and validation
details that already live in the action graph.

This audit does not:

- edit `.chezmoiscripts/*`
- add, remove, or normalize trigger hashes
- change `.chezmoi.toml.tmpl`
- change `.bootstrap-identity.sh`
- change `.chezmoiexternal.toml.tmpl`
- change `.chezmoidata/*`
- change `.chezmoitemplates/*`
- change mise task behavior
- change provisioning, identity, SSH, WSL2, shell, editor, terminal, Git,
  Homebrew, mise, or GitHub Actions behavior
- edit generated `repomix-*.xml` files

## Semantics boundary

This audit uses official chezmoi script semantics:

- `run_onchange_` scripts re-run when their rendered script content changes.
- Template scripts are rendered before chezmoi decides whether their content has
  changed.
- Including another source file's checksum in rendered script content is a
  documented pattern for making that source file affect `run_onchange_`
  behavior.
- `run_once_` scripts are tracked by unique rendered content and should not be
  treated as `run_onchange_` trigger-normalization targets.

Repository-local terminology:

- `[Trigger]` is a repository-local documentation label.
- Chezmoi does not parse or require the literal `[Trigger]` label.
- A checksum comment without `[Trigger]` can still affect `run_onchange_`
  behavior when it renders into script content.
- A comment-only edit to a `run_onchange_` script changes rendered script content
  and can cause the script to re-run.

Official references:

- https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/
- https://www.chezmoi.io/reference/special-directories/chezmoiscripts/

## Evidence used

This audit is based on:

- the current action graph baseline in
  [Chezmoi action graph](./action-graph.md)
- the read-only inspection workflow in
  [Chezmoi script contract inspection](./script-contract-inspection.md)
- fresh local inspection output collected for issue #150

Fresh inspection summary:

- Current `.chezmoiscripts/*` count: 14
- `run_once`: 1 script
- `run_onchange`: 13 scripts
- `before`: 5 scripts
- `after`: 9 scripts
- Scripts without an explicit `[Trigger]` label are not automatically defects.

## Trigger-contract status categories

| Status | Meaning |
| --- | --- |
| Explicit checksum trigger | The script renders a checksum comment for a source input. The comment may or may not use the repository-local `[Trigger]` label. |
| Rendered-content dependency | The script has rendered values, branches, paths, lists, or generated content that can change the rendered script without an explicit `[Trigger]` label. |
| Dynamic rendered branch | The script renders host, CI, identity, or session-specific branches that can affect rendered script content. |
| `run_once` content contract | The script is governed by `run_once_` rendered-content semantics, not `run_onchange_` trigger semantics. |
| Follow-up candidate | A future issue could clarify or normalize documentation labels, but this audit does not require a script change. |
| No action recommended | No trigger-contract change is recommended from this audit. |

## Script trigger audit

| Script | Trigger-contract status | Evidence | Follow-up recommendation |
| --- | --- | --- | --- |
| [`.chezmoiscripts/run_onchange_before_00-backup-legacy-dots.sh.tmpl`](../../.chezmoiscripts/run_onchange_before_00-backup-legacy-dots.sh.tmpl) | Rendered-content dependency without explicit `[Trigger]` label. | The script is `run_onchange_`; rendered paths and the hardcoded legacy target list are part of script content. | No action recommended for issue #150. A future behavior-sensitive issue could review whether this script needs clearer trigger documentation, but this audit does not recommend adding a hash. |
| [`.chezmoiscripts/run_onchange_before_00-install-windows-deps.sh.tmpl`](../../.chezmoiscripts/run_onchange_before_00-install-windows-deps.sh.tmpl) | Explicit checksum trigger. | The script renders a `[Trigger]` checksum for `.chezmoidata/packages.yaml` and also renders the Windows package list. | No action recommended. |
| [`.chezmoiscripts/run_onchange_before_00-validate-session.sh.tmpl`](../../.chezmoiscripts/run_onchange_before_00-validate-session.sh.tmpl) | Dynamic rendered branch without explicit `[Trigger]` label. | The script content is driven by `.op_status` and `CI`. This is volatile session-state-adjacent evidence, not a stable source-file checksum input. | No action recommended. Do not hash volatile 1Password session state as part of this audit. |
| [`.chezmoiscripts/run_onchange_before_10-setup-infrastructure.sh.tmpl`](../../.chezmoiscripts/run_onchange_before_10-setup-infrastructure.sh.tmpl) | Explicit checksum content with mixed repository-local label style. | The macOS branch renders a Brewfile hash without `[Trigger]`; the Linux branch renders a `[Trigger]` checksum for the generated Linux package list. | Follow-up candidate only for label consistency. Do not normalize the comments or hashes in issue #150. |
| [`.chezmoiscripts/run_once_before_10-setup-workspace.sh.tmpl`](../../.chezmoiscripts/run_once_before_10-setup-workspace.sh.tmpl) | `run_once` content contract. | The script renders identity directory mappings and home-path data, but it is `run_once_`, not `run_onchange_`. | No action recommended. Do not treat this as a trigger-normalization target. |
| [`.chezmoiscripts/run_onchange_after_20-setup-runtimes.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_20-setup-runtimes.sh.tmpl) | Explicit checksum trigger. | The script renders `[Trigger]` checksums for `dot_config/mise/config.toml.tmpl` and `.chezmoidata/tools.yaml`. | No action recommended. |
| [`.chezmoiscripts/run_onchange_after_21-generate-completions.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_21-generate-completions.sh.tmpl) | Explicit checksum trigger. | The script renders a `[Trigger]` checksum for `.chezmoidata/tools.yaml`. | No action recommended. |
| [`.chezmoiscripts/run_onchange_after_22-bat-cache.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_22-bat-cache.sh.tmpl) | Explicit checksum trigger. | The script renders a `[Trigger]` checksum for the rendered Catppuccin Mocha bat theme file. | No action recommended. |
| [`.chezmoiscripts/run_onchange_after_22-vale-sync.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_22-vale-sync.sh.tmpl) | Explicit checksum trigger. | The script renders a `[Trigger]` checksum for `dot_config/vale/vale.ini.tmpl`. | No action recommended. |
| [`.chezmoiscripts/run_onchange_after_23-compile-pbfile.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_23-compile-pbfile.sh.tmpl) | Explicit checksum trigger. | The script renders a `[Trigger]` checksum for `dot_local/share/pbcopy/pbfile.swift`. | No action recommended. |
| [`.chezmoiscripts/run_onchange_after_50-converge-identities.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_50-converge-identities.sh.tmpl) | Explicit dynamic trigger content. | The script renders a `[Trigger]` value for `.ssh_keys_hash` and includes rendered per-identity key and Git config material. | No action recommended. Future identity-trigger changes should be scoped separately because identity rendering is behavior-sensitive. |
| [`.chezmoiscripts/run_onchange_after_51-sync-windows-agent.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_51-sync-windows-agent.sh.tmpl) | Explicit checksum trigger from prior behavior-sensitive follow-up. | The script now renders a `[Trigger]` checksum for `dot_config/1Password/ssh/private_agent.toml.tmpl`, preserving the WSL2-only branch. | No action recommended. This already reflects the completed narrow follow-up from issue #146. |
| [`.chezmoiscripts/run_onchange_after_52-sync-wezterm-config.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_52-sync-wezterm-config.sh.tmpl) | Explicit checksum trigger. | The script renders a `[Trigger]` checksum for `dot_config/wezterm/wezterm.lua.tmpl`. | No action recommended. |
| [`.chezmoiscripts/run_onchange_after_90-enable-services.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_90-enable-services.sh.tmpl) | Explicit checksum trigger. | The script renders a `[Trigger]` checksum for `dot_config/systemd/user/1password-bridge.service.tmpl`. | No action recommended. |

## Follow-up candidates

These candidates are not hidden requirements for issue #150.

- Clarify repository-local trigger comment labels if consistent wording is still
  desired.
- Decide whether checksum comments without `[Trigger]` should use a consistent
  repository-local label.
- Review volatile dynamic inputs separately from checksum-driven source inputs.
- Consider a focused future issue for scripts without explicit `[Trigger]`
  labels only if a behavior-sensitive trigger contract change is explicitly
  scoped.
- Keep WSL2, 1Password, SSH agent, identity routing, and service bridge changes
  out of generic trigger-label cleanup.

## Review guidance for future trigger changes

Before changing a trigger contract:

- Start from [Chezmoi action graph](./action-graph.md).
- Collect read-only evidence with
  [Chezmoi script contract inspection](./script-contract-inspection.md).
- Treat comment-only edits in `run_onchange_` scripts as behavior-sensitive
  rendered-content changes.
- Distinguish explicit checksum inputs from dynamic rendered branches.
- Do not add, remove, or normalize trigger hashes without explicit issue scope.
- Do not treat missing `[Trigger]` labels as defects by default.
- Review WSL2 paths as WSL-to-Windows bridge behavior, not generic Linux
  behavior.
- Keep inspection evidence separate from validation evidence.
- Do not claim convergence, idempotency, or CI success without command output,
  CI evidence, or explicit confirmation.
