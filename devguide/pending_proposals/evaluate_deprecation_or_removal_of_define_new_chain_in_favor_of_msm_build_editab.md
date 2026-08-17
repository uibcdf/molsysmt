---
summary: evaluate deprecation or removal of define_new_chain in favor of msm.build.editable
issue: uibcdf/molsysmt#167
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

# Evaluate deprecation or removal of `define_new_chain()` in favor of `msm.build.editable()`

**Reported:** 2026-08-17 during User Guide audit of `tools/build/`.
**Status:** Open proposal under review.

## What

`msm.build.define_new_chain` is a thin functional wrapper that alters chain assignments for selected residues/atoms. It also exhibited issues with entity/chain splitting (see bug issue uibcdf/molsysmt#160).

With `msm.build.editable(molsys)` and `MolSysBuilder`, users have explicit, transparent control over chain definitions and group assignments:
```python
builder = msm.build.editable(molsys)
builder.assign_groups_to_new_chain(group_indices=[...], chain_name='C')
new_molsys = builder.build()
```

## How

1. Assess whether `msm.build.define_new_chain` should be marked for formal deprecation in favor of `msm.build.editable()`.
2. Evaluate backwards compatibility requirements and migration paths for existing workflows.
3. Keep `editable.ipynb` as the canonical tutorial demonstrating chain reassignment.

## Why

Relying on the robust, native `MolSysBuilder` staging environment eliminates subtle chain segmentation defects and simplifies the public API surface.
