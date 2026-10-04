---
summary: Perceive aromatic atom and bond flags on a detached declared chemical graph
issue: uibcdf/molsysmt#314
status: resolved
opened: 2026-10-04
closed: 2026-10-04
verification: measured
area: [physchem]
guard: tests/physchem/test_get_aromaticity.py
normative: docs/content/user/tools/physchem/get_aromaticity.md
blocked_by: []
supersedes: []
---

# Perceive aromatic atom and bond flags on a detached declared chemical graph

**Reported:** 2026-10-04, while designing chemical AutoDock typing under
uibcdf/molsysmt#222.
**Status:** Resolved. The public detached perception tool and its documented
model boundary are implemented and verified.

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

## Implementation and verification — 2026-10-04

`physchem.get_aromaticity` requires complete supported covalent chemistry and
closed-shell charge/radical prerequisites, returns bool arrays with source atom
and bond indices, and preserves stored assignments. Known contradictions fail.
The criterion is named fused_ring_electron_count, with explicit
rdkit.AROMATICITY_RDKIT implementation and original producer versions. It is not
claimed as an original MolSysMT aromaticity formula or a universal definition.
RDKit is lazy; optional Ackredit records detached references without making
science depend on its availability.

The common detached inventory/state view and explicit-frame validation now live
behind existing public chemical tools in topology._chemical_graph. Charges reuse
those private helpers. No public placeholder utility or competing store is added.
Numeric H5MSM routes retain their chemistry-only loading behavior; rich selections
can load coordinates. No graph-wide peak-memory or speed benchmark is inferred.

Controls include benzene, pyridine, pyrrole, aliphatic/cyclic nonaromatic graphs,
naphthalene and the RDKit Book fused-ring example with aromatic endpoints but a
nonaromatic connecting bond. Caffeine native/SDF/H5MSM forms, selection/empty shapes,
nonreference states, frame validation, query/metals/radical rejection and required
prerequisites are tested. A primitive numerical count typo and NumPy-bool doctest
representation were corrected during development; neither changes the criterion.
The known source contradiction check does not silently overwrite stored flags.

Command:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm tests/physchem/test_get_aromaticity.py tests/physchem/test_get_partial_charges.py tests/build/test_assign_partial_charges.py --doctest-modules molsysmt/physchem/get_aromaticity.py
```

Result: 71 passed in 28.12 s. Ruff and 235-public-function docstring validation
pass; course structure remains valid for 156 notebooks. Foundations, Toolbox,
native-SDF Cookbook and Common Core module 12 describe the new boundary.
Provider-consumer AutoDock typing remains separate under uibcdf/molsysmt#222.

## Provenance

Local Linux x86_64, Python 3.13.14, NumPy 2.4.6, pandas 2.3.3 and RDKit 2025.09.5,
2026-10-04. Released ArgDigest 0.13.0 source snapshot at
/tmp/molsysmt-readiness-argdigest-013, commit
9880fa7b990fd0987ff0de715b665eb9e11c11b2, under the bounded environment deviation
uibcdf/molsysmt#237. This is neither a full supported-platform release gate nor
an aromaticity-accuracy or docking-preparation qualification.

Final focused verification after protecting rich RDKit selections: 22 passed
in 9.77 s, including the doctest. The HTML build completes with existing warnings;
the touched get() return-description formatting was also repaired so it no
longer emits a docutils indentation error. This does not certify a warning-free
full documentation build.
