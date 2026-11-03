---
summary: Course plotting examples block the macOS source test matrix
issue: uibcdf/molsysmt#528
status: resolved
opened: 2026-11-02
closed: 2026-11-02
severity: medium
verification: reproduced
area: [tests, docs, ci]
guard: tests/documentation/test_center_examples.py::test_geometric_course_executes_with_local_source_substitutions
normative:
blocked_by: []
supersedes: []
---

# Course plotting examples block the macOS source matrix

## What

All four macOS cells of [source run 41152714070](https://github.com/uibcdf/molsysmt/actions/runs/41152714070)
are cancelled at the three-hour job limit. Their retained per-phase streams
all end after setup of
`tests/documentation/test_center_examples.py::test_geometric_course_executes_with_local_source_substitutions[Alzheimer]`,
without its call outcome or a final session result. Python versions are
3.11–3.14; provider `8feefc96842d56dd03010e81289864eb8b78c0f1`, controlled Viewer
`ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352`. This blocks #255 source acceptance.

```bash
python -m pytest --receptor=ci --junitxml=junit.xml --receptor-events=.pytest-receptor/events.jsonl
```

## How

The course guard executes real notebook code including `plt.show()`, but had
not selected a noninteractive backend. A macOS GUI event loop is a plausible
blocking point. The retained phases identify the test, not the precise Python
statement; there is no direct faulting-frame evidence for `show()` in the old
run. Do not treat that hypothesis as an independently observed stack trace.

The shared guard fixture now runs both geometric notebooks and all four
comparison lessons with scoped Agg/noninteractive rendering, restoring the
preceding backend and interactive setting afterward. The expanded-scope section
below records why the initial two-notebook correction was insufficient.
It still executes the real display call, scientific transformations and
assertions. A display spy requires an Agg canvas and writes the actual figure
to PNG bytes, so the test proves rendering instead of replacing display with a
no-op. The course files, code cells and scientific criteria remain unchanged.

## Why

CI must finish these examples without waiting for a window to close. Selecting
a headless backend in the test harness preserves interactive notebook behavior
for users. No global runtime Matplotlib setting or scientific API is changed.

## What is measured and what is assumed

Observed: all four incomplete artifacts end at the same Alzheimer setup phase;
all four jobs terminate at the configured execution limit. Native Linux
3.12–3.14 completes the same suite, with 23,631 passes and 102 skips per cell.
The Linux/Python 3.11 native abort is a different #527 failure.

Local regression command, before the fixture correction:

```bash
MPLBACKEND=svg python -m pytest --receptor=llm tests/documentation/test_center_examples.py
```

The renderer guard fails for both notebook cases and passes the cookbook case
(run 188, exit 1, 7.77 seconds): both figures have SVG rather than Agg canvases.
This is a controlled nondefault-backend regression, not a local reproduction of
a Cocoa GUI hang. After the correction, the same nondefault backend plus OpenMM
pinning and CI-receptor controls passes 12 cases (189, exit 0, 7.05 seconds).
Existing legacy/projection warnings and two noninteractive-show warnings remain
visible; no warning filter is added.

Still required: execute the corrected complete macOS source cells. A passing
local Linux test does not establish that their cancellation is resolved.

## What was refuted

Increasing the job timeout or skipping the course examples would not establish
that the notebooks run correctly in CI. Replacing `show()` with a no-op would
lose actual rendering coverage. Selecting Agg only through an environment
variable would not control a backend already imported by earlier tests.

## Scope and exclusions

Only the automated example harness changes. Do not remove notebook plots or
weaken geometric checks. The #527 OpenMM abort and release/installed-artifact
qualification are separate work.

## Acceptance criteria

- Both real notebooks execute, render their figures and preserve their existing
  geometric/source-selection assertions under a nondefault incoming backend.
- The fixture restores plotting state and closes its figures even on failure.
- The exact corrected macOS source matrix finishes rather than being cancelled
  in this test; retain the failed run and its incomplete artifacts.

## Provenance

Inspection date: 2026-11-02. Hosted `macos-15`, Python 3.11–3.14, source IDs above;
Pytest Receptor 1.1.0. Local Linux development Python 3.14.7 with Matplotlib
3.11.2; logs/XML are retained under the #255 qualification scratch directory.


## Expanded local control — 2026-11-02

The documentation, OpenMM-force and CI-receptor selection passes **594 tests**
with two workers and incoming `MPLBACKEND=svg`, exit 0, 212.25 seconds (190).
Its 528 visible warnings include Sphinx deprecations, legacy/projection notices
and noninteractive plotting messages. No warning filter is added. Ruff,
formatting and all 14 fast gates (191) pass. These results qualify the harness
locally; the complete macOS source acceptance remains open.


## Completing the plotting scope — 2026-11-02

A follow-up audit finds the four Module 34 comparison lessons executing their
own `plt.show()` outside the first module-local fixture. Correcting only Module
46 would leave these subsequent display calls uncontrolled; no complete macOS
success was claimed for that initial patch. The backend/display/rendering
fixture now belongs to `tests/documentation/conftest.py` and is requested
explicitly by both notebook guards, covering all six actual lessons. It does
not affect tests that do not request plotting or globally change library users.

The comparison rendering guard first fails four cases under incoming SVG
(run 193, exit 1, 4.98 seconds), with the nonplotting cookbook case passing.
After shared headless execution, those cases, both geometric lessons, native
authority/component-assignment controls and documentation source controls pass
**104 tests** (194, exit 0, 18.01 seconds). PNG bytes are checked inside the real
display spy, and every notebook test requires an actual display call. Original
RMSD and geometric assertions, input substitutions, notebook cells and saved
outputs are unchanged. All six noninteractive-show warnings remain visible.
Hosted acceptance must use the complete six-lesson correction rather than
assuming the earlier exact commit contains it.


## Partial hosted evidence — 2026-11-02

The old two-notebook-only source run 41552267703 is now terminal: all four
macOS jobs are cancelled, three Linux cells succeed and Linux/Python 3.11 aborts
natively. Its result is preserved and does not qualify the later shared fixture.

The complete six-lesson fixture is present in dbcb4582c. Its macOS/Python 3.14
full suite reaches a terminal summary in 2,305.58 seconds: 23,599 passed,
54 failed, 103 skipped, 40 deselected, exit 1 (231). All failures are the
independent MDTraj SASA issue #529; the six plotting lessons execute and the
six real noninteractive-show warnings are retained. The separate scientific
certificate passes 79/79 cases for 59 nodes. This demonstrates progress past
the prior plotting boundary in that one cell, not a successful complete macOS
matrix. Other active cells and final candidate de7ffad2a retain their actual
independent outcomes. Complete hosted acceptance remains pending.


## Final-candidate Linux rendering execution — 2026-11-02

All six actual plotting-lesson calls are matched to passing phase records in
each final-source Linux 3.11/3.12/3.13 artifact (243/244). Complete suites pass,
and their primary evidence is finalized/integrity-valid/untruncated and agrees
with JUnit. These checks preserve real show/render and scientific assertions;
they do not establish that all four pending macOS suites finish. Hosted macOS
acceptance remains open rather than being inferred from Linux.


## Resolution — 2026-11-02

The shared scoped Agg/noninteractive fixture covers both geometric and all four comparison lessons, executes real display/PNG rendering and restores plotting state. Every one of those six actual lesson calls passes in all eight final-source cells, including complete macOS Python 3.11–3.14 suites; the old time-limit cancellations remain preserved. No notebook plot/scientific assertion, runtime backend policy, timeout or test selection is weakened. Final runtime de7ffad2a has complete intact primary evidence and matching JUnit; this resolves the source-harness defect without claiming installed/browser/Qt release qualification.

The complete source matrix is [41572981893](https://github.com/uibcdf/molsysmt/actions/runs/41572981893), officially successful on de7ffad2a. The #255 source closeout records full counts, omissions, science scopes and evidence limits. No main merge, package promotion or release is performed.
