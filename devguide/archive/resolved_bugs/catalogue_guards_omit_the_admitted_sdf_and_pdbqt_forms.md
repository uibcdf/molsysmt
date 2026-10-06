---
summary: Catalogue guards omit the admitted SDF and PDBQT forms
issue: uibcdf/molsysmt#340
status: resolved
opened: 2026-10-06
closed: 2026-10-06
severity: medium
verification: reproduced
area: [tests, form]
guard: tests/basic/test_get_form_battery.py::test_the_battery_covers_the_catalogue
normative:
blocked_by: []
supersedes: []
---

# Catalogue guards omit the admitted SDF and PDBQT forms

**Reported:** 2026-10-06, while reconciling older automatic full-suite failures
under S5/#237. **Status:** Resolved with real catalogue routes and preserved
independent supported-table expectations.

## What

The catalogue census fails because `file:pdbqt` and `string:pdbqt_text` are
registered but absent from its routes and explicit unreachable set. Three
supported-table tests also reject registered `file:sdf` and the two PDBQT forms.

```bash
python -m pytest --receptor=llm \
  tests/basic/test_get_form_battery.py::test_the_battery_covers_the_catalogue \
  tests/supported/test_supported.py
```

The four selected cases fail on clean source `ce769ffb7` with exact extra-form
assertions. This reproduces those failures from automatic producer `a8f567c82`;
it does not attribute all its failures to one cause.

## How

The maintained expectations did not follow the admitted adapters. Add actual
file and explicitly prefixed text routes using the existing pinned Vina 1iep
ligand fixture. Add the corresponding explicit supported forms/conversion rows,
including SDF. Preserve exact census equality and the independent expected
catalogue; do not generate expected output from the implementation under test.

## Why

Required full CI fails despite working registered adapters. Incorrectly adding
these forms to the unreachable set or omitting the census would hide the coverage
gap. The defect concerns test inventory maintenance, not chemical correctness.

## What is measured and what is assumed

**Reproduced:** four failures in 15.65 seconds on Python 3.14.7 with the exact
released SMonitor 0.18.0, DepDigest 0.13.0, PyUnitWizard 0.28.1 and ArgDigest
0.13.0 provider directory. After correction, 45 cases pass in 25.75 seconds
without skips, including both real file/text detection routes and existing
five-system native Vina PDBQT contract cases. One expected legacy H5MSM warning
comes from the battery's bundled origin. Ruff check/format pass.

The [dated artifact](../../../devtools/data/catalogue_guards_20261006.json) retains
both outcomes, commands, fixture and changed-test hashes. The separate native
provider smoke at `ce769ffb7` passes on Python 3.14 in run `37423046917`;
its successful test step is distinct from these local inventory repairs.

## What was refuted

These four assertions are not evidence that the parser misrecognizes or corrupts
PDBQT/SDF: they explicitly name extra registered forms, and actual recognition
and existing parsing/fidelity cases pass. This result does not eliminate other
full-suite chemistry, optional-provider or converter failures.

## Scope and exclusions

Only catalogue routes and independently maintained test expectations change.
No public API, parser, molecular data or scientific assertion is changed. The
full installed/cross-platform candidate gates remain #237/#334/S6 work.

## Acceptance criteria and resolution

The catalogue census includes both new routes and still rejects an unaccounted
registered form. File/text recognition uses a real pinned input. Supported table
expectations explicitly include admitted SDF/PDBQT entries. Existing real-PDBQT
fidelity tests pass. All criteria are satisfied by the 45-case selection.

The front-matter guard protects route coverage; `tests/supported/test_supported.py`
additionally guards supported form/type and both conversion-table contracts.
Neither exact equality nor scientific fidelity assertions are weakened.

## Provenance

2026-10-06, host nauta, Python 3.14.7, base `ce769ffb7`, isolated exact released
provider sources recorded under #237. Results apply to this scoped editable
source selection, not a release package or complete test matrix.
