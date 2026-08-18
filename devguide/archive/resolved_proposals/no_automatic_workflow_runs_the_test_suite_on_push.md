---
summary: No automatic workflow runs the test suite on push
issue: uibcdf/molsysmt#171
status: resolved
opened: 2026-08-18
closed: 2026-08-18
verification: measured
area: [ci, tests]
guard:
normative: devguide/release_gate.md
blocked_by: []
supersedes: []
---

# Nothing runs the suite between one weekly job and a manual dispatch

**Reported:** 2026-08-18. A regression sat on `origin/main` for a full day. The one
job that detected it — `CI weekly` — had already failed on 2026-08-17 and nobody
read it.
**Status:** open proposal.

## What

No workflow runs the pytest suite in response to a push. The full matrix runs only
when a human asks for it.

```bash
$ for f in .github/workflows/*.y*ml; do ... done
benchmarks.yml                        pull_request, workflow_dispatch
build_and_upload_conda_packages.yaml  release, workflow_dispatch
ci-devguide.yaml                      push, pull_request, workflow_dispatch
ci-full.yaml                          workflow_dispatch
ci-rust-wheels.yaml                   workflow_dispatch, pull_request
ci-smoke.yaml                         push, pull_request, workflow_dispatch
ci-weekly.yaml                        schedule, workflow_dispatch
ruff.yaml                             push, pull_request, workflow_dispatch
```

Three workflows react to a push: `ci-smoke`, `ci-devguide` and `ruff`. None of them
runs the suite. `ci-full.yaml`, which does, is `workflow_dispatch` only.

This compounds with the project's commit convention. Every commit carries
`[skip ci]` by default, so even the three push workflows usually do not run. The
last full matrix on record is the F5 candidate `38ab61f6e`.

## How

Two independent gaps, and the second is the one that matters:

**The trigger.** `ci-full.yaml` line 9-10 declares `on: workflow_dispatch:` and
nothing else. A green matrix is therefore never a consequence of pushing; it is
always a deliberate act.

**The fast gate does not stand in for it.** `devtools/scripts/release_gate.py`
returned **13/13 PASS** on a tree with 185 failing tests. It validates the stability
registry, form-adapter delivery contracts, Tier 1 conversion fidelity, the devguide,
the course, demo assets, citation metadata and Rust hot paths, and then runs a
five-line smoke: import, `get_form`, `get`, `convert`, `select`, `get_center`. That
smoke passes on a package whose element helpers have lost half their parameters.

The result is a green signal that reads as "the code works" and means "the
registries agree".

## Why

The 2026-08-18 regression is the worked example. `93171c547` landed with
`[skip ci]`, no push workflow ran, the fast gate said 13/13, and `main` carried
`195 failed, 30 errors` for a day. `CI weekly` failed on schedule and produced no
action, because a scheduled failure has no author watching for it.

This also has a direct bearing on 1.0. `devguide/release_gate.md` requires a green
`ci-full` matrix **on the exact committed tag candidate**. With `[skip ci]`
universal and `ci-full` manual, that requirement can only ever be met by remembering
to dispatch it by hand — which is precisely the kind of step that is skipped under
release pressure.

## What is measured and what is assumed

Measured, on this checkout:

- Workflow triggers, from parsing the `on:` block of all 11 files in
  `.github/workflows/` (table above).
- `release_gate.py` printed `Fast gates: 13/13 passed` on a tree where
  `pytest -n 14 --dist loadfile` returned `185 failed, 33 errors`.
- Latest recorded runs before 2026-08-18: `CI weekly` failure on 2026-08-17T09:45,
  `Developer guide integrity` failure twice on 2026-08-17T07:4x, `CI smoke` and
  `Ruff` success on `0977aa3c3`.
- Suite cost locally: 9991 tests in ~350 s wall clock with `-n 14`.

Assumed:

- That the local wall clock is indicative of runner cost. A GitHub runner has fewer
  cores than the 14 used here, so the real figure is higher — this is an estimate,
  not a measurement.
- That `[skip ci]` is applied by convention rather than enforced. It is a stated
  preference, not a hook.

## What was refuted

*Omitting `[skip ci]` on an important commit is enough to get the matrix to run.*
It is not, and this was believed during the session that produced this report:
`ci-full` has no `push` trigger, so the marker is irrelevant to it. Dropping the
marker buys `ci-smoke`, `ci-devguide` and `ruff` — none of which runs a test.

*The fast release gate covers this.* It does not, by design; it is explicit that a
heavy gate is still required. The problem is not that it lies, it is that 13/13 is
read as more than it claims.

## Scope and exclusions

Covers what should run automatically, and on what.

Excludes the `[skip ci]` convention itself, which exists for good reasons on
documentation-only commits and is the maintainer's call.

Excludes the cost question — whether the full matrix on every push is affordable is
exactly what the options below trade against, and it needs a runner-minutes budget
this report does not have.

## Options

Three, not exclusive:

1. **A push-triggered suite job on a single platform.** One runner, one Python
   version, the whole suite. Catches everything this regression was, at roughly a
   sixth of the matrix cost. The matrix stays manual for release candidates.
2. **Make the fast gate honest about its scope.** Have `release_gate.py` print, next
   to `13/13`, the date and commit of the last suite run it knows about — so a stale
   or absent one is visible at the moment someone reads the green.
3. **Route the weekly failure somewhere with an owner.** A scheduled job that fails
   into an empty room is not a signal. Opening or updating an issue on failure would
   have surfaced this on 2026-08-17.

Option 1 is the one that would have prevented the incident; option 3 is the one that
would have shortened it from a day to an hour.

## Acceptance criteria

- A commit that breaks the suite cannot reach `origin/main` without an automatic,
  attributable failure signal. Names the `guard` field once the mechanism is chosen.
- `release_gate.md` states plainly that the fast portion does not execute the suite,
  and what the green does and does not mean. Names the `normative` field.

## Dependencies and risks

Related: [uibcdf/molsysmt#169](https://github.com/uibcdf/molsysmt/issues/169), the
regression that motivated this, and
[uibcdf/molsysmt#170](https://github.com/uibcdf/molsysmt/issues/170), the linter
blind spot that let its first symptom through.

Risk of option 1: a slow required check on every push is the kind of friction that
gets bypassed. Keeping it to one platform and one Python version is what keeps it
tolerable.

## Provenance

Host: this development checkout, molsysmt at
`51102b03e` and `e7f2e8ce9`. Python 3.13.14, `gh` against `uibcdf/molsysmt`.
2026-08-18.
