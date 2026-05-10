# Core Contract

## Purpose

This document defines the portable core surface for agent collaboration
contracts. It gives later contracts a stable place to extend the shared rules
without mixing reusable guidance with project-local facts or tool-specific
payloads.

## Owns

The core contract owns:

- the boundary between portable contracts, project-local extensions,
  missing-only routing shims, platform collaboration surfaces, and tooling;
- the expectation that agents inspect current repository evidence before acting;
- the expectation that durable claims are backed by observed evidence;
- the rule that portable contracts remain repository-agnostic and
  vendor-agnostic;
- the reading order from the root entry point to this contract set and then to
  any consumer-owned project extension.

## Must Not Own

The core contract MUST NOT own:

- repository names, maintainers, host paths, local commands, secrets, or
  operational assumptions;
- artifact schemas or detailed validation vocabulary;
- detailed thread-role, handoff, or workflow rules;
- vendor shim payload text, collaboration-surface payloads, or
  platform-specific runtime behavior;
- installer implementation details or portability-lint rules.

Those topics belong to their dedicated contracts, project extensions,
consumer-owned platform surfaces, or tools.

## Extension Path

Later detailed contracts should extend this file only when they need to add a
portable principle shared across the whole contract set. Topic-specific details
should be added to the owning document:

- artifact rules in [artifacts.md](artifacts.md);
- source precedence and trust-boundary rules in [sources.md](sources.md);
- agent-authored output rules in [outputs.md](outputs.md);
- workflow rules in [workflows.md](workflows.md);
- validation rules in [validation.md](validation.md);
- evidence-packing rules in [evidence-packing.md](evidence-packing.md);
- evaluation rules in [evaluations.md](evaluations.md);
- ownership and installer safety rules in [ownership.md](ownership.md).
