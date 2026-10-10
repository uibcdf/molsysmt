---
summary: Translated co-located fit anchors admit underdetermined rotations.
issue: uibcdf/molsysmt#367
status: resolved
opened: 2026-10-10
closed: 2026-10-10
severity: high
verification: reproduced
area: [structure, tests]
guard: tests/structure/fit/test_degenerate_anchors.py::test_translated_coincident_anchors_are_rejected_before_mutation
normative:
blocked_by: []
supersedes: []
---

# Translated fit anchors admit underdetermined rotations

**Reported:** 2026-10-10, provider request from PharmacophoreMT.
**Status:** Resolved; translated degenerate anchors are rejected before fitting.

## What

`structure.least_rmsd_fit` accepts exactly two distinct centers represented by
three atoms at some translated origins, despite promising to reject fit or
reference selections that cannot determine a unique three-dimensional rotation.

```bash
python -m pytest --receptor=llm -n 12 tests/structure/fit/test_degenerate_anchors.py
```

Before the repair, the initial double-precision matrix reports **61 failed, 60 passed** on source
`a1ad51b7c2296c667f6221ccca5cfa37ab74ac67`. Sixty failures are accepted
degenerate source/reference selections; the remaining failure admits a later
degenerate structure into an in-place fit. The tests check exact represented
duplicates, three origins, three orders, mixed nm/angstrom inputs and both
mutation modes. Valid triangle controls and existing collinearity cases pass.

## How

The private uniqueness check in
[`least_rmsd_fit.py`](../../../molsysmt/structure/least_rmsd_fit.py) subtracts the
arithmetic mean before computing numerical matrix rank. Rounded centering can
invent an independent singular direction for coincident anchors.

Subtract an existing represented anchor instead. This preserves exact duplicates
and the linear dependence of the two distinct represented centers, including
when the distinct center is first. Retain NumPy's default numerical rank policy
after the existing shared unit alignment. Validate every requested source and
reference structure before dispatching a fit or mutating coordinates.

## Why

An arbitrary rotation about the remaining line can move other atoms unpredictably.
PharmacophoreMT's explicit alignment mappings rely on this provider contract;
consumer ownership is tracked in uibcdf/pharmacophoremt#31 and
uibcdf/pharmacophoremt#41. This is a correction to an existing scientific
validation boundary and belongs in bounded pre-1.0 stabilization.

## What is measured and what is assumed

The pre-repair public test outcome above is measured, including a valid triangle
with an independent known rigid transformation. Exact duplicate identity is
asserted on the supplied arrays. No performance claim or installed-package
qualification is made. Arbitrarily near-collinear geometry is subject to
floating-point numerical rank, not a new physical tolerance.

## What was refuted

The detector/kernel is not the source of the admission: invalid geometry passes
the Python boundary before Kabsch execution. More atom labels do not supply more
distinct centers. Canonical nm input alone is insufficient: translated failures
occur without unit conversion. No consumer Kabsch implementation is required.

## Scope and exclusions

Repair source/reference uniqueness validation, preserve accepted noncollinear
fits, and document rejection and mutation safety. No public signature, fitting
method, physical tolerance, Rust kernel or new geometry diagnostic is introduced.
Publication remains paused under [the release ledger](../../release_1_0_status.md).

## Acceptance criteria

- Public translated duplicate and collinear selections are rejected in both axes.
- Permutations and mixed length units do not admit the duplicate-anchor case.
- All requested structures are checked before any in-place transformation.
- Analytic noncollinear fits retain accuracy through native and dictionary forms.
- Docstrings, User Guide, Cookbook and affected course modules explain the contract.

## Provenance

Linux development environment, Python 3.14.7, NumPy 2.4.6; 2026-10-10.
The command above uses pytest-receptor and twelve pytest workers. The executable
tests retain the durable reproduction; the initial matrix was extended to include
single precision and selection of valid structures alongside an excluded degenerate
structure after reproducing the original defect. Source evidence is distinct from
frozen artifacts.

## Resolution and validation — 2026-10-10

The uniqueness boundary now checks differences from the first represented point,
with an explicit rejection of fewer than three anchors. Public signatures and
Kabsch kernels are unchanged. The expanded regression includes single/double
precision, mixed forms and units, both degenerate axes, order permutations,
in-place failure safety and nonconsecutive structure selection.

The combined focused invocation passes **242 tests**:

```bash
python -m pytest --receptor=llm -n 12 \
  tests/structure/fit tests/structure/test_least_rmsd_fit_gpu.py \
  tests/scientific_truth/structure/test_alignment.py \
  tests/scientific_truth/structure/test_rigid_transformations.py \
  molsysmt/structure/least_rmsd_fit.py --doctest-modules
```

Three warnings concern reading bundled legacy H5MSM 0.4 data. The strict Sphinx
render of the changed public docstring passes separately; two Python warnings
report upstream Sphinx 11 deprecations, with no RST warnings.

**Contract-tested:** rejection of underdetermined geometry and validation before
mutation. **Scientifically validated:** the independent known proper rotation
recovers noncollinear reference coordinates, including translated triangles,
within the test's absolute 1e-12 nm tolerance in double precision. These claims
do not extend to arbitrary near-collinear inputs or installed artifacts.

The Foundations explanation, tool tutorial, Cookbook recipe and all four
comparison/superposition course modules now describe the fit requirement. Their
existing notebook code cells, execution metadata and saved outputs are unchanged.

All 14 fast release gates, Ruff checks and the public signature comparison against
the parent pass. This does not execute or replace the heavy release qualification.
