---
summary: Support paired rigid and flexible receptor PDBQT forms
issue: uibcdf/molsysmt#225
status: open
opened: 2026-09-22
closed:
verification: inspected
area: [form, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# Support paired rigid and flexible receptor PDBQT forms

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Open; MolSysMT proposal is post-1.0.

## What

Read and write the rigid and flexible PDBQT components of a receptor as a coherent molecular-system projection.

## How

Partition selected flexible atoms from the rigid receptor without duplicates, serialize flexible-residue records and torsion tree, and preserve atom mapping for reconstruction.

## Why

Vina accepts separate rigid and flexible receptor PDBQT inputs; the first PDBQT form proposal explicitly excludes this layout.

## What is measured and what is assumed

**Inspected:** Inspected the uibcdf/molsysmt#214 record and Vina Python documentation. No flexible receptor fixture has been validated yet.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Treating the flexible component as an ordinary independent ligand was rejected because it remains covalently connected to the receptor.

## Scope and exclusions

Paired PDBQT representation and fidelity; selection of flexible residues and Vina execution belong to DockingMT.

## Acceptance criteria

- Round trips preserve the receptor atom partition, residue identity, supported coordinates, charges, types, and torsions.
- Duplicate or missing atoms and unsupported layouts fail explicitly; representative flexible-residue fixtures are tested.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#214
Cross-component implementation links: uibcdf/dockingmt#7.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.
