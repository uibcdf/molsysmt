---
summary: Profile and reduce test-suite runtime without weakening coverage
issue: uibcdf/molsysmt#122
status: open
opened: 2026-09-19
closed:
verification: measured
area: [tests, performance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Profile and reduce test-suite runtime without weakening coverage

**Reported:** 2026-09-19, after an accidental serial full-suite run made the cost of
routine local validation directly observable. This adopts the much older, one-line
fixture proposal in uibcdf/molsysmt#122 and broadens its diagnosis without assuming that
fixture scope is the only or the dominant cause.
**Status:** open. The need is measured; the cost distribution and the right interventions
still require profiling.

## What

Profile the complete MolSysMT test suite and reduce both wall-clock time and avoidable
work while preserving the same behavioral, scientific, dependency, and form-contract
evidence. Treat fixture reuse as one candidate intervention, not as the conclusion.

The campaign must distinguish:

- inherently expensive scientific or integration evidence;
- repeated construction, conversion, parsing, serialization, or dependency startup that
  can be shared safely;
- duplicated cases that prove no distinct contract;
- collection and doctest overhead;
- scheduling imbalance under `pytest-xdist`;
- tests whose cost belongs in a focused or scheduled lane without disappearing from the
  release gate.

## How

1. Establish comparable cold- and warm-cache baselines for serial execution and the
   documented large-suite mode, `-n 12 --dist loadfile`, recording total wall time, summed
   test time, collection time, and the slowest nodes and modules.
2. Profile before changing fixture scopes. Identify the constructors, conversions, file
   reads, optional-dependency imports, and parametrized paths responsible for most of the
   cumulative cost.
3. Remove avoidable work with the smallest safe mechanism: immutable session/module
   fixtures, shared bundled artifacts, narrower setup, parametrization consolidation,
   or better xdist grouping. A shared fixture must not leak mutable state between tests.
4. Keep a machine-readable inventory of collected, executed, skipped, deselected, and
   registered scientific-evidence nodes before and after each optimization.
5. Re-measure on the same host and environment. Report wall-clock and aggregate CPU/test
   time separately so parallel scheduling is not mistaken for elimination of work.

The existing `devtools/tests` timing and coverage targets should be reused or extended;
this proposal must not introduce a second test runner with a competing policy.

## Why

Full local validation is frequent during stabilization. A serial run on the reference
development environment executed only 3,793 of 10,228 collected tests in 760.75 seconds
before it was deliberately interrupted; extrapolating linearly would put that run above
34 minutes. The repository already prescribes 12 xdist workers for broad validation, but
parallelism only reduces elapsed time: it does not remove redundant setup, I/O, imports,
or repeated molecular-system construction.

A lighter suite improves feedback time and makes developers more likely to run the full
evidence before committing. The constraint is stronger than “keep the count green”:
tests may become faster only if the intent of every gate remains protected.

## What is measured and what is assumed

**Measured:**

```bash
pytest -p no:rerunfailures --receptor=llm
# INTERRUPTED: 3791 passed, 2 skipped, 40 deselected;
# 3793 of 10228 executed in 760.75 s
```

The command was serial because `pytest.ini` has no xdist `addopts`. It was interrupted
once that mistake was identified; no test had failed.

The documented parallel mode completed on the same working tree:

```bash
pytest -p no:rerunfailures --receptor=llm -n 12 --dist loadfile
# PASS: 10217 passed, 11 skipped in 377.90 s
```

The 11 skips are the existing environment/dependency omissions: nine obsolete PyTraj
finalizer cases, one RDKit SMILES case, and one unavailable CuPy case. This is a valid
full-suite checkpoint, not yet an optimization baseline: it has no repeated samples,
cold/warm separation, or aggregate per-node timing.

**Measured:** `devguide/testing_strategy.md` defines `pytest -n 12 --dist loadfile` as the
default full-suite confirmation when xdist is available, and `devtools/tests/Makefile`
already exposes worker count, distribution mode, slowest-test, and coverage targets.

**Assumed:** repeated setup and conversion account for a material fraction of aggregate
test time. This is plausible and is the premise of the original fixture issue, but no
profile yet establishes its share.

**Estimate:** the serial full-suite projection above is a linear extrapolation, not a
baseline. Test costs are not uniformly distributed, so it must not be used to claim a
speedup.

## What was refuted

**That the suite was already running on 12 workers by default.** It was not.
`pytest.ini` configures doctests, quiet output, and import mode, but no `-n` option.
Parallelism is a documented invocation policy rather than an automatic pytest default.

**That adding fixtures alone is an adequate plan.** Broader-scoped fixtures can save
substantial setup, but they can also create order dependence and mutable-state leakage.
The bottlenecks must be measured before choosing scopes or sharing objects.

**That xdist solves the optimization problem.** It shortens wall time by spending work
concurrently. It can hide redundant CPU work and can perform poorly when slow files are
imbalanced under `loadfile`; both dimensions require separate measurements.

## Scope and exclusions

Covered: test implementation cost, fixture lifetimes, reusable test data, collection and
doctest overhead, parametrization, xdist scheduling, and lane placement for genuinely
heavy evidence.

Excluded: weakening assertions, deleting distinct contract cases, converting failures to
skips, lowering coverage thresholds, or removing nodes from the scientific-evidence
registry. Product-code performance belongs in its own performance work unless a test is
performing unnecessary product work solely as setup.

## Acceptance criteria

- A dated baseline identifies cumulative time by node and module for serial and
  `-n 12 --dist loadfile` execution on the same environment.
- The dominant avoidable costs are named from profiles rather than intuition.
- The optimized suite preserves the collected contract inventory, the zero-skip
  registered scientific-evidence execution, and the full release-gate result.
- Every shared mutable fixture has an isolation guard, or is redesigned as immutable.
- Repeated measurements demonstrate a material reduction in both parallel wall time and
  avoidable aggregate test work; the closing record reports exact numbers and variance.
- `devguide/testing_strategy.md` and `devguide/devtools_and_ci.md` describe the resulting
  maintained workflow and are named as the normative outcome.

## Dependencies and risks

Coverage runs and warning aggregation have known xdist-specific behavior. Optimizations
must retain the documented `loadfile` warning policy and verify that coverage data still
combines correctly. Session-scoped molecular systems are particularly risky when public
operations mutate in place.

## Provenance

Linux, Python 3.13, pytest 9.1.1, pytest-xdist 3.8.0, MolSysMT working tree based on
`a68454a24`, 2026-09-19.
