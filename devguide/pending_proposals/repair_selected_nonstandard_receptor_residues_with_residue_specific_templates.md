---
summary: Repair selected nonstandard receptor residues with residue-specific templates
issue: uibcdf/molsysmt#228
status: blocked
opened: 2026-09-22
closed:
verification: inspected
area: [build]
guard:
normative:
blocked_by: [uibcdf/molsysmt#227]
supersedes: []
---

# Repair selected nonstandard receptor residues with residue-specific templates

**Reported:** 2026-09-22, during the MolSysMT–DockingMT chemical preparation review.
**Status:** Blocked post-1.0 proposal; the named dependency must be resolved first.

## What

Add an initial bounded native repair route for incomplete nonstandard protein residues without replacing their chemical identity.

## How

Start with curated MSE and SEP component-specific templates; match atoms by name, element and connectivity, place only missing atoms from a documented local geometry, and preserve original atoms, residue identity and provenance.

## Why

The current native heavy-atom placement database contains standard residues and caps, while receptor preparation can encounter selenium or phosphorylated residues requiring their own chemistry.

## What is measured and what is assumed

**Inspected:** `molsysmt/build/add_missing_heavy_atoms.py` and
`molsysmt/data/databases/residue_templates/README.md`; neither MSE nor SEP
has a native placement template. The [MSE](https://files.rcsb.org/ligands/view/MSE.cif)
and [SEP](https://files.rcsb.org/ligands/view/SEP.cif) chemical components
provide the distinct element and bond inventories. No coordinate-accuracy
measurement has been made.
**Assumed:** Scientific generality beyond the bounded fixtures is not established.

## What was refuted

Renaming modified residues to MET or SER during repair was rejected because it discards selenium or phosphate chemistry. Universal automatic repair is outside this initial delivery.

## Scope and exclusions

Template-based heavy-atom repair for the chosen MSE and SEP fixtures, with explicit unsupported status elsewhere; hydrogen placement and environment-dependent protonation remain separate.

## Acceptance criteria

- A partially observed MSE and SEP fixture are repaired with the correct elements, bonds, atom IDs and residue names; already present atoms and coordinates remain stable.
- Ambiguous template matches and unsupported modifications fail or remain unassessed without adding parent-residue atoms; tests compare repaired chemistry and bounded geometry against curated references.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#218, uibcdf/molsysmt#227.

## Provenance

Source inspection on the local checkout `e9df1d1bd`, Python 3.13.14,
2026-09-22. No timing or geometric-accuracy measurement was made.
