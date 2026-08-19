---
summary: No test workflow runs on a push to main and the CI badge names a missing workflow.
issue: uibcdf/molsysmt#185
status: open
opened: 2026-08-19
closed:
severity: high
verification: measured
area: [ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Bug: `main` accumulates untested commits, and the badge says otherwise

**Reported:** 2026-08-19, during an external audit, while establishing how
[#182](https://github.com/uibcdf/molsysmt/issues/182) survived a commit and a day.
**Status:** open. Measured on `b9a2098e4` against the live run history.

## What

Three facts, each checkable, that compose into one:

**No test has run against `main` for 109 commits.** The last executed `CI smoke` run is
`0977aa3c3`, 2026-08-17 01:05.

```bash
$ git rev-list --count 0977aa3c3..HEAD
109
$ for c in $(git rev-list 0977aa3c3..HEAD); do
      git log -1 --format=%B $c | grep -q 'skip ci' && echo skip; done | wc -l
107
```

The two commits without `[skip ci]` touched only `devguide/`, which `ci-smoke.yaml`
lists under `paths-ignore`. So every commit in that range was excluded, by one mechanism
or the other, from the only test workflow a push can start.

**The exclusion is policy, not accident.** [`AGENTS.md`](../../AGENTS.md) requires
`[skip ci]` in every commit message unless explicitly instructed otherwise, and
`ci-smoke.yaml` skips when the head commit message contains it:

```bash
$ n=0; s=0
$ while read -r c; do n=$((n+1));
      git log -1 --format=%B "$c" | grep -q 'skip ci' && s=$((s+1)); done < <(git log -100 --format=%H)
$ echo "$s of $n"
100 of 100
```

**The badge names a workflow that no longer exists.** `README.md` renders
`actions/workflows/CI.yaml/badge.svg`. There is no `CI.yaml`:

```bash
$ ls .github/workflows/CI.yaml
ls: cannot access '.github/workflows/CI.yaml': No such file or directory
```

The workflow named `CI` last ran on 2025-11-21, on the last pull request the repository
received.

## How

The trigger matrix, read from `.github/workflows/`:

| workflow | trigger | reaches a push to `main`? |
|---|---|---|
| `ci-smoke.yaml` | push, pull_request | yes, unless `[skip ci]` or an ignored path |
| `ruff.yaml` | push, pull_request | yes — lint only |
| `ci-devguide.yaml` | push on `devguide/**` and named validators | yes — document integrity only |
| `ci-weekly.yaml` | schedule, Monday 09:00 | no; up to seven days later |
| `ci-full.yaml` | workflow_dispatch | no |
| `test_import.yaml` | workflow_dispatch | no |
| `benchmarks.yml` | pull_request, workflow_dispatch | no |
| `ci-rust-wheels.yaml` | pull_request, workflow_dispatch | no |

Development is direct to `main`; the last `pull_request` event of any kind was
2025-11-21. So the two `pull_request`-only workflows have not fired from their own
trigger in nine months, and everything else that is not `ci-smoke`, `ruff` or
`ci-devguide` is manual or weekly.

**The release gate is inside the manual branch.** `devtools/scripts/release_gate.py`
aggregates twelve validators, including `validate_demo_assets.py`, and runs only in
`ci-full.yaml`. That is why the truncated artifact in
[#182](https://github.com/uibcdf/molsysmt/issues/182) reached `main` past a gate that
detects it exactly.

**The weekly signal is red and has been for three weeks.**

| run | date | outcome |
|---|---|---|
| `32016849113` | 2026-08-17 | 3 failed, 9989 passed, on 3.11, 3.12 and 3.13 — the cross-repo unit-policy tests |
| `31378634895` | 2026-08-10 | failed in `Setup conda env` |
| `30813688402` | 2026-08-03 | failed in `Setup conda env` |

Two of the three never reached the suite at all. A signal that is red for infrastructure
reasons stops being read, which is how the third one — a real failure — arrives already
discounted.

## Why

**The verification apparatus is not connected to the act of committing.** The repository
carries a stability registry, a form-adapter delivery gate, a scientific evidence
registry, a demo-asset manifest and a twelve-validator release gate. On a push, three of
those run and none of them executes a test. The gap between what the project can check
and what it does check on each change is the whole finding; #182 is one instance of it.

**The badge makes a claim the repository does not support.** A reader arriving from the
paper sees a CI badge on the front page. It points at a workflow that was deleted, so it
reports on nothing, and the project's actual continuous signal — weekly, currently red —
is not shown anywhere.

**Detection latency sets the cost of a defect, not its severity.** A bad commit found in
minutes is a fix; found on the following Monday under a week of commits, it is a bisect.
The 109-commit gap is the current worst case and it is the normal case, not an outlier.

Severity is `high`: nothing is scientifically wrong because of this on its own, but it is
the mechanism that lets everything else through, and the project is at F6, one commit
from a 1.0 tag.

## What is measured and what is assumed

Measured: the 109-commit gap and its composition; 100 of the last 100 commits carrying
`[skip ci]`; the trigger of every workflow; the absence of `CI.yaml`; the last
`pull_request` event; the three weekly outcomes and the failing step of each; the
membership of `validate_demo_assets.py` in `release_gate.py` and of `release_gate.py` in
`ci-full.yaml` alone.

Assumed: nothing load-bearing. The reason `[skip ci]` became universal is not recorded
here and matters to the fix — [#123](https://github.com/uibcdf/molsysmt/issues/123),
opened 2025-11-10, asked for the skip mechanism, and the run history is consistent with a
runner-cost or noise motive, but the audit did not establish it.

## What was refuted

*No CI runs at all.* Wrong, and worth stating because it was the audit's first reading.
`Ruff` and `Developer guide integrity` run on nearly every push and pass; `CI smoke` ran
on 2026-08-12 through 08-17 on the commits that omitted `[skip ci]`; the weekly job runs
the full suite plus the scientific-truth gate. The defect is that the test signal is
opt-out by default and the default is exercised.

*The weekly job makes the push gap harmless.* It has failed for three consecutive weeks,
twice before reaching the suite. A safety net that has not caught anything in three weeks
is not measurably a safety net.

## Scope and exclusions

Covers the trigger policy for tests on `main`, the badge, and the placement of the
release gate relative to the push path.

Excludes the content of any suite, and excludes the currently failing cross-repo
unit-policy tests, whose theme is
[`../pending_proposals/pyunitwizard_global_standards_conflict.md`](../pending_proposals/pyunitwizard_global_standards_conflict.md).
Excludes the reliability of the benchmark comparison, which is
[`../pending_proposals/benchmark_regression_gate_reliability.md`](../pending_proposals/benchmark_regression_gate_reliability.md).

## Acceptance criteria

1. A push to `main` that changes anything under `molsysmt/` or `tests/` runs at least the
   smoke suite, whatever the commit message says. `[skip ci]` may keep suppressing runs
   for documentation-only changes; it may not suppress them for source changes.
2. A push that changes anything under `molsysmt/data/` runs `validate_demo_assets.py`.
3. The README badge points at a workflow that exists and reports the signal a reader
   would assume it reports.
4. The weekly run is green, or its failure is tracked by an open entry naming it.
5. A test asserts that the workflow whose badge the README renders exists in
   `.github/workflows/`. This is the `guard`, and it is the one part of this entry a test
   can hold.

## Dependencies and risks

Re-enabling per-push tests raises runner usage, which is the pressure `[skip ci]` was
introduced to relieve. The smoke tier is minutes; the cost is bounded by keeping the full
matrix manual and weekly, which this entry does not propose changing.

## Provenance

Measured 2026-08-19 against the live GitHub Actions history via `gh`, at repository
commit `b9a2098e4`. Run identifiers are recorded above so the outcomes remain checkable
after the history scrolls.
