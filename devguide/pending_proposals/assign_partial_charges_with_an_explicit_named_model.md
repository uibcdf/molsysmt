---
summary: Assign partial charges with an explicit named model
issue: uibcdf/molsysmt#221
status: open
opened: 2026-09-22
closed:
verification: inspected
area: [build, attribute]
guard:
normative:
blocked_by: []
supersedes: []
---

# Assign partial charges with an explicit named model

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Open; MolSysMT proposal is post-1.0.

## What

Assign per-atom partial charges to a selected chemical state using an explicit method, starting with a bounded Gasteiger route.

## How

Use an optional lazy backend; preserve atom order and IDs, record method and version, and validate finite values, coverage, and an explained total-charge tolerance.

## Why

MolecularMechanics can hold partial_charge and RDKit conversion can read previously calculated Gasteiger values, but that is not a general assignment operation.

## What is measured and what is assumed

**Inspected:** Inspected molsysmt/native/molecular_mechanics.py and molsysmt/form/rdkit_Mol/get_mechanical_attributes.py. No charge-quality benchmark was performed.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Writing zero charges into PDBQT as a default was rejected because it hides missing parameterization.

## Scope and exclusions

Named charge assignment and diagnostics, not AutoDock atom typing or selection of a docking protocol.

## Acceptance criteria

- A named method assigns charges with atom-aligned values and recorded provenance for supported inputs.
- Missing prerequisites, nonfinite values, partial coverage, and total-charge discrepancies have explicit tested behavior.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#214
Cross-component implementation links: uibcdf/dockingmt#5.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.
