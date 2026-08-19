---
summary: evaluate if msm.topology.add_bonds is redundant given msm.build.editable
issue: uibcdf/molsysmt#166
status: resolved
opened: 2026-08-17
closed: 2026-08-19
verification: inspected
area: [docs]
guard:
normative: devguide/BUILDER_API.md
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

## Resolution — 2026-08-19

**No module-level `add_bonds` or `remove_bonds` is to be added.** The tools
namespaces are already free of them and must stay that way.

Measured on this checkout at `29580a571`:

```
msm.build      ['add_missing_bonds', 'get_disulfide_bonds', 'get_missing_bonds']
msm.topology   ['get_bondgraph']
msm.basic      []
msm.structure  []
```

The proposal asked whether a standalone functional API is desirable given the
builder. It is not, and the reason generalises past bonds: the line falls between
**explicit editing** and **chemically-informed inference**.

Explicit editing states what the answer is — bond these two atoms, these groups are
now a chain — and belongs to the builder alone. Inference works out what the answer
should be, and stays in the tools: `add_missing_bonds`, `get_missing_bonds`,
`get_disulfide_bonds`, `get_bondgraph`. None of them asks the caller which bonds to
create.

This is the same answer `uibcdf/molsysmt#167` reached for `define_new_chain` on the
same day, by the same reasoning.

### What this does not touch

`molsysmt.Topology.add_bonds` stays. It is the native class method the rest of the
library is built on — `native/molsys.py:573`, `native/topology.py:1932`,
`form/molsysmt_Topology/add_bonds.py:30`, and the PyTraj and NGLView adapters all
call it. It is machinery, not a competing public path, and the question here was
never about it.

Removed with this: two orphaned `add_bonds.nbconvert.log` files left in
`tools/build/` and `tools/topology/` by tutorials that no longer exist. Their pages
and index entries were already gone.
