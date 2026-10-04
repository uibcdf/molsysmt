---
summary: SDF structure-count getter rejects dispatcher structure_indices
issue: uibcdf/molsysmt#312
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: medium
verification: measured
area: [form, attribute]
guard: tests/form/file_sdf/test_structure_count.py
normative:
blocked_by: []
supersedes: []
---

# SDF structure-count getter rejects dispatcher structure_indices

**Reported:** 2026-10-04, during the MolSysViewer public loading review.
**Status:** Resolved. Correction and public regression guard are implemented
and verified.

## What and how

The public dispatcher passes structure_indices to attributes that run on
structures. The direct single-record SDF count getter lacked that argument,
raising UnknownArgumentError instead of reporting the supported frame count.

The fix accepts digested structure selections, preserves the one-record parsing
contract, rejects indices other than 0, and returns zero for an empty selection.
Repeated requested indices follow the existing native count semantics. The guard
uses msm.get directly, rather than converting to native as a workaround.

Consumer context: uibcdf/molsysviewer#151; provider form work:
uibcdf/molsysmt#215. Provider verification does not establish an executed Viewer
load or consumer acceptance. The original consumer reproduction used Python
3.14.7; local regression uses the bounded environment below.

## Why

Public loading and composition must preserve the declared source axes and partial
information. The consumer must not implement a private provider workaround.

## What is measured and what is assumed

The consumer supplied a concrete public reproduction in the owning issue.
The seven focused tests passed in 6.51 s (four existing structural warnings).
The final broad regression passed 1480 tests in 115.88 s, with 15 warnings in six
groups (legacy H5MSM and expected structural/unit diagnostics). Command:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm tests/form/molsysmt_Topology tests/form/file_sdf tests/basic/add tests/basic/test_extract.py
```

Ruff, docstring validation and 156-notebook course structure pass. Other forms retain their existing delivery routes.

## What was refuted

Converting first or fabricating missing identities would bypass the broken public
contract without repairing it. Missing parent membership is not index zero.

## Scope and exclusions

Repair the supported public native/SDF route. No new chemical preparation,
residue inference or universal hierarchy completeness is introduced.

## Acceptance criteria

The public regression guard passes and validates source axes and missing values
without backend bypass or mutation.

## Provenance

Local Linux x86_64, Python 3.13.14, NumPy 2.4.6 and pandas 2.3.3, 2026-10-04.
Tests use the released ArgDigest 0.13.0 source snapshot at
/tmp/molsysmt-readiness-argdigest-013, under uibcdf/molsysmt#237's bounded
environment deviation. No release matrix or consumer acceptance is inferred.
