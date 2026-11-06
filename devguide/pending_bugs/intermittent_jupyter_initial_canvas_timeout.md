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
