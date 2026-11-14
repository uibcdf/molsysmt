---
summary: Prolonged Jupyter receiver masks Python errors and controller ownership.
issue: uibcdf/molsysmt#754
status: resolved
opened: 2026-11-14
closed: 2026-11-14
severity: medium
verification: reproduced
area: [component:molsysviewer]
guard: tests/molsysviewer_molsysmt/test_jupyter_cell_receiving.py
normative: devguide/jupyter_memory_sampling_method.md
blocked_by: []
supersedes: []
---

# Jupyter receiver loses the first Python failure and binding context

**Reported:** 2026-11-14 by MolSysViewer while reconciling its #354 evidence.
**Status:** corrected; real Jupyter controls and the actual prolonged entry point receive typed error/phase/ownership evidence.

## What

MolSysViewer supplies an original failed receiving record whose Python assertion
occurs before the save/recovery operation. The receiver instead reports a marker
timeout and records a controller without demonstrating that it belongs to the
expected recovered output. The supplied observation therefore does not establish
a recovered canvas stuck at structure zero. The original producer, hashes,
pre-save assertion and ordering are recorded in uibcdf/molsysmt#754. Its raw
private evidence has not been independently received or replayed here.

## How

Inspection at `baedf4c702e6b9438a63b097e1b048bf1ab3df6d` confirms the current
receiver still uses the reported pattern. In
`tests/molsysviewer_molsysmt/prolonged_session_jupyter.mjs`, `marker()` searches
the document for `.jp-OutputArea-error` or marker text. It does not bind the
Python error to the executing cell. The coherent-save/recovery line awaits
that marker before reading the recovered identity, waiting for its canvas,
binding it and checking its structure. The catch records `__longActive`
without expected/observed identity or binding-stage attribution.

The actual Jupyter error DOM and first-reached phase must be received before
choosing a replacement locator. Retain the Python exception and distinguish
it from a genuinely absent marker. Record expected output/widget identity,
observed controller identity and whether binding has occurred; label a previous
or unbound controller as such. Bound and sanitize diagnostics without tokens.

## Why

A diagnostic tool that names an unreached phase can send client debugging in
the wrong direction. Correct receiving evidence is necessary before interpreting
pre-1.0 prolonged-session results. This is receiver ownership in MolSysMT;
it does not assign the underlying Python/frontend disagreement to an engine.

## What is measured and what is assumed

Inspection of the original source confirms the locator, operation order and missing
identity fields. The original Python exception and stack attribution are
upstream-reported evidence, not a newly reproduced current failure. A later
successful 30-cycle receiving remains successful at its original source and
does not causally explain that earlier disagreement. No new browser execution
has been started for this report.

## What was refuted

The current operation order does not support describing the reported marker
failure as proof of a ninth recovered-session failure. Neither a passing later
session nor renaming a CSS class without observing real Jupyter output proves
the diagnostic defect repaired.

## Scope and exclusions

Correct receiver error/phase/identity reporting and focused regressions. Do not
retry away the assertion, relax deadlines, change molecular algorithms, or treat
this as resolution of the separate initial-cell investigation #615 / MolSysViewer
#384. No candidate, installed pair or publication authorization is implied.

## Acceptance criteria

- A real Jupyter cell raising before its marker exposes its Python error and
  first reached phase, rather than a generic marker timeout.
- Successful-marker and genuinely missing-marker controls preserve their outcomes.
- A stale prior-controller control identifies the expected/observed owners and
  uncompleted binding instead of attributing it to the recovered surface.
- Diagnostics are bounded, token-safe and preserve original errors/deadlines.
- Applicable local guards pass; any complete visual campaign retains its own
  source/runtime identity and remains separate from final-pair qualification.

## Reproduced mechanism and correction — 2026-11-14

The original marker function is evaluated from its unchanged source, rather
than replaced with a hand-written baseline. A plain Jupyter cell raises before
its marker. The actual DOM has zero `.jp-OutputArea-error` elements; the error
uses `application/vnd.jupyter.stderr` inside the ordinary output container.
The original marker waits 30.008 seconds and raises `TimeoutError`. This
reproduces the diagnostic mechanism, not the original private cycle-nine
molecular disagreement. The first observation attempt fails earlier in its
own overly exact text locator; that failure is retained separately and is
not counted as a reproduced product defect.

`jupyter_cell_receiving.mjs` passively observes typed execution messages.
It arms the actual notebook-manifest cell ID and matches the request and
parent ID on the same socket. It decodes JSON and both supported binary
layouts without decoding widget buffers or retaining executed code. The
independent Jupyter Server serializers supply parity inputs, including
2-MiB widget buffers. Unknown transport is counted as missing evidence,
not manufactured into a Python exception. A successful marker also requires
the matching successful reply and idle notification. Another cell's output,
a previous run, ordinary stderr and a delayed unrelated error cannot supply
that result. The default deadline remains 30 seconds.

The prolonged entry point now keeps the executing-cell phase separate from
canvas readiness and controller binding. Its failure record preserves the
Python name/value/traceback, expected surface/viewer and observed controller.
Identity, containment and a completed bind are all required for attribution;
unknown identity stays unbound. Known credentials are redacted before text
truncation. Error values/traces and diagnostic window/frame counts are
bounded. Whole-notebook DOM and screenshots containing arbitrary cell output
are no longer dumped automatically. The original scientific cell contents,
calculations, assertions, raw memory sampler and prior successful evidence
are unchanged.

## Verification and receiving limits

The final selected session passes 72 pytest cases with zero skips, failures
or errors; the supported receptor reader agrees with same-invocation JUnit.
Thirteen Node controls execute within one pytest case, not as additive pytest
coverage. Real Jupyter controls cover the original exception, success after
error, repeating the same cell, ordinary stderr, an absent marker, credential
redaction and bounded large errors. Six synthetic controller controls run in
that actual Jupyter document: different ID, different surface, matching but
unbound, genuinely bound and unknown-identity dispositions remain distinct.
They do not qualify an actual Mol* canvas.

A second guard drives the actual prolonged script. Its intentional plain
initial-cell assertion produces the expected nonzero producer exit and a
typed failure before the first marker/canvas/bind. The guard itself passes.
Both actual kernels assert absence of molecular/AnyWidget imports. No system
preparation, save/recovery science or thirty-cycle campaign is rerun. The
original private record, underlying Python/structure disagreement, #615,
installed/platform and final-pair qualification retain their existing scope.

The final bounded session uses one CPU and at most 2 GiB, peaks at 848.34 MiB
and retains more than 16 GiB host-available memory. Original failures,
source/runtime identities, native exits and scope are retained in the
[receiving receipt](../../../devtools/data/jupyter_cell_diagnostics_receiving_754_20261114.json).
The [operational method](../../jupyter_memory_sampling_method.md#receiving-python-failures-and-controller-ownership)
owns the maintained diagnostic/command contract.
