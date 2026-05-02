# Repomix context routing

## Purpose

This directory contains tracked guidance for generating and consuming Repomix
context artifacts.

Use [Repomix instruction router](./instructions.md) as the instruction file
configured by `repomix.config.json`.

## Generated output

Repomix generated output is routed to [`.context/repomix/`](../../../.context/repomix/).
Generated output in that directory is read-only evidence and must not be edited
directly or tracked as source documentation.

## Scope boundary

This directory contains Repomix consumption guidance only. Reusable operating
rules belong in [`../kernel.md`](../kernel.md), reusable output contracts belong
in [`../protocols.md`](../protocols.md), regression cases belong in
[`../evals.md`](../evals.md), dotfiles-specific repository rules belong in
[`../repo.md`](../repo.md), surface routing belongs in
[`../surfaces.md`](../surfaces.md), and workflow procedure belongs in
[`../workflows.md`](../workflows.md).
