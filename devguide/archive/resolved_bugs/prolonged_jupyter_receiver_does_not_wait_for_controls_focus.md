---
summary: Prolonged Jupyter receiver does not wait for controls focus
issue: uibcdf/molsysmt#718
status: resolved
opened: 2026-11-11
closed: 2026-11-11
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


## Owner passive-observer correction — 2026-11-11

The owner receives PR #721 at 5816bec8 onto de578b72a, retaining the existing
single report and release-ledger row. A fresh-process guard reproduces imports
by the contribution's observer; loaded-provider and missing-file controls also
fail on that original implementation. The corrected observer reads sys.modules
and stored module metadata only, records loaded versus absent explicitly, and
uses the private receiving schema @2. It does not invoke lazy module attributes
or activate missing providers. Its file/entry-point record remains distinct
from a complete source manifest or installed identity.

The three new guards and 53 existing receiver/import controls pass (56 cases,
zero skips). Original baseline failures remain retained. Ruff/format and Node
syntax checks pass. Actual changed-observer Jupyter receiving is still pending;
the original thirty-cycle contribution retains its active-observer composition
and copied-source/client/runtime scope. No full-source or installed acceptance
is inferred, and no publication/candidate pause is lifted.


## Owner receiving and metadata refinement — 2026-11-11

Clean integration source 687220ac9 passes both actual-Jupyter guards: cold
initial canvas and one complete prolonged cycle over 5,000 structures with
scientific calculations, hidden-control keyboard navigation, both popups,
coherent save/recovery and ten seconds of actual playback. The frozen client
is the independently received 5164f13b source/runtime, with published
PyUnitWizard 0.29.2 and reviewed support copies. All 4,860 selected files
remain unchanged; native bytes remain canonical. The two cases finish with
zero skips/errors/failures. The source is clean before and after. The four-GiB,
two-CPU service peaks at about 1.99 GiB and preserves at least 10.49 GiB host
available memory, with no observed limit/OOM or reserve stop.

A final metadata-only refinement bypasses custom module __getattribute__ when
reading the stored dictionary. The extra fresh probe reproduces activation by
vars(module); the correction and fourth guard pass in the final 57-case
headless cohort. The first file-path probe failed to import tests and is
retained separately; the corrected -c probe establishes the behavior. The GUI
result remains scoped to 687220ac9, before that one-line refinement. No GUI
rerun, whole-current-main or installed qualification is inferred. The earlier
thirty-cycle contribution retains its distinct scientific/client/provider and
active-observer composition; the corrected navigation driver is byte-identical.


## Resolution

The owner integration receives actual visible focus before submitting keyboard
navigation and keeps the scientific/window/session assertions and deadlines.
The original corrected browser driver is unchanged. Four new passive-observer
guards and the existing receiver controls pass (57 cases); two actual-Jupyter
guards pass on clean 687220ac9. The later metadata-only refinement belongs to
67a094749 and has separate focused receiving, not a relabelled GUI result.

The primary guard starts with fully hidden controls, requires actual Next
focus and structure navigation, and completes a real scientific/popups/session/
playback cycle. It cannot pass on method names or fabricated output alone.
The [owner receipt](../../../devtools/data/jupyter_focus_receiving_718_20261111.json)
owns exact source/runtime/native identity, initial loaded/absent snapshots,
4,860 unchanged selected files, failed probes and resource retirement. The
[contribution receipt](../../jupyter_receiver_focus_receiving_20261112.md)
retains the separate original thirty-cycle composition and reported growth.

This closes receiver readiness/provenance only. #723 owns qualified memory
metrology and host-only controls; #615/#713 original causes, client lifetimes,
installed/platform and final-candidate acceptance remain open. There is no
publication authorization or new formal score credit.
