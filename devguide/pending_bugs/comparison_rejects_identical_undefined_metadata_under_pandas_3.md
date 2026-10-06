---
summary: Comparison rejects identical undefined metadata under pandas 3.
issue: uibcdf/molsysmt#345
status: partial
opened: 2026-10-06
closed:
severity: medium
verification: reproduced
area: [basic, deps, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# Comparison rejects identical undefined metadata under pandas 3

**Reported:** 2026-10-06 by the eight-cell source matrix for #334.
**Status:** corrected locally; focused checks pass; corrected hosted matrix pending.

## What

`msm.compare(molsys, msm.copy(molsys), attributes_type="topological",
coordinates=True, box=True)` returns False for the bundled pentalanine
trajectory under pandas 3.0.6. Even `msm.compare(molsys, molsys,
chain_type=True)` returns False. The copy retains the original information.

## How

The source adapter returns `[nan]` for undefined chain types. NumPy infers
float64 for this list. `array_equal_normalized` in `molsysmt/basic/compare.py`
handles coincident missing object entries, but its numeric branch uses
`np.allclose` without equal-NaN handling. Undefined metadata therefore compares
unequal to itself depending on its inferred array dtype.

## Why

Supported pandas 3 can preserve missing string metadata as NaN. Public equality
and copy-integrity checks must not report data loss when both systems retain
the same undefined entries. This is a stabilization defect under #334; #343
corrected different native pandas operations and did not cover this comparison.

## What is measured and what is assumed

Source run [37441978743](https://github.com/uibcdf/molsysmt/actions/runs/37441978743)
at `5bd893c85` fails Linux/Python 3.14 only at
`tests/basic/test_copy.py::test_copy_1`: 13,286 pass, 26 skip, 40 deselect,
one fails in 1,594.97 s with 2,653 warnings. Its scientific certificate passes
all 54 registered cases. The installed wheel matrix independently passes.
The remaining source cells are still executing at this initial diagnosis.

The same copy test reproduces locally with the existing pandas 3.0.6 overlay,
compatible controlled providers and the shared Python 3.14 environment:
one failure in 9.67 s with twelve workers and receptor's `llm` profile.
An attribute-level dictionary isolates `chain_type`; both source and copy
return the identical `[nan]`, float64 representation. Self-comparison is False.

## What was refuted

Copy data loss and a MolSysViewer baseline mismatch do not explain this
failure: native source/copy values are identical, and self-comparison fails
without involving Viewer. The new consumer source reference is a separate
integration advance, not a fix for this defect.

## Scope and exclusions

Normalize matching missing entries for equality of metadata arrays while
retaining shape checks, numeric tolerances and inequality when a missing entry
is replaced by a populated one. Coordinate, velocity and box-array comparisons
retain their independent geometric checks. No new API or dependency is needed.

## Acceptance criteria

- The original complete-copy test passes under supported pandas 2 and 3.
- Undefined metadata compares equal to itself and to matching NaN/None/pd.NA.
- A populated value in place of missing metadata is still unequal.
- The compare regression selection and docstring examples pass.
- Preserve the original hosted failure and local before/after results; execute
  a corrected source matrix using the delivered immutable Viewer candidate.

## Provenance

Hosted Linux/Python 3.14.7, NumPy 2.5.3, pandas 3.0.6, controlled ArgDigest
0.14.0; local shared Python 3.14.7, NumPy 2.4.6, pandas 3.0.6 overlay.
MolSysMT source `08bd8c850` retains the same executable code as `5bd893c85`.
The local and hosted commands use receptor rendering; only local execution
uses twelve workers. The scientific certificate runner executes serially.

## Correction and bounded validation — 2026-10-06

The numeric metadata branch uses `np.allclose(..., equal_nan=True)`, retaining
its existing shape checks and tolerances. Coordinate/velocity/box-array
branches keep their existing independent numerical comparisons. Three new
regression cases fail before the correction: self-comparison with numeric
NaN metadata rejects equality. Afterwards the 61-case compare/copy selection
passes under pandas 3.0.6 (28.27 s) and pandas 2.3.3 (26.38 s), with zero
skips/failures. It also asserts inequality after replacing missing metadata
with a populated chain type. The comparison docstring passes its doctest.
Warnings remain recorded. The User Guide tutorial and comparison course
module explain the missing-entry semantics; executable notebook cells are
unchanged.

The complete original matrix finishes with six failures and two passing
Python 3.11 cells. Every failed cell names only `test_copy_1`; all eight
scientific certificates pass. The
[recovery receipt](../../devtools/data/stabilization_s6_source_recovery_20261006.json)
retains actual per-cell summaries and log hashes, initial/local regression
failures and corrected results. Hosted logs report 26 Linux/27 macOS skips
and 40 deselections per cell; the earlier workflow did not retain full-suite
JUnit. The next workflow uploads each produced JUnit even on test failure.
These omissions are not passing coverage, and a local focused fix does not
qualify the full source gate.
