---
summary: Generate 3D conformers for a fixed small-molecule chemical state
issue: uibcdf/molsysmt#219
status: open
opened: 2026-09-22
closed:
verification: inspected
area: [build, structure]
guard:
normative:
blocked_by: []
supersedes: []
---

# Generate 3D conformers for a fixed small-molecule chemical state

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Open; MolSysMT proposal is post-1.0.

## What

Generate one or more 3D conformations without changing the chosen ligand chemical state.

## How

Use a lazy optional chemistry backend, preserve the molecular graph and atom IDs, state seed and algorithm, and return distinct structure coordinates in MolSysMT units.

## Why

MolSysMT stores conformations but has no general public operation identified for generating them from a fixed ligand graph.

## What is measured and what is assumed

**Inspected:** Source search found no public conformer-generation operation; feasibility and scientific coverage are not yet measured.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Combining conformer generation with tautomer or stereoisomer enumeration would obscure whether chemistry or geometry changed.

## Scope and exclusions

A fixed, chemically complete small-molecule state; no state enumeration, docking search, or guarantee for all chemistries.

## Acceptance criteria

- The same graph and atom identity survive deterministic seeded generation.
- Unsupported chemistry and failed embedding return explicit diagnostics; generated coordinates use nanometers.

## Dependencies and risks

Related tracked work: None established.
Cross-component implementation links: uibcdf/dockingmt#4.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.
