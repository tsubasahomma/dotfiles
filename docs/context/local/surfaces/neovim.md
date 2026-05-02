# Neovim surface capsule

## Purpose

Use this capsule when work touches or cites Neovim source state, LazyVim
configuration, provider health, plugin lockfile synchronization, or headless
integration behavior.

Keep Neovim guidance local to this dotfiles repository. Do not import generic
editor advice unless current repository evidence and the active issue require it.

## Predictable LLM failure modes

- Treating this repository as a general Neovim distribution instead of a
  chezmoi-rendered LazyVim-based configuration.
- Editing rendered Neovim target files instead of `dot_config/nvim/**` source
  state.
- Changing plugin selections, provider paths, or `lazy-lock.json` as incidental
  cleanup.
- Hand-editing lockfile state instead of using the repository's update and
  integration paths.
- Assuming provider health without `doctor:nvim` or equivalent evidence when
  Neovim behavior changes.
- Applying generic keymap, LSP, or plugin recommendations without local scope.

## Behavior-sensitive boundaries

Neovim behavior is produced from chezmoi source-state templates, LazyVim plugin
configuration, mise-managed tools, provider resolution, and lockfile state.

Treat these as behavior-sensitive unless explicitly scoped:

- `dot_config/nvim/**`, especially `.tmpl` files and `lazy-lock.json`;
- `dot_config/mise/tasks/integrate/executable_nvim.tmpl`;
- `dot_config/mise/tasks/doctor/executable_nvim.tmpl`;
- `dot_config/mise/tasks/update/executable_lazy-lock.tmpl`;
- Node, Python, and Neovim provider assumptions resolved through mise;
- headless integration commands and plugin restoration behavior.

## Evidence and routing links

- [Repository operating contract](../../repo.md)
- [`dot_config/nvim/`](../../../../dot_config/nvim/)
- [`dot_config/nvim/lazy-lock.json`](../../../../dot_config/nvim/lazy-lock.json)
- [`dot_config/mise/tasks/integrate/executable_nvim.tmpl`](../../../../dot_config/mise/tasks/integrate/executable_nvim.tmpl)
- [`dot_config/mise/tasks/doctor/executable_nvim.tmpl`](../../../../dot_config/mise/tasks/doctor/executable_nvim.tmpl)
- [`dot_config/mise/tasks/update/executable_lazy-lock.tmpl`](../../../../dot_config/mise/tasks/update/executable_lazy-lock.tmpl)
- [README](../../../../README.md)

## Validation routing

For documentation-only capsule or routing edits, use baseline documentation
validation from the [Repository operating contract](../../repo.md).

If a change touches Neovim source state, rendered templates, providers, plugin
configuration, lockfile state, or integration behavior, route validation to the
relevant Neovim checks. Consider `mise run integrate:nvim`, `mise run doctor` or
`doctor:nvim`, headless Neovim startup, and rendered-output inspection according
to the actual touched files.

## Out of scope

This capsule does not authorize plugin changes, keymap changes, lockfile edits,
provider changes, generic editor recommendations, runtime version changes, or
Neovim behavior changes.
