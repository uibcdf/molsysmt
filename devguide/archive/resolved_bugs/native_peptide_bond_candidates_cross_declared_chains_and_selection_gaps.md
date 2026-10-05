---
summary: Native peptide bond candidates cross declared chains and selection gaps
issue: uibcdf/molsysmt#328
status: resolved
opened: 2026-10-05
closed: 2026-10-05
severity: high
verification: reproduced
area: [build]
guard: tests/build/get_missing_bonds/test_peptide_candidates.py
normative:
blocked_by: []
supersedes: []
---

# Native peptide candidates ignore source adjacency and chain boundaries

**Reported:** 2026-10-05, while qualifying reusable native bond candidates for
uibcdf/molsysmt#304.
**Status:** Resolved in the general build tool; reader-engine qualification remains separate.

## What

`msm.build.get_missing_bonds()` proposes a peptide C–N pair between separate
chains when the atoms are nearby. It also proposes a link across an omitted
group and links nearby nonadjacent groups. An integer atom selection raises
an out-of-range group-index error because the nested group query interprets it
on a different axis. `add_missing_bonds()` inherits the erroneous candidates.

The guard builds complete heavy-atom alanines with no declared edges through
public PDB-text conversion with `get_missing_bonds=False`. Independent literal
ALA edges protect the expected intra-group chemistry. In the separate-chain
case, C at source atom index 2 and N at index 5 are 1.4 angstrom apart, but their
chain indices are 0 and 1. The erroneous extra pair is `[2, 5]`.

```bash
python -m pytest --receptor=llm \
    tests/build/get_missing_bonds/test_peptide_candidates.py \
    --junitxml=/tmp/molsysmt-328-before.xml
```

## How

In `molsysmt/build/get_missing_bonds.py`, the template loop numbers selected
groups afresh instead of preserving their source group indices. The peptide
helper collects C and N from successive local numbers, then searches the
Cartesian product of both lists. It neither restricts returned pairs to their
intended adjacent groups nor checks chain membership. The group query also
receives an atom-index list as a group-index list.

The correction resolves an atom selection and derives its selected source
groups. The peptide candidate set uses actual source group indices `g` and
`g + 1`, requiring one defined, identical chain index for both. It delegates
only those explicit C–N pairs to `structure.get_distances(pairs=True)`, reusing
unit-aware Rust geometry and MIC through the existing general tool. The
returned list still excludes already stored edges and keeps both endpoints
inside the atom selection. No reader-specific geometry or chemical store is
introduced.

## Why

This is a scientific-integrity defect in a reusable repair operation: adding
these candidates can connect separate molecules or invent sequence adjacency.
It affects the native build engine and blocks treating its peptide candidates
as qualified evidence for the DockingMT-requested PDB reader in
uibcdf/molsysmt#304. This fix alone does not qualify that reader engine.

## What is measured and what is assumed

At base commit `60667ad5e23c53e95583ed508198e494806005ef`, the initial
14-control version of the guard run with the command above reports **7 failed, 7 passed in 5.63 s**. Five assertions expose spurious
candidates (native input, H5MSM input, copy-producing repair, selection gap,
and nonadjacent proximity); two valid atom-index selections raise group-axis
errors. The existing positive, cutoff, PBC and user-unit controls pass.
This is a regression-test receipt, not a performance benchmark.

## What was refuted

- Distance alone is insufficient: the negative chain case has the same 1.4
  angstrom separation as the accepted same-chain neighbor.
- Restricting only the chain is insufficient: the three-amino-acid-group case has a
  nearby C–N pair within one chain that skips a source group.
- Preserving source group numbers alone is insufficient: a Cartesian neighbor
  search still admits unintended pair combinations.
- H5MSM persistence is not the cause: the native and persisted two-chain
  controls both reproduce the extra pair.

## Scope and exclusions

This covers native peptide candidate adjacency, chain membership, explicit
atom selections and the inherited `add_missing_bonds()` behavior. Public
signatures, defaults and result types stay unchanged.

Unknown-group distance fallback, valence certification, explicit engine
provenance, parser preservation of same-ID TER segments and alternative sites,
and nonconsecutive declared peptide edges remain outside this correction.
Already declared bonds are preserved; the tool does not delete or certify them.
No default PDB inference engine changes. Reader qualification remains #304.

## Acceptance criteria

- No peptide candidate crosses declared chain indices or a gap in source group
  indices; nearby nonadjacent groups do not acquire a candidate.
- Explicit atom-index selections keep the atom axis, and valid adjacent pairs
  remain detectable with source indices.
- Candidate distance tests honor the cutoff, MIC and user-selected length units.
- Native/H5MSM input and the copy-producing repair follow the same constraints;
  candidate discovery and copy repair leave the source unchanged.
- Existing alanine-dipeptide selection and complete-recovery checks still pass.
- The guard and public documentation explain the limits without claiming a
  complete validated chemical graph.

## Provenance

Linux x86_64 development host, 2026-10-05. Runtime environment
`molsyssuite@uibcdf_3.14`: Python 3.14.7, NumPy 2.4.6, pandas 2.3.3,
h5py 3.16.0, OpenMM 8.6.1. The runtime uses authentic released ArgDigest 0.13.0
source in the isolated public-support overlay; source and installation metadata
are distinct. No external oracle or online fixture is required by the guard.

## Resolution — 2026-10-05

**Implemented and contract-tested.** Source group indices and chain membership
now constrain peptide pairs before distance evaluation. Integer atom selections
are mapped to source groups explicitly; the final endpoint mask remains on the
atom axis. The public signatures, defaults and list return type are unchanged.
The geometry delegates to the existing general paired-distance tool, including
its Rust kernels and MIC handling. No new dependency or chemical store is added.

The final guard has 22 public controls: declared chain separation, selection
gaps, atom-list selection, nearby nonadjacent groups, positive adjacency,
cutoff, nonconsecutive group IDs, absent/ambiguous chain membership, interleaved
atom order, structure indices distinct from structure IDs, empty selection,
PBC and nm/pm policies, H5MSM input, copy repair and preservation of declared
edges. Literal expected intra-group/peptide pairs protect scientific intent,
not only output shape. `add_missing_bonds()` inherits the corrected candidates.

```bash
python -m pytest --receptor=llm \
    tests/build/get_missing_bonds/test_peptide_candidates.py \
    tests/build/get_missing_bonds/test_get_missing_bonds.py::test_get_missing_bonds_with_selection_preserves_pairs \
    tests/build/add_missing_bonds/test_add_missing_bonds.py \
    --doctest-modules molsysmt/build/get_missing_bonds.py \
    molsysmt/build/add_missing_bonds.py \
    --junitxml=/tmp/molsysmt-328-after.xml
```

Receipt: **28 passed in 6.00 s** (22 guard controls, four existing recovery
controls and two public docstrings). Seven warnings remain visible: six expected
legacy H5MSM deprecations and one existing pandas setter FutureWarning when a
fixture declares absent chain membership. The pre-existing optional PyTraj
comparator is not part of this run. The add-missing-bonds docstring example was
corrected to query pairs instead of atom membership; both examples now execute.

Ruff, public signature/stability classification, public docstring fidelity,
optional-dependency imports and the 156-module course structure pass. Foundations,
Toolbox, Cookbook and Common Core module 12 now explain the same group/atom-axis
constraints. Notebook code cells and saved outputs are unchanged. Incremental
Sphinx HTML completes successfully with 31 existing warnings already present
in the earlier #304 build; this is not a warning-free documentation claim.

This closes the bounded candidate defect. Native reader coverage, segment and
alternative-site interpretation, engine selection and provenance remain
uibcdf/molsysmt#304. No reader default is changed by this correction.
