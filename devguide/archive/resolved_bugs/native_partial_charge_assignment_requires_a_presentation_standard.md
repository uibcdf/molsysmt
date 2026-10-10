---
summary: Native partial-charge assignment requires an unrelated presentation standard.
issue: uibcdf/molsysmt#381
status: resolved
opened: 2026-10-10
closed: 2026-10-10
severity: medium
verification: reproduced
area: [build, units, tests]
guard: tests/build/test_assign_partial_charges.py
normative: devguide/partial_charge_assignment.md
blocked_by: []
supersedes: []
---

# Native partial-charge assignment requires a presentation standard

**Reported:** 2026-10-10 by DockingMT, consumers uibcdf/dockingmt#5 and
uibcdf/dockingmt#49.
**Status:** Resolved in source; canonical computation and quantity presentation
have separate boundaries.

## What

Native `build.assign_partial_charges` fails when a caller configures length and
time standards without a charge standard, although its native store uses fixed
elementary-charge values. This reproduces on source `aedd5a76d195d10fc2c1fb9ac6d24c96cc751a28`:

```python
import molsysmt as msm
import pyunitwizard as puw

molsys = msm.convert('methanol.sdf', to_form='molsysmt.MolSys')
with puw.context(standard_units=['pm', 'fs']):
    msm.build.assign_partial_charges(molsys, method='gasteiger_marsili')
```

The six-atom explicit-H methanol fixture supplied by DockingMT raises
`NoStandardsError`. With `['pm', 'fs', 'coulomb']`, assignment succeeds and stores
approximately `[0.03194068372, -0.39963024356, 0.05268663182, 0.05268663182,
0.05268663182, 0.20962966439]` in elementary-charge units; the source remains
unchanged.

## How

The shared private `calculate` in `molsysmt/_private/partial_charges.py` finishes
with `puw.quantity(..., 'elementary_charge', standardized=True)`.
`build.assign_partial_charges` calls the quantity-returning getter and converts
its presentation back to canonical numbers. Standardization is unnecessary for
the native storage boundary and fails when that dimension has no standard.

The repair keeps one shared scientific calculation returning canonical
numbers and its original report. The public physchem getter constructs the
standardized quantity at its return boundary. The build operation attaches the
same canonical values without invoking presentation standardization. Both retain
public argument validation and optional-provider checks.

## Why

An explicitly selected, otherwise supported charge model cannot supply the native
assignment requested by a consumer under a legitimate partial unit policy.
Applications must not compensate by changing caller configuration or inventing
charges. This affects both charge models through their shared output boundary;
it does not indicate an error in either scientific model.

## What is measured and what is assumed

The local six-atom reproduction was executed with and without coulomb configured.
Its successful control agrees with the reported values to absolute tolerance
`1e-10 e`. No speed, memory or scientific-accuracy claim follows from this check.
Force-field coverage still requires the existing real-system guard.

## What was refuted

- The missing standard is not missing chemical input: changing only the policy
  resolves the failure for the same molecule and explicit method.
- A library configuration override or implicit charge standard would change
  caller policy. Neither is needed for a fixed-unit native store.
- A second charge algorithm or consumer-side fallback would duplicate the owner.
  The existing private calculation can serve both public boundaries.

## Scope and exclusions

Preserve public signatures, supported forms, chemistry validation, conservation
checks, producer versions, scientific attribution and source immutability. The
quantity-returning getter continues to require a configured charge standard and
to honor it. Native numbers and report totals retain elementary-charge units.
MolecularMechanics remains experimental and excluded from H5MSM 0.5. This repair
does not change a frozen release artifact or qualify a new candidate.

## Acceptance criteria

- Native assignment succeeds with a length/time-only policy for both models.
- Canonical native charges and provenance match the configured-charge controls.
- Scalar total declarations in other charge units remain supported.
- Source domains and caller configuration are unchanged on success and failure.
- The getter preserves configured presentation and its missing-standard error.
- API, User Guide, Cookbook and relevant course guidance explain the distinction.

## Provenance

Linux, Python 3.14.7, shared MolSysSuite development environment, 2026-10-10.
Diagnosis source: `aedd5a76d195d10fc2c1fb9ac6d24c96cc751a28`.
PyUnitWizard `0.28.1+3.g2ab37a5`, RDKit `2025.9.5`, OpenMM `8.6.1`,
ArgDigest `0.15.0+1.g5c6711e`, SMonitor `0.19.0`, Ackredit `0.11.0+3.g71f7f19`.
The reported external fixture is used only for diagnosis; committed guards use
local deterministic molecules and bundled systems.

## Resolution — 2026-10-10

`calculate` returns validated numeric elementary-charge values with the existing
report. The public getter constructs a standardized quantity; the build tool
attaches the canonical values directly. Both retain their argument-digestion and
conditional provider decorators. Attribution still identifies the shared physchem
operation as scientific owner, including for native attachment; producer versions,
method parameters and references retain their existing schema.

Before the repair, the seven-case policy selection produced **four failures and
three passes**. The failures covered both native/RDKit methanol inputs, a nonzero
unitful total and real OpenMM template charges. The configured-coulomb native
controls and the getter's intentional missing-standard error passed already.
This distinguishes the storage defect from the preserved presentation contract.

After repair, **71 cases pass with no skips** in the shared development environment:

```bash
python -m pytest tests/build/test_assign_partial_charges.py \
  tests/physchem/test_get_partial_charges.py tests/basic/test_set_partial_charge.py \
  --doctest-modules molsysmt/build/assign_partial_charges.py \
  molsysmt/physchem/get_partial_charges.py --receptor=llm -n 12
```

The guard module checks methanol against the reported six-atom numerical control,
native and RDKit source immutability, canonical storage under both omitted and
coulomb charge standards, producer/reference retention, nonzero declarations in
coulomb, and untouched caller configuration on success and a total conflict.
The real alanine guard compares stored N/H/O values with independent ff14SB
template controls under a length/time-only policy. Existing guards retain
scientific rejection, projection, stale binding and PDBQT export behavior.
The getter guard retains the missing-standard error without configuration or
source mutation. These are contract and implementation controls, not new evidence
of physical charge accuracy or arbitrary force-field coverage.

Both public docstrings pass their doctests and strict parameter/default/content
checks; AST comparisons retain their signatures and validation/provider
decorators. Nine Python blocks across the three affected User Guide/Toolbox/
Cookbook pages execute, including the new length/time-only recipe. Foundations,
the native owner contract and Common Core course module 12 explain the distinction.
Course code, saved outputs and metadata remain unchanged.

Repository Ruff checks and formatting, whitespace checks, and all fourteen fast
development gates pass. These gates include dependency routes, optional import
boundaries, developer-guide integrity and course structure; they do not execute
the release's required full source or installed-package matrices.

No frozen artifact, reference or release publication state changes. Source
qualification does not qualify a replacement installed candidate.
