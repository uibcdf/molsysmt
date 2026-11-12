---
summary: Prolonged Jupyter receiver does not wait for controls focus
issue: uibcdf/molsysmt#718
status: active
opened: 2026-11-11
closed:
severity: medium
verification: upstream
area: [tests, diagnostics]
guard:
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
uses MolSysViewer c5115dff and the qualified native binary. The reporter corrected
its original provider claim: the outer supervisor declared archived MolSysMT
aee7aa65, but the generated notebook imported another copied working source,
identifying itself as 0.23.0+757.g08f0afdb8.dirty. Its selected-input snapshot did
not cover that entire inner source. Retain the observed focus trace within that
copied-source scope; it is not exact aee7aa65 receiving. The external measured
result has not been rerun here.

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

## Source identity prerequisite — 2026-11-11

The maintained launcher chooses its source from its own repository location,
sets that root in the kernel's PYTHONPATH, and asserts the actual MolSysMT and
MolSysViewer import paths in the generated initial cell. Inspection confirms
that behavior; a consumer wrapper must not describe a different outer checkout
as the imported provider. The copied-source discrepancy is receiving provenance,
not evidence that the scientific provider selected an arbitrary source.

Before the next actual-GUI or thirty-cycle run, freeze and record the launcher,
fixture, kernel-imported provider root, native binary and host/runtime bytes.
Verify the same inner source before/after, including any intentionally dirty
patches. Retain observed imports/versions separately from declared commits and
from package qualification. Do not substitute selected outer-file counts for
that proof. Draft PR #721 is now delivered at 076bc95affac57a6f0c05f0a780cce37a6610617.
An initial owner-side source review requests consolidation into this existing
report/ledger row and a passive import observation that does not warm absent
modules before cold initialization. Its reported current-support guards and
in-progress thirty-cycle campaign are not local receiving or merge acceptance.
Review the completed contribution before integration. Independent documentation
and native correctness work can continue.


## Contribution checkpoint — 2026-11-11

Draft PR #721 at 5816bec8 consolidates the existing report/ledger and reports
a terminal thirty-cycle functional campaign on its declared copied scientific
source, canonical native bytes and PyUnitWizard development overlay. This is
contribution evidence, not a new owner execution or current-main qualification.
Browser-memory growth retains separate consumer #356/#315 work. Owner review
6815289098 still requests a passive provenance observer: the present helper
force-imports providers before the demo and may change cold initialization.
Retain existing functional results for their actual composition; changed-input
receiving and owner integration remain pending. Publication pause is unchanged.
