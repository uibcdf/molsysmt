---
summary: Jupyter popup receiving loses the current Add-ons header during bootstrap.
issue: uibcdf/molsysmt#614
status: partial
opened: 2026-11-06
closed:
severity: medium
verification: reproduced
area: [tests, jupyter, molsysviewer]
guard: tests/molsysviewer_molsysmt/jupyter_receiving_guard.py::test_actual_jupyter_analysis_distance_family
normative:
blocked_by: []
supersedes: []
---

# Popup bootstrap navigation identity

## Owner receiving follow-up — 2026-11-08

Actual Jupyter receiving on clean MolSysMT `731bf01ea8a07e3ad8a7477700c4ae1e24730062`
and Viewer `e4dd58cf0edcb2c3afb2c982ccd50d3899d504ab` reproduces the same
inactive-only Add-ons locator in the System and independent-results drivers.
Both reach their popup stages, then wait for an inactive button that is hidden
because Add-ons is current. Initial notebook cells finish in 5.97 s and 5.83 s;
these failures do not establish #615's initial-canvas timeout. The two failures
are retained; the nine-scenario campaign was deliberately interrupted, with
pytest exit 2 and no acceptance claimed for the uncompleted scenarios. All
8,560 fingerprinted inputs remain unchanged. Peak charged memory is
2,358,976,512 bytes, host available memory stays above 14,493,093,888 bytes,
and no memory/task limit or OOM events occur.

Eleven remaining Jupyter drivers now delegate workspace navigation to the
existing shared `openMolecularPanel` helper while retaining each original final
panel/heading readiness check. The superposition driver's embedded result View
also recognizes the current header. No result acknowledgement, exact title,
coordinate/data oracle, browser error check, lifetime assertion or deadline is
relaxed. This extends the already received helper to old consumers; it does not
change scientific or Viewer product code. Directed System/results receiving and
then a clean combined receiving campaign remain required before closure.

## Isolated owner receiving review — 2026-11-07

The complete 5,009-case Python selection on isolated merge `653ed8e0` does not
discover the explicit Jupyter guard. A read-only review finds its Analysis
wrapper still expecting seven completed steps, while the current driver also
performs five later row-selection/live-measure/ensemble steps. The driver records
all twelve completed names. This is a stale wrapper expectation, not an observed
graphical or scientific failure. The wrapper now requires the complete ordered
twelve-name sequence rather than an anonymous count, tracked separately in
[the #632 record](../archive/resolved_bugs/analysis_jupyter_wrapper_expects_obsolete_step_count.md);
no driver assertion, title,
deadline or numerical oracle is removed. Actual Jupyter receiving of this
combined source and Viewer `25061d9e9` remains due. The original #614 and #615
failures and historical campaigns below are retained.

## What

Analysis and published Chemistry-preparation receiving look for the selectable
Add-ons header and a nonexistent selected attribute. When bootstrap selects
Add-ons, the real current span no longer matches either selector, so a waiting
click can fail after its original button detaches.

## How

Actual Jupyter Analysis receiving passes all preceding native coordinate-oracle,
empty/count-neighbor and paging checks, then fails navigating detached Studio
in 67.07 s. The root cause is observed in the retained Playwright traceback and
host TypeScript: active uses data-molsysviewer-panel-stack-current; inactive
uses data-molsysviewer-panel-stack-option. The receiving code incorrectly names
panel-stack-selected. The same driver code is published in Chemistry preparation
at 4f1710c5e; the already-qualified pending-reader helper has the correct identity.

## Why

This is a receiving-harness race, not a molecular or Viewer runtime failure.
It is distinct from #609's result-window-title acknowledgement race. The full
545-issue inventory and relevant owner reports were reviewed before filing.

## Correction and acceptance

The complete clean b18d5d823 / Viewer 737f9bc3 campaign now passes all eleven
actual-Jupyter scenarios and 76 steps in 671.62 s, including Analysis,
Chemistry preparation and pending readers in one run. All 4,456 selected
tracked inputs and both checkout identities/status remain unchanged. Earlier
failed attempts and #615's separate initialization observation are preserved.
Owner review/integration remains pending; the source correction is proposed
through PR #543 rather than installed or merged qualification.

A shared test helper waits for attached workspace metadata, resolves either
the current or selectable Add-ons header and waits for the requested panel.
Analysis, Chemistry preparation and the pending-reader driver reuse it.
Numerical/coordinate, source, page, exact-title, popup and lifetime assertions
and their deadlines remain unchanged. No sleep, forced click, numerical
workaround or placeholder acceptance is added.

The shared-helper campaign passes Chemistry preparation and pending-reader
receiving. Analysis times out before its first canvas under the separate #615
observation, then passes all seven steps in a scoped diagnostic run (39.36 s).
Keep that two-plus-one scope and original failure; no single green three-case
campaign is claimed. Owner integration and final exact-head gate review remain
pending. No runtime/scientific change is included.
