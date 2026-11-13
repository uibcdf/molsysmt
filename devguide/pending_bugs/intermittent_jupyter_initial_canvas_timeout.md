---
summary: Investigate intermittent Jupyter initialization before the first molecular canvas.
issue: uibcdf/molsysmt#615
status: active
opened: 2026-11-06
closed:
severity: medium
verification: measured
area: [tests, jupyter, initialization, molsysviewer]
guard: tests/molsysviewer_molsysmt/test_jupyter_stage_diagnostics.py
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

The single instrumented follow-up on clean e65dd49ed passes all three scenarios:
20 browser checks. Properties captures one connected source controller with
24 caffeine atoms after replacement, no output errors and structure index zero.
The scope peaks at 2.22 GiB, retains at least 11.28 GiB host memory available,
and has no pressure/OOM/reserve stop. No timeout, assertion or warm-up changed.
This is receiving on those inputs, not a causal repair or closure of #615;
the preceding one-pass/two-failure campaign remains failed.


## Combined construction receiving — 2026-11-10

Clean cdf6e878f / raw-blob-verified Viewer b010ab76 passes four actual Jupyter
workflows and 26 checks: construction, assessed protonation, properties and
interaction/mechanics. Existing waits, source/scene comparisons and scientific
criteria remain unchanged. The scope peaks at 2.50 GiB and retains at least
9.04 GiB of host available memory; no own OOM or reserve stop occurs. Global
full-memory pressure briefly peaks at 3.24 in the shared host; that observation
does not establish a product or timing cause. See the
[combined receiving record](../../devtools/data/construction_native_owner_receiving_421_695_696_697_698_699_20261110.json).

This is additional exact-source receiving, not a causal repair or closure of
#615. The original executing-cell, later pre-execution, cold-server and final
replacement observations remain distinct failed stages in their own receipts.

## Post-attempt session diagnostics — 2026-11-10

Inspection confirms that the original failed kernel trace is empty; it cannot
identify the missing causal stage. The owned receiving launcher now queries the
isolated server's read-only `/api/sessions` endpoint after the browser attempt
and before shutdown. It records only bounded session roles, declared kernel
execution state and connection counts. Tokens, paths, IDs, exception contents
and molecular data are excluded. Unavailable evidence remains distinct from an
empty session list. No request runs against an unready or exited server.

Twenty focused lifecycle/diagnostic controls pass, including malformed/oversized
responses, transport failures, failed diagnostic writes and credential/content
exclusion. These observations cannot change the browser verdict, restart a
kernel, warm imports or extend the existing readiness/canvas/browser deadlines.
Actual-server receiving remains required before adopting the instrumentation.
Even a passing instrumented run does not establish the cause or closure of #615.

The endpoint follows the [Jupyter Server REST API](https://jupyter-server.readthedocs.io/en/latest/developers/rest-api.html).
The installed server supplies `execution_state` and `connections` through its
kernel model; this is test-harness diagnostic metadata, not a new MolSysMT API
or public runtime dependency. The guard is
`tests/molsysviewer_molsysmt/test_jupyter_stage_diagnostics.py`.

## Actual session-endpoint receiving — 2026-11-10

On clean d36d25929 / verified Viewer 5164f13b, the first split browser campaign
passes visual adoption's six checks and fails Analysis after nine completed
checks because the raw source export has no generated test-only harness. The
launcher captures both attempts through the real server endpoint. A separately
verified harness build changes no published Viewer source bytes; the deliberate
Analysis follow-up passes all 22 checks with unchanged deadlines and assertions.
All three bounded snapshots are available and report two post-attempt idle
kernels with zero connections after browser retirement. That is valid diagnostic
receiving, not a causal explanation for the original executing-cell timeout.

The [owner receipt](../../devtools/data/figure_context_owner_receiving_701_702_615_20261110.json)
retains the failed first campaign, exact generated-harness provenance, all three
sanitized snapshots and the passing scoped follow-up. Actual native Wayland Qt
receiving passes four reported steps with embedded stored-context checks.
Neither that Qt result nor the passing browser follow-up closes #615. No warm-up,
restart, timeout increase, source/scene mismatch waiver or missing-canvas
acceptance was introduced. The original causal/environmental disposition remains
required, and receives no formal plan credit.

## Joint pre-timeout capture disposition — 2026-11-10

MolSysMT accepts the Analysis runner and kernel/server side of the bounded
capture proposed in [uibcdf/molsysviewer#315](https://github.com/uibcdf/molsysviewer/issues/315)
at Viewer `4f05a6c6ea3f7ca78929e9f2592360f0e6ae38fa`. Viewer owns the matching
mount, scene and draw observations. The existing Python snapshot runs after
the browser subprocess completes. The proposed capture must take place while
the browser is still connected to the isolated server.

For one targeted Analysis diagnostic when scheduled, arm the observations
before Run on the original 1TCD initial cell. Retain the existing 30-second
canvas wait, 15-second kernel stack timer, cold imports and lifecycle.
MolSysMT records submission and actual cell start, import/load/display
boundaries, completion or exception, and bounded `/api/sessions` samples at
about 15 seconds and at the failing canvas wait before browser teardown. The
browser verdict and original deadline are authoritative. Use the existing
authenticated, read-only and size/time-bounded sampling contract. Mark a missing
or unavailable sample explicitly.

Correlate both sides with one local attempt label and a common Run anchor for
monotonic elapsed observations. At the handoff record the first observed widget
comm acknowledgement or bootstrap event. Viewer records mount, the connected
canvas/controller, registration of the expected 3,983-atom scene and the first
new native Mol* draw for that scene. Keep the private kernel traces and publish
only sanitized, bounded metadata. Report the earliest missing transition only
if the relevant observer was armed. Readiness failure before the cell belongs
to the separate #705 scope.

This is an agreed diagnostic disposition. A causal correction or an evidenced
bounded environmental disposition is still required for closure. Implementation
and an instrumented execution remain pending.

## Owner kernel and live-session diagnostics received — 2026-11-10

The local owner branch `wip/jupyter-canvas-615-owner-20261110` at
`8060ba0eb0490534e936c1c49339ebdfd18501af` incorporates draft
[#707](https://github.com/uibcdf/molsysmt/pull/707) and the MolSysMT-side capture.
The opt-in `--scenario analysis --initial-canvas-only` run correlates the
observed Run click, cold kernel imports, demo load, display expression and
cell completion with the widget bootstrap, mount, scene and first native draw.
One attempt label identifies all three records. The original 30-second canvas
wait and 15-second kernel stack timer are retained.

The session reader samples the existing authenticated endpoint about 15
seconds into a pending wait and again on a canvas timeout before the browser
closes. Its results contain bounded execution states and connection counts.
A controlled timeout-clock run exercises both reads and verifies that tokens
and kernel identifiers are absent from the record. An early canvas records the
first checkpoint as not reached.

**44 launcher and diagnostic cases pass** with loopback available. The first
sandboxed attempt passes 36 and reports eight socket-permission failures.
Two cold Jupyter and Chromium runs against Viewer `5164f13b` and native
`4ffb82e4` reach the 3,983-atom scene. In the final opt-in run, the native
scene registers 8.05 seconds after observer arming and the first native draw
occurs at 12.83 seconds on that clock. The canvas belongs to the initial cell. The run captures both
kernel and browser milestones and reaches the canvas before the live-session
checkpoint. The original intermittent failure has yet to recur with the
diagnostics armed. #615 remains open.

## Reviewed owner integration — 2026-11-11

The owner increment incorporates PR #707 source
`cdcb8ed7c682a384a8f65b1f38d6b46cead23b1c` and the local branch's paired
kernel/live-session capture, with new source review and executable controls before main delivery.
The native library and addon runtime are unchanged. The existing full Analysis
workflow remains the default; `--initial-canvas-only` is an explicit,
Analysis-only receiving mode. It adds no warm scientific imports or larger
canvas deadline. The isolated plain-notebook control retains its own kernel.

Review found four reproducible journal failure paths: open, write, flush and
close errors could interrupt the instrumented kernel. All four fail the added
controls before correction. Optional timeline I/O now fails without changing
kernel work. A missing/partial journal means unavailable evidence, not proof
that the cell never started. Normal and exception completions write bounded
JSONL metadata without serializing exception contents.

**52 Python controls and six Node controls pass.** The latter exercise mount
before DOM attachment, exclusion of a cached draw, wrong-scene rejection,
unavailable/unarmed capture, write failure, early completion, sampler startup
failure and two real authenticated loopback session reads before timeout cleanup.
The Node command declares the qualified Python through
`INITIAL_CANVAS_TEST_PYTHON` and is run explicitly with `node --test`.
This is helper/observer receiving, not proof of a causal timeout repair.

The browser trace labels its arming anchor and records actual
`run_clicked_epoch_ms` separately. Its historical `run_epoch_ms` field is the
arming epoch. Node session samples label their pre-click sampler anchor;
correlate their absolute epoch with the actual browser click and the shared
attempt label. Kernel rows retain epoch nanoseconds and cell-local monotonic
elapsed time. Do not compare unrelated processes' relative elapsed values
as though they had one clock origin.

A controlled source-generation comparison against `00bec2941` confirms exact
Analysis/contact/property notebook program equality after replacing only each
owned output-directory prefix. It prepares source text, never runs molecular
work or starts a server. Initial probe import-path failures are not receiving
passes. The opt-in source has a new explicit actual-Jupyter guard in
`jupyter_receiving_guard.py`; receive it on the committed integration next.
Existing readiness, canvas and browser verdicts remain separate.

### Exact-source actual Jupyter receiving

The [bounded receipt](../../devtools/data/initial_canvas_diagnostic_receiving_615_20261111.json)
records source `7ccb00b93` with all 2,581 published MolSysViewer `5164f13b`
files verified against the earlier Git-object manifest. The generated test
harness is identified separately. The first actual attempt fails before browser
startup because the frozen export has no Playwright resolution. The corrected
dependency attempt fails at Chromium ProcessSingleton creation: the long
workspace TMPDIR exceeds the Unix-socket path allowance. Neither starts the
molecular cell or reproduces the historical #615 stage. Both failures, JUnit
identities and owned resource records remain retained.

Existing Playwright 1.57.0 is then linked into the private source export without
an install, sibling edit or runtime-bundle rewrite. A short owned TMPDIR on the
workspace filesystem avoids that specific socket failure. The final cold
Jupyter/Chromium diagnostic **passes its one explicit guard**, with the original
30-second canvas wait and 15-second kernel timer. It sees the original cell's
3,983-atom scene, nine kernel-stage records and an eligible new native draw at
14.30 seconds after the browser's observed click. The halfway live-session
checkpoint is explicitly not reached: the canvas wait ended earlier. The
separate controlled Node test covers two authenticated reads while its test
server remains busy; it does not fabricate a real original-timeout recurrence.

Browser stage intervals use one monotonic clock. The first kernel epoch is
about 53 ms earlier than the observed browser click epoch in this record.
Retain that discrepancy without clamping: clock mapping or event dispatch is
not resolved here. Cross-process epochs are correlation evidence, not precise
causal ordering. Kernel-local monotonic durations retain their own meaning.

The two-CPU scope peaks at about 1.35 GiB under a 4-GiB/no-swap cap. The reserve
watchdog observes at least 12.83 GiB host memory available and no own OOM or
reserve stop; this is not an exclusive reservation or a global resource claim.
Temporary settings and configuration files are retired. Published receipt
metadata excludes auth tokens, kernel/session identifiers, private notebook
paths, stack contents and molecular payloads. Private raw artifacts remain in
`.pytest_cache/pre1-review-20261111/initial-canvas-615/` with hashes retained.

The six Node controls pass on both Node 24.21.0 and the actual runner's Node
22.22.1. The initial short source-review probes with missing script import paths
and the raw-source-versus-ready-harness path mistake are not qualification
passes; corrected default-program comparison and ready-export verification
succeed. The scientific runtime and addon API remain unchanged.

The reviewed #707 diagnostic contribution is received for main incorporation.
**#615 stays active:** no causal correction or evidenced disposition of the
original executing-cell timeout has been established. This is one initial-canvas
receiving case, not the complete default Analysis, installed-pair or Qt gate.

Earlier 8.05/12.83-second observations are arming-relative, not a verified
exact click-relative latency. The wording above is corrected accordingly;
the original captured values remain unchanged.


## Proposed completion disposition — 2026-11-13
The [completion packet](../pre_1_0_completion_handoffs_20261110.md#remaining-technical-decision-for-615713--2026-11-13)
owns the proposed options and conditions. The recommendation retains the
original failed attempt and this open, causally unresolved operational risk while
allowing exact-candidate qualification with all original checks and deadlines.
Any recurrence stops acceptance of the affected gate. This requires an explicit
maintainer revision of the current blocking criterion; no decision, risk
acceptance, closure, score change or publication permission is inferred.
