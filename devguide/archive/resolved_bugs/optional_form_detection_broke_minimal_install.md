# Optional Form Detection Broke a Minimal Installation

**Resolved:** 2026-07-28  
**Fix commit:** `c4d8e9074`  
**Regression:** `tests/basic/test_get_form.py`

## Symptom

The installed public-runtime smoke converted the bundled Trp-Cage H5MSM system
to `molsysmt.MolSys`, but the immediately following
`molsysmt.get(..., n_atoms=True)` rejected that native object:

```text
ArgumentError: Error in argument 'molecular_system' with value
'<molsysmt.native.molsys.MolSys ...>'
```

The failure reproduced on Python 3.11, 3.12, and 3.13. It was absent from the
development environment because OpenMM was installed there.

## Root Cause

`molsysmt.form._dict_modules` deliberately exposes known optional forms when
`show_all_capabilities=True`. `get_form()` incorrectly treated every visible
form as an executable detector. While classifying the native `MolSys`, it
reached `openmm_GromacsTopFile.is_form()`, which imports `openmm.app`.
OpenMM was intentionally absent from the minimal installed-wheel environment,
so classification stopped with `ModuleNotFoundError` before reaching the
native-form detector.

The specific form also lacked its `openmm` entry in the central
`molsysmt._depdigest.MAPPING`. This prevented both registry filtering and
runtime detector filtering from applying the declared soft-dependency policy.

## Resolution

The fix makes two complementary contracts explicit:

1. `openmm_GromacsTopFile` is mapped to the `openmm` soft dependency.
2. `get_form()` skips a detector when its mapped soft dependency is not
   installed, while keeping the form visible for capability introspection.

The implementation does not catch arbitrary `ModuleNotFoundError` exceptions.
If an installed detector is broken, that defect remains visible rather than
being misclassified as an unsupported molecular system.

## Evidence

- focused form and workflow contract tests: 29 passed;
- molecular-system validation plus focused contracts: 35 passed;
- complete `tests/basic` surface: 449 passed;
- dependency-boundary validator: passed;
- Ruff and developer-guide validation: passed;
- a clean local wheel installed non-editably in an isolated Python 3.13
  environment without OpenMM passed the complete installed public-runtime
  validator;
- GitHub Actions run `30394881487` passed the installed public-runtime smoke on
  Python 3.11, 3.12, and 3.13.

## CI Feedback Correction

The Linux x86_64 wheel is now an independent prerequisite for the public
smokes and NumPy-floor jobs. Those checks start as soon as the Linux artifact
is available; the four remaining portability builds continue in parallel.
Run `30394881487` started all three public smokes after the Linux wheel
completed in 3 minutes 19 seconds, without waiting for macOS Intel.
