---
summary: H5MSM conversion silently discards stored partial charges.
issue: uibcdf/molsysmt#234
status: resolved
opened: 2026-10-02
closed: 2026-10-02
severity: high
verification: reproduced
area: [form, h5msm, molecular_mechanics]
guard: tests/form/file_h5msm/test_public_h5msm_v05.py::test_public_05_writers_reject_mechanics_without_creating_a_file
normative:
blocked_by: []
supersedes: []
---

# H5MSM conversion silently discards stored partial charges

**Reported:** Existing upstream issue, rechecked locally on 2026-10-02.
**Status:** Resolved with executable regression guards.

## What

The original issue reported that atomic partial charges disappeared from an H5MSM snapshot while its nonexhaustive conversion report said equivalent. The public writer no longer accepts such a snapshot.

## How

H5MSM 0.5 rejects any nonempty MolecularMechanics domain before creating a file. The existing writer guard now also covers partial-charge-only data, through both h5msm.write and public convert, and asserts that source charges survive the rejected operation.

## Why

Failing explicitly prevents consumers from treating a file without assigned charges as a faithful chemical snapshot.

## What is measured and what is assumed

The original silent loss was reported against 0.21.0+606.ga03eb4bf6.
Main 78981d6c1 instead rejected the charge-bearing RDKit input with the
explicit MolecularMechanics error. The strengthened guard tests that
current error path for charge-only data and preserves the source charges.

## What was refuted

The current public writer does not silently discard these charges.
Successful round-trip persistence is not required to fix the reported
silent-loss defect: explicit rejection satisfies the requested alternative.

## Scope and exclusions

The error route is supported and tested; charge persistence is not implemented. The maintainer deferred MolecularMechanics persistence to H5MSM 0.6 after 1.0 under uibcdf/molsysmt#256. The guard protects explicit rejection and the absence of a partial output file, rather than claiming a charge round trip.

## Acceptance criteria

The addressable guard `tests/form/file_h5msm/test_public_h5msm_v05.py::test_public_05_writers_reject_mechanics_without_creating_a_file` must pass and fail when its reported mechanism
returns. The public documentation and affected course modules describe the
observable behavior.

## Provenance

Linux x86-64, CPython 3.13.14, NumPy 2.4.6, Pandas 2.3.3, h5py 3.16.0;
2026-10-02. Focused pytest runs use the repository's Pytest Receptor profile.
