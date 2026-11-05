---
summary: Alternate-location occupancy selection can choose a lower-occupancy site
issue: uibcdf/molsysmt#569
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: high
verification: reproduced
area: [build, structure]
guard: tests/build/solve_atoms_with_alternate_location/test_alternate_location_contract.py::test_maximum_occupancy_only_prefers_a_when_it_shares_the_half_tie
normative:
blocked_by: []
supersedes: []
---

# Alternate-location occupancy selection can choose a lower-occupancy site

## What

The default maximum-occupancy route selects A=0.2 over B=0.5. Source order, an unequal A near the maximum, true half-occupancy ties and missing evidence need explicit controls.

## How

The old helper replaces the argmax with A whenever the maximum is close to 0.5, without checking that A shares that maximum.

## Why

A selected crystallographic observation differs from the documented criterion.

## Reproduction and acceptance

The new public regression module
`tests/build/solve_atoms_with_alternate_location/test_alternate_location_contract.py`
reproduces the reports with small native systems. After correcting two fixture
setup errors (the required Interactions method and its read-only mapping), the
original runtime fails 24 of 30 controls. The five existing real-system tests
are retained. The first repaired receiving passed all 35 cases; final receiving is recorded
below.

#571 owns shared staging; this report owns maximum and tie semantics. Public input stays form-agnostic. Preserve alternate records and
unselected observations, selected interaction coverage and physical units.
Prevalidate every selected site and quantity before delegation; invalid requests
must preserve coordinates, labels, occupancy, B factors and analysis identities.
Ordinary mutable backend failures retain their existing conservative coverage
policy; this is not crash-transactional file I/O.

## Provenance

Linux/Python 3.14.7, existing shared development environment, owner source
`d3650cc09735ccfc7bf02d35ca4e0a746f83f96f` plus the bounded local repair.
Pytest Receptor 1.2.1, two workers. Local XML is under
`.pytest_cache/alternate-locations-569-571/`: `reproduced-before.xml` and
`first-repair.xml`. Initial fixture setup errors are not scientific reproductions.
No new native binary, environment or dependency is produced.


## Resolution — 2026-11-05

The occupancy selector retains the finite argmax. A may replace that position
only when the maximum is close to 0.5 and A shares it within rtol=1e-5,
atol=1e-8. Other ties retain source order. The A=0.2/B=0.5 example now chooses
B, independent of metadata ordering; an unknown A cannot displace a known B.
No renormalization or stochastic site selection is introduced. All-unknown
occupancy requires an explicit label; invalid probabilities reject before any
publication.

The addressable guard checks literal expected labels, coordinates and source IDs
for unequal occupancies, source-order permutations, true ties with/without A and
unknown values. The shared repair, 4,639-case receiving, 50-case published-floor
receiving, documentation, initial failures and scientific limits are recorded
once in the [#571 resolution](invalid_alternate_location_requests_partially_modify_earlier_structures.md#resolution--2026-11-05).
The [receipt](../../devtools/data/alternate_location_receiving_569_571_20261105.json)
retains tested source hashes. This source correction does not qualify a release.
