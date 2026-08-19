---
summary: evaluate if msm.topology.add_bonds is redundant given msm.build.editable
issue: uibcdf/molsysmt#166
status: open
opened: 2026-08-17
closed:
verification: asserted
area: [docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Evaluate if `msm.topology.add_bonds()` is redundant given `msm.build.editable()`

**Reported:** 2026-08-17 during User Guide audit of `tools/build/` and `tools/topology/`.
**Status:** Open proposal under review.

## What

`add_bonds` is currently exposed as a class method on `molsysmt.Topology` and `molsysmt.MolSys`, but is not an independent module-level function `msm.build.add_bonds()` or `msm.topology.add_bonds()`.

With the introduction of the high-level `msm.build.editable()` tool and the native `molsysmt.MolSysBuilder` container, users can add or modify bonds on any molecular system via:
```python
builder = msm.build.editable(molsys)
builder.add_bond(atom_index_1, atom_index_2, bond_order=1)
new_molsys = builder.build()
```

## How

1. Evaluate whether a standalone top-level functional API `msm.topology.add_bonds(molecular_system, ...)` is desirable.
2. Compare whether the builder-based pattern (`msm.build.editable`) renders an explicit top-level function redundant.
3. Align documentation and public API surfaces accordingly.

## Why

Providing a unified, clear API path prevents user confusion regarding where and how bonds should be added or edited in molecular topologies.
