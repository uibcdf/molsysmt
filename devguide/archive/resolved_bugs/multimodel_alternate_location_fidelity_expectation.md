---
summary: Reconcile multi-model alternate-location fidelity with stable-ID preflight.
issue: uibcdf/molsysmt#612
status: resolved
opened: 2026-11-06
closed: 2026-11-08
severity: medium
verification: reproduced
area: [build, convert, tests, molsysviewer]
guard: tests/conversion_truth/test_pdb_fidelity.py::test_pdb_multimodel_alternate_locations_share_a_canonical_atom_axis
normative: devguide/testing_strategy.md
blocked_by: []
supersedes: []
---

# Multi-model alternate-location fidelity and stable IDs

## What

The PDB fidelity test expects occupancy winners A and B in two structures of one
canonical atom axis, although those observations have different global atom IDs.
The current native whole-request preflight rejects that inconsistent assignment.
The scientific label contract and the test expectation need owner reconciliation;
this does not establish that the safety guard is a product defect.

## How

On native ed09f64539a5af6c1dbe9bd352c7ef65dcd4a7a6, independently of Viewer:

```bash
python -m pytest --receptor=llm tests/conversion_truth/test_pdb_fidelity.py::test_pdb_multimodel_alternate_locations_share_a_canonical_atom_axis
```

The one case fails in 1.07 s. Both structures contain CA/A with serial 1 and
CA/B with serial 2. Occupancy selects A in the first structure and B in the
second. `solve_atoms_with_alternate_location` rejects the different stable IDs
before publication, at its native request-planning boundary.

The same failure occurs in Python 3.13 job 127885168430 of source matrix
42215709260, contribution 699fc69be57ac0e89f9bced3fd4f39139ccabf38. That cell
has 33 failures, 29,192 passes, 112 skips and 40 deselections; it is not green.
Other failure mechanisms remain under #594–#598. This report does not claim to
diagnose or fix them.

## Why

An accepted stable-label safety condition must agree with canonical-axis fidelity
tests. This is a follow-up to closed #571's whole-request atomicity contract,
not a request to restore partial mutation. It affects full qualification of the
tools addon under #421 / PR #543 and uibcdf/molsysviewer#264.

## Acceptance

Decide the supported multi-model stable-ID semantics. Protect valid canonical-axis
resolution and rejected conflicting IDs without relaxing atomicity. If the
fixture is stale, adjust only its inconsistent inputs or expectation and retain
coordinate, alternate-record and PDB round-trip coverage. Rerun the affected
native contract/fidelity cases and retain exact-head full-suite evidence. No
consumer classifier, ID substitution or downstream scientific workaround is added.

The complete 543-issue inventory and related alternate-location reports were
reviewed before opening this follow-up. No native repair or test change is
included in the reporting contribution.


## Owner acceptance review — 2026-11-07

Current main already contains the corrected fixture expectation from
`ab789897bad51a7258f366aadc01840895d6366e`. The stable-ID preflight is retained:
a single canonical atom axis cannot publish serial 1 in one structure and
serial 2 in another. An occupancy-based conflicting request must fail before
any primary coordinate or ID changes. Choosing A explicitly is valid across
both structures. No label substitution or consumer workaround is accepted.

The existing affected battery passes 103 cases, including five independent
pagination controls for #587. That overlapping scope is not the full source
suite required by this report. #587 is separately accepted and closed.

Owner receiving strengthens the existing PDB round-trip guard beyond shapes:
primary and alternate coordinates in nanometers, occupancies, B factors in
square nanometers, alternate labels and serials, and stable primary atom and
structure IDs are compared with the literal two-model fixture. Atomic rejection
and valid explicit-A resolution remain in the same test. Runtime code and the
scientific decision are unchanged.

The strengthened affected battery passes 103 cases (native exit 0). The
unmodified historical test body from `ed09f64539a5af6c1dbe9bd352c7ef65dcd4a7a6`,
executed as an isolated negative control against the current runtime, still
fails once at the stable-ID preflight (native exit 1). This preserves the
original disagreement rather than weakening the scientific safety boundary.

The strengthened guard is committed at
`2465d6b0cb137446f9917c971572a921003a9b89`. Fourteen fast gates also pass.
The complete default source suite was started on that clean commit with twelve
workers, without marker/path exclusions. The maintainer terminated the processes
after the shared machine exhausted RAM. The outer command exits 143; there is
no finalized JUnit or pytest outcome. Pytest Receptor's supported reader reports
an incomplete artifact and no final record. Its last rendered 6,344/31,719
threshold is not the final executed count. A teardown closed-channel error after
termination does not establish a Pytest Receptor or pytest defect.

Point observations fell from roughly 16 GiB available to 5.7 GiB on a 30 GiB
machine, with 8 GiB swap already used and twelve workers around 0.9–1.3 GiB RSS
each. These are not measured peaks or reserved resources. The execution should
have been stopped when shared-host pressure made that concurrency unsafe.

The [receiving record](../../../devtools/data/alternate_location_owner_receiving_612_20261107.json)
retains the passing focused controls, original negative control, interrupted
command, partial-artifact status and resource observations. Logs and partial
stream remain in private evidence; no completed result is invented. No heavy
retry is launched. Next: select a bounded execution route and measure a small
representative workload before choosing concurrency for the remaining exact-
source acceptance. Lack of safe capacity postpones this gate, not ordinary
lightweight development. #612 stays open; the joint #612/#587 milestone receives
no credit from this interrupted attempt. Local full-source evidence also does
not replace platform, installed-pair or final-candidate gates under #334.


## Bounded pilot follow-up — 2026-11-07

The original complete attempt remains interrupted, not passing. A new one-case
pilot on public source `3b16f23c5` passes under a verified 2 GiB process-tree
limit, one-CPU quota and zero swap; its peak is 292,397,056 bytes. This is a
sizing/control pilot, not complete-suite evidence. The
[related owner receipt](../../../devtools/data/group_naming_owner_receiving_549_20261107.json)
retains its command and measured controls alongside #549's scoped receiving.
The private selector error and protected stop during that receiving are
separate from the maintainer-terminated original attempt recorded above.

#549 is now source-accepted and closed. #612 remains active until its complete
exact-source gate is met. Any next attempt must use an explicitly inspected
serial command and bounded resources; the successful small campaigns do not
establish the complete suite's peak requirements. Other incoming/API work can
proceed independently without relabelling this gate.

## Measured concurrency and full-suite blockers — 2026-11-08

The maintainer requested measured use of shared resources beyond the one-CPU
pilot. The serial full attempt on `6205fcc78` is deliberately interrupted after
1,544 passes; it is not a passing full run. Four-worker/6-GiB receiving then
reaches a 128-task ceiling (160 blocked creations, peak memory 5,343,064,064
bytes), causing EAGAIN and thread-creation failures. It is stopped; final
pytest/Receptor evidence is incomplete, and ending Git metadata capture also
fails under task starvation. There is no OOM or host-reserve violation.

A controlled serial diagnosis proves six independent test defects and seven
passing formerly starved cases. #649/#650 correct only positive export fixtures
and test-package ownership. The corrected four-worker pilot on `a2993b8f0ec0bbf34b95966891f9b783f61dbe85`
passes 525 cases, peaks at 3,292,508,160 bytes and 32 tasks, with zero task-cap
or memory events. Rayon/BLAS/OpenMP/OpenMM environment defaults are one; explicit MolSysMT
per-call Rust pools retain their requested size. The finite task ceiling is 512. CPU remains four cores, memory 6 GiB max/5 GiB
high and zero swap. The maintainer sets the absolute shared-host reserve to
2 GiB; the controller stops 512 MiB above it. These observations do not reserve
resources or qualify the full suite. Preserve all three incomplete full attempts.

The [resource adjustment record](../../../devtools/data/source_suite_resource_adjustments_612_20261108.json)
retains actual attempts, stop evidence and limits; the
[fixture receipt](../../../devtools/data/conversion_fixture_receiving_649_650_20261108.json)
retains scoped correction evidence. Next receive the full exact-source suite
with the inspected thread-controlled route. #612 remains active.

## Further interrupted attempts and correction — 2026-11-08

The next four-worker 6-GiB attempt stops on the controller's global memory
pressure branch, with 7,306,313,728 bytes still available, peak process-tree
memory 5,454,446,592 bytes and 1,609 high-memory events. No max/OOM or task-cap
event occurs. Throttling coincides with global pressure; its sole cause is not
established. Final partial-stream review recovers 12,017 passing calls and
one stale placement-guard failure, now separately fixed under #651. The
stream has no session_finish. Earlier progress observations are not its final
outcome and must not be described as failure-free acceptance.

An eight-GiB attempt was started before that final review; it is deliberately
interrupted once the defect is recovered. Its 2,490 passes and exit 2 do not
complete the default 32,038-case scope. Peak memory is 3,991,306,240 bytes; no
memory/task limit event occurs. Preserve this premature restart and all prior
attempts in the resource receipt. #651's 598-case receiving fixes the discovered
example test; it does not complete this issue's acceptance.

The environment thread variables set defaults, not a hard one-thread guarantee
for explicit Rust pools. Inspection finds a cache keyed by requested pool size;
#652 records the bounded retention/overhead review without attributing all
observed threads to it or changing native behavior. The next fresh full run
uses four workers, four CPU equivalents, 8 GiB max/7 GiB high, zero swap and
512 tasks, with a 45-minute bound, a 2 GiB host reserve and monitored stopping
512 MiB above that floor or on global memory pressure. Source inputs remain
frozen for that run. Admission is not a reservation. #612 remains active.

## Resolution — 2026-11-08

The corrected fixture `ab789897bad51a7258f366aadc01840895d6366e` and
independent strengthened guard `2465d6b0cb137446f9917c971572a921003a9b89`
are accepted without relaxing stable-ID atomicity. Clean source
`03c59caef9823bbca186aa4213626ddc5eb890f3` completes the normal CPU-default
suite: 32,014 passes, 25 skips and no failures/errors over 32,039 cases.
All 8,555 tracked inputs and native bytes remain unchanged. Separately, all
23 Amber/LEaP omissions pass with the activated development tools, including
three independent construction oracles. Preserve both original counts; the
remaining SMILES-ambiguity/CuPy omissions are not silently removed.

The [full receipt](../../../devtools/data/full_source_receiving_612_20261108.json)
retains native exits, complete JUnit, the valid final Receptor counters and
explicitly truncated detail policy, versions, hashes and scope. Its
[resource history](../../../devtools/data/source_suite_resource_adjustments_612_20261108.json)
retains every earlier failed/interrupted campaign, the observed implicit GPU
allocation and the corrected CPU/default execution. Peak charged memory is
6,840,324,096 bytes; host availability never falls below 9,789,304,832 bytes.
No memory/task-limit or OOM event occurs. Initial PSI warnings are retained.

The [testing strategy](../../testing_strategy.md) explains explicit OpenMM CPU
selection independently of product defaults. This closes the owning source
acceptance only. It does not replace the platform, registered scientific,
installed-pair or final-candidate gates under #334, qualify GPU execution or
authorize publication.
