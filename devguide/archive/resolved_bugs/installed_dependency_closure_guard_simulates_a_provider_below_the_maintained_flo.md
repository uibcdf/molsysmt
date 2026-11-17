---
summary: Installed dependency closure guard simulates a provider below the maintained floor
issue: uibcdf/molsysmt#771
status: resolved
opened: 2026-11-17
closed: 2026-11-17
severity: medium
verification: reproduced
area: [tests, ci]
guard: devtools/tests/test_installed_runtime_dependencies.py::test_controlled_gate_rejects_transitive_conflict_above_direct_floor
normative:
blocked_by: []
supersedes: []
---

# Dependency guard fixtures retain an obsolete provider version

**Reported:** 2026-11-17, by the finite #334 offline qualification preflight.
**Status:** resolved; expanded offline controls pass without relaxing production requirements.

## What

Two positive controls simulate PyUnitWizard 0.28.1 while the maintained direct
runtime floor is 0.29.2. `test_controlled_gate_rejects_transitive_conflict_above_direct_floor`
therefore still fails after correcting its simulated ArgDigest conflict. The
separate actual-contract CLI fixture fails before its intended rejection check.

## How

`devtools/tests/test_installed_runtime_dependencies.py` combines a transitive
closure scenario with current source metadata. The direct PyUnitWizard refusal
is correct, but it prevents the test from isolating its intended mechanism.
`test_validate_controlled_dependencies.py` also retains the old positive fixture.

The transitive scenario now owns a minimal temporary project and exact-shaped
controlled pins. Both direct requirements are satisfied first; the single
captured refusal must identify the transitive conflict. Correcting only that
conflict then passes. The separate real-project fixture uses the actual admitted
0.29.2 provider version and still rejects the incompatible ArgDigest version.
Production dependency requirements, controlled-source parsing and validators
remain unchanged.

## Why

A release/preflight regression test must distinguish actual incompatibility from
an obsolete simulated positive environment. Removing closure checks or reducing
the public provider minimum would disguise the failure rather than fix it.

## Evidence and exclusions

The first offline batch records 45 passing cases and this transitive-control
failure. The second original-fixture run records three passes and the independent
actual-contract failure. Both native nonzero exits remain in the
[finite receiving record](../../../devtools/data/independent_native_work_334_20261116.json).
The corrected expanded batch passes 159 cases with zero skips, including direct
floor, source-pin, runtime closure, staging identity, citation and native-example
controls. These are offline tests with simulated package records, not evidence
of a clean installed candidate or permission to build/publish one.

## Acceptance

- The transitive refusal is the exact captured cause after direct floors pass.
- Correcting that conflict alone returns zero.
- The real-project positive fixture satisfies the actual current requirements;
  its deliberate incompatible version still returns nonzero.
- Existing staging identity, closure/markers/extras and artifact guards remain
  passing, with original failed runs retained.
