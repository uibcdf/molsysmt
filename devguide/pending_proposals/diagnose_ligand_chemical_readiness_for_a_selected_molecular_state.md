---
summary: Diagnose ligand chemical readiness for a selected molecular state
issue: uibcdf/molsysmt#217
status: open
opened: 2026-09-22
closed:
verification: inspected
area: [basic, diagnostics]
guard:
normative:
blocked_by: []
supersedes: []
---

# Diagnose ligand chemical readiness for a selected molecular state

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Open; MolSysMT proposal is post-1.0.

## What

Provide an inspectable assessment of a selected small-molecule chemical state before downstream preparation.

## How

Report element identity, atom and bond identity, bond order, formal charge, stereochemistry, coordinates, and ambiguous or inferred fields. Distinguish absent, unsupported, and assessed data without silently completing chemistry.

## Why

MolSysMT can convert MolSys to rdkit.Mol, but a consumer needs to know whether the input chemistry was explicit and sufficient for its intended operation.

## What is measured and what is assumed

**Inspected:** Inspected molsysmt/form/molsysmt_MolSys/to_rdkit_Mol.py and the native topology attributes. No completeness claim or scientific validation was measured.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

A successful conversion alone is insufficient evidence that every chemical field was present in the source.

## Scope and exclusions

General diagnostics for one selected state and structure; no chemical-state enumeration, atom typing, or Vina policy.

## Acceptance criteria

- A structured result distinguishes present, inferred, missing, and unassessed chemistry by field and atom or bond where useful.
- Tests include complete, incomplete, and ambiguous ligand examples, with no silent chemical assignment.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#214
Cross-component implementation links: uibcdf/dockingmt#4.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.
