---
summary: define_new_chain creates multiple chain entities with identical name instead of a single merged chain
issue: uibcdf/molsysmt#160
status: open
opened: 2026-08-17
closed:
verification: asserted
severity: medium
area: [build]
guard:
normative:
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
