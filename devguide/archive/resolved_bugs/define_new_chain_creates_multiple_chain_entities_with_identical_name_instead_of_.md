---
summary: define_new_chain creates multiple chain entities with identical name instead of a single merged chain
issue: uibcdf/molsysmt#160
status: resolved
opened: 2026-08-17
closed: 2026-08-19
verification: reproduced
severity: medium
area: [build]
guard:
normative: devguide/BUILDER_API.md
blocked_by: []
supersedes: []
---

# `define_new_chain` creates multiple chain entities with identical name instead of a single merged chain

**Reported:** 2026-08-17 during User Guide audit of `docs/content/user/tools/build/define_new_chain.ipynb`.
**Status:** Open defect under investigation.

## What

When `msm.build.define_new_chain(molsys, selection='molecule_type=="water"', chain_name='C')` is invoked on a system where selected atoms (e.g. water molecules) belong to multiple distinct pre-existing chains (such as chains 'A' and 'B' in PDB `1TCD`), `define_new_chain` modifies `chain_name` and `chain_id` on the original chain fragments rather than consolidating all selected atoms into a single contiguous chain entity `'C'`.

As a result, `msm.info(molsys, element='chain')` displays two separate chain entities both named `'C'`, each containing half of the water molecules, instead of a single merged chain `'C'`.

```python
import molsysmt as msm
molsys = msm.convert('1TCD')
msm.build.define_new_chain(molsys, selection='molecule_type=="water"', chain_name='C')
print(msm.get(molsys, element='chain', chain_name=True))
# Returns: ['A', 'B', 'C', 'C'] instead of ['A', 'B', 'C']
```

## How

The internal implementation delegates directly to `msm.set(molsys, selection=..., chain_name='C', chain_id='C')`. `msm.set` updates attributes on existing topology elements (chains) element-by-element without merging or restructuring the underlying topology graph / chain list.

To fix this, `define_new_chain` must create a single new chain element in the topology object and reassign the chain pointer/index of all atoms matching `selection` to that newly created single chain entity.

## Why

Users expect `define_new_chain` to produce a single, unified chain entity containing all selected atoms. Having multiple chain entities with the exact same `chain_name` and `chain_id` breaks topological invariants in downstream exporters (e.g., OpenMM, PDB, MDAnalysis, NGLView) which assume unique chain identifiers per chain entity.

## Scope and exclusions

This bug affects `msm.build.define_new_chain` when selected atoms span multiple pre-existing chains.

## Acceptance criteria

1. Calling `msm.build.define_new_chain(molsys, selection='molecule_type=="water"', chain_name='C')` on PDB `1TCD` produces exactly 3 chain entities (`['A', 'B', 'C']`).
2. A unit test `tests/build/test_define_new_chain.py` is added to guard against regression.

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

The defect needed no separate fix: the function is gone. Its cause is worth keeping
anyway, because it explains why renaming was never going to work. `define_new_chain`
delegated to `msm.set(molecular_system, selection=..., chain_id=..., chain_name=...)`,
which relabels the chains the selected atoms already belong to. When the selection
spanned two chains, both were relabelled `'C'` and the topology still held two chain
entities. Defining a chain requires restructuring the topology, which is what
`MolSysBuilder.add_chain` does and `set()` does not.

Reproduced on 2026-08-18 before removal, at `eb381f7ea`:

```python
>>> molsys = msm.convert('1TCD')
>>> msm.build.define_new_chain(molsys, selection='molecule_type=="water"', chain_name='C')
>>> msm.get(molsys, element='chain', chain_name=True)
['A', 'B', 'C', 'C']
```
