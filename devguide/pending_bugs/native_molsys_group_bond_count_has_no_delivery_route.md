---
summary: Native MolSys group-level bond counts have no delivery route.
issue: uibcdf/molsysmt#284
status: open
opened: 2026-10-01
closed:
severity: medium
verification: reproduced
area: [attribute, form]
guard:
normative:
blocked_by: []
supersedes: []
---

# Native MolSys group-level bond counts have no delivery route

**Reported:** 2026-10-01 while validating the TopoMT report `uibcdf/molsysmt#283`.
**Status:** Reproduced; separate follow-up, no implementation started.

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
