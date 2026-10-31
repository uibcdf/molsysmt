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
