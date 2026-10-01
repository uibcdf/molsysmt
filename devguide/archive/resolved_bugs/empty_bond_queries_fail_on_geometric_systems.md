---
summary: Empty bond queries fail on valid geometric systems.
issue: uibcdf/molsysmt#283
status: resolved
opened: 2026-10-01
closed: 2026-10-01
severity: medium
verification: measured
area: [attribute, form, tests]
guard: tests/form/molsysmt_Topology/test_empty_bond_queries.py
normative:
blocked_by: []
supersedes: []
---

# Empty bond queries fail on valid geometric systems

**Reported:** 2026-10-01 by TopoMT; related consumer `uibcdf/topomt#79`.
**Status:** Resolved; correction and affected-area validation complete.

## What

Per-atom bond-index and count queries raise an internal NumPy dimensionality
error for a valid four-carbon geometric PDB with no bonds. The report's current
source reproduction must specify `element='atom'`; the default system-level
query already returns the aggregate zero count correctly.

```python
molsys = msm.convert('topomt_geometric_tetrahedron.pdb', to_form='molsysmt.MolSys')
msm.get(molsys, element='atom', selection='all', n_bonds=True)
# ValueError: all the input arrays must have same number of dimensions ...
```

## How

`form.molsysmt_Topology.get_bond_index_from_atom` receives an empty list of bonded
pairs. NumPy infers shape `(0,)` when stacking it with an `(0, 1)` bond-index
column. `get_inner_bond_index_from_atom` uses the same construction. Explicit
selected pair queries also convert the empty list without preserving a pair axis.
The group-level inner-index helper deletes a conditional local `pairs` even
when no group contains bonds; that becomes a second empty-case failure after
repairing the shared atom route.

Normalize pair buffers to integer shape `(n_bonds, 2)` at their numerical
consumption boundaries, retaining the public list return conventions. Remove
that unconditional deletion. Preserve selected chemical-state resolution and
existing nonempty graph semantics.

## Why

A geometric system with no bonds is valid. Public queries must return one empty
collection or zero count per requested atom, including subsets and no atoms.
TopoMT's parameter-table/explicit-radius path appropriately avoids unnecessary
chemical interpretation. Fixing this query does not certify complete chemical
connectivity for its ProtOr path or change the consumer's dependency boundary.

## What is measured and what is assumed

The dimensionality error is reproduced on the exact pinned consumer fixture.
No performance or chemical-completeness claim is made. Tests compare public
queries across PDB, native MolSys and native Topology, plus aggregate levels,
zero-atom input and a nonempty bonded control.

## What was refuted

Changing the public bonded-pair result to an ndarray would unnecessarily change
its list contract. Treating no bonds as invalid would reject legitimate geometric
workflows. Globally swallowing the exception would also hide malformed chemistry.

## Scope and exclusions

Empty connectivity and related list-shape handling only. No invented bonds,
chemical typing, radius assignment, chemistry repair or TopoMT source changes.
The dirty, behind TopoMT worktree reported by the suite status tool is preserved.

## Acceptance criteria

Return `[0, 0, 0, 0]` per-atom bond counts and `[[], [], [], []]` per-atom bond
indices from the fixed PDB; subsets and empty selections must retain their shape.
Related inner/group queries must work. Preserve nonempty bond identity and
selection semantics. Add a frozen offline guard and provenance, clarify public
query documentation, update the maintained developer record and close #283 with
the published fix and guard.

## Provenance

Source baseline `4e8c126d2`, Python 3.13.14, Linux x86_64; source fixture copied
byte-for-byte from TopoMT commit `88e2164c17b118327ff8fc7383a9b2a4c1e60ed0`:
[original PDB](https://github.com/uibcdf/topomt/blob/88e2164c17b118327ff8fc7383a9b2a4c1e60ed0/docs/content/showcase/dfnd/artifacts/regular_tetrahedron_v1/input_castp.pdb).
Local offline fixture: `tests/form/molsysmt_Topology/data/topomt_geometric_tetrahedron.pdb`.
SHA256: `e40db4e92eb260682c4e77e43873425efda37f96a55008da0e2a0721c57bc5cb`.


## Resolution

Pair buffers are integer `(n_bonds, 2)` arrays before numerical stacking or column
selection, including `(0, 2)`. Public returns stay lists. Group inner-bond queries
no longer delete an unassigned conditional buffer. No bonds are inferred or
chemical state ownership changed.

The frozen original PDB now yields per-atom counts `[0, 0, 0, 0]` and bond-index
lists `[[], [], [], []]`. Subsets and empty selections retain their per-atom
shape; zero-atom topology, internal bonds and fully populated hierarchy controls
also work. Bonded controls protect original source bond indices and internal
selection semantics. The file:PDB adapter's unavailable pair attribute retains
its existing `None` result; converted native systems expose an empty pair list.
A separate missing native MolSys group-count delivery route was reported as
`uibcdf/molsysmt#284`; it is not repaired or hidden by this change.

Validation on 2026-10-01:

```bash
python -m pytest --receptor=llm tests/form/molsysmt_Topology tests/basic/get
```

**1,349 passed**, exit 0, 53.02 seconds. The 26 warnings are 24 legacy H5MSM reads,
one structural-attribute axis warning and one reference-provider dummy-box warning.
The focused offline guard has 16 passing cases. All 25 examples across the public
get docstring and the native Topology getter module pass. These are validation
elapsed times, not performance benchmarks or a complete release gate.

Ruff passes for `molsysmt` and the new test. Public signature validation detects no
drift. Docstring fidelity and course-structure validation pass. Sphinx builds with
exit 0; existing course header/directive/reference and tutorial admonition warnings
remain. The documentation changes are prose only: existing executable cells and
outputs are preserved, and the new semantics are exercised by the doctests and
public offline fixture guard. Foundations, Toolbox and Common Core Module 08 now
clarify empty data, the per-atom/system distinction and chemical-completeness limits.

The guard fails on the original array-dimensionality bug, the selected-pair
indexing bug and the group cleanup bug, while also checking nonempty behavior.
TopoMT's parameter-table radius boundary and its ProtOr completeness checks remain
consumer-owned; no TopoMT worktree changes were made.
