---
summary: Reconcile multi-model alternate-location fidelity with stable-ID preflight.
issue: uibcdf/molsysmt#612
status: open
opened: 2026-11-06
closed:
severity: medium
verification: reproduced
area: [build, convert, tests, molsysviewer]
guard:
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
