---
summary: MolSys atom_ff_type setting lacks its native adapter
issue: uibcdf/molsysmt#376
status: open
opened: 2026-10-10
closed:
severity: medium
verification: reproduced
area: [api, attribute, form, native]
guard:
normative:
blocked_by: []
supersedes: []
---

# MolSys atom_ff_type setting lacks its native adapter

**Reported:** 2026-10-10, uibcdf/dockingmt#49 and uibcdf/dockingmt#5.
**Status:** Reproduced; admitted to pre-1.0 public-boundary stabilization.

## What

The public MolSys route declares `atom_ff_type` available but setting that field
fails with a raw missing-function AttributeError. The owning mechanical setter
works on the same system's MolecularMechanics domain.

```python
import molsysmt as msm
from molsysmt.native import MolSys
system = MolSys(n_atoms=2)
msm.set(system, element='atom', atom_ff_type=['C', 'O'])
# AttributeError: module 'molsysmt.form.molsysmt_MolSys' has no attribute
# 'set_atom_ff_type_to_atom'
msm.set(system.molecular_mechanics, element='atom', atom_ff_type=['C', 'O'])
msm.get(system.molecular_mechanics, element='atom', atom_ff_type=True)
# array(['C', 'O'], dtype=object)
```

These arbitrary labels demonstrate delivery, not chemical typing correctness or
named AutoDock assignment evidence. The consumer uses such labels as a negative
admission control and has a supported mechanical-domain workaround.

## How

`molsysmt/form/molsysmt_MolSys/attributes.py` declares the attribute and the getter
delivers it; its `set.py` lacks `set_atom_ff_type_to_atom`. `basic.set` dispatches
to that absent function. `molsysmt_MolecularMechanics/set.py` already owns manual
label validation/storage and assignment-provenance invalidation. The neighboring
MolSys partial-charge setter demonstrates delegation with an explicit full-system
atom count and no competing chemical store.

Prefer completing that provider-owned delegation for the existing mechanical
attribute. Validate value shape, selected indices/order and the full atom axis
before allocation/mutation. Reuse the existing setter's provenance invalidation;
do not invent a named assignment report or infer types from arbitrary labels.
If the maintainers instead declare MolSys setting unsupported, it needs a precise
capability error and documented supported route, rather than raw AttributeError.

## Why

DockingMT needs truthful public delivery and explicit manual-assignment behavior.
The setter repaired under #316 is on MolecularMechanics; it does not by itself
cover the combined MolSys adapter. This is a missing/unclear delivery boundary
for an existing attribute, not new chemical typing coverage. Repair is appropriate
before final qualification without making the consumer migration a release gate.

## What is measured and what is assumed

The local reproduction above executed on source
`a54dd36889e90d8cd4c3a04b3a2ce01acc0f004a`, Linux/Python 3.14.7. The consumer
independently reports the same failure on an explicit-H methanol fixture at
`739395d7ea31bec5c3f77cdcb1135ecf7e7c9bac`. Only the small local public
reproduction ran here; no installed package or chemical-method comparison ran.

## What was refuted

This is not a request for a downstream chemical assignment engine. Manual labels
are not authenticated named assignments. A getter-delivery audit cannot prove
that the setter exists; both directions need their own contract evidence.

## Acceptance criteria

- Declare and test MolSys setter support, or its explicit capability-error policy.
- For supported delegation, verify full/nonconsecutive/empty selections, retained
  atom-axis length and independently expected label alignment.
- Reject malformed values/indices before mutation; manual changes invalidate
  named typing provenance according to the existing owning-domain contract.
- Preserve ChemicalStates, source coordinates and unrelated mechanical fields;
  complete public docstrings, User Guide and course/consumer guidance.
- Name an addressable guard and retain the original consumer failure evidence.

No graph repair, automatic type inference, downstream setter implementation or
new H5MSM mechanics persistence is included.
