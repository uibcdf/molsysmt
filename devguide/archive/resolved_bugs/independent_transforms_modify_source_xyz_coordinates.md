---
summary: Independent rotation and translation modify source XYZ coordinates.
issue: uibcdf/molsysmt#633
status: resolved
opened: 2026-11-07
closed: 2026-11-07
severity: high
verification: reproduced
area: [structure, ownership, coordinates]
guard: tests/structure/test_transform_input_ownership.py
normative:
blocked_by: []
supersedes: []
---

# Transform input ownership

## What

Independent rotation and translation edit borrowed XYZ coordinate storage before
copying their output. Full-axis inputs therefore change even with
`in_place=False`. This violates the existing transform ownership contract.

## How

The new #602 signed-rotation control detects the changed original quantity.
Six plain public probes on `3f66f5931`, Python 3.14 and public PyUnitWizard 0.28.1,
show the defect for both operations on XYZ, with unchanged-source controls for
native Structures and MolSys. Their transform source bytes match owner `030c201a5`.
The getter can return a normalized borrowed quantity; the editor then assigns
to its magnitude before calling the existing copy/set boundary. Partial index
selection happens to make an intermediate copy, so it can mask this ownership
error. The omitted-element XYZ getter question is already tracked in #610.

## Why

A requested independent result must not change its source. Read-only sources
and a rotation protocol that fails after one structure also need source
preservation. A rotation around a fixed center calls translation, so both owning
tools must honor the boundary. Do not force every general getter to copy just
to compensate for an editor borrowing mutable data.

## Intended correction and acceptance

Compute on an independent selected-coordinate magnitude, preserving the existing
unit/form/dtype behavior, then publish through the existing setter after success.
This adds selected-block storage rather than a complete molecular snapshot solely
for computation. Native matrix/object handling, in-place returns, edited scopes
and existing interaction invalidation remain with their owners. Receive full
and reordered subsets, units, XYZ/native controls, independent/in-place output,
read-only inputs, failure after partial computation and captured-center geometry.
The addressable guard uses independent signed-axis/translation expectations and
an intentionally interrupted rotation, not a copied implementation.

This is an included-operation data-integrity correction under #334/#421; it adds
no scientific method, public API, progress weight or publication authorization.

## Local correction and receiving — 2026-11-07

Both owners now take one independent selected-coordinate magnitude before
arithmetic, keeping the original dtype and unit policy. No general getter or
setter is changed. The original 57-case guard run fails six cases: full-axis
independent XYZ rotation/translation, both read-only operations and both
interrupted-rotation modes. Its other native/unit/subset controls pass. Adding
the canonical-unit captured-center control gives 58 guards; all pass in the
324-case combined #602/#633 receiving, with zero errors/failures/skips.
Source/public delivery, broader consumers and documentation closeout remain due.

The later 7,764-case native geometry/addon/documentation receiving passes with
zero errors/failures/skips. New #638 separately records accepted XYZ ranks and
integer precision; do not read the canonical-rank floating ownership guards as
qualification of those other representation cases. This correction preserves
the existing numeric storage behavior rather than claiming to repair #638.

The portable [combined receiving receipt](../../../devtools/data/axis_angle_and_transform_receiving_602_633_634_637_20261107.json) retains native exits, original failed attempts, source fingerprints and the separately incomplete candidate/host gates. All fourteen final fast source gates pass.

## Resolution — 2026-11-07

The correction is delivered on main in checkpoint
`684a5b0cb9991e0538a0bd55bc934a5b57719a97`. An independent, complete GitHub
API tree matches all 141 changed source/record paths against the local commit.
The guard named in this record protects the stated boundary; its receiving and
original failures are retained in the linked portable receipt. The earlier
local/pending statements describe prior stages, not the current disposition.

This closes this bounded correction only. #421 graphical/installed/human scope,
#524 public-host/installed closure and the separate #635/#636/#638 work remain
open. No final-candidate, stability promotion or release approval is implied.
