---
summary: Enumerate ligand tautomers and stereoisomers as explicit chemical states
issue: uibcdf/molsysmt#229
status: blocked
opened: 2026-09-22
closed:
verification: inspected
area: [build, structure]
guard:
normative:
blocked_by: [uibcdf/molsysmt#220]
supersedes: []
---

# Enumerate ligand tautomers and stereoisomers as explicit chemical states

**Reported:** 2026-09-22, during the MolSysMT–DockingMT chemical preparation review.
**Status:** Blocked post-1.0 proposal; the named dependency must be resolved first.

## What

Implement a bounded first route for tautomer and stereoisomer enumeration as distinct operations on small molecules.

## How

Use lazy optional RDKit enumerators with named rules, deterministic limits, duplicate removal, state provenance and parent-to-child atom mapping. Preserve assigned stereochemistry by default and distinguish bond-order changes from geometry changes.

## Why

MolSysMT can store chemical states but does not yet generate these two common ligand-state families for downstream selection.

## What is measured and what is assumed

**Inspected:** Native chemical-state storage and MolSysMT→RDKit conversion.
RDKit documents its [tautomer](https://www.rdkit.org/docs/source/rdkit.Chem.MolStandardize.rdMolStandardize.html)
and [stereoisomer](https://www.rdkit.org/docs/source/rdkit.Chem.EnumerateStereoisomers.html)
enumerators; no MolSysMT state-generation validation set exists yet.
**Assumed:** Scientific generality beyond the bounded fixtures is not established.

## What was refuted

Treating new conformers as new chemical states was rejected because conformer generation is tracked separately in uibcdf/molsysmt#219.

## Scope and exclusions

Representative tautomer and unassigned-stereocenter cases after the identity contract in uibcdf/molsysmt#220; no protomer enumeration, pH ranking or exhaustive chemical-space claim.

## Acceptance criteria

- A tautomer example changes appropriate bond/H placement and a stereocenter example yields only allowed distinct stereoisomers, each with stable source correspondence.
- Rules, limits, duplicate handling, stereochemistry retention and unsupported chemistry are documented and tested; output states can be selected independently for DockingMT.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#220, uibcdf/molsysmt#219, uibcdf/dockingmt#4.

## Provenance

Source inspection on the local checkout `e9df1d1bd`, Python 3.13.14,
2026-09-22. No timing or chemical-coverage measurement was made.
