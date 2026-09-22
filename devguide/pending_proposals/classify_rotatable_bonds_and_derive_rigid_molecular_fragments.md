---
summary: Classify rotatable bonds and derive rigid molecular fragments
issue: uibcdf/molsysmt#224
status: open
opened: 2026-09-22
closed:
verification: inspected
area: [structure, build]
guard:
normative:
blocked_by: []
supersedes: []
---

# Classify rotatable bonds and derive rigid molecular fragments

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Open; MolSysMT proposal is post-1.0.

## What

Expose reusable torsion candidates and the rigid fragments induced by chosen active bonds.

## How

Classify eligible bonds from chemical graph information, explain exclusions such as rings and amides, then derive connected rigid fragments while preserving source atom and bond IDs.

## Why

Existing covalent-block and dihedral operations do not provide a general small-molecule torsion model needed by a flexible PDBQT ligand writer.

## What is measured and what is assumed

**Inspected:** Inspected topology/get_covalent_blocks.py and structure/get_dihedral_quartets.py; Meeko documents configurable rotatable-bond rules.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Making ROOT/BRANCH records the general torsion representation was rejected because those records are PDBQT-specific.

## Scope and exclusions

Chemical classification and fragment graph; rooted PDBQT serialization belongs to uibcdf/molsysmt#214, protocol selection to DockingMT.

## Acceptance criteria

- Tests distinguish acyclic single bonds, ring bonds, amides, and incomplete bond-order inputs.
- Selected active bonds produce deterministic rigid fragments and atom/bond correspondence; unsupported cases fail explicitly.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#214
Cross-component implementation links: uibcdf/dockingmt#6.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.
