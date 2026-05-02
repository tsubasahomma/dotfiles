# Local glossary

## Purpose

Use this glossary for repository-specific terms that appear across local context,
surface, and workflow guidance.

## Terms

| Term | Meaning in this repository |
| --- | --- |
| source state | Files tracked in this repository and consumed by chezmoi as the editable source of workstation configuration. |
| rendered target state | Files, scripts, configuration, and local artifacts produced by chezmoi in the target home directory or host environment. |
| source-state path | A repository path using chezmoi source-state naming, such as `dot_config/**`, `private_dot_ssh/**`, or `.chezmoiscripts/**`. |
| target path | The rendered path managed or affected by chezmoi after source-state attributes and templates are evaluated. |
| generated context artifact | A generated Repomix artifact under `.context/repomix/**`; it is read-only evidence, not tracked source documentation. |
| local context layer | `docs/context/local/**`, the dotfiles-specific extension layer for repository identity, behavior boundaries, validation routing, and local routing. |
| surface capsule | A compact document under `docs/context/local/surfaces/**` that prevents predictable mistakes for one behavior-sensitive local surface. |
| workflow guidance | Local issue, pull request, validation, merge, closure, Commander, and Worker procedures under `docs/context/local/workflows/**`. |
| retired legacy surface | A former documentation surface recorded in the migration map after its durable guidance was migrated or intentionally discarded. |
| root context manifest | `AGENTS.md`, the concise repository-wide assistant entry point. |
| adapter | Vendor-specific assistant entry point such as `.github/copilot-instructions.md`; adapters should route to the LLM-agnostic context architecture. |
| 1Password identity | Repository-discovered identity metadata from prepared 1Password SSH Key items used for Git authoring, SSH signing, and SSH routing. |
| WSL2 bridge | The Windows-to-WSL2 identity and SSH agent path involving Windows 11, WSL2 Ubuntu, Windows 1Password Desktop, `op.exe`, `npiperelay.exe`, and user systemd. |
| doctor task | A repository-local mise validation or readiness check under `dot_config/mise/tasks/doctor/**`. |
| repair candidate | A current behavior that may be mutation-oriented and may need a future explicit `repair:*` decision; it is not authorization to change current tasks. |
