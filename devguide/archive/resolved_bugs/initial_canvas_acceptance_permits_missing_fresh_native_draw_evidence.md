---
summary: Initial-canvas acceptance permits missing fresh native draw evidence
issue: uibcdf/molsysmt#762
status: resolved
opened: 2026-11-15
closed: 2026-11-15
severity: medium
verification: reproduced
area: [tests, molsysviewer]
guard: tests/molsysviewer_molsysmt/test_initial_canvas_acceptance.py
normative:
blocked_by: []
supersedes: []
---

# Initial-canvas acceptance permits missing native draw evidence

**Reported:** 2026-11-15 while reviewing the proposed #615 disposition.
**Status:** resolved; actual-guard counterexamples and real Jupyter receiving complete.

## What

The opt-in initial-canvas guard accepts a trace without `first_native_draw`.
It checks draw ordering only when that mark exists. The browser waits for an
arbitrary canvas element, so the required newly drawn molecular scene is not
an enforced acceptance condition.

## How

Synthetic receipts are delivered through the actual existing opt-in pytest
guard, without opening a browser or replacing molecular calculations. Before
the correction, missing draw, draw before scene registration and draw later
than the original 30-second allowance all pass the guard: three negative
controls fail because the expected rejection never occurs. The valid control
and already rejected pre-observer/cached draw control pass.

## Why

#615's proposed bounded disposition relies on a real first-draw acceptance
condition. A created canvas or registered structure cannot substitute for it.
This is a receiver defect, not a diagnosis of the historical timeout, a new
MolSysViewer product defect or a reason to certify the final pair.

## Correction and acceptance criteria

Require all correlated Run/controller/observer/scene/new-draw marks, finite
values and valid ordering. Require a fresh native draw within 30 seconds of
the observed Run and a positive connected canvas. The opt-in browser path uses
one 30-second wait for the native observer, with timer polling; it does not
add another deadline, force a draw, retry or warm imports. Other Analysis
workflows retain their existing canvas wait.

Keep the observer's cached-emission suppression and wrong-scene refusal. Run
its seven Node controls through an addressable pytest wrapper, then receive
the explicit actual-Jupyter guard on a recorded frozen composition under the
shared-host resource policy. Synthetic controls alone do not establish an
actual browser or final-candidate pass.

## Provenance and limits

Source parent 2801677bc, existing Linux/Python 3.14.7. Baseline has three
failures/two passes. The initial corrected Python selection has five passes.
An initial direct Node invocation omits the required
`INITIAL_CANVAS_TEST_PYTHON` setting: six controls pass and its live sampler
control refuses the missing prerequisite. That operator error is retained and
is not a provider defect. The first wrapper also used the wrong environment
key; its 43-pass/one-failure cohort remains failed. The corrected wrapper supplies the actual current
interpreter through the required key. No package/scientific/Rust
implementation, dependency floor, candidate or release changes here.

## Resolution — 2026-11-15

The final selected cohort passes 44 pytest cases without skips, including the
pytest bridge to all seven Node observer controls. One actual fresh-Jupyter
invocation also passes the opt-in guard: the initial cell owns the observed
3,983-atom scene and all nine kernel stages match its attempt. A new eligible
native draw occurs 16.38 seconds after observed Run, after observer arming and
scene registration. The corrected browser branch uses one original 30-second
wait with timer polling; it does not force drawing or add time. Non-opt-in
Analysis keeps its original wait. One browser error matches the plain Jupyter
control; the receipt does not claim zero page errors.

The [receipt](../../../devtools/data/three_closeout_receiving_615_256_524_762_20261115.json)
retains native outcomes, structured pytest/JUnit agreement, original failures,
source hashes and resource observations. The real invocation uses the existing
frozen documentation host/support and ipykernel 7.3.0, with an unchanged native
file and no shared installation. It qualifies this receiver correction on those
inputs, not all current client-host behavior, a native ABI or the final pair.
The original #615 cause and principal-maintainer disposition remain separate.

All fifteen offline fast release gates, converter/index agreement, repository-wide
Ruff lint/format, changed JavaScript syntax and diff checks pass. The bounded
check scope peaks at 0.54 GiB, with unchanged inputs and no resource stop. All
eight owned services are retired after recording their original outcomes; the
one owned Chromium temporary root is removed. Required evidence is retained.
