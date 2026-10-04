---
summary: Public set rejects partial charge values before native mechanical delegation
issue: uibcdf/molsysmt#311
status: resolved
opened: 2026-10-03
closed: 2026-10-04
severity: medium
verification: measured
area: [attribute, diagnostics]
guard: tests/basic/test_set_partial_charge.py
normative:
blocked_by: []
supersedes: []
---

# Public set rejects partial charge values before native mechanical delegation

**Reported:** 2026-10-03, while validating manual replacement of the named
charge assignments tracked in uibcdf/molsysmt#221.
**Status:** Resolved. Public setter validation and native mechanical delivery
are repaired and verified.

## What

Every finite partial-charge vector was refused by public argument digestion:

```python
import molsysmt as msm
molsys = msm.convert(msm.systems['caffeine']['caffeine.sdf'], to_form='molsysmt.MolSys')
msm.set(molsys, selection=[0], partial_charge=[0.2])
```

This raised `ArgumentError` from `digest_partial_charge`, before mechanical
delegation. Calling the mechanical form setter directly instead raised
`ArgumentError` from `digest_value`. MolSys also lacked the actual atom-level
partial-charge setter used by general dispatch.

## How

The charge digester accepted only getter booleans and conversion inputs;
the value digester lacked partial-charge dispatch. Add finite one-dimensional
setter validation, explicit charge-unit conversion, and the native MolSys
delivery route. Preserve chemical formal charges and keep unknown unselected
mechanical values missing. Do not invent zero charges or broadcast a scalar.

## Why

Users could not replace or initially supply mechanical charges through the
general attribute-editing boundary. This also prevented testing manual replacement
independently of a calculation backend. The defect has medium severity: the
native property is a workaround but bypasses public validation.

## What is measured and what is assumed

**Reproduced:** The public call above failed with `ArgumentError` in the
focused assignment validation. A direct form-setter call also failed before
mutation. The separate guard covers creation, selected replacement, charge
quantities, invalid units/shapes/nonfinite values, absent coverage, full-column
clearing and empty selections. The guard passed 12 tests in 4.19 s with
`env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm tests/basic/test_set_partial_charge.py`.
The final combined charge/native/extraction/PDBQT regression passed 459 tests
in 87.38 s (51 warnings). The guard assertions prevent the original valid-vector
rejection and validate failure before mutation, rather than bypassing digestion.

**Assumed:** External forms retain their existing setter capabilities. This
change establishes native MolSys delivery, not write support for every form.

## What was refuted

Skipping argument digestion is not an adequate public repair. Converting values
to the session standard unit is insufficient: native mechanical storage and
PDBQT use elementary charge even if output quantities use coulombs.

## Scope and exclusions

Validated manual partial-charge writes for native MolSys and its delegated
mechanical form setter. No model calculation, chemical-state change, automated
charge aggregation or H5MSM mechanical persistence is introduced by this repair.

## Acceptance criteria

- Finite full or selected vectors can be set through `msm.set`.
- Charge quantities normalize to native elementary-charge values.
- Unknown unselected atoms remain unknown; malformed inputs fail before mutation.
- Formal charges remain unchanged and the focused guard passes.

## Provenance

Local Linux x86_64 environment, Python 3.13.14, NumPy 2.4.6, pandas 2.3.3,
verified on 2026-10-04, using the released ArgDigest 0.13.0 source snapshot at
`/tmp/molsysmt-readiness-argdigest-013` under uibcdf/molsysmt#237's bounded
environment deviation. This is not a full supported-platform release gate.
