# WSL2 surface capsule

## Purpose

Use this capsule when work touches or cites Windows 11 plus WSL2 Ubuntu behavior,
Windows interop, the 1Password SSH agent bridge, user systemd, or Windows-side
sync paths.

Keep WSL2 guidance separate from generic Linux guidance. CI is not local WSL2
validation.

## Predictable LLM failure modes

- Treating WSL2 as ordinary Linux and ignoring Windows-side dependencies.
- Treating GitHub Actions Ubuntu results as proof that local WSL2 interop works.
- Replacing `op.exe` or `npiperelay.exe` bridge assumptions with generic Unix
  SSH agent assumptions.
- Changing user systemd service behavior without local service evidence.
- Moving or normalizing Windows-side sync paths as path cleanup.
- Printing unredacted local Windows profile paths, account identifiers, or
  secret-adjacent bridge output unnecessarily.

## Behavior-sensitive boundaries

WSL2 convergence spans Linux source state, rendered Linux target state, Windows
host tools, Windows 1Password Desktop, named pipes, user systemd, SSH agent
routing, and Windows-side copied configuration.

Treat these as behavior-sensitive unless explicitly scoped:

- `op.exe` discovery and Windows 1Password Desktop assumptions;
- `npiperelay.exe` bridge path and named-pipe invocation;
- `dot_config/systemd/user/1password-bridge.service.tmpl` rendering;
- `run_onchange_after_51-sync-windows-agent.sh.tmpl` Windows-side sync behavior;
- WSL-specific conditional branches in templates and scripts;
- local SSH agent socket routing used by Git and SSH.

## Evidence and routing links

- [Local repository profile](../profile.md)
- [Local behavior boundaries](../boundaries.md)
- [Local validation map](../validation.md)
- [Identity surface capsule](./identity.md)
- [README](../../../../README.md)
- [`dot_config/systemd/user/1password-bridge.service.tmpl`](../../../../dot_config/systemd/user/1password-bridge.service.tmpl)
- [`.chezmoiscripts/run_onchange_after_51-sync-windows-agent.sh.tmpl`](../../../../.chezmoiscripts/run_onchange_after_51-sync-windows-agent.sh.tmpl)
- [`dot_config/1Password/ssh/private_agent.toml.tmpl`](../../../../dot_config/1Password/ssh/private_agent.toml.tmpl)

## Validation routing

For documentation-only capsule or routing edits, use baseline documentation
validation from [Local validation map](../validation.md).

If the change touches WSL2 bridge behavior, Windows interop, user systemd,
Windows-side sync paths, SSH agent routing, or WSL-specific rendered branches,
local WSL2 evidence is required. Do not substitute GitHub Actions CI for local
WSL2 convergence evidence.

## Out of scope

This capsule does not authorize bridge rewrites, service changes, Windows path
changes, package provisioning changes, identity behavior changes, or use of CI as
proof of local WSL2 convergence.
