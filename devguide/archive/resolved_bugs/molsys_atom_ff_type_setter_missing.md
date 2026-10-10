---
summary: MolSys atom_ff_type setting lacks its native adapter
issue: uibcdf/molsysmt#376
status: resolved
opened: 2026-10-10
closed: 2026-10-10
severity: medium
verification: reproduced
area: [api, attribute, form, native]
guard: tests/native/test_molsys_mechanics_setters.py
normative:
blocked_by: []
supersedes: []
---

# MolSys atom_ff_type setting lacks its native adapter

**Reported:** 2026-10-10, uibcdf/dockingmt#49 and uibcdf/dockingmt#5.
**Status:** Resolved; the existing mechanical setter now has a validated MolSys adapter.

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

## Resolution — 2026-10-10

**Contract-tested.** `set_atom_ff_type_to_atom` validates selected atom indices,
full-axis table length and value shape before allocating a mechanical table. It
reuses the existing MolecularMechanics setter with validated arguments. A first
subset edit allocates the full source atom axis; labels are stored in explicit
selection order and unselected rows remain unknown. Empty selections do not
allocate, and None clears the complete type column without removing charges.

The regression module named in `guard` checks independently expected labels,
full/subset/empty and malformed selections, no mutation on rejection, preserved
coordinates/ChemicalStates and both full and structures-only MolSys objects.
`tests/build/test_assign_autodock_atom_types.py::test_manual_mechanics_subset_setter_clears_typing_provenance`
additionally edits a real named assignment through both owning-domain and MolSys
routes and checks that typing attribution is cleared while charge values and
serialized charge attribution are unchanged.

On Linux/Python 3.14.7, before the adapter existed, the new regression selection
reported 21 missing-adapter failures (and seven passing controls). After repair,
the regression module plus the complete existing AutoDock assignment module
passes **39 tests** with this selection:

```bash
python -m pytest --receptor=llm -n12 tests/native/test_molsys_mechanics_setters.py tests/build/test_assign_autodock_atom_types.py
```

The new strict Sphinx render/doctest guard passes **one test**, executing all four
example statements. Two Sphinx/Napoleon deprecation warnings remain; no RST
rendering error occurs. Temporary local receipts are not the durable guard.

The public setter docstring, basic.set notes, native Foundations, Toolbox,
charge Cookbook and shared Common Core module 12 now describe the editing and
provenance contracts. All four course paths consume that shared module.
Mechanical edits still require explicit owner invalidation of dependent analyses;
there is no automatic detector invocation or new H5MSM mechanical persistence.
This source repair does not qualify or replace the paused frozen artifacts.

Focused Ruff checks and `git diff --check` pass. The 14 fast release gates
pass, including adapter delivery, dependencies, devguide integrity, course
structure and public smoke. These are scoped development checks, not the
mandatory heavy or installed-candidate qualification.
