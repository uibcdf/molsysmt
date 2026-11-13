---
summary: OpenMM coordinate projections lose structure axes and atom correspondence
issue: uibcdf/molsysmt#735
status: active
opened: 2026-11-12
closed:
severity: high
verification: reproduced
area: [form, extract, units]
guard: tests/form/openmm_PDBFile/test_ensemble_axes.py
normative: devguide/forms_and_conversions.md
blocked_by: []
supersedes: []
---

# Coherent OpenMM coordinate projections

## What

The bounded #727 review reproduces twelve failures on e6e81533c. PDBFile
queries have an unadvertised count getter and read only the first model;
subset extraction imports a nonexistent box getter. Same-form adapter
conversion reuses the input even when its copy flag requests independence.
Modeller subsets retain source-sorted unique topology but unsorted repeated
coordinates with an extra structure axis; copies share the source topology.

## How

A deterministic four-atom hierarchy is written in memory as three PDB models
with distinguishable coordinates and a common box. Public queries, extraction
and conversion exercise nonconsecutive structures [2, 0, 2], atom selection
[3, 1, 1] and both nm/ps and pm/fs. All twelve original controls fail without
fixture or provider errors. The receipt will retain exact paths and outcomes.

## Why

A valid-looking Modeller can associate an atom with another atom's position.
PDB models can disappear silently. These are admitted correctness/data-integrity
repairs, not optional new engines or expanded scientific scope. Native conversion
must also project duplicate atom requests coherently in inventory and geometry.

## Repair and limits

Reuse the existing OpenMM Topology extraction tool for source-sorted unique
inventory and declared chemistry. Project coordinates with exactly that atom
axis and explicit model positions. Restore the single-structure Modeller shape
and independence. PDBFile has no public projection constructor: a local clone
replaces its known position stores/cache together without serialization,
rounding, bond inference or copying every unselected source model. Public
position/count access and cache-invalidating projection are guarded together;
future OpenMM cache/layout changes require this adapter's receiving again.

A Modeller cannot represent zero or multiple structures. A PDBFile projection
requires at least one model; empty query results remain separately shaped.
No complete heterogeneous-PDB chemistry or arbitrary-provider qualification
is claimed. Docstrings, form articles and maintained conversion guidance must
reflect the repaired contracts before closure.


## Source receiving — 2026-11-12

The first corrected cohort passes seventeen controls. The extended existing
OpenMM/chemistry/doctest cohort has 476 passes and two test-draft errors from
indexing OpenMM's list output as a numpy array; the expected-value reader is
corrected without changing any geometric assertion. A separate old MDTraj guard
expects one model even though the source has 38; its original failure is kept
and the stronger check compares every model/selected atom against the reader.
The corrected focused cohort passes 34 cases without warnings or omissions,
including #736's separate State/Context controls and updated doctests. Broader
final receiving, form documentation and public closeout remain due.
