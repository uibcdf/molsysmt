---
summary: OpenMM attribution metadata conflicts between implicit models and solvation.
issue: uibcdf/molsysmt#583
status: open
opened: 2026-11-05
closed:
severity: medium
verification: reproduced
area: [build, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# OpenMM identity across alternative models

## What

Constructing an OBC1 model and then solvating the unchanged original source in
one Ackredit session emits AttributionConflictError for the same OpenMM version.
The solvation completes, but its capture omits the executed OpenMM reference.

## How

Reproduced without Viewer on published native 8c2661293, Python 3.14 and OpenMM
8.6.1. Convert the native 22-atom alanine fixture to openmm.System with OBC1,
then capture native OpenMM cubic solvation of the original source with 0.35 nm
clearance, zero requested ions and seed 1. The result has 151 atoms. Its
solvation usage-tree node is empty while child native ion-replacement references
remain. `_private.scientific_attribution.credit_implicit_solvent` uses canonical
title OpenMM and its website; `build.solvate` supplies lowercase openmm and
different metadata under the same software/version identifier. Ackredit
correctly refuses the collision and preserves the earlier reference.

## Why

Independent alternatives and unrelated molecules can share one attribution
session. Diego also identifies a legitimate staged workflow: minimize with
OBC1, explicitly change the force field/solvent model, then solvate for dynamics.
The minimal reproduction isolates metadata identity; it does not execute or
qualify that full minimization/dynamics workflow. Scientific results and model
contexts must remain distinct from coherent software bibliographic identity.

## Acceptance

Reuse canonical native OpenMM metadata and test both orders in separate
captures within one session. Preserve successful OBC paper/model context,
solvation and child uses; metadata-only lookups must not imply engine execution.
Preserve independent scientific outputs and optional-provider failure behavior.
No consumer copy, disabled conflict detection or scientific workaround is needed.

Related consumer: uibcdf/molsysviewer#264; implementation contribution #421 / PR
#543. The source receiving receipt retains the original warning and capture.
