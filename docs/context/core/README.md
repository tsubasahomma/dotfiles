# Core context guidance

## Purpose

This directory contains reusable, repository-agnostic context guidance for
LLM-assisted maintenance.

Copy this layer to another repository when the target repository wants shared
rules for evidence handling, routing, output formats, review classification,
validation reporting, generated artifacts, drift control, and out-of-scope
findings.

## Core documents

- [Context principles](./principles.md): reusable context architecture,
  routing, scope, maintenance, and out-of-scope finding principles.
- [Evidence discipline](./evidence.md): source hierarchy, unknown-state rules,
  validation evidence, generated artifacts, and sensitive data handling.
- [Output discipline](./output.md): output format selection, strict patch rules,
  guarded scripts, non-patch deliverables, and whitespace discipline.
- [Review discipline](./review.md): review priorities, finding classification,
  validation review, drift control, and follow-up handling.

## Reusable boundary

Core guidance should describe durable rules that transfer across repositories.
Keep repository-specific identity, behavior boundaries, domain constraints,
workflow procedures, and tool-specific operating details in the local context
layer instead of duplicating them here.

Before adding guidance to this layer, remove repository-specific nouns,
host-specific assumptions, operator-specific procedures, and issue-specific
history. Preserve the reusable rule, not the old document shape.
