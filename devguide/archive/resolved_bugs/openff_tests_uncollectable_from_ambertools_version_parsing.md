---
summary: Five OpenFF test modules fail at collection because the toolkit misparses the AmberTools version.
issue: uibcdf/molsysmt#143
status: resolved
opened: 2026-08-08
closed: 2026-08-09
severity: low
verification: reproduced
area: [tests, deps]
guard: tests/test_openff_dependency_contract.py::test_openff_runtime_bounds_are_in_ci_and_development_environments
normative: devguide/testing_strategy.md
blocked_by: []
supersedes: []
---

# The OpenFF test modules cannot be collected in this environment

**Reported:** 2026-08-08, seen in a full-suite run (9878 passed, 2 skipped) as the only
remaining red. Pre-existing: it also fails on a clean checkout and is unrelated to any
MolSysMT change.

**Status:** resolved. The parser defect was upstream, but MolSysMT's unconstrained test
environment and permissive skip logic were local defects.

**Severity:** low in kind, real in effect. No MolSysMT code is wrong, but five test modules
never run, so the `openff.Molecule` and `openff.Topology` support they cover is unverified
here -- and a full-suite run exits non-zero, which trains people to ignore a red suite.

## Symptom

```
$ python -m pytest tests/form/openff_Molecule tests/form/openff_Topology -q
COLLECTION_ERROR exit=2 | incomplete: 0 of 0 executed | 1 root cause

[1] IndexError | 5 tests | collect
    toolkit/utils/ambertools_wrapper.py:64
    IndexError: list index out of range
```

Affected: `tests/form/openff_Molecule/` (`test_chemical_metadata.py`,
`test_get_topological_attributes.py`, `test_structures_and_subset.py`) and
`tests/form/openff_Topology/` (`test_chemical_contract.py`,
`test_get_topological_attributes.py`).

Not a parallelism artifact: it fails the same way with and without `-n 14`.

## Diagnosis

OpenFF Toolkit 0.10.7 reads the AmberTools version by parsing the output of
`antechamber -L`:

```python
# openff/toolkit/utils/ambertools_wrapper.py:64
# TODO: More reliable way to extract AmberTools version
out = subprocess.check_output(["antechamber", "-L"])
ambertools_version = out.decode("utf-8").split("\n")[1].split()[3].strip(":")
```

AmberTools 24.8 uses `antechamber -L` to list formats and charge methods; it does not put a
version in the position expected by OpenFF Toolkit 0.10.7. The index therefore fails and
the exception escapes at import time. OpenFF fixed this parser in PR #1866, first released
in 0.16.1. Version 0.17.1 is the first release that both includes the fix and explicitly
declares support for Python 3.11, 3.12, and 3.13.

`import openff.toolkit` on its own succeeds; `import openff.toolkit.topology` is what
fails, which is why only these modules are affected. The environment manifests did not
request OpenFF at all, so an obsolete version left from an earlier solve could survive
indefinitely.

Updating only `openff-toolkit-base` exposed a second incompatible leftover:
`openff-units 0.1.8` imports the removed private symbol `pint.measurement._Measurement`.
OpenFF Toolkit 0.17.1 documents support for the `openff-units 0.3.x` line and modern Pint.
The old test modules caught this nested `ModuleNotFoundError` through `importorskip` and
reported 21 skips, turning a broken installation into a green run with no OpenFF coverage.

## Resolution — 2026-08-09

1. The CI and development environments now require `openff-toolkit-base >=0.17.1` and
   `openff-units >=0.3.0`. MolSysMT already installs RDKit and AmberTools separately, so
   the heavier `openff-toolkit` metapackage and its optional NAGL/PyTorch stack are not
   required.
2. The `soft` Python extra carries equivalent lower bounds for non-Conda installations.
3. OpenFF test modules check whether the `openff.toolkit` import root exists and skip only
   when it is absent. An exception raised while importing an installed OpenFF stack now
   remains a collection error.
4. `openff.Molecule` and `openff.Topology` moved from `UNREACHED` into executable routes
   in the catalogue-wide `get_form` battery.
5. The soft-import validator now derives its roots from the normative
   `molsysmt/_depdigest.py` registry instead of maintaining an incomplete second list. It
   also guards the OpenFF bounds in the CI environment.

The durable absent-versus-broken dependency rule is recorded in
`devguide/testing_strategy.md`.

Validation evidence:

- The exact minimum pair (`openff-toolkit-base 0.17.1`, `openff-units 0.3.2`) imports with
  Python 3.13, registers RDKit 2025.09.5 and AmberTools 24.8, and passes all 30 OpenFF
  adapter tests.
- Conda dry-runs resolve the declared lower bounds with RDKit and AmberTools for Python
  3.11 and 3.12; Python 3.13 was tested by execution.
- `python -m pytest --receptor=llm tests/form/openff_Molecule tests/form/openff_Topology tests/test_openff_dependency_contract.py tests/basic/test_get_form_battery.py`
  passes 235 tests.
- `python -m pytest --receptor=llm -n 12 tests/form tests/test_dependencies_architecture.py tests/test_openff_dependency_contract.py`
  passes 6,717 tests with two unrelated, explicit skips and no OpenFF skip.
- `python devtools/scripts/validate_dependencies.py` passes both the lazy-import and
  OpenFF environment checks.
- `python devtools/scripts/release_gate.py` passes all 12 fast gates.
