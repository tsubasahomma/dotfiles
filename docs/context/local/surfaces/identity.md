# Identity surface capsule

## Purpose

Use this capsule when work touches or cites 1Password identity metadata,
generated Git identity files, SSH signing, scoped Git identity routing, SSH agent
behavior, or secret-adjacent local evidence.

Keep identity guidance strict and redaction-aware. Generated identity outputs are
behavior-sensitive evidence, not safe material to copy into docs.

## Predictable LLM failure modes

- Treating 1Password item metadata as interchangeable labels instead of routing
  keys for generated identity behavior.
- Reading generated identity files as source of truth instead of repository data
  and templates.
- Printing account IDs, item IDs, key material, local profile paths, or SSH agent
  output when structural evidence would be enough.
- Changing SSH signing, `allowed_signers`, or scoped Git identity includes as
  incidental cleanup.
- Assuming locked or missing 1Password state in CI proves local workstation
  behavior.
- Collapsing WSL2 bridge behavior into generic identity validation.

## Behavior-sensitive boundaries

Identity convergence combines 1Password SSH Key item metadata, chezmoi template
data, generated public key files, generated Git identity includes,
`allowed_signers`, SSH config routing, and SSH agent availability.

Treat these as behavior-sensitive unless explicitly scoped:

- `.chezmoidata/**` identity fields and schema assumptions;
- `.chezmoitemplates/git_identity_config.tmpl`;
- `.chezmoiscripts/run_onchange_after_50-converge-identities.sh.tmpl`;
- `dot_config/1Password/ssh/private_agent.toml.tmpl`;
- `dot_config/ssh/**` routing and `core.sshCommand` assumptions;
- generated Git identity includes, generated public keys, and
  `allowed_signers` content.

## Evidence and routing links

- [Local behavior boundaries](../boundaries.md)
- [Local validation map](../validation.md)
- [Bootstrap and identity boundary](../../../chezmoi/bootstrap-identity-boundary.md)
- [Chezmoi data contract boundary](../../../chezmoi/data-contract-boundary.md)
- [WSL2 surface capsule](./wsl2.md)
- [`dot_config/mise/tasks/doctor/executable_identity.tmpl`](../../../../dot_config/mise/tasks/doctor/executable_identity.tmpl)
- [`.chezmoitemplates/git_identity_config.tmpl`](../../../../.chezmoitemplates/git_identity_config.tmpl)

## Validation routing

For documentation-only capsule or routing edits, use baseline documentation
validation from [Local validation map](../validation.md).

If a change touches identity data, templates, generated identity routing, SSH
signing, SSH config, or agent behavior, validation must use redacted structural
evidence. Prefer rendered-output inspection, scoped Git config inspection,
`doctor:identity`, and host-specific checks that match the changed surface.

## Out of scope

This capsule does not authorize exposing secrets, changing 1Password metadata
contracts, changing generated identity file names, changing SSH signing, changing
Git identity routing, changing SSH agent bridge behavior, or editing generated
identity outputs directly.
