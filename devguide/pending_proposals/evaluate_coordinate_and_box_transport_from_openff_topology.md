---
summary: Evaluate coordinate and box transport from OpenFF Topology
issue: uibcdf/molsysmt#741
status: open
opened: 2026-11-12
closed:
verification: measured
area: [form, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# Evaluating OpenFF Topology geometry transport

## What

Evaluate a reusable geometry-delivery contract for `openff.Topology`, including
its provider positions and optional periodic box, through native Structures and
MolSys conversion. This is **post-1.0 optional work**, not an additional release
prerequisite. #727 documents the current scope; #181 owns broader conversion-edge
execution coverage and #524 owns independent installed/provider compatibility.

## How

A six-atom synthetic methanol molecule with one explicit angstrom conformer is
converted to an OpenFF Topology under OpenFF Toolkit 0.19.0. The provider's
`get_positions()` returns shape (6, 3). Current `msm.has_attribute(...,
'coordinates')` returns False. Native MolSys conversion keeps six atoms but zero
structures; the direct Structures route also returns an empty container. The
source positions are unchanged when compared with their own before-read values.

The current adapter does not declare coordinates or other structural values.
Its `to_molsysmt_Structures` routine creates an empty Structures instance, and
MolSys conversion delegates to that routine. This is a measured limitation of an
undeclared capability, not a claim that the current supported geometry profile
has been implemented or validated. No box-loss runtime measurement is claimed.

## Why

OpenFF Topology can supply useful geometry even though its present MolSysMT
adapter does not transport it. A future implementation should expose honest
availability and preserve explicit units, atom correspondence and box geometry.
Registered conversion alone must not be presented as geometry preservation.
Until this work is decided, user documentation must state the empty geometry
route, and consumers needing conformers can use the supported Molecule route.

## Scope to decide

- Determine whether the provider exposes one declared global position set or
  independently indexed molecular conformers. Do not align or combine the latter
  by assumption. Define zero/missing positions, box-only inputs and empty axes.
- Reuse general quantity and selected-axis tools. Keep shape (n_structures,
  n_atoms, 3), explicit source units and row-vector boxes. Test a non-default
  application policy, such as pm/fs, as well as customary units.
- Keep ordered atom correspondence, native canonical inventory selection and
  structure indices distinct from labels. Define selections and refusals before
  implementing them; preserve the source during successful and rejected calls.
- Keep chemical assignments in ChemicalStates and stored mechanical charges in
  MolecularMechanics. Geometry transport must not prepare chemistry, invent
  parameters or create a competing store.
- Decide explicit refusal or loss reporting when requested geometry cannot be
  represented. A registered empty result must not become a lossless claim.
- Receive supported provider floors separately. Do not raise floors or claim
  every platform/interpreter solely from this local 0.19.0 observation.

## Acceptance criteria

1. Source data and public availability agree for supported geometry cases.
2. Native Structures/MolSys carry the intended units, coordinates, selected axes
   and optional box, or refuse/report unsupported representations explicitly.
3. Independent numerical expectations cover source preservation, absent and
   supplied geometry, unit conversion, atom selection and supported structure
   selection. Avoid count-only agreement with an already-empty result.
4. Update the form guide and conversion contract, and link broader edge coverage
   without making this proposal a pre-1.0 blocker by implication.

## Evidence and limits — 2026-11-12

The [geometry witness receipt](../../devtools/data/openff_topology_geometry_witness_741_20261112.json)
retains the bounded source/provider witness and source fingerprints. No runtime
library code, schema or dependency is changed by this proposal. The first probe
incorrectly compared unit-converted provider coordinates with the original bare
array bit for bit; its failed assertion is retained. Comparing actual provider
values before and after establishes source preservation. This correction is
not evidence of a provider or native conversion mutation.
