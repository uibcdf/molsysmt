---
summary: Addon panel guards discard explicitly addressed primary-widget state.
issue: uibcdf/molsysmt#635
status: resolved
opened: 2026-11-07
closed: 2026-11-07
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

## Owner receiving — 2026-11-07

Combined owner `b10160f29` and head `42f5ed3bc` pass all 356 directed panel and
native/inventory controls on the exact public Viewer e4dd58cf snapshot. Its
2,462 source blobs independently match GitHub; the existing matching-lock tools
build only the declared test harness, not a replacement runtime. A deliberate
removal of destination filtering causes exactly the real-two-View guard to
fail (native one); exact original bytes are restored before further receiving.

The first complete owner campaign passes 5,427 and fails one command-completeness
preflight: owner #602 omitted its new test module from smoke. This is separately
owned #639. No molecular assertion or routing guard fails, and all selected
source fingerprints are unchanged during the run. Original failures remain;
combined zero-failure and actual Jupyter receiving follow after the workflow fix.

After #639's one-argument correction, the complete combined owner selection
passes **5,428 cases** without failures/errors/skips, retaining all three
mandatory preflights, owner coordinate/constructor/certificate guards and
independent conformation controls. The original failed campaign remains in the
[owner receipt](../../../devtools/data/bound_tools_newer_host_source_receiving_635_639_20261107.json).
Actual seventeen-step Jupyter receiving and source publication follow separately.

## Resolution — 2026-11-07

Owner merge `0ddb99c2b31ba4f63c40c0c43da038895b21c70d` receives the incoming
exact-primary oracle without stripping envelopes or weakening foreign/popup
identity. All 5,428 combined source cases pass after the separately owned #639
workflow correction. The deliberately weakened oracle fails the real-two-View
guard, and original bytes are restored before full qualification.

All four selected actual Jupyter scenarios pass together: Analysis seventeen
ordered steps, Preparation six, Pending Chemistry eight and Periodic eight.
They retain numerical/source/scene/geometry/popup checks and original deadlines.
Page errors match their plain-Jupyter controls; no zero-error or #615 causal
closure is claimed. The actual molecular runner also passes 107 cases/68 nodes
with `--require-clean` on the clean merge, all fourteen fast gates pass and HTML
compiles with six retained existing warnings. The
[completion receipt](../../../devtools/data/bound_tools_newer_host_completion_receiving_635_639_20261107.json)
keeps exact host/source/backend identities and separate evidence scopes.

This resolves #635's bounded guard compatibility. Main delivery/board verification
follow in the ledger; remaining #421 families/full GUI session, #524 public-host/
installed and postponed human/Qt acceptance remain open. No candidate or release
is selected, and historical archives remain unchanged.
