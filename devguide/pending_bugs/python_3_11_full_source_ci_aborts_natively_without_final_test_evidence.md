---
summary: Python 3.11 full source CI aborts natively without final test evidence
issue: uibcdf/molsysmt#527
status: active
opened: 2026-10-30
closed:
severity: medium
verification: reproduced
area: [ci, tests]
guard: devtools/tests/test_pytest_receptor_ci_contract.py::test_full_ci_preserves_partial_phase_evidence_after_abrupt_exit
normative:
blocked_by: []
supersedes: []
---

# Python 3.11 source qualification aborts without final test evidence

**Reported:** 2026-10-30, inspecting the exact-source matrix for #255.
**Status:** Active; diagnostic retention is implemented, but the native abort's
cause and correction remain unestablished.

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

The cause is unknown. The last compact progress record is approximately 80%,
18,986/23,732 cases, around 2,715 seconds. These are progress observations,
not final passed/failed counts. The faulthandler output contains numerous
waiting threads in `nglview/remote_thread.py:47` and ends in an ellipsis; it
does not identify the faulting Python frame. No responsible native extension
has been established from this dump.

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

No native root-cause hypothesis has been eliminated by a narrow reproduction
yet. The presence of waiting NGLView threads does not prove that NGLView is
responsible. Neither Rust, PyTraj, BLAS nor the reporter is identified as the
cause. The Pandas fix is not described as fixing this independent abort.

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
