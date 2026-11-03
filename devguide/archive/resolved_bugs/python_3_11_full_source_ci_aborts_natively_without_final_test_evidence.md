---
summary: Python 3.11 full source CI aborts natively without final test evidence
issue: uibcdf/molsysmt#527
status: resolved
opened: 2026-10-30
closed: 2026-11-02
severity: high
verification: reproduced
area: [ci, tests]
guard: tests/form/openmm_Topology/test_native_inference_boundary.py::test_edge_free_conversion_enters_the_native_reader_once
normative:
blocked_by: []
supersedes: []
---

# Python 3.11 source qualification aborts without final test evidence

**Reported:** 2026-10-30, inspecting the exact-source matrix for #255.
**Status:** Active; retained Linux/macOS traces and a bounded regression identify
a recursive edge-free OpenMM conversion. The correction passes local controls and the final-candidate complete
Linux/Python 3.11 suite; remaining cross-platform qualification is pending.

## What

The Linux/Python 3.11 full-suite job ends in a segmentation fault, exit 139,
without a final pytest summary or JUnit artifact. It is a failed source gate,
independently of the Pandas assertion failures owned by #526.

```bash
python -m pytest --receptor=ci --junitxml=junit.xml
```

This is the command executed by `ci-full.yaml` in
[run 41141703873, job 124357390493](https://github.com/uibcdf/molsysmt/actions/runs/41141703873/job/124357390493),
on MolSysMT `9fb77c3583b44dda31c0466348369de137301df9` with controlled Viewer
`ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352`.

## How

At opening, the cause was unknown. The last compact progress record was approximately 80%,
18,986/23,732 cases, around 2,715 seconds. These are progress observations,
not final passed/failed counts. The faulthandler output contains numerous
waiting threads in `nglview/remote_thread.py:47` and ends in an ellipsis; it
does not identify the faulting Python frame. No responsible native extension
has been established from this dump.

The later retained current-thread traces and bounded conversion regression establish
consumer-side OpenMM conversion recursion; see the cause-specific section below.
The initial uncertainty and failed diagnostic attempts are preserved as history,
not as the current diagnosis. The corrected full source matrix remains pending.

The workflow now requests pytest-receptor's bounded, flushed per-phase JSONL
stream alongside JUnit, and uploads either existing file even after failure.
Only those explicit paths are uploaded; the hidden JSONL path is enabled
explicitly. Native pytest/process exit status remains authoritative.

The guard executes the actual workflow command in a temporary test project:
one case passes, the next exits abruptly with status 17. It verifies the real
exit status, retained preceding test/phase evidence and incomplete artifact
without a final record through `pytest_receptor.read_artifact`. This proves
diagnostic retention, not a correction or reproduction of the segmentation
fault. The workflow runs this guard before its full suite.

## Why

The eight-cell source qualification for #255 cannot pass with an aborted cell.
Without retained phases, a long-running abort also lacks the evidence needed
to select a narrower reproduction. Passing registered scientific cases from
the earlier step do not replace the full-suite gate.

## What is measured and what is assumed

Observed failure: the job and command above, retained in local qualification
log `provider-ci-linux311-182.log`, exit 139. The last progress count and thread
dump do not establish the crashing node or library.

Local development verification: the abrupt-exit guard fails without a JSONL
artifact (run 183). After the workflow change, the CI/scientific-executor
control selection passes 37 tests (184, exit 0, 11.32 seconds); its receptor
contract subset passes 6 tests (185, exit 0, 0.58 seconds). These tests do not
substitute for executing the corrected exact-source matrix.

The JSONL stream is bounded to 50 MiB by default. It records reported phases,
not a guaranteed last-started node when a process aborts during setup. An
incomplete or truncated trace is diagnostic evidence, never a passing result.
The CI-pinned pytest-receptor 1.1.0 source supports this stream and reader;
no dependency bump or speculative provider fix is required for retention.

## What was refuted

At opening, no native root-cause hypothesis had been eliminated by a narrow
reproduction. Waiting NGLView threads did not identify NGLView as responsible.
The later bounded regression establishes recursive consumer conversion without
requiring an OpenMM Context or modifying a native provider. No Rust, PyTraj, BLAS,
Pandas or reporter memory-corruption defect is established. The separate Pandas
compatibility correction is not the cause-specific fix for this recursion.

## Scope and exclusions

Retain actionable evidence, identify and reproduce the native failure, correct
its cause and requalify the exact source. Do not disable affected tests, hide
exit status or infer a complete suite result from partial artifacts. This work
does not authorize releases, installed-package qualification or main integration.

## Acceptance criteria

- The abrupt-exit retention guard passes in the controlled CI environment.
- A subsequent exact-source run produces sufficient evidence to identify the
  aborting scope, or a documented narrow reproduction establishes its cause.
- The cause receives an appropriate regression guard and correction; a retry
  alone or the current diagnostic guard does not establish this condition.
- The complete required source matrix passes on the final candidate, with old
  failed runs retained and all skipped/deselected scopes reported separately.

## Dependencies and risks

Shares the source-qualification milestone with #526 but has no demonstrated
causal dependency on that issue. Process-abort diagnostics must not expand
uploaded artifacts to unrestricted checkout files or credentials.

## Provenance

2026-10-30: GitHub-hosted `ubuntu-latest`, Python 3.11, exact provider/Viewer
commits and job identified above. Local guard measurements use the shared Linux
development environment, Python 3.14.7 and pytest-receptor
1.2.1+22.g00a31c4; the CI tool pin remains 1.1.0. Local logs and JSONL outputs
are retained under the #255 qualification scratch directory.


## Retained evidence narrows the abort — 2026-11-02

The corrected-provider run [41152714070, Linux/Python 3.11 job 124392743149](https://github.com/uibcdf/molsysmt/actions/runs/41152714070/job/124392743149)
also aborts with exit 139. The new JSONL artifact is retained, incomplete and
below its size bound (33,976,517 bytes). Its final phase is the successful setup
of `tests/third_party/openmm/forces/test_pin_atoms.py::test_pin_atoms_3`; the
preceding test has passed call/teardown records. This identifies the active
call scope, not its precise native instruction or root cause. The raw fault
dump still omits the current Python call site among many background threads.

All seven original/new #526 regression calls pass even in this incomplete
Python 3.11 run. Linux 3.12, 3.13 and 3.14 independently finish the complete
suite with 23,631 passes, 102 skips and 40 deselections, exit 0. The independent
macOS cancellations are now tracked in #528. None of those outcomes clears
this abort.

The isolated three-test pinning module passes in local Python 3.14.7/OpenMM
8.6.1 (187, exit 0, 4.43 seconds). This does not reproduce the hosted Python
3.11.18/OpenMM `8.6.1-py311h1aadaef_0` environment. The next source workflow
runs the pinning module before the full suite, without changing the full-suite
selection, to distinguish isolated failure from accumulated process state.
A temporary fixture scopes faulthandler to the current thread within that
module so a repeated native fault's Python call site is not lost behind widget
threads; it restores pytest's all-thread setting afterward. This is diagnostic
instrumentation, with removal after the cause-specific regression is settled,
not a fix or a dependency attribution. Combined local controls pass 12 cases
(189); hosted reproduction and the crash correction remain pending.


## Isolated controlled-environment probe — 2026-11-02

The exact `2f046721bbe7b399377d8f6f73f17c605d6741b8` source execution
[41552267703](https://github.com/uibcdf/molsysmt/actions/runs/41552267703)
reports the isolated OpenMM pinning step as successful in every one of its eight
cells, including the previously aborting Linux/Python 3.11 environment. Counts
remain subject to the eventual raw job log; this observation is the official
step conclusion, not an invented full-suite summary. All eight complete suites
are still running at this observation.

This motivates investigating accumulated state or an intermittent failure;
an isolated successful step does not distinguish those possibilities or prove
a root cause. Keep the current-thread crash diagnostic and full-suite evidence.
No new full execution is launched merely because observation was delayed.


## Capture-descriptor regression and correction — 2026-11-02

The same exact-source run's Linux/Python 3.11 job
[125642612697](https://github.com/uibcdf/molsysmt/actions/runs/41552267703/job/125642612697)
ends with exit 139 again. Its raw log contains no fatal Python traceback. The
isolated pinning step passed three cases in 1.92 seconds; that success does not
clear the full-suite failure. Linux 3.12/3.13/3.14 complete with 23,631 passes,
102 skips and 40 deselections each, exit 0; macOS cells remain active at this
observation.

The initial per-test current-thread fixture redirected faulthandler into pytest's
temporary FD capture. Abrupt process exit loses that captured output. This is a
separate diagnostic defect, not the native crash's established cause. A real
subprocess regression now imports the actual fixture, enables native pytest FD
capture, starts 110 background waiting threads and raises SIGSEGV. Core dumping
is disabled in that child only. Before correction the subprocess exits by signal
with empty stderr and the regression fails (205, one failure). After correction
its retained stderr contains the fatal error and active Python call site, without
the background-thread dump.

The fixture now borrows pytest's pre-capture duplicated stderr descriptor and
restores the plugin's all-thread mode afterward. Pytest owns the descriptor's
lifetime; no new file descriptor or retained engine object is introduced. There
is no public pytest descriptor accessor, so this temporary test-only integration
uses `_pytest.faulthandler.fault_handler_stderr_fd_key`. The behavioral subprocess
regression protects that private integration against dependency drift. A disabled
faulthandler plugin remains disabled. The local pytest version is 9.1.1.

`devtools/tests/test_pytest_receptor_ci_contract.py::test_native_fault_trace_survives_pytest_capture_and_background_threads`
is the new capture regression. All seven CI-contract tests plus three actual
OpenMM pinning cases pass (206, 10 passed, exit 0, 4.40 seconds). The integrated
builder/documentation/diagnostic selection also passes (209, 237 passed, exit 0,
20.48 seconds). These are diagnostic and targeted source results. The crash's
cause-specific correction and a complete hosted source matrix remain pending;
this report stays active and its original incomplete/failed runs remain retained.


## Separate diagnostic-provider handoff — 2026-11-02

The passing isolated Python 3.11 probe also reports two SMonitor argument-summary
recursion warnings, for the ArgDigest wrapper and native MolSys constructor.
Their observed provider is SMonitor 0.21.0 at
`066b69cad8896cdc126d5586fd53268af4ea6490`, with ArgDigest 0.15.0 at
`57447cc4ec1f7ce85078f8a939892efd075bc919`. The actionable diagnostic limitation
is handed to [SMonitor #56](https://github.com/uibcdf/smonitor/issues/56), with
sanitized messages and the exact passing-probe evidence. No minimal recursive
input or causal connection to the later native crash has been established.
No warning is suppressed and no dependency pin is changed.

The corrected capture fixture is now published in provider
`dbcb4582cbd93bef7b8b8ed4f3dfad1483fd05c7` and is being exercised by
[exact-source run 41562051654](https://github.com/uibcdf/molsysmt/actions/runs/41562051654)
against the same frozen Viewer ca7 source. The new diagnostic guard and isolated
pinning steps report success before the complete suites in all five matrix cells
that have started; three macOS cells remain queued at this observation. Those
step conclusions are not a completed full-suite verdict. Older runs are retained.


## Retained call stacks establish converter recursion — 2026-11-02

The corrected descriptor captures the current Python call stack in both
[Linux/Python 3.11 job 125674802433](https://github.com/uibcdf/molsysmt/actions/runs/41562051654/job/125674802433)
and [macOS/Python 3.11 job 125674802426](https://github.com/uibcdf/molsysmt/actions/runs/41562051654/job/125674802426).
Both terminate with exit 139 on provider dbcb4582c. The repeated call path is:

```text
openmm_Topology._read_native.read_native
  -> build.get_missing_bonds(original_openmm_topology)
  -> basic.get(group attributes)
  -> basic.convert(to molsysmt.MolSys)
  -> openmm_Topology._read_native.read_native
```

The reader constructs native inventory, then asks the original foreign object
for inference. Bulk metadata queries pipe that foreign object back through the
same converter. Its broad exception handler masks recursion/inference failures.
The MolSys converter does not forward the shared get_missing_bonds option, and
the Topology converter exposes it but also fails to forward it. This permits
unbounded nested construction. The deepest observed allocation in Pandas is a
call site inside that cycle, not evidence of a Pandas memory-corruption defect.
No OpenMM Context instruction is required for the bounded reproduction.

A counted reader guard permits the first actual conversion, stops a second
entry before an uncontrolled stack overflow, and asserts one entry. Additional
controls require explicit inference opt-out, inference on the constructed native
domains, retained original source and propagation of injected allocation/runtime
failures. Before correction seven of eight cases fail (224); the declared-edge
control already passes. No recursion limit is raised and no native crash is
silently retried.

The correction calls the existing general build.get_missing_bonds tool on the
constructed MolSys with with_distances=False: OpenMM Topology has no coordinates.
Available intra-group template pairs retain inferred evidence and partial
connectivity; unsupported groups stay unavailable. Recorded edges remain
explicit. Both converters forward the existing opt-out; MolSys receives the
option keyword-only, preserving its existing positional arguments. Unexpected
inference exceptions now propagate instead of being discarded. All this uses
existing native/build tools, without another chemistry store or provider pin.

The first corrected scope passes 12 cases (225, exit 0, 1.27 seconds), including
the three actual pinning tests and the new converter doctest. The broader native
OpenMM/conversion-truth scope passes **826 cases**, exit 0, 258.47 seconds (227).
Additional inventory-piping and unknown-group controls are included there. The
standalone guard suite, actual pinning and CI-contract scope are rechecked after
optional-backend fixture and workflow receiving. The full CI preflight now runs
these bounded conversion guards before the unchanged complete suite. Controlled
Python 3.11 and full-matrix acceptance remain required before this report closes.


## Correcting the diagnostic handoff — 2026-11-02

SMonitor #56 receives a cause clarification after the consumer cycle is established.
Its original warnings do not show that SMonitor creates recursion or fails on an
ordinary nonrecursive input. The fallback retained the successful probe outcome;
no independent summary reproducer or necessary provider fix is established.
Original evidence remains intact, and final controlled-probe disposition awaits
its actual log. The broad 826-case correction scope remains local evidence,
not a prematurely asserted complete Python 3.11/platform result.


## Controlled probe disposition and superseded-run retirement — 2026-11-02

The actual 64b8694e9 Linux/Python 3.11 raw job log confirms the combined
conversion/pinning probe passes **13 cases**, exit 0, 1.25 s (240). It contains
no argument-summary recursion warning; the separate scientific certificate
passes 79/79 cases/59 nodes. This supports the cause-specific correction but
is not a completed full Python 3.11 suite. SMonitor #56 is withdrawn as not
planned: no independent ordinary-input provider defect is established and no
provider change is claimed. Its original warnings and consumer diagnosis stay
publicly preserved. Residual diagnostic bugs would need an independent input.

The 64b Linux/Python 3.13 complete suite independently passes 23,668 cases,
with 102 skips and 40 deselections, exit 0, 2,859.04 s. Both preceding matrices
are then retired for their established obsolete source defects, after recording
exact heads, job states and artifact manifests. Runs 41562051654 and
41569717011 are now officially completed/cancelled; completed successful and
failed cells retain those actual individual conclusions. The active de7 source
matrix 41572981893 and final local run 236 are preserved. This retirement is
not an observation-timeout retry or a waiver of final full-matrix acceptance.


## Complete final-candidate Linux 3.11 success — 2026-11-02

Final de7ffad2a source run 41572981893/job 125710060189 completes with
**23,672 passed, 102 skipped, 40 deselected**, zero failures/errors/not-executed,
exit 0, 2,189.90 seconds. The actual canonical artifact is finalized, complete,
integrity-valid and untruncated; JUnit independently agrees (243). All ten
cause-specific bounded conversion controls are matched to executed passing
calls. The earlier isolated probe is no longer the only Linux 3.11 evidence.
No responsible provider memory-corruption claim is introduced. The final macOS
3.11 and other remaining full cells still need their actual outcomes before
this report's complete-matrix condition is satisfied.


## Resolution — 2026-11-02

The consumer's recursive OpenMM conversion is corrected by inferring on the constructed native domains and honoring the existing explicit opt-out. The bounded real-reader regression protects one conversion entry and preserved source/error semantics. Final runtime de7ffad2a completes every full source cell, including both formerly aborting Linux/macOS Python 3.11 cells, and all ten cause-specific controls pass in every cell. Complete canonical primary evidence and JUnit agree; earlier aborted/interrupted runs stay retained. The scoped current-thread fault fixture is deliberately retained as useful test-only diagnostic infrastructure, with its real captured-SIGSEGV regression passing on the supported POSIX source lanes. This supersedes the initial transient-removal suggestion: it is not the crash fix and introduces no runtime store/hook. Its private pytest descriptor integration remains explicit and regression-protected. SMonitor #56 is withdrawn after the consumer cause and corrected probe are established; no provider fix or corruption attribution is claimed.

The complete source matrix is [41572981893](https://github.com/uibcdf/molsysmt/actions/runs/41572981893), officially successful on de7ffad2a. The #255 source closeout records full counts, omissions, science scopes and evidence limits. No main merge, package promotion or release is performed.
