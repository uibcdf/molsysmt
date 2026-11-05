---
summary: Resolving an alternate location retains the previous primary occupancy
issue: uibcdf/molsysmt#570
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [build, structure]
guard: tests/build/solve_atoms_with_alternate_location/test_alternate_location_contract.py::test_selected_primary_observation_includes_its_occupancy
normative:
blocked_by: []
supersedes: []
---

# Resolving an alternate location retains the previous primary occupancy

## What

Explicit B changes coordinates, B factor and atom label but retains the former primary occupancy.

## How

The writer only publishes coordinates and optionally B factors; occupancy is absent from its update dictionary.

## Why

Exported/queried primary observations combine different alternate sites. This is independent of #556 occupancy acquisition.

## Reproduction and acceptance

The new public regression module
`tests/build/solve_atoms_with_alternate_location/test_alternate_location_contract.py`
reproduces the reports with small native systems. After correcting two fixture
setup errors (the required Interactions method and its read-only mapping), the
original runtime fails 24 of 30 controls. The five existing real-system tests
are retained. The first repaired receiving passed all 35 cases; final receiving is recorded
below.

#571 owns shared validation/publication; this report owns coherent optional observation metadata. Public input stays form-agnostic. Preserve alternate records and
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

The chosen site's occupancy is published beside its coordinates and B factor.
Missing selected measurements become unknown rather than retaining a prior
site's value. Unselected positions and original alternate dictionaries survive.
New primary metadata storage is initialized with unknowns and integer storage
is promoted for fractional assignments. Native public setters reuse their
existing ArgDigest value validators; initialization uses stored axis dimensions
without reading or copying coordinates.

The addressable guard checks both explicit B and occupancy-policy resolution,
selected/unselected atom and nonconsecutive/repeated structure positions,
primary B-factor/occupancy values and selective interaction invalidation.
Additional controls cover absent/integer storage, unknown observations, physical
units under a pm/fs application policy, coordinate-materialization refusal and
H5MSM persistence. Shared staging, 4,639-case receiving, 50 published-floor cases,
documentation and failure history are recorded once in the
[#571 resolution](invalid_alternate_location_requests_partially_modify_earlier_structures.md#resolution--2026-11-05).
The [receipt](../../devtools/data/alternate_location_receiving_569_571_20261105.json)
retains source hashes and limits. CIF occupancy acquisition remains separately
owned by #556; no parser repair or release qualification is claimed here.
