---
summary: Prolonged Jupyter receiver does not wait for controls focus
issue: uibcdf/molsysmt#718
status: partial
opened: 2026-11-11
closed:
severity: medium
verification: measured
area: [tests, diagnostics]
guard: tests/molsysviewer_molsysmt/jupyter_receiving_guard.py::test_actual_jupyter_prolonged_popup_controls
normative:
blocked_by: []
supersedes: []
---

# Receiving keyboard-control readiness in prolonged Jupyter tests

## What

MolSysViewer reports a controlled actual-Jupyter reproduction in which Enter
still targets the control-reveal hotspot after the receiver attempts to focus
Next. No Next click occurs. A positive control that waits for visible keyboard
focus advances both canvases. This is receiver-readiness evidence, not a causal
observation of the original fourth-cycle timeout, whose focus was not captured.

## How

Local source inspection confirms prolonged_session_jupyter.mjs controls()
focuses the reveal hotspot and returns immediately after pressing Enter. The
popup path then calls next.focus() and Enter without receiving the visible
focus transfer. MolSysViewer reports that transfer happens on a later animation
frame and focus can be rejected during the visibility reversal. Its diagnostic
uses recorded MolSysViewer source c5115dff and the unchanged qualified native
binary. The original outer aee7aa65 attribution did not identify its copied
kernel source; the issue's opening correction and consumer #364 retain that
qualification gap. Do not call the original diagnostic exact-aee7aa65 receiving.

## Why

The prolonged source campaign cannot receive a scientific navigation assertion
when its control action was never submitted. Preserve the distinction between
this receiver defect, original #615 uncertainty, MolSysViewer #354/#305 and its
#356 molecular-buffer lifetime work. This report does not establish their cause
or qualify installed packages.

## Intended correction and acceptance

Receive actual visible focus in the intended control scope before targeting
Next. Review the incoming owner-proposed PR before integration. Do not add a
fixed sleep, retry, corrective seek, fake response or larger timeout. Preserve
all coordinate, index, popup, session and scientific assertions and original
wait budgets. Add a bounded actual-GUI guard with fully hidden popup controls;
then receive the complete thirty-cycle campaign against recorded unchanged
inputs and native bytes. Select shared-host limits from measured pilot demand,
retain original failed attempts and retire only owned processes.

## Scope and coordination

Owner: uibcdf/molsysmt#718; consumer context: uibcdf/molsysviewer#315 and #356.
This is the next local validation priority after #716/#717 closeout. No new
scientific calculation, public API, dependency floor, candidate, tag or release
is requested. The current construction/hosted-qualification/publication pause
remains; source controls do not replace the final installed pair.

## Provenance

2026-11-11 intake and source inspection. External evidence and exact composition
are in the owning issue. No actual-Jupyter or thirty-cycle execution was launched
as part of this intake. Await and review the concrete proposed correction.

The [2026-11-12 contribution receipt](../jupyter_receiver_focus_receiving_20261112.md)
receives two explicit current-support guards and 52 separate affected controls.
Actual kernel origins/hashes are now recorded, and 3,169 scientific/addon Python
files independently match aee7aa65 in the receiving tree. The thirty-cycle
campaign and owner integration remain separate; PR #721 is a contribution,
not an integration or installed qualification.
