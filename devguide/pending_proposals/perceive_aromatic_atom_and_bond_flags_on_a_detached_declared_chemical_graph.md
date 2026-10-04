---
summary: Perceive aromatic atom and bond flags on a detached declared chemical graph
issue: uibcdf/molsysmt#314
status: active
opened: 2026-10-04
closed:
verification: inspected
area: [physchem]
guard:
normative:
blocked_by: []
supersedes: []
---

# Perceive aromatic atom and bond flags on a detached declared chemical graph

**Reported:** 2026-10-04, while designing chemical AutoDock typing under
uibcdf/molsysmt#222.
**Status:** Active; contract design and implementation are in progress.

## What

Expose aromatic atom and bond perception as a general physchem tool, independent
of docking, through an explicitly documented optional RDKit aromaticity model.
Existing get_aromatic_rings consumes stored flags; it does not fill missing ones.

## How

Resolve a complete selected chemical graph, preserve its source axes and chemistry,
and use a detached provider graph. Validate elements, charge/radical prerequisites,
covalent orders and known aromatic contradictions before returning aligned flags,
source indices, state, model and original producer provenance. Match the full graph
before filtering; do not guess aromaticity from ring planarity or atom names.

## Why

SDF may supply complete Kekule orders without stored aromatic flags. AutoDock typing
and future general chemical analyses need auditable aromatic perception. Hiding it
inside a typing function would duplicate a reusable chemical operation.

## What is measured and what is assumed

**Inspected:** Existing get_aromatic_rings and the chemistry-aware RDKit conversion
confirm the ownership boundary and provider route. No runtime qualification is
claimed yet. Model coverage and failure behavior require independent controls.

## What was refuted

A ring alone, planar coordinates and a residue name are not aromaticity evidence.
Changing the source ChemicalStates during a read-only analysis is rejected.

## Scope and exclusions

Detached chemical aromaticity flags, not state repair, graph completion, protonation,
metal typing, geometric pi interactions or a new competing chemical store.

## Acceptance criteria

- Known aliphatic, aromatic and fused-ring graphs yield expected aligned flags.
- Unsupported/incomplete/contradictory chemistry fails without mutation.
- Forms, state/selection axes, empty results and original provider versions are
  documented and tested; source structures need not be loaded for numeric queries.

## Dependencies and risks

Consumer: uibcdf/molsysmt#222. Scientific evidence must name the exact provider
model and distinguish implementation controls from physical accuracy.
