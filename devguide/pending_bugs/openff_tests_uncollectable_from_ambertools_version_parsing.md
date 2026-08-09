---
summary: Five OpenFF test modules fail at collection because the toolkit misparses the AmberTools version.
issue: uibcdf/molsysmt#143
status: open
opened: 2026-08-08
closed:
severity: low
verification: upstream
area: [tests, deps]
guard:
normative:
blocked_by: []
supersedes: []
---

# The OpenFF test modules cannot be collected in this environment

**Reported:** 2026-08-08, seen in a full-suite run (9878 passed, 2 skipped) as the only
remaining red. Pre-existing: it also fails on a clean checkout and is unrelated to any
MolSysMT change.

**Status:** open, upstream. Nothing to fix in MolSysMT.

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

The OpenFF Toolkit reads the AmberTools version by parsing the output of `antechamber -L`:

```python
# openff/toolkit/utils/ambertools_wrapper.py:64
# TODO: More reliable way to extract AmberTools version
out = subprocess.check_output(["antechamber", "-L"])
ambertools_version = out.decode("utf-8").split("\n")[1].split()[3].strip(":")
```

The `antechamber` in this environment prints something whose second line has fewer than
four fields, so the index fails and the exception escapes at import time. Their own comment
marks the approach as provisional.

`import openff.toolkit` on its own succeeds; `import openff.toolkit.topology` is what
fails, which is why only these modules are affected.

## Next steps

1. Check whether a different AmberTools build in the environment prints the expected
   format -- this may be a version pairing rather than a permanent incompatibility.
2. If it is not fixable locally, decide what the suite should do: skipping the modules with
   a reason keeps a full run honestly green, but silently drops coverage of two supported
   forms, so it should be a deliberate choice rather than a workaround.
3. Either way, `tests/basic/test_get_form_battery.py` already records `openff.Molecule` and
   `openff.Topology` in `UNREACHED`, so the census does not pretend they are covered.
