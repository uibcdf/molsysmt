---
summary: OpenMM system conversion ignores the requested constraint policy.
issue: uibcdf/molsysmt#581
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [api, convert]
guard: tests/form/openmm_Topology/test_implicit_solvent.py::test_constraint_policy_matches_the_requested_physical_constraints
normative:
blocked_by: []
supersedes: []
---

# Requested physical constraint policy is ignored

## What and how

The OpenMM topology adapter always passed `constraints=app.HBonds` to
ForceField.createSystem, ignoring its public constraints argument. The original
adapter body at `d2c0882ede355e475a3b8f8a6e618d5021d01ba1` confirms the mechanism.
The general convert boundary additionally refused explicit None, despite the
adapter admitting it. String 'none' was accepted but ignored.

This surfaced while checking #580 against a frozen, unconstrained upstream
OBC1 force reference. All seven OBC1 resource repairs were correct, but the
reference force comparison differed at bonds involving hydrogen. OpenMM omits
stretch terms for constrained bonds by default; these are different physical
configurations, not grounds to relax a numerical tolerance.

## Intended outcome

Retain the default 'hbonds'. Translate engine-neutral policies None/'none',
'hbonds', 'all bonds' and 'h angles' inside the OpenMM adapter and reject unknown
policies. The public conversion boundary should admit explicit None without
broadening unrelated callers. Retain stored settings and explicit override
precedence from the shared conversion resolution boundary.

Guard actual constraint pairs/distances against direct engine construction,
including no constraints, and keep the default unchanged. The frozen #580
reference must be tested with its original unconstrained configuration and
original force tolerances. No new constrained dynamics implementation is added.

## Provenance

2026-11-05, Linux/Python 3.14.7/OpenMM 8.6.1. Base
`d2c0882ede355e475a3b8f8a6e618d5021d01ba1`, plus the #580 working patch.
A short diagnostic process overlapped the repair and observed the repaired
counts 0/12/21 for none/hbonds/all bonds; those are not presented as the red
baseline. Baseline evidence is the literal hard-coded HBonds call and the
failed frozen reference comparison before correcting that call. Related
consumer: #421 / PR #543 and uibcdf/molsysviewer#264.

## Resolution — 2026-11-05

Physical constraint names are translated in the OpenMM adapter. None and 'none'
request no constraints; 'hbonds' retains its prior default; 'all bonds' and
'h angles' select their actual engine controls. Unknown policies raise a native
choice diagnostic before force-field construction. The public convert boundary
admits explicit None for this argument without loosening unrelated callers.

The guard compares every returned constraint pair and distance with a direct
engine construction for five accepted policy spellings. A separate rejection
control catches unknown policies. The #580 frozen force-reference test now uses
its actual unconstrained recipe rather than altering numerical tolerances.
Receiving: 1,817 affected tests, 234 published-support-floor controls and 570
documentation/doctest controls, with overlapping suites. The shared
[receipt](../../../devtools/data/implicit_solvent_receiving_580_581_20261105.json)
and [model record](amber14_obc1_conversion_omits_implicit_solvent_force.md)
retain complete scope and evidence. No constraint integrator or new dynamics
algorithm is implemented. Public signatures and default HBonds behavior remain.
