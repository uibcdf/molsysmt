---
summary: Molecular mechanics identity converters reject valid input forms
issue: uibcdf/molsysmt#418
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: low
verification: reproduced
area: [form, convert]
guard: tests/form/molsysmt_MolecularMechanics/test_identity_conversion.py
normative:
blocked_by: []
supersedes: []
---

# Molecular mechanics identity converters reject valid input forms

**Reported:** 2026-10-22, while executing the resident-native conversion profile for uibcdf/molsysmt#181.
**Status:** Resolved; both adapters validate the correct registered form.

## What

Both identity adapters reject their own valid input form with `ArgumentError`:

```python
from molsysmt.native import MolecularMechanics
from molsysmt.form.molsysmt_MolecularMechanics.to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics
from molsysmt.form.molsysmt_MolecularMechanicsDict.to_molsysmt_MolecularMechanicsDict import to_molsysmt_MolecularMechanicsDict

to_molsysmt_MolecularMechanics(MolecularMechanics())
to_molsysmt_MolecularMechanicsDict({"forcefield": "amber14-all.xml"})
```

## How

The decorators in the two identity converter modules use `MoleculeMechanics`
and `MoleculeMechanicsDict`, while the registered form names contain
`MolecularMechanics`. Correcting the metadata retains normal item validation
and delegates to the existing extraction/copy implementation.

## Why

Direct consumers of the declared adapter cannot perform identity conversion.
Public routing may optimize same-form requests, so the defect is narrower than
all mechanics conversion. No energy calculation or H5MSM mechanics persistence
is introduced by the repair.

## What is measured and what is assumed

The first execution of the 41-edge native profile produced 46 passes and two
failures (including its harness controls). Both failures are these adapters:

```bash
python -m pytest tests/conversion_truth/test_declared_native_edges.py devtools/tests/test_audit_conversion_execution.py --receptor=llm -n 12
```

The smoke harness checks reachability and output form, not full fidelity.
Mirrored regression tests additionally exercise copy policy, stored values and
rejection of foreign forms with digestion enabled.

## What was refuted

These are not missing optional dependencies: validation rejects the correctly
recognized input before extraction. Skipping digestion would hide the defect
and is not the repair.

## Scope and exclusions

Only the two identity adapters and their regression guards. Mechanics remains
experimental; H5MSM 0.5 still excludes nonempty mechanics persistence.

## Acceptance criteria

Both adapters admit their own form, preserve their existing copy policy and
values, and reject a foreign native form with normal validation enabled. The
resident-native direct/public smoke profile must pass without excluding either
edge.

## Provenance

Linux, Python 3.14.7, current development checkout based on cdf7808e1,
pytest 9.1.1, NumPy 2.4.6; 2026-10-22. Local source evidence only.

## Resolution — 2026-10-22

Both form names are corrected, with normal argument digestion retained. The
mirrored regression modules reproduce four failures on the original metadata
(two foreign-form rejection controls already pass), then all six cases pass.
They check both copy flags, parameter values and detached nested mutable data.
The direct/public conversion and related mechanics selection passes 194 tests
with no skips; see the command above. Four expected legacy H5MSM warnings remain.
The general execution profile continues to include both formerly failing edges.

Only decorator metadata and the copy-policy docstrings change in production.
No mechanics storage, scientific model or public signature changes. The guard
below names the native regression module; the parallel dictionary guard is
`tests/form/molsysmt_MolecularMechanicsDict/test_identity_conversion.py`.
