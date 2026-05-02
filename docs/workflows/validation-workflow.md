# Validation workflow

## Purpose

Use validation to prove that a change is correct for its touched surface.

Validation requirements are what should be checked. Validation evidence is what
was actually observed.

Do not claim validation passed unless command output, CI evidence, or explicit
confirmation exists.

## Requirements vs evidence

Keep these separate:

- Required validation: checks that should be run before completion.
- Completed validation: checks that have evidence.
- Skipped validation: checks not run, with the reason.
- Failed validation: checks that failed, including retry evidence if retried.

Do not mark a checkbox complete because a check is expected to pass.

## Baseline checks

Common checks:

```sh
git diff --check
pre-commit run --all-files
repomix
```

Use the explicit Repomix fallback only when needed:

```sh
repomix --config repomix.config.json
```

## Documentation-only validation

For documentation-only changes, usually run:

```sh
git diff --check
pre-commit run --all-files
```

If the change adds or moves many Markdown links, also run the Markdown relative
link helper below.

If the change affects LLM routing or Repomix guidance, also run:

```sh
repomix
```

## LLM and workflow documentation validation

For documentation changes that affect LLM or workflow guidance, use:

```sh
git diff --check
pre-commit run --all-files
repomix
```

Also run the Markdown relative link helper when the change adds, removes, or
updates repository-relative links.

Do not require `chezmoi diff` unless `.chezmoiignore.tmpl` or other
rendered-output-sensitive template files change.

## Documentation impact scanning

Plan a documentation impact scan when a change deletes, renames, or
semantically changes code, scripts, mise tasks, source-state files, operator
commands, documented behavior, or validation entry points. The scan checks
whether durable docs still describe the old name, behavior, command, phase, task,
or file as current.

Choose search terms from the changed surface, such as the old filename, new
filename, task name, command name, script phase, documented behavior phrase, and
operator-facing command. Focus on likely documentation surfaces first:

```sh
rg -n "old-name|new-name|task-name|command-name" README.md AGENTS.md .github docs
```

The scan is validation planning, not permission to broaden the patch. Fix stale
current-scope documentation that would make the PR misleading. Report adjacent
or non-blocking findings as follow-ups unless the issue explicitly scopes them.

## Markdown relative link validation

Use this helper when documentation changes introduce repository-relative links:

```sh
python - <<'PY'
from pathlib import Path
import re

root = Path(".").resolve()
files = list(Path("docs").rglob("*.md")) + [
    Path("AGENTS.md"),
    Path("README.md"),
    Path(".github/copilot-instructions.md"),
    Path(".github/pull_request_template.md"),
]

link_re = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
errors = []

for file in files:
    if not file.exists():
        continue
    text = file.read_text()
    for match in link_re.finditer(text):
        target = match.group(1)
        if (
            target.startswith(("http://", "https://", "mailto:"))
            or target.startswith("#")
        ):
            continue
        path = target.split("#", 1)[0]
        if not path:
            continue
        resolved = (file.parent / path).resolve()
        try:
            resolved.relative_to(root)
        except ValueError:
            errors.append((file, target, "outside repository"))
            continue
        if not resolved.exists():
            errors.append((file, target, "missing"))

if errors:
    for file, target, reason in errors:
        print(f"{file}: {target} -> {reason}")
    raise SystemExit(1)

print("All checked Markdown links resolve.")
PY
```

## Repomix routing validation

Run `repomix` when changes affect:

- `repomix.config.json`
- `docs/context/repomix/instructions.md`
- LLM routing docs
- snapshot guidance
- repository context generation

Check that the command completes and that generated snapshots include the
expected guidance and writes generated output under `.context/repomix/**` without
including generated `repomix-*.xml` artifacts as source.

## Chezmoi template and rendered-output validation

Use `chezmoi diff` when changes touch:

- `.chezmoiignore.tmpl`
- `.chezmoi.toml.tmpl`
- `.chezmoiscripts/*`
- `.chezmoitemplates/*`
- rendered configuration templates
- source files where whitespace trimming affects rendered output

Use `chezmoi verify` when checking target drift against source-state
expectations.

Do not require full `chezmoi init --source="$PWD" --apply` unless the issue
explicitly justifies heavyweight apply validation in a safe environment.

## Identity-sensitive validation

For changes touching identity, 1Password, SSH signing, SSH agent bridging, or
generated identity files, validation must be explicitly scoped.

Potential checks may include:

- `chezmoi diff`
- `mise run doctor:identity`
- targeted file inspection
- CI evidence when applicable

Do not request secret values or unredacted private key material.

## Neovim validation

For Neovim behavior changes, choose checks that match the change.

Potential checks include:

- `mise run integrate:nvim`
- `mise run doctor:nvim`
- targeted `nvim --headless` commands
- inspection of `dot_config/nvim/lazy-lock.json` when plugin state changes

Do not run Neovim checks for unrelated documentation-only changes.

## WezTerm validation

For WezTerm template or WSL sync changes, use rendered-output inspection and
targeted commands appropriate to the environment.

Do not assume macOS and WSL behavior are equivalent.

## zsh and shell validation

For shell changes, consider:

- `pre-commit run --all-files`
- `shfmt` through pre-commit for pure shell files
- rendered shell inspection for `.tmpl` files
- targeted shell syntax checks when appropriate

Templates may not be valid shell before rendering, so avoid applying pure shell
linters to template source without understanding the surface.

## mise and toolchain validation

Use `mise run doctor` when changes touch setup instructions, toolchain behavior,
mise tasks, rendered configuration behavior, or validation entry points.

Do not require `mise run doctor` for documentation-only changes that do not
alter setup, toolchain, rendered configuration, or task behavior.

## GitHub Actions validation

For GitHub Actions changes, local validation is not enough.

Use:

- YAML syntax checks through pre-commit when available
- PR GitHub Actions results
- focused review of changed workflow semantics

Do not claim CI passed until the user provides CI evidence.

## Documentation impact and stale-reference reporting

When a docs impact scan finds stale references, report how they were handled:

- updated in the current patch because they were current-scope and misleading
- reported as non-blocking follow-ups because they were useful but outside scope
- left unchanged because they were historical records or intentionally scoped
  decision logs

Do not mark the scan complete unless the searched terms and touched surfaces are
clear from command output, review notes, or maintainer confirmation.

## Avoid heavyweight checks by default

Avoid heavyweight checks when lighter evidence is sufficient.

Examples:

- Do not require `chezmoi diff` for pure `docs/` changes.
- Do not require `mise run doctor` for docs that do not change setup behavior.
- Do not require full apply flows for documentation or router-only edits.
