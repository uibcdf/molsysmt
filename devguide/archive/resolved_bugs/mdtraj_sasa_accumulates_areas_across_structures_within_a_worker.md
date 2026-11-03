---
summary: MDTraj SASA accumulates areas across structures within a worker
issue: uibcdf/molsysmt#529
status: resolved
opened: 2026-11-02
closed: 2026-11-02
severity: high
verification: reproduced
area: [tests, units, deps]
guard: tests/physchem/get_sasa/test_get_sasa_units.py::test_mdtraj_structure_results_do_not_depend_on_previous_structures
normative:
blocked_by: []
supersedes: []
---

# MDTraj SASA accumulates areas across structures within a worker

**Reported:** 2026-11-02, while completing the ChemicalStates source qualification.
**Status:** The adapter protection passes focused/local science and three complete
final-source Linux suites. Remaining source/platform qualification is pending.
Future upstream batching qualification and removal are tracked separately in #530.

## What

The macOS/Python 3.14 cell of source run 41562051654, provider dbcb4582c,
completes with 23,599 passes, 54 failures, 103 skips and 40 deselections,
exit 1. All 54 failures are MDTraj isolated-carbon area cases. An isolated
carbon of inflated radius 0.31 nm must have area 1.207628216 nm² in every
structure, within the declared float32 tolerance. The observed sequence is
1.207628250, 1.209147453, 1.209149361 nm².

This is reproducible directly in MDTraj 1.11.1 with OMP_NUM_THREADS=1;
MolSysMT's batch adapter exposes the same error. Independent one-structure
MDTraj calls all return 1.207628250 nm². The upstream issue is already open:
[mdtraj/mdtraj#2195](https://github.com/mdtraj/mdtraj/issues/2195), observed
open on this date with milestone 1.12.0. That milestone is not proof of a fix
or a qualified minimum version.

```bash
OMP_NUM_THREADS=1 python -m pytest --receptor=llm   tests/physchem/get_sasa/test_get_sasa_units.py
```

## How

The inspected upstream `mdtraj/geometry/src/sasa.cpp` allocates a zeroed
`outframebuffer` once per worker. Its structure loop reuses that buffer without
clearing it. `asa_frame` increments and rescales the same areas. Consequently,
the next structure includes the previous area's scaled contribution. With
OpenMP the first structure per worker is correct, which can hide the defect
on hosts with more threads than structures. Our direct shared-environment
probe reproduces the macOS numbers on Linux when constrained to one thread.

The MolSysMT correction preallocates the final float32 atomic output and calls
MDTraj once per requested structure, using a single-structure slice without a
coordinate copy. Output selection, all-atom occlusion, grouping, units and
source immutability retain their existing contracts. No alternate algorithm,
radius, tolerance or implicit native-engine substitution is introduced.

## Why

The defect affects scientifically meaningful solvent exposure, depends on worker
assignment and can silently pass a short trajectory on a many-core host. Raising
the tolerance would accept systematic incorrect areas. A newer native domain
layout does not cause the provider's accumulation, but this existing public
adapter must deliver correct results before its source qualification closes.

## What is measured and what is assumed

- The real-provider subprocess guard uses one and two OpenMP threads, more
  requested structures than threads, atom/group outputs, changing overlap,
  nonconsecutive/repeated structure indices, pm output policy and immutable input.
  Independent single-structure results are cross-checked against an analytic
  isolated sphere. Before correction all four cases fail (232, exit 1, 8.76 s).
- The corrected complete SASA directory plus public function doctest passes
  263 cases, exit 0, 56.50 s (233), with 23 retained warnings. The supported
  receptor reader verifies finalized, complete, integrity-valid evidence and
  no dropped records. A reference-link-only docstring edit overlapped this run;
  the final frozen-source check passes the same 263 cases, exit 0, 57.53 s (234). No executable or test inputs changed during that final check.
- This is focused Linux/shared-environment evidence, not a passing macOS matrix
  or installed package qualification. Earlier full-source runs do not test the
  correction and retain their actual outcomes.
- Additional provider-call overhead is inherent to the workaround. No speedup
  or performance magnitude is claimed; no MDTraj parallelism across structures
  is retained. The native compiled engine remains available for large ensembles.

## What was refuted

The first hypothesis was a unit conversion or platform tolerance discrepancy.
An equivalent direct provider call reproduces the failure in nm without
PyUnitWizard or MolSysMT conversion, and separate calls return the analytic
area. The buffer recurrence explains the measured bias. Increasing sampling
density reduces this bias but cannot repair retained worker state. Tests and
scientific tolerances therefore remain unchanged.

## Scope and exclusions

This adapter correction covers Cartesian MDTraj SASA for all requested
structures before output selection/aggregation. Native Rust kernels, PBC
screening, chemistry ownership, public schema and dependency floors do not
change. No third-party checkout or package is modified. The already-reported
upstream defect is linked rather than duplicated.

## Acceptance criteria

1. The new real-provider worker-reuse guard fails before correction and passes
   afterward, independently of OpenMP thread count and output aggregation.
2. Existing analytic unit, occlusion, probe/sampling, form and periodic-contract
   tests and the public doctest retain their strict expectations.
3. Docstring, Foundations, Toolbox, Cookbook and relevant course pages explain
   independent structure evaluation and its performance tradeoff.
4. Record final source and platform outcomes honestly before closeout. Retain a
   tracked removal condition: restore batched provider evaluation only after
   a published MDTraj fix is independently qualified by the worker-reuse guard.

## Dependencies and risks

The workaround works with the currently supported provider and does not require
an unverified version floor. Per-structure provider overhead may be material for
large ensembles. The native engine is the documented performance route while
upstream batch correctness is unavailable. The guard remains useful after a
provider upgrade and must not be removed with the workaround.

## Provenance

Observed 2026-11-02 local date (2026-11-03 UTC). Hosted macOS 15/arm64,
Python 3.14.10, full source dbcb4582c; exact raw logs retained privately as
macos314-old-231. Local Linux, shared Python 3.14.7, MDTraj 1.11.1,
NumPy 2.4.6; native binary unchanged. Local red/green artifacts are retained
under the owning ChemicalStates qualification workspace, suffixes 232/233.
No package, merge, release or all-platform success is asserted.


## Corrected-source local qualification — 2026-11-02

The final frozen-source SASA directory plus doctest passes all 263 cases,
exit 0, 57.53 seconds (234), retaining the 23 warnings. The canonical artifact
is finalized, session-complete and integrity-valid with no dropped records.
Ruff and formatting pass for 4,221 files, fast gates pass 14/14 and the
docstring validator passes 246 public functions. Strict serial Sphinx HTML
passes (235); the upstream issue link is present on all eight relevant rendered
API, guide and course pages. Existing notebook code/outputs/metadata and the
four unrelated dirty API stubs retain their exact prior bytes. An earlier
Sphinx command used an incorrectly typed CLI override and failed with
configuration warnings; its unsuccessful log is preserved separately. These
results qualify the adapter correction locally, without relabeling older
full-suite or in-progress platform evidence.


## Final-candidate Linux worker-reuse execution — 2026-11-02

All four real-provider worker-reuse cases are matched to passing call records
in each final-source Linux/Python 3.11, 3.12 and 3.13 complete artifact (243/244),
not hidden in optional-dependency omissions. Each full suite passes 23,672 cases,
with 102 skips and 40 default-policy deselections, exit 0; complete canonical
primary evidence and JUnit agree. The actual macOS suites, including the
original failing platform, remain pending. Keep the documented performance
tradeoff and upstream-fix qualification/removal condition explicit.

Future restoration of batched provider evaluation is explicitly owned by #530
and its [acceptance plan](../../pending_proposals/qualify_corrected_mdtraj_batch_sasa_and_retire_independent_structure_evaluation.md).
That post-1.0 performance work retains the real worker-reuse guard and does not
turn the protected adapter into an unresolved scientific correctness defect.


## Resolution — 2026-11-02

The MDTraj adapter preallocates atomic output and evaluates each requested structure independently using no-copy slices, preventing retained provider worker areas while preserving method, radii, occlusion, order/repetitions, grouping, units and source identity. Final runtime de7ffad2a completes all eight full source cells, including the original macOS Python 3.14 failure context, and the constrained one/two-thread worker-reuse guard passes all four cases in every cell. The complete local default selection passes 23,774 cases with two disclosed skips. No numerical tolerance or provider identity is changed. The call-overhead/parallelism tradeoff is documented; future published-fix qualification, measured batching recovery and older-Python compatibility remain separately tracked in #530. This is a protected-adapter correctness fix, not a claim that upstream #2195 is fixed.

The complete source matrix is [41572981893](https://github.com/uibcdf/molsysmt/actions/runs/41572981893), officially successful on de7ffad2a. The #255 source closeout records full counts, omissions, science scopes and evidence limits. No main merge, package promotion or release is performed.
