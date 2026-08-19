---
summary: evaluate deprecation or removal of define_new_chain in favor of msm.build.editable
issue: uibcdf/molsysmt#167
status: resolved
opened: 2026-08-17
closed: 2026-08-19
verification: reproduced
area: [docs]
guard:
normative: devguide/BUILDER_API.md
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

## Resolution — 2026-08-19

`molsysmt.build.define_new_chain` was removed. The maintainer's decision is that the
function should not exist: a chain is defined with the builder.

```python
builder = msm.build.editable(molecular_system)
builder.add_chain(group_indices=[...], chain_name='C')
molecular_system = builder.build()
```

Removal needed no deprecation cycle. The symbol was classified `experimental` in
`devtools/data/public_api_stability.json`, and `deprecation_policy.md` section 5
places experimental symbols outside the policy. That classification was chosen on
2026-08-18 precisely to keep this answer available; `stable` would have decided it by
omission. The registry drops from 189 to 188 symbols.

The surface was small: no tests referenced it, the course never used it, its User
Guide tutorial had already been removed, and it had no dedicated argument digesters.
What remained was the module, its import in `molsysmt/build/__init__.py`, the registry
entry, the API reference page and one orphaned `.nbconvert.log`.

**How it stays removed.** `validate_api_stability.py` rejects any public export
missing from the registry, so reintroducing it fails the release gate with
`Unclassified public export` until someone classifies it deliberately.
