---
summary: Restore current Codecov evidence before reintroducing the coverage badge.
issue: uibcdf/molsysmt#286
status: partial
opened: 2026-10-01
closed:
verification: inspected
area: [governance, ci, coverage]
guard: devtools/tests/test_nightly_full_gate.py
normative: coverage_reporting.md
blocked_by: []
supersedes: []
---

# Current coverage reporting with preserved test outcomes

## What

The public main-branch badge inherited March coverage while recent complete
scientific executions did not upload their generated reports. The initial
maintainer decision deferred a forced suite; on 2026-10-01 the maintainer then
authorized one complete Linux/Python 3.13 execution to refresh the report.

## How

The existing weekly workflow gains an explicit manual single-interpreter option.
Its scheduled/default route retains the three-minor matrix and existing gates.
A pytest step retains the real exit status; only normal completed-suite statuses
0/1 allow artifact retention and main-branch coverage upload. Failed tests still
fail CI. Aborted/invalid suites cannot produce an accepted reporting claim.
See [the maintained procedure](../coverage_reporting.md).

## Why

Run 36868722733 on 2026-10-01 executed the full Python 3.13 suite: 4 failed,
10,298 passed, 2 skipped, 40 deselected, in 1,763.88 seconds. The preceding
scientific gate passed 54 cases. Upload was skipped solely because the package
tests failed. A coverage report and scientific pass are separate facts.

## What is measured and what is assumed

Read-only native job/log inspection establishes the prior execution and skipped
upload. Current source is being prepared for the authorized manual run; neither
a new accepted report nor a passing full matrix is claimed yet.

## What was refuted

Requiring a scientific pass before retaining/reporting coverage suppresses useful
measurement. Treating upload acceptance as test success would hide the failure.
Running all three Linux interpreters is unnecessary for the authorized single
report and cannot be confused with clearing full-matrix debt.

## Scope and exclusions

Reporting and explicit manual scope only. Existing scientific assertions, skips,
coverage exclusions, dependency sources and release rules retain their ownership.
No scientific repair or public package release is included.

## Acceptance criteria

One exact-source Linux/Python 3.13 full suite executes; actual results and XML
are retained; Codecov independently exposes a complete report for the uploader
SHA and numeric SVG; the README gains a scoped live badge. The matrix-debt guard
proves that one interpreter cannot pay full-suite debt; the maintained reporting
contract specifies failure and abort handling.

## Provenance

2026-10-01, host nauta for read-only preparation; prior hosted run
https://github.com/uibcdf/molsysmt/actions/runs/36868722733. The new hosted identity
and actual report/source observation will be added after execution.
