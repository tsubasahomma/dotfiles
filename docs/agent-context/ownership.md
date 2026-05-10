# Ownership And Installer Safety Contract

This document defines the portable ownership model for installing agent-context
contracts into a consumer repository.

The public distribution model is one installer command. It is not a local
package manager lifecycle, does not expose public `init` or `sync` subcommands,
and does not create a consumer-side lock file or equivalent state file.

## Terms

- **Source repository**: the repository that publishes the portable agent
  context package.
- **Source channel**: the configured branch, tag, or commit selector requested
  by a consumer. The default channel is `main`.
- **Resolved source commit**: the immutable full commit SHA resolved from the
  configured source channel for one installer run.
- **Consumer repository**: the destination repository where the installer is run.
- **Source-owned portable payload**: `AGENTS.md` plus
  `docs/agent-context/**`, copied from the resolved source commit and owned by
  the source repository.
- **Consumer-owned local context**: `docs/project/**`, owned by the consumer
  repository after creation.
- **Missing-only payload**: destination-shaped starter files under
  `payload/missing-only/**`, copied only when the mirrored destination file is
  absent.
- **Vendor routing shim**: a thin missing-only instruction file for a specific
  agent or platform that routes readers back to `AGENTS.md`,
  `docs/agent-context/README.md`, and relevant `docs/project/**` files.
- **Platform collaboration surface**: a platform-native issue form, pull request
  template, review form, workflow template, or similar collaboration file.

## Public Installer

The public installer is the root `install.sh` command exposed by the source
repository:

```sh
curl -fsSL <source-install-url> | sh
```

The command runs from a consumer repository root. The same command handles
first-time adoption and later refreshes.

For each run, the installer MUST:

1. resolve the configured source channel to a full commit SHA;
2. download one source archive for that resolved commit;
3. copy the source-owned portable payload from that archive;
4. seed missing-only payload files only when destination files are absent;
5. leave no consumer-side package state file.

The installer MAY provide diagnostic options such as `--dry-run`, but public
adoption and refresh do not require subcommands.

## Ownership Categories

| Category | Source path | Destination path | Installer behavior |
| --- | --- | --- | --- |
| Source-owned portable payload | `AGENTS.md` | `AGENTS.md` | Overwrite from the resolved source commit on every run. |
| Source-owned portable payload | `docs/agent-context/**` | `docs/agent-context/**` | Replace from the resolved source commit on every run. |
| Consumer-owned local context | `payload/missing-only/docs/project/**` | `docs/project/**` | Create absent files only; preserve existing files. |
| Missing-only vendor shim | `payload/missing-only/CLAUDE.md` | `CLAUDE.md` | Create only if absent; preserve existing files. |
| Missing-only vendor shim | `payload/missing-only/GEMINI.md` | `GEMINI.md` | Create only if absent; preserve existing files. |
| Missing-only vendor shim | `payload/missing-only/.github/copilot-instructions.md` | `.github/copilot-instructions.md` | Create only if absent; preserve existing files. |
| Platform collaboration surface | None by default | `.github/ISSUE_TEMPLATE/**`, `.github/pull_request_template.md`, `.gemini/config.yaml`, `.gemini/styleguide.md`, or similar | Not installed by default. |

## Source-Owned Portable Payload

`AGENTS.md` and `docs/agent-context/**` are maintained by the source repository.
Consumer repositories SHOULD NOT place local identity, commands, secrets policy,
workflow exceptions, validation commands, or platform-specific collaboration
rules in these paths.

Because these paths are source-owned, the installer overwrites or replaces them
from the resolved source commit on every run. A consumer that needs local policy
MUST put that policy under `docs/project/**` or another explicitly documented
consumer-owned local extension path.

## Missing-Only Seeding

Missing-only seeding is file-level:

- if the mirrored destination file is absent, the installer MAY create it;
- if the mirrored destination file exists, the installer MUST preserve it;
- the installer MUST NOT overwrite, patch, delete, rename, diff-apply, merge,
  or track previous content for missing-only files.

Missing-only behavior does not depend on whether existing content resembles the
source starter file. Existing files are consumer-owned.

`payload/missing-only/**` mirrors consumer destination paths. It is not active
context for this source repository and MUST NOT be read as this repository's
local project extension.

## Vendor Routing Shims

Vendor shims are thin instruction-discovery files. They MAY be seeded
missing-only so agent-specific tools can find the portable and local context.

Vendor shims MUST route readers to:

- the root `AGENTS.md`;
- `docs/agent-context/README.md`;
- relevant files under `docs/project/**` when present.

Vendor shims MUST NOT duplicate portable doctrine, embed repository-local facts,
or become a substitute for the portable contract set. Existing vendor files in a
consumer repository are consumer-owned and MUST NOT be overwritten by the
installer.

## Platform Collaboration Surfaces

Platform collaboration surfaces are not installed by default. They often encode
review policy, issue routing, release gates, labels, checkboxes, or other local
workflow details that need consumer ownership.

The simplified installer MUST NOT install default payload for:

- `.github/ISSUE_TEMPLATE/**`;
- `.github/pull_request_template.md`;
- `.gemini/config.yaml`;
- `.gemini/styleguide.md`.

If a consumer wants platform collaboration surfaces, that workflow belongs to
consumer-owned local policy or a separate explicitly scoped mechanism.

## State And Safety Boundaries

The installer MUST NOT create `agent-context.lock.json` or an equivalent
consumer-side state file. It MUST NOT require previous installer state to decide
whether a missing-only file may be changed. It MUST NOT expose public
`init`/`sync` lifecycle commands.

Before writing any source-owned or missing-only destination, the installer MUST
refuse unsafe destination parents. Unsafe parents include symlinked parent
components and parent components that exist as files instead of directories.
Refusal preserves the target-repository boundary and prevents partial writes
outside the intended managed paths.

Without consumer-side package state, the safety model is simple:

- source-owned portable payload is refreshed from the resolved source commit;
- missing-only payload is created only when destination files are absent;
- consumer-owned local context and existing vendor files are preserved;
- platform collaboration surfaces remain outside the default installer.

## Boundary Rules

Ownership and installer safety rules own:

- the source-owned portable payload boundary;
- the consumer-owned local context boundary;
- missing-only file-level seeding behavior;
- vendor shim installation boundaries;
- default exclusion of platform collaboration surfaces;
- the absence of consumer-side package state files and public lifecycle
  subcommands.

Ownership and installer safety rules MUST NOT own:

- repository identity, local commands, local workflow exceptions, branch policy,
  release policy, or secrets policy details;
- platform-specific issue or pull request template content;
- agent-specific runtime behavior beyond the vendor-shim routing boundary;
- portability-lint implementation details;
- validation command selection or CI job names.
