---
summary: Conversion and form-detection fixtures violate explicit ParmEd export prerequisites
issue: uibcdf/molsysmt#649
status: active
opened: 2026-11-08
closed:
severity: medium
verification: reproduced
area: [tests, convert]
guard: tests/conversion_truth/test_declared_native_edges.py::test_external_water_fixtures_preserve_explicit_single_bond_orders
normative:
blocked_by: []
supersedes: []
---

# Explicit chemistry in ParmEd-positive fixtures

## What

Five cases in the bounded complete-source attempt on `6205fcc78` fail at the
intended strict ParmEd boundary. Two form-census cases convert an old native
alanine-dipeptide fixture with unknown bond type/order. Three declared-resident
edges construct literal water in MDTraj/OpenMM without declaring its known
single bond orders. A positive conversion assertion cannot demand fabrication
of that missing chemistry.

## Evidence

The partial receptor records identify NotCompatibleConversionError for native
MolSys to ParmEd and MDTraj Topology/Trajectory or OpenMM Topology to ParmEd.
#629 deliberately refuses unknown numeric orders; ParmEd cannot preserve them.
This is a positive-fixture mismatch, not evidence that rejecting unknown input
is a runtime bug. Separate EAGAIN/thread failures in that campaign came from its
128-task ceiling and remain in #612's operational record. Reproduce these five
selectors serially before editing the fixtures.

## Intended correction

Construct a nonempty explicit water directly for the ParmEd form census, using
its already optional provider. Declare order one on the literal O–H source
bonds in MDTraj/OpenMM. Keep every positive edge, both public/direct execution
and the existing explicit unknown-order rejection controls. Add an independent
literal [1,1] bond-order witness across those external-water fixtures and
export. Do not change native scientific tables, infer arbitrary alanine orders,
weaken the strict adapter, skip the cases or shrink the edge inventory.

## Acceptance

Receive the original failures and corrected targeted modules, existing strict
ParmEd negative controls and applicable Ruff checks. Keep original atom/structure
axes and optional-dependency behavior. Requalify the complete source scope under
#612 after correcting the independent test-namespace defect #650. No installed
artifact, scientific-method or 1.0 candidate claim follows.

## Directed receiving — 2026-11-08

The original thirteen-case serial diagnosis yields six failures (five explicit
ParmEd prerequisites and one test-namespace refusal) and seven passes after
controlling Rayon threads. Corrected complete form-census/resident-edge/docking
and strict ParmEd modules pass 518 cases, zero skips/failures/errors. Source
fixtures declare known single O–H bonds; runtime unknown-order refusals remain.
The fresh child executes all original docking cases from an unrelated temporary
working directory under the same blocked optional engines. This is source test
receiving; exact committed-source/fast and full-suite acceptance remain due.
