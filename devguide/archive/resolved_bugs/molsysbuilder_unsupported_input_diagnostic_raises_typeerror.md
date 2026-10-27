---
summary: MolSysBuilder unsupported-input diagnostic raises TypeError
issue: uibcdf/molsysmt#493
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: low
verification: measured
area: [native, diagnostics]
guard: tests/native/test_group_free_molecules.py::test_builder_rejects_unsupported_input_with_the_declared_diagnostic
normative:
blocked_by: []
supersedes: []
---

# Unsupported builder inputs lose the intended diagnostic

**Reported:** 2026-10-26 during group-free inventory validation under
uibcdf/molsysmt#491. **Status:** resolved; the intended catalog diagnostic receives the rejected value.

## What

MolSysBuilder accepts None or a native MolSys, but passing an unsupported object
raises a Python TypeError while constructing its intended ArgumentChoiceError:

```python
import molsysmt as msm
msm.MolSysBuilder(object())
# TypeError: ArgumentChoiceError.__init__() missing 1 required positional argument: 'value'
```

## How

The unsupported-input branch in `native/molsys_builder.py::__init__` supplies
argument, choices, caller and message but omits the required value field.

## Why

Users receive an internal exception-construction failure instead of the declared
input contract. This does not block the supported None/MolSys constructor paths
or authorize extending constructor support to dictionaries.

## Acceptance criteria

Pass the rejected value through the supported catalog exception contract. Add a
public-constructor regression asserting ArgumentChoiceError and actionable
supported choices for an unsupported input, while retaining valid construction.
No hierarchy behavior or constructor signature should change.

## Provenance and limits

Linux/Python 3.14.7, source parent 39bb09715 with the #491 working changes.
Reproduced both with an unsupported dictionary and object input; supported
construction is qualified separately under #491. No user data or network needed.


## Resolution

The unsupported-input branch now passes value=molecular_system to the existing
ArgumentChoiceError constructor. It still rejects the same unsupported inputs;
no constructor signature or supported input set is expanded. The guard requires
the intended exception with its actionable contract message and also checks
valid empty construction. The final native/builder/TPSA block passes 121 tests
in 17.33 seconds. This one-field diagnostic fix has no scientific algorithm,
unit or provider change. Source checks and limitations are recorded with the
[shared qualification receipt](../../../devtools/data/group_free_molecule_inventory_20261026.json).
