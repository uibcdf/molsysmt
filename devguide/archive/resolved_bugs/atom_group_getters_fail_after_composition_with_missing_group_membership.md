---
summary: Atom group getters fail after composition with missing group membership
issue: uibcdf/molsysmt#313
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: medium
verification: measured
area: [form, attribute]
guard: tests/basic/add/test_partial_hierarchy.py
normative:
blocked_by: []
supersedes: []
---

# Atom group getters fail after composition with missing group membership

**Reported:** 2026-10-04, during the MolSysViewer public loading review.
**Status:** Resolved. Correction and public regression guard are implemented
and verified.

## What and how

Joining a conventional protein and native caffeine leaves 24 ligand atoms
without group membership. Identity getters indexed NumPy arrays with a nullable
parent-index array, raising IndexError. Missing membership must not become an
arbitrary real group or invented residue.

Map nullable parent indices through the existing native hierarchy tables. Group
ID/name/type and the same group-based molecule/entity paths return one value per
selected atom: actual identity where present, None where a parent is missing.
A wholly absent group table retains the existing group-identity None contract.
No source table, hierarchy, atom order or ID is reconstructed by a getter.

The guard composes 596 villin atoms and 24 caffeine atoms through msm.add,
checks full/selected/empty identity queries, and repeats them after extraction
and H5MSM 0.5 round trip. It checks all group-based molecule/entity paths to
prevent another field from reproducing the same nullable-index failure.
Consumer context: uibcdf/molsysviewer#151. Provider checks do not establish
executed scene reconstruction or Viewer acceptance.

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
