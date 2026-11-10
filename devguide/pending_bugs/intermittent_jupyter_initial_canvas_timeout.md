---
summary: Investigate intermittent Jupyter initialization before the first molecular canvas.
issue: uibcdf/molsysmt#615
status: open
opened: 2026-11-06
closed:
severity: medium
verification: measured
area: [tests, jupyter, initialization, molsysviewer]
guard:
normative:
blocked_by: []
supersedes: []
---

# Initial molecular canvas timeout

## Observation

One actual Jupyter Analysis case times out after the existing 30 s canvas wait,
before Analysis is opened. The same campaign passes Chemistry preparation and
pending-reader receiving: one failure/two passes in 243.40 s. The initial cell
is marked executing; no Python exception or introduced page error is captured.
The original faulthandler dump at 45 s comes after the failing deadline and its
trace file is empty. The failing stage/cause is not established.

Inputs: native ed09f6453, Viewer e920faf9 (runtime/API unchanged from 177e19a8)
and the Analysis working increment over owner 4f1710c5e. No scientific or
Analysis operation runs before this failure. This differs from #614's confirmed
later Add-ons-header bootstrap identity race.

## Diagnostic receiving

The runner now captures a stack at 15 s and initial-cell start/completion times,
without changing the canvas deadline or warming scientific/display imports.
The scoped next Analysis run passes all seven native-oracle/Jupyter/popup/source
steps in 39.36 s. Its initial Python cell takes 3.357631 s. Neither that passing
run nor the instrumentation establishes a repair or origin for the failure.
Preserve two-plus-one receiving; no single green three-case campaign is claimed.

## Follow-up

Complete clean follow-up receiving on b18d5d823 / Viewer 737f9bc3 passes all
eleven actual-Jupyter scenarios and 76 steps in 671.62 s; the before/after
source snapshots agree. Initial Python cells take 3.27–5.10 s. This adds a
conclusive campaign on those inputs, without establishing a cause or repair
for the earlier timeout. This report remains open; no deadline or assertion
was relaxed and no warm-up was introduced.

On recurrence identify the live kernel/library, widget-transport/bootstrap or
first-draw stage and capture its actual stack/status before changing behavior.
Do not infer process termination from an observation timeout, restart a live
kernel, increase waits, add warm-up, skip the case or accept missing canvases to
obtain green. A closure needs a causal correction and relevant receiving, or an
evidenced environment limitation with owner/removal conditions.

The complete 545-issue inventory plus the newly opened #614 was reviewed for
equivalent initialization observations. This report tracks uncertainty for
#421 / PR #543 and uibcdf/molsysviewer#264; it is not a proven numerical failure
or universal product defect. Human/installed and publication scopes stay separate.

## Separate startup and late-workflow observations — 2026-11-10

#690 receiving on clean 573476e70 / Viewer 9b8662cf retains three failed
actual-Jupyter attempts. The four-CPU cold-server attempt reaches its unchanged
20-second readiness limit before any canvas or molecular cell; the 15-second
stack is importing JupyterLab extension code. A same-input repeat starts the
server and advances through numeric geometry and PCA, then exhausts the
unchanged 300-second browser deadline during PCA popups. The two-CPU attempt
also reaches a later workflow deadline. Host pressure stays zero and no own OOM
or reserve stop occurs. See the [native receipt](../../devtools/data/native_neighbor_allocation_receiving_690_20261110.json).
These distinguish stages and preserve failures; they do not establish the cause
or repair of this report's original first-canvas timeout. No warm-up, increased
deadline or acceptance waiver is introduced; #615 remains open.

## Distinct pre-execution and replacement waits — 2026-11-10

The final 0d8b8c9ac / frozen Viewer b9f3be01 Jupyter campaign has one passing
assessed-protonation scenario and two failed scenarios. Properties completes
six checks, including categorical DSSP and both popups. Its same-View caffeine
replacement prints 24 native atoms, but the observed original controller does
not report 24 within the existing 30-second wait. This is after initialization;
a stale observer or host replacement race remains a hypothesis. It is not
evidence of incorrect native ring results.

Interaction/mechanics instead stops before the initial Python cell executes:
the kernel label stays Unknown rather than Idle. There is no initial-cell
trace file or molecular calculation at this stage. This differs from the
original executing-cell timeout. The scope peaks at 1.82 GiB under a 4 GiB cap,
keeps at least 9.33 GiB host memory available and has no OOM/reserve stop.

Retain both failures and their private artifacts. Bounded browser diagnostics
now capture kernel status, output-error count and each observed controller's
connected canvas, atom count, structure index and selection size. No molecular
arrays, credentials or private settings enter that snapshot. Existing waits,
source/scene comparisons and scientific assertions are unchanged. One deliberate
instrumented follow-up may distinguish stages; even a passing follow-up does
not establish the cause or repair of the original #615 observation.
