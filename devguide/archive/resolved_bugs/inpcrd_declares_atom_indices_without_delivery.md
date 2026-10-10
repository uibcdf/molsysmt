---
summary: INPCRD declares atom indices without a delivery route.
issue: uibcdf/molsysmt#362
status: resolved
opened: 2026-10-09
closed: 2026-10-09
severity: medium
verification: reproduced
area: [form, attribute]
guard: tests/form/file_inpcrd/test_getters.py::test_atom_indices_preserve_source_positions
normative:
blocked_by: []
supersedes: []
---

# INPCRD declares atom indices without a delivery route

**Reported:** 2026-10-09, during the pre-1.0 audit of #139.
**Status:** Resolved for source-position metadata delivery.

## What

The adapter declares `atom_index` and knows the header atom count, but cannot
return source atom positions:

```python
msm.get(inpcrd, element="atom", atom_index=True)
# NotWithThisFormError: no get_atom_index_from_atom, derivation or delivery pipe
```

Public all, reordered/repeated and empty selections fail on a well-formed
three-atom coordinate file. Coordinates do not require atomic names or chemical
assignments to have a positional atom axis.

## How

`molsysmt/form/file_inpcrd/get_topological_attributes.py` implements only
`get_n_atoms_from_system`, which reads the header count. No topological pipe is
declared. Add a direct atom-index getter calling that existing tool, rather than
loading the coordinate array or adding a general chemistry reconstruction.

## Why

Positional selection and association with coordinate results are existing public
contracts. This form can deliver indices from its own data without inference,
new dependencies or a change to the reader's scientific behavior.

## What is measured and what is assumed

All three public query failures were reproduced on a tiny valid INPCRD with three
atoms. Regression guards additionally compare ordered/repeated positions with
analytical coordinates and verify a 5,207-atom bundled query without coordinate
conversion. The latter is an execution-path guard, not a memory benchmark.

## What was refuted

Removing the declaration would hide available positional information. Converting
to Structures could derive positions but would unnecessarily load coordinates
and require its optional reader for a header-only query. Reusing the existing
header count is sufficient; an independently public range-construction tool is
not needed.

## Scope and exclusions

Return source indices as a list, retaining selection order and repetitions.
No atom IDs, names, groups, bonds or chemical states are inferred. Preserve the
format's existing coordinate and unit converters, and its current support tier.
The broader legacy-format and CIF delivery debt remains under #139.

## Acceptance criteria

The public facade returns source positions for all, scalar, repeated/reordered
and empty selections. Positions align with selected coordinate values. The
metadata-only query does not materialize coordinates. Remove only this resolved
baseline bit and synchronize Foundations, Toolbox, Cookbook and course guidance.

## Provenance

Linux, Python 3.14.7, shared `molsyssuite@uibcdf_3.14` development environment,
2026-10-09. Existing frozen artifacts and the publication pause remain unchanged.

## Resolution

The direct, digested atom-level getter reuses the existing public header-count
getter for an unrestricted query. Selected positions retain the public facade's
validated order and repetitions; an empty selection returns an empty list.
The implementation neither reads coordinate arrays nor infers atomic identities.

The original tiny test fixture had correct header metadata but incorrectly
formatted coordinate fields. Its first combined control failed five cases for
missing delivery and one during coordinate parsing. The fixture now writes
AMBER's fixed-width 12.7 fields. Repeating the six controls with that valid
fixture fails all six solely for missing atom-index delivery before repair.
After repair, all 28 tests in the adapter module and one getter doctest pass.
They include analytical coordinate alignment and the 5,207-atom bundled case.

The guard compares exact source-index lists for all, scalar, reordered/repeated
and empty selections. Returning only a count, an empty stub or renumbered subset
cannot satisfy it. Companion guards compare selected coordinates in explicit
nanometers and reject a metadata query that calls the coordinate converter.
Only the resolved `file:inpcrd` atom-index bit is removed from the delivery
baseline. Foundations, the form Toolbox, conversion Cookbook and Common Core
Module 8 describe this positional contract. The broader #139 issue remains open.
