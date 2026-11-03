---
summary: Developer-guide CI times out fetching full history before running validators.
issue: uibcdf/molsysmt#536
status: resolved
opened: 2026-11-03
closed: 2026-11-03
severity: medium
verification: reproduced
area: [ci, tests]
guard: devtools/tests/test_devguide_workflow.py::test_full_history_devguide_job_has_bounded_budget_and_retains_integrity_gates
normative:
blocked_by: []
supersedes: []
---

# The integrity job exhausts its budget before validation

**Reported:** verification of the documentation-only #532 closeout.
**Status:** bounded budget correction and exact-head hosted recovery qualified.

## What and how

Run [41680061695](https://github.com/uibcdf/molsysmt/actions/runs/41680061695)
on 27c6bd3c0b4adfc1b7c3b635b9f30bcf6ffa0cab cancelled twice in full-history
`actions/checkout@v7`. Jobs 126071031623 and 126076905510 did not execute any
validator. Attempt 2's authoritative check annotation states that the job
exceeded its maximum execution time of 5m0s. Its fetch ran from 17:22:40 UTC
until cancellation at 17:27:36 UTC; cleanup finished at 17:27:38 UTC.

The original scientific source CI remains successful under #532. Both failed
administrative attempts and native job logs are retained rather than counted
as passing checks. All five validation commands pass locally on that documentation
source, including Git archive restoration and API baseline comparison; that does
not claim their hosted execution.

## Why

The integrity gate cannot protect developer records, retained experiments,
scientific declarations or API transitions if it cannot finish checkout.
Incremental archive restoration requires real ancestry and borrowed Git objects;
silently making this a shallow clone would weaken its intent.

## Bounded correction and guard

Allow 15 minutes for the entire job, retaining full history, Python setup, all
four integrity validators and the push/PR API baseline check. This is a bounded
recovery, not a measured speed improvement or a change to the scientific suite.

`devtools/tests/test_devguide_workflow.py` rejects the original insufficient
five-minute budget and protects bounded time, full ancestry, mandatory validator
commands, absence of skip/failure suppression and both API baseline sources.
Its original-budget run fails, exit 1. The corrected guard passes in the local
2,818-case selection. A static budget assertion alone does not prove checkout
or validation succeeded; the hosted execution below supplies that evidence.

## Evidence and limits

Local Git packed objects occupy about 507 MiB on 2026-11-03. This is a local
inventory measurement, not hosted transfer throughput or a complete estimate
of future execution time. Original checkout failure, annotations and receptor
evidence are retained in ignored task caches. No history, tag or artifact is
rewritten; no validator is dropped, shallow fallback introduced or test assertion
relaxed. Broader historical-object cleanup remains separate future work.

## Exact-source hosted recovery — 2026-11-03

Source **d8ea626a0ab6dbd976d0e04ad9299019e4ae0a42** passes
[Developer guide integrity run 41687790369](https://github.com/uibcdf/molsysmt/actions/runs/41687790369),
job 126098035521. All four integrity validators and the API baseline comparison
execute and succeed after the full-history checkout. The job runs from
17:51:06 to 17:54:42 UTC. GH Run Receptor's metadata watch terminates with
GitHub `conclusion=success` and exit 0; the native job log retains the individual
commands and step results.

Checkout takes 209 seconds in this successful attempt, below the old five-minute
budget. This demonstrates successful recovery with every gate retained; it
does not show that increasing the budget accelerated checkout or that every
future attempt requires more than five minutes. The original two five-minute
timeouts remain failed administrative evidence. This change provides bounded
headroom for the observed variability without relaxing validation.
