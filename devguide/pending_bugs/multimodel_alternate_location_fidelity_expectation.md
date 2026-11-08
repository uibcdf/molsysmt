---
summary: Reconcile multi-model alternate-location fidelity with stable-ID preflight.
issue: uibcdf/molsysmt#612
status: active
opened: 2026-11-06
closed:
severity: medium
verification: reproduced
area: [build, convert, tests, molsysviewer]
guard: tests/conversion_truth/test_pdb_fidelity.py::test_pdb_multimodel_alternate_locations_share_a_canonical_atom_axis
normative:
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

The [receiving record](../../devtools/data/alternate_location_owner_receiving_612_20261107.json)
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
[related owner receipt](../../devtools/data/group_naming_owner_receiving_549_20261107.json)
retains its command and measured controls alongside #549's scoped receiving.
The private selector error and protected stop during that receiving are
separate from the maintainer-terminated original attempt recorded above.

#549 is now source-accepted and closed. #612 remains active until its complete
exact-source gate is met. Any next attempt must use an explicitly inspected
serial command and bounded resources; the successful small campaigns do not
establish the complete suite's peak requirements. Other incoming/API work can
proceed independently without relabelling this gate.
