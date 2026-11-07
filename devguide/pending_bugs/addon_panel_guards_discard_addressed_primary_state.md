---
summary: Addon panel guards discard explicitly addressed primary-widget state.
issue: uibcdf/molsysmt#635
status: partial
opened: 2026-11-07
closed:
severity: medium
verification: reproduced
area: [tests, molsysviewer, panels]
guard: tests/molsysviewer_molsysmt/test_system_panel.py::test_primary_state_reader_rejects_other_real_views_route
normative:
blocked_by: []
supersedes: []
---

# Addressed primary-widget state in addon guards

## What

The Python addon panel guards discard genuine primary-widget state from the current Viewer host because they expect `target_endpoint_id=None`. Viewer explicitly addresses its primary AnyWidget route as `widget-host:<session id>`; popup routes remain distinct. The panel mounts and publishes correctly, but the guard filters out its state and raises `IndexError`.

## How verified

On isolated MolSysMT review `3f66f593` reconciled with qualified contribution `e1199534`, against exact Viewer `e4dd58cf0edcb2c3afb2c982ccd50d3899d504ab`, the directed Analysis/preflight selection returns 133 failed and 36 passed. All 133 failures have the same state-reader root cause. A separate real-demo diagnostic observes successful Analysis mount and actual mount/state/context messages addressed to the owning primary widget; calling `on_mount` directly succeeds too. The scientific calculation has not started at this failure point.

The same `target_endpoint_id == endpoint` default occurs in the System, Geometry, Chemistry and Analysis test helpers. This is a guard compatibility defect, not evidence of a scientific calculation or graphical delivery failure. Related integration: #421, PR #543, uibcdf/molsysviewer#315. #632 concerns the independent Jupyter step-count wrapper.

## Proposed correction and acceptance

Bind captured messages to the exact expected primary endpoint of their real View. Preserve actual message envelopes, explicit popup targets and strict identity checks; do not strip targets or accept arbitrary widget-host prefixes. Add a real-two-View isolation check so a foreign primary state cannot satisfy the oracle. Rerun the affected panel guards, mandatory addon preflights and complete paired-source selection; retain the original failing attempt. Deliver through PR #543 for owner review, without modifying owner main or claiming installed/publication acceptance.

## Local receiving — 2026-11-07

The shared capture oracle retains every actual envelope and binds its exact
primary destination independently from the owning View. System, Geometry,
Chemistry and Analysis reuse it. All 321 panel cases pass. A deliberate
foreign-route acceptance mutation fails the real-two-View guard; its original
source is restored without a Git checkout. The full paired-source addon and
three mandatory preflights then pass 5,059 cases without omissions on
`11796a8a`, with 4,747 selected inputs unchanged and 36 owned processes closed.
This is local source receiving; PR delivery, owner integration and board
closeout remain pending. Scientific runtime code is unchanged by this fix.
