---
summary: Review inherited Python ecosystem policy in MolSysMT.
issue: uibcdf/molsysmt#244
status: partial
opened: 2026-09-25
closed:
verification: inspected
area: [ci, deps]
guard:
normative:
blocked_by: []
supersedes: []
---

# Review inherited Python ecosystem policy in MolSysMT

**Reported:** 2026-09-25, from the MolSysSuite member rollout under
`uibcdf/molsyssuite#6`.
**Status:** Developer tools and support libraries are both partially reviewed.

## Public receiving reconciliation — 2026-10-07

The [published pair ledger](../release_1_0_status.md#current-pre-10-checkpoint--2026-10-07)
and [original handoff receipt](../../devtools/data/stabilization_023_staging_handoff_20261006.json)
now supply the completed pre-1.0 8/8 exact-source, native-wheel and 16/16
public installed-pair evidence for MolSysMT 0.23.0 / MolSysViewer 0.24.0.
GH Run Receptor independently rechecked the source and public-pair terminal
conclusions. No later source fix is attributed to those immutable files.

The inspected central `suite.toml` still records MolSysMT's Python transition
as `authorized` and its support-library/developer-tool review as `partial`.
The local public delivery is complete, but central receiving reconciliation is
still required before changing those states or closing this owner report.
The selected four support-provider pins remain published exact sources; current
Viewer development routes now select the delivered 0.24.0 build-1 producer.
The existing quantity/argument/diagnostic/dependency guards and original
full-matrix evidence retain their scope. #155's optimization audit and #292's
portable optional-attribution migration remain post-1.0, not invented gaps in
this delivered runtime. Post-publication #349 is separately guarded and its
repair requires fresh future-candidate qualification under #334.

The final public receiving handoff was delivered to uibcdf/molsyssuite#51
(comment 6053257691); its complete body was checked after publication.
The central owner must reconcile its registry or identify a concrete missing
check; this local report remains partial until that response.

## What

Review MolSysMT against the inherited MOLI Python support-library and
developer-tool policies. Track the two adoption states independently in the
MolSysSuite inventory.

## How

Pin published pytest-receptor 1.1.0 in the Conda test and development
environments. Use the `ci` profile in the standalone data-integrity workflow
and preserve its curated test selection. Retain the existing
`receptor_rerun_command` in `pytest.ini` for the repository's
`python -m pytest` invocation. The smoke, full, and weekly
workflows already select `--receptor=ci`; inspect hosted results with
gh-run-receptor and retain native GitHub checks when exact dependencies or
commands must be confirmed.

Review public API argument validation through ArgDigest, optional dependency
handling through DepDigest, diagnostic paths through SMonitor, and physical
quantity handling through PyUnitWizard. A declared runtime dependency is a
starting point, not proof that every applicable boundary is covered.

## Why

MolSysMT is a priority Python member in MolSysSuite. Before this review, the
test environment pinned receptor 0.6.0, the development environment omitted
it, and the standalone data-integrity workflow used plain pytest. Existing
main CI profiles already aligned with the MOLI rule but did not settle the
version pin or support-library applicability.

## What is measured and what is assumed

The initial discrepancy is inspected in `devtools/conda-envs/test_env.yaml`,
`development_env.yaml`, and `.github/workflows/ci-data-integrity.yaml` at
the source commit that opened this issue. Local receptor tests passed for the
curated provenance selector (one test) and the focused dependency and unit
policy selectors (nine tests). Ruff check and format, the dependency import
validator, and developer-guide validator passed. Hosted results will be added
after the exact implementation commit runs. No claim is made that the Python
3.14 transition in `uibcdf/molsysmt#237` is complete: the initial MolSysSuite
repository checker reported the then-existing `requires-python <3.14` and
missing Python 3.14 CI literals while this authorized transition is active.

## What was refuted

The existing `--receptor=ci` calls in smoke, full, and weekly CI do not imply
that every pytest workflow has the profile or that the declared plugin release
is current and reviewed.

## Scope and exclusions

This review does not alter scientific algorithms, public Python support
metadata, the MolSysViewer dependency, or the release gates of
`uibcdf/molsysmt#237`. It does not treat the backup workflow under
`.github/workflows/backups/` as an active CI gate.

## Acceptance criteria

- Every active hosted pytest command uses `--receptor=ci` with a declared
  published receptor release; local agent tests use `--receptor=llm`.
- The exact source commit passes applicable local checks and hosted gates,
  or the remaining failures are identified and linked without weakening tests.
- The member issue and MolSysSuite inventory record applicable support-library
  boundaries, evidence, and any bounded remaining work.

## Dependencies and risks

`uibcdf/molsysmt#237` separately owns the Python 3.14 transition. Its active
CI and packaging work can affect broad hosted gates, so receptor adoption
must be judged on its own evidence as well as the full workflow conclusion.

## Support-library applicability checkpoint

All four inherited boundaries are present in MolSysMT. Public argument
digesters live in `molsysmt/_argdigest.py` and the private digester modules;
optional backend declarations and checks live in `molsysmt/_depdigest.py` and
form adapters; coded diagnostics live in `molsysmt/_smonitor.py` and the
SMonitor integration; unit policy and quantity conversion use
`molsysmt/_pyunitwizard.py` and PyUnitWizard at public physical-quantity
boundaries. The runtime metadata declares all four libraries. Local focused
receptor tests passed 82 cases across quantity digesters, SMonitor contracts,
and diagnostic exceptions, in addition to the nine dependency and unit-policy
cases above.

This is a `partial` support-library review. Existing targeted tests show active
integration, but `uibcdf/molsysmt#155` still tracks the PyUnitWizard fast-path
audit, and `uibcdf/molsysmt#236` tracks warning reconstruction against SMonitor
0.16. The Python 3.14 published-installation claim belongs to
`uibcdf/molsysmt#237`. These open boundaries need explicit decisions or tests
before calling the member review adopted; the dependency list alone is not
enough.

## Hosted checkpoint for source commit de9e9c9

The [bundled data integrity run](https://github.com/uibcdf/molsysmt/actions/runs/36105299656)
passed. Its native log confirms published PyPI `pytest-receptor==1.1.0` and
the curated `--receptor=ci` command, with one test passed. The
[developer-guide run](https://github.com/uibcdf/molsysmt/actions/runs/36105299549)
passed. GH Run Receptor inspected both. The smoke run `36105275404` was
cancelled during the test step, so it supplies no successful test conclusion.
The [weekly run](https://github.com/uibcdf/molsysmt/actions/runs/36105275495)
failed in all three Python cells, and the
[six-cell full matrix](https://github.com/uibcdf/molsysmt/actions/runs/36105299602)
failed in all six cells. Each failing job reached its full pytest step.
The Python 3.12 Ubuntu matrix log confirms `pytest-receptor 1.1.0 py_1` from
`uibcdf` and a native pytest exit status of 1, preserved in receptor's
`FAIL exit=1` report. In both workflows, three assertions in
`tests/cross_repo/test_unit_policy_authority.py` fail: import order does not
produce one shared unit policy, and importing MolSysViewer resets a user's
chosen unit. The receptor did not report a rendering error. The same full
matrix passed on separate source revision `8d58581` with newer controlled
SMonitor, ArgDigest, and MolSysViewer revisions; this comparison suggests an
outdated controlled source set at `de9e9c9`, but does not isolate one
package as the sole cause. This member review keeps developer tools `partial`
until the ordinary test gate passes on the exact integrated revision. The
controlled-source update also had to coordinate with the Python 3.14 transition in
`uibcdf/molsysmt#237` and `uibcdf/molsyssuite#29`.

## Later main integration

After the failed `de9e9c9` runs, MolSysMT merged candidate `89ceda0ad` into
`main`. This merge contains the later controlled source revisions and the
authorized Python 3.14 metadata; the earlier failing runs remain evidence
about `de9e9c9`, not a conclusion about the merged `main`. On the merged
checkout, the MolSysSuite repository checker passed, and the focused
`tests/cross_repo/test_unit_policy_authority.py` selector passed six tests
locally with `--receptor=llm`. The developer-guide validator and Ruff check
also passed. The earlier candidate `e28ceb9ea` passed the six-cell full
matrix in run `36120923064` with controlled MolSysViewer commit
`cf427942d0b08a1c5c60f262c6a6b33f248d6f8b`, but that branch had not yet
merged this review's receptor 1.1.0 pins. The merged `main` advanced to
`6a334cc3e` with a Conda validation change. Its exact-commit full matrix was
dispatched as run `36132035176` using the same controlled Viewer commit. In
its first attempt, the macOS/Python 3.11 cell stopped while building the
editable MolSysMT package: rustup reported that `rustc` was absent from the
runner's `1.97.1-aarch64-apple-darwin` toolchain. That cell did not reach
pytest, so it provides no evidence about the receptor or the unit policy.
The other five test cells were still running at this checkpoint. The
developer-tools review remains `partial` until an integrated full gate passes.

## S5 reconciliation — 2026-10-06

The current central source at `0448098` and synchronized policy-v1.5.7 guide
require routine Python 3.14, weekly Linux 3.11–3.14, and recurring macOS arm64.
The workflow migration under #237 implements those cells and preserves the
bounded direct-push selection owned by #185. Configured routes are not executed
admission evidence. The new eight-cell full source matrix and installed candidate
closure remain mandatory before closing this review or claiming 3.14 support.

S5 passes 89 focused dependency/matrix/provenance/unit-policy/argument-contract
checks. The current unit-policy and converter-table tests pass locally; that does
not erase their old hosted failures or qualify the controlled installed pair.
All 14 fast gates pass. Actual effective support distributions and test-tree hashes
are retained in the [scoped artifact](../../devtools/data/stabilization_s5_20261006.json).
The local tests in that first selection used receptor's `ci` rendering; this
records the actual command rather than relabelling it as `llm`. Hosted gates
continue to use the declared published receptor 1.1.0.

#236 is resolved with a guard against duplicate SMonitor warning reconstruction;
it is not an open adoption blocker. #155 remains a performance optimization
review, deferred by the scope freeze; it does not permit skipping public unit
validation or introducing an unreviewed runtime exception. S2 already completed
Interactions' public ArgDigest boundary under #252. Broader installed/public
closure and the full integrated test gate still require exact-candidate evidence.

The independent automatic coverage producer `37328009946` used receptor 1.1.0,
retained real failures and published a processed report. Reporting closure #286
does not mean the full matrix passed: the Python 3.13 job has 11 failed tests.
Its older source and a second later run's larger failure set must be compared with
the current tree under #237/#334 before S6. No gate is weakened and no new
support-library or developer-tool exception is granted.

A separate fresh `--receptor=llm` support/presentation selection passes 68 cases
in 4.00 seconds without warnings, including the #236 reconstruction guard,
quantity digesters, SMonitor contracts and the OpenFF dependency contract.
This is scoped boundary evidence, not the full installed candidate closure.

## Complete shared development execution — 2026-10-06

The [shared-environment receipt](../../devtools/data/stabilization_s5_shared_20261006.json)
records the clean MolSysMT source `5e2721691`, released SMonitor 0.18.0,
DepDigest 0.13.0, ArgDigest 0.13.0 and PyUnitWizard 0.28.1 from exact controlled
sources. The complete Python 3.14 suite passes 13,313 cases with two explicit
skips, no failures/errors and 1,763 warnings. The independent registered
scientific gate passes all 54 cases from 47 nodes without skips. The complete
suite and recovery use twelve workers and receptor's local `llm` profile; the
scientific certificate runner is serial by design.

The actual shared plugin is editable pytest-receptor `1.1.0+19.g6d87a24`,
whereas hosted recipes continue to declare published 1.1.0. Viewer and Ackredit
are editable siblings, and Viewer changed concurrently during this development
checkpoint. Preserve those limits rather than presenting this as the exact
controlled-source or installed release gate. This materially advances the
integrated runtime review, but the new eight-cell matrix, installed closure and
central adoption remain pending. No historical failed gate is erased and no
support-library exception is introduced.

## Required closure correction and complete execution — 2026-10-06

#344 identifies a limitation in the earlier successful source checks: installed
PyUnitWizard 0.28.1 requires ArgDigest >=0.14.0, so the former 0.13.0 pin does
not establish a coherent runtime closure. The corrected pin is published
ArgDigest 0.14.0 at `0fa776af2d271065c60727c28480b20c3ce09aee`. Both controlled
and installed public gates now recursively inspect actual dependency metadata.
Earlier execution counts remain valid development observations.

At clean `865ff6ec6`, the complete shared Python 3.14 suite using that closure
passes 13,313 cases with two skips, no failures/errors and 1,770 warnings in
404.84 s (twelve workers, receptor `llm`). The independent scientific runner
passes 54 cases from 47 nodes without skips in 6.94 s. Editable sibling limits
remain; these runs do not identify a final immutable Viewer candidate.

All four installed public wheel smokes pass on Python 3.11–3.14, using published
Viewer baseline `cf427942d0b08a1c5c60f262c6a6b33f248d6f8b`. Wheel run
[37438849560](https://github.com/uibcdf/molsysmt/actions/runs/37438849560) still
concludes **failure** because Rust formatting rejects one import ordering.
Clippy, Rust tests and cargo-deny remain unexecuted in that run; the formatting
correction requires a new exact-source workflow. The
[execution receipt](../../devtools/data/wheel_execution_20261006.json) retains
these outcomes and five artifact identities. This is successful installed
dependency evidence, not complete 1.0 qualification or central admission.

The separate corrected-source wheel run
[37441629705](https://github.com/uibcdf/molsysmt/actions/runs/37441629705)
concludes success on `5bd893c85`: all thirty applicable jobs pass, including
format, Clippy, 81 Rust tests, cargo-deny and every installed public smoke.
The original failed run remains recorded. The
[corrected receipt](../../devtools/data/wheel_corrected_execution_20261006.json)
retains all five artifact identities and independently hashed files.
Source run [37441978743](https://github.com/uibcdf/molsysmt/actions/runs/37441978743)
passes the 54-case scientific certificate without skips in all eight cells;
its full suites are still executing. No final current Viewer agreement,
Conda installed-pair qualification or publication is inferred.

## Corrected delivered source-pair checkpoint — 2026-10-06

The original source run `37441978743` finishes with six failures, each only
at the complete-copy comparison test. #345 reproduces matching undefined
metadata comparing unequal under pandas 3 and corrects that numeric branch.
The original failed evidence remains preserved.

With clean MolSysMT `bb4781c5ae0b725d0c904cfd8bae1f44a1b13123` and delivered
Viewer `c046fca173f501c6e259761ef8f3d6b1825f17e8`, source run
[37449282864](https://github.com/uibcdf/molsysmt/actions/runs/37449282864)
passes all eight Linux/macOS Python 3.11–3.14 full cells. Each Linux cell passes
13,290 cases with 26 skips, and each macOS cell passes 13,289 with 27 skips;
all have 40 deselections. All eight scientific certificates pass 54 cases with
zero skips. Hosted pytest executes serially. Wheel run
[37449284817](https://github.com/uibcdf/molsysmt/actions/runs/37449284817)
passes all thirty applicable jobs, including the four installed public smokes,
81 Rust tests and platform/runtime checks, with one expected PR-only skip.

The [pair receipt](../../devtools/data/stabilization_s6_pair_20261006.json)
retains job/file identities, hashes and actual omission nodes/reasons. The
maintainer selects 0.23.0 as the next pre-1.0 package checkpoint while retaining
the feature freeze. Development artifacts above do not certify 0.23.0 packages,
central admission or final Conda/consumer-installed qualification. Select and
qualify the exact 0.23.0 producer and paired Viewer package version next.
