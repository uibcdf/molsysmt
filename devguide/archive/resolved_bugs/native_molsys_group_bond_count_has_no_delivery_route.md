---
summary: Native MolSys group-level bond counts have no delivery route.
issue: uibcdf/molsysmt#284
status: resolved
opened: 2026-10-01
closed: 2026-10-01
severity: medium
verification: reproduced
area: [attribute, form]
guard: tests/form/molsysmt_MolSys/test_group_bond_counts.py
normative:
blocked_by: []
supersedes: []
---

# Native MolSys group-level bond counts have no delivery route

**Reported:** 2026-10-01 while validating the TopoMT report `uibcdf/molsysmt#283`.
**Status:** Resolved with a native MolSys getter delegating to the existing
Topology tool and a public regression suite.

## What

Native MolSys declares bond-count capability, but querying group-level counts
raises NotWithThisFormError because no getter, derivation or usable pipe delivers
that attribute at the requested element level.

```python
molsys = msm.convert('tests/form/molsysmt_Topology/data/topomt_geometric_tetrahedron.pdb',
                     to_form='molsysmt.MolSys')
msm.get(molsys, element='group', n_bonds=True)
# NotWithThisFormError: ... does not implement get_n_bonds_from_group ...
```

## How

The native Topology adapter has `get_n_bonds_from_group`, but the native MolSys
adapter has no corresponding route. This fails before the shape handling repaired
in #283 and still fails after that correction. The registered support and actual
delivery need to agree. Preserve the selected ChemicalStates bond owner when
implementing delegation; a topology facade must not introduce competing storage.

## Why

Clients cannot use a declared attribute consistently across native representations.
Related consumer: `uibcdf/topomt#79`. TopoMT's geometric radius path does not need
this query; the finding is a separate provider limitation discovered during the
consumer regression review, rather than a remaining part of #283.

## What is measured and what is assumed

The public query failure was reproduced before and after the #283 correction.
Source baseline: `4e8c126d2`, Python 3.13.14, Linux x86_64. No performance claim.
The offline fixture and upstream hash are documented in its local data README.

## What was refuted

Returning zero for every missing route would silently corrupt bonded systems.
Treating native Topology parity as proof of native MolSys delivery is insufficient.

## Scope and exclusions

Group-level native MolSys bond-count delivery, with selected-state semantics.
No connectivity inference, chemistry repair, radius assignment or TopoMT changes.

## Acceptance criteria

A public regression checks correct per-group counts for empty and bonded native
MolSys inputs, selections, and explicit/reference chemical states. Preserve absent
or ambiguous-domain diagnostics and parity with the corresponding Topology getter.
Declare only routes that actually deliver the requested attribute.

## Resolution

Added the validated `get_n_bonds_from_group` native MolSys adapter. It delegates
to the existing Topology getter with already-normalized group indices. The
topology facade resolves bonds from the ChemicalStates domain selected by the
public `get` boundary, including explicit indices and structure associations.
No new bond store, broad adapter pipe, dependency or public signature is needed.

Counts are unique incident bonds per group: an internal bond counts once; a
bond between groups contributes once to each group. Groups without incident bonds return zero,
and an empty group selection returns an empty list. Missing topology remains
unavailable (`None`); ambiguous state selection still raises rather than
silently reporting zero.

Updated the `get` docstring, the adapter's executable example, User Guide
Foundations and Toolbox, the binding-pocket Cookbook, and Common Core Module 8.

## Verification

Contract-tested on Python 3.13.14, Linux x86_64:

- The original frozen TopoMT PDB reproduced the missing getter before the fix.
- `tests/form/molsysmt_MolSys/test_group_bond_counts.py`: **14 passed**, covering
  empty and bonded groups, cross-group and internal bonds, ordered and empty
  selections, masks, combined attributes, explicit/reference states,
  structure-associated states, absent topology, and ambiguous/invalid states.
  The selected-state parity cases check that the reference and shared owner remain
  unchanged. Counts are also checked against the native Topology getter.
- Affected native MolSys getters, Topology empty/chemical-state queries,
  `tests/basic/get`, ChemicalStates, and MolSys state associations:
  **582 passed**. Existing warnings concern legacy H5MSM, structural attributes
  off the selected axis, and a dummy PDB unit cell.
- `python -m pytest --receptor=llm --doctest-modules molsysmt/basic/get.py
  molsysmt/form/molsysmt_MolSys/get_topological_attributes.py`: **2 passed**.
- Sphinx HTML compilation returned exit 0; existing get-docstring indentation,
  course/MyST and toctree diagnostics remain outside this adapter correction.
  Notebook code cells and outputs were preserved. No performance or chemical
  completeness claim is inferred from these delivery tests.
- Ruff, developer-guide validation, public signature stability, and the form
  adapter audit passed (93 forms; no new unreachable declarations).
