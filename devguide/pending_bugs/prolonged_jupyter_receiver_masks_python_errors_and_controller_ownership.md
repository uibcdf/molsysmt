---
summary: Prolonged Jupyter receiver masks Python errors and controller ownership.
issue: uibcdf/molsysmt#754
status: open
opened: 2026-11-14
closed:
severity: medium
verification: inspected
area: [component:molsysviewer]
guard:
normative:
blocked_by: []
supersedes: []
---

# Jupyter receiver loses the first Python failure and binding context

**Reported:** 2026-11-14 by MolSysViewer while reconciling its #354 evidence.
**Status:** admitted to #334; correction and real-Jupyter regressions pending.

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

Current source inspection confirms the locator, operation order and missing
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
