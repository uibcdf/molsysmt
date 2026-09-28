---
summary: Repair selected nonstandard receptor residues with residue-specific templates
issue: uibcdf/molsysmt#228
status: resolved
opened: 2026-09-22
closed: 2026-09-28
verification: measured
area: [build]
guard: tests/build/add_missing_heavy_atoms/test_modified_residues.py
normative:
blocked_by: []
supersedes: []
---

# Repair selected nonstandard receptor residues with residue-specific templates

**Reported:** 2026-09-22, during the MolSysMT–DockingMT chemical preparation review.
**Status:** Resolved on 2026-09-28. The prerequisite correctness defect in
uibcdf/molsysmt#227 was resolved on the same date.

## What

Add an initial bounded native repair route for incomplete nonstandard protein residues without replacing their chemical identity.

## How

Start with curated MSE and SEP component-specific templates; match atoms by name, element and connectivity, place only missing atoms from a documented local geometry, and preserve original atoms, residue identity and provenance.

## Why

The current native heavy-atom placement database contains standard residues and caps, while receptor preparation can encounter selenium or phosphorylated residues requiring their own chemistry.

## What is measured and what is assumed

**Inspected at filing:** `molsysmt/build/add_missing_heavy_atoms.py` and
`molsysmt/data/databases/residue_templates/README.md`; neither MSE nor SEP
had a native placement template. The [MSE](https://files.rcsb.org/ligands/view/MSE.cif)
and [SEP](https://files.rcsb.org/ligands/view/SEP.cif) chemical components
provide the distinct element and bond inventories.
**Measured at resolution:** `python -m pytest --receptor=llm -q
tests/build/add_missing_heavy_atoms/test_modified_residues.py` passes nine
chemical and geometric checks. Reconstructing the missing backbone O in the
bundled experimental MSE residue (3c8h, A27) gives a 0.0074 nm displacement
from the deposited position. The SEP O1P fixture uses a rigidly transformed
CCD ideal conformer and has numerical-roundoff reconstruction error; it is a
template-consistency check, not an experimental accuracy estimate.
**Assumed:** Scientific generality beyond the bounded fixtures is not established.

## What was refuted

Renaming modified residues to MET or SER during repair was rejected because it discards selenium or phosphate chemistry. Universal automatic repair is outside this initial delivery. The bundled SEP residue from 1atp was not used as a positive geometry reference: its deposited O1P position differs by 0.107 nm from placement using the other phosphate atoms.

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

## Resolution — 2026-09-28

Added pinned, whitespace-normalized, checksum-verified CCD snapshots and an offline generator for
MSE/SEP heavy-atom templates. The native assessment uses exact atom names and
elements; repair validates observed connectivity and bond orders, aligns local
anchors, checks new bond lengths, and appends atoms with explicit elements,
orders, collision-free string IDs, and unchanged original atom records and
coordinates. Unsupported modified residues and ambiguous or conflicting cases
emit `UnassessedResidueWarning` and remain unchanged. The native route retains
MSE and SEP residue names. Hydrogenation and protonation remain separate.

The guard exercises a deposited MSE geometry, ideal CCD geometry for SEP and
selenium, chemical inventory, existing-coordinate and ID preservation,
ambiguous phosphate gaps, incompatible chemistry, missing bonds, and an
unsupported modified residue. The test bounds the delivered behavior; it does
not establish reliable coordinate prediction for every experimental conformer.
