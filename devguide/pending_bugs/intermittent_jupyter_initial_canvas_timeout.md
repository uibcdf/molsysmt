---
summary: Investigate intermittent Jupyter initialization before the first molecular canvas.
issue: uibcdf/molsysmt#615
status: blocked
opened: 2026-11-06
closed:
severity: medium
verification: measured
area: [tests, jupyter, initialization, molsysviewer]
guard: tests/molsysviewer_molsysmt/test_jupyter_stage_diagnostics.py
normative:
blocked_by: [uibcdf/molsysviewer#384]
supersedes: []
---

# Initial molecular canvas timeout

## Current lead and consumer dependency — 2026-11-13

At the principal maintainer's request, uibcdf/molsysviewer#384 owns the lead
audit and requested resolution. MolSysMT #615 stays open as a blocked consumer
and coordinated-release dependency. Its accepted resolution is required before
the MolSysMT 1.0.0 / MolSysViewer 1.0.0 pair.

The handoff includes the original observations, all distinct subsequent stages,
the owned cold initial-canvas guard and immutable diagnostic receipt.
Assigning the audit lead does not establish a MolSysViewer production-code
cause. If the evidence points to the kernel, MolSysMT or another provider,
return that stage and bounded reproduction to the appropriate owner.
MolSysMT retains its kernel-side support and checks the returned resolution
and applicable final-pair receiving before clearing this dependency.

## Maintainer decision: continue the investigation — 2026-11-15

Diego explicitly chooses to keep #615 open and investigate it. The proposed
closure with an unknown historical cause is **not accepted**. There is no
outstanding request to approve that proposal. MolSysViewer #384 retains the
lead; this report remains a blocked consumer and pre-pair dependency.

The next work must distinguish causes rather than accumulate passing retries:

1. Review the retained original fixture/source path and available records to
   identify which initialization transitions are observable and which are
   missing. Keep preparation/import, kernel message admission, widget/runtime
   bootstrap, scene registration and native drawing distinct.
2. Use that review to select a bounded discriminating control. The separate
   #392 scene-lock defect and #396 kernel comm stall are hypotheses for this
   path only if their required conditions and missing transition can be
   demonstrated. A shared installed version or a later passing run is not
   sufficient. Any provider comparison must retain actual loaded origins and
   change one relevant input without modifying the shared prefix.
3. On a reproduced initial-scene failure, preserve the correlated kernel,
   transport and draw timeline and the pre-deadline stack. Keep the original
   30-second allowance and 15-second stack capture; do not force drawing,
   warm imports, enlarge deadlines or retry blindly to obtain a pass.
4. Return the demonstrated cause, applicable correction and regression, or
   the precise remaining uncertainty and next discriminating control. If the
   historical record cannot establish a cause, report that limit to the
   maintainer; it does not authorize closure.

The repaired #762 guard and later successful startup controls remain useful
receiving evidence. They do not resolve this investigation. Existing final-pair
checks and the build/hosted/tag/publication pause remain unchanged.

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


## Maintainer disposition — 2026-11-13

The [completion packet](../pre_1_0_completion_handoffs_20261110.md#maintainer-audit-direction-for-615713--2026-11-13)
records the requested owner handoff. The earlier risk-acceptance proposal
was not adopted. This issue remains blocked on uibcdf/molsysviewer#384;
no causal repair, environmental attribution, acceptance or score change follows
from delegating its audit.

## Lead review and proposed disposition — 2026-11-15

The lead publishes its audit, original-data reinspection, separate #392 causal
fix and normal/contended startup controls in immutable MolSysViewer `342e6309`.
The [bounded owner review](../../devtools/data/initial_canvas_disposition_review_615_20261115.json)
verifies all three public Git blobs. The historical executing-cell timeout has
no usable pre-deadline trace; neither a different fixture exception, #392 nor
later successful draws establishes its cause.

The concrete lead proposal is to retain that unknown cause and the original
failure, receive the exact final composition through the phase-observed guard,
and block acceptance on recurrence. This closes only the historical
investigation by an explicitly accepted disposition; it does not describe a
causal repair or mark the candidate/installed gates as passed. The principal
maintainer was asked to decide this specific resolution. **He chooses to keep
#615 open and investigate it; the proposed closure is not accepted.**

The guard review finds #762: the original opt-in pytest admits absent first-draw
evidence and checks ordering only when a mark is present. Its actual synthetic
counterexamples expose three false acceptances. The corrected receiver requires
a new eligible native draw in the original single 30-second window, after the
observer and expected scene, without forced state, retries or warmed imports.
The final selected cohort passes 44 cases, including all seven Node observer
controls. One actual fresh-Jupyter invocation receives all nine kernel stages,
the expected 3,983-atom scene and a new draw 16.38 seconds after observed Run.
Its frozen source/support composition and ipykernel 7.3.0 remain explicit.
One page error matches the plain-Jupyter control; no zero-error claim follows.
See the [source receipt](../../devtools/data/three_closeout_receiving_615_256_524_762_20261115.json).

This qualifies the repaired receiver on those inputs, not the final pair or
historical causality. MolSysViewer's separate #396 kernel-communication study
must retain its own causal/provider evidence; this passing check neither
attributes #615 to that cause nor qualifies an older kernel for final use.
The unchanged startup requirement is explicit in the authoritative release
checklist; principal acceptance of a disposition cannot replace that check.

### Later immutable environment supplement — 2026-11-15

MolSysViewer `f6765f6c680b82f47de0ae94dcd459ac32a79138` publishes the
preserved original environment supplement and its separate #396 provider
study. All three public report blobs are verified in the same
[bounded review](../../devtools/data/initial_canvas_disposition_review_615_20261115.json).
The historical inventory reports ipykernel 7.3.0 and the neighbouring failure
matches the original digest. This is associated distribution metadata, not
an observation of the module loaded in that kernel or its missing transition.

The lead separately reports a molecular-free comm counterexample and original
isolated 7.4.0 receiving, including one canonical ten-edit/eight-phase Movie
pytest. These published scoped claims do not reconstruct #615; their private
execution/provider evidence is not independently reproduced here. The lead's
current notebook-host baseline is ipykernel >=7.4.0, with controlled shared-host
adoption owned by uibcdf/molsyssuite#200. No shared prefix, dependency floor or
candidate is changed here. The causal investigation and applicable exact-pair
startup receiving remain required; this supplement adds no progress credit.

## Controlled initial-execute mechanism received — 2026-11-15

MolSysViewer `3aff1d48a5a38fb9854efe2c95a9a8f35cadbccb` publishes paired
native-kernel and actual-Jupyter/TcTIM diagnostics under its lead #384.
The [owner review](../../devtools/data/initial_canvas_disposition_review_615_20261115.json)
verifies the public receipt's Git blob, all eight retained diagnostic-program
hashes and all 28 listed original molecular-record hashes. Read-only inspection
of the correlated request, recorded kernel version, transport timestamps,
first-line marker and new-draw observations confirms these scoped facts:

| Controlled arm | Observed result |
| --- | --- |
| ipykernel 7.3.0 | A native execute reaches the server promptly but is admitted by the kernel about 30.52 seconds after its send. The first line is later than the original allowance; no molecular canvas appears before the unchanged timeout. The 15-second stack records a waiting shell. |
| ipykernel 7.4.0 | The corresponding execute is admitted about 1.6 milliseconds after server send. The actual initial cell presents 3,983 atoms and a fresh native draw 6.547 seconds after observed Run. |

The diagnostic deliberately overlaps one real history reply and initial execute
using a bounded scheduling hold. Native send/dispatch functions delegate once;
it does not insert a 30-second artificial sleep, fabricate a reply or warm
molecular imports. A first-line marker and transport observations are added.
This demonstrates a mechanism capable of producing the initial-scene symptom,
not a spontaneous recurrence or proof of that schedule in the original event.
Cross-process click/first-line clock offsets are not interpreted as latency.

Original combined driver 923 remains exit 1: its final assertion checked marker
absence after retiring the host, when the old kernel had entered late. The
separate offline verifier 924 is reported exit 0. This review independently
checks the retained observations without re-running either molecular arm or
rewriting either original verdict. The reviewed sources use receiver tests
`bc5a9297a` with scientific source `aee7aa65`, native `4ffb82e4` and isolated
original kernel providers; this is not current/final installed qualification.
Provider archives and all private custody files are not independently
requalified by the selected read-only review.

**#615 stays open under the maintainer's decision.** The answer to recurrence
is now precise: the symptom has been reproduced under controlled scheduling;
no spontaneous recurrence or exact historical cause is established. Retain
lead review of applicability and the already required uninstrumented final-pair
startup on the corrected host profile. No extra blind retry, new matrix,
shared-prefix change, candidate, progress credit or publication is authorized.

## Joint recommendation requested by the maintainer — 2026-11-15

The maintainer asks both teams to agree whether a corrected kernel minimum
is sufficient or further causal investigation is required. MolSysMT and
MolSysViewer agree on a conditional technical recommendation:

1. Require ipykernel >=7.4.0 for the Jupyter host profile, without adding a
   mandatory dependency to the scientific core or headless/Qt profiles. The
   [upstream correction](https://github.com/ipython/ipykernel/pull/1529) and
   [7.4.0 release notes](https://github.com/ipython/ipykernel/releases/tag/v7.4.0)
   identify the shell-message transport repair; paired controls 919/923
   demonstrate its applicability to a controlled initial-execute failure.
2. Receive one normal TcTIM initial startup through the original #762 guard,
   without the experimental history-reply barrier or scheduling/server
   delegates. Require the recorded loaded kernel version/source, initial-cell
   ownership, 3,983 atoms and a fresh native draw within the original 30-second
   limit, retaining pre-deadline diagnostics. MolSysViewer will receive this
   finite case in its existing local checkpoint; MolSysMT will not duplicate it.
3. If that normal case passes, recommend a documented technical closure on
   the corrected supported host profile. Preserve the uncertainty about the
   exact original event; reconstructing its unobserved transition indefinitely
   would not be an additional technical prerequisite of this recommendation.
   The exact final-candidate, installed, platform and publication gates remain
   separate and mandatory.

No existing result is substituted for step 2: startup controls 845/847 receive
3,983 atoms with the older host, while normal 7.4.0 Movie control 916 uses a
62-atom pentalanine system. The controlled 923 startup adds a scheduling
barrier. None is the requested normal corrected-kernel TcTIM case.

This is a jointly agreed recommendation, not a claimed pass or authorization
to close. #615 remains open under the maintainer's current decision pending
that finite result and review. No shared-prefix modification, new matrix,
package build or publication is requested by this agreement.

## Agreed normal-source startup received — 2026-11-15

MolSysViewer `7d88b56a6514dc1509ae0cfb85bb77ca1b12c0c9` publishes normal
control 928. The [owner review](../../devtools/data/initial_canvas_disposition_review_615_20261115.json)
verifies the public Git blob, custody manifest and all 37 retained file hashes,
then independently checks the actual kernel-origin record, nine correlated
kernel stages, scene/draw observations and unchanged receiver source bytes.

The loaded kernel is original isolated 7.4.0. Normal TcTIM preparation produces
3,983 atoms and a fresh native draw **10.7884 seconds after observed Run**,
after observer arming and scene registration and within the original 30-second
allowance. Receiver files match `bc5a9297a`; actual MolSysViewer source is
`6f80cc915`, with unchanged native `4ffb82e4`. The private driver changes only
the isolated kernel path and passive post-preparation module provenance. There
is no history-reply barrier, scheduler/server/comm delegate, molecular import
warm-up, deadline increase or identical retry. One actual page error matches
the plain-Jupyter control; output and observer errors are zero.

The native driver exits 0, records unchanged inputs and retires all 27 tracked
processes without a resource stop. Setup 927 failed before browser/kernel and
remains separate. This owner review does not execute another molecular case,
independently requalify the complete kernel archive or every client package
source, or turn a source result into an installed/platform/human acceptance.

**The jointly prescribed normal-source startup condition is satisfied.** Both
teams' conditional recommendation is now ready for maintainer review: adopt
the corrected Jupyter minimum and close the technical host-profile defect,
retaining the original event's unproven exact cause. #615 remains open under
the existing explicit decision; closure is not inferred from the agreement or
this pass. Final exact-candidate/installed checks, controlled legacy-prefix
adoption and publication retain their separate owners and gates.
