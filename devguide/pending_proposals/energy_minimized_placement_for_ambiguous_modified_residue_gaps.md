---
summary: Energy-minimized placement for ambiguous modified-residue gaps
issue: uibcdf/molsysmt#249
status: open
opened: 2026-09-28
closed:
verification: measured
area: [build]
guard:
normative:
blocked_by: []
supersedes: []
---

# Energy-minimized placement for ambiguous modified-residue gaps

**Reported:** 2026-09-28, after the bounded MSE/SEP template repair in
uibcdf/molsysmt#228 and an audit of the remaining modified residues in the
bundled PDB fixtures.
**Status:** Open proposal. Current repair must continue to leave these gaps
unassessed.

## What

Develop a separate, optional reconstruction route for modified-residue heavy
atoms whose coordinates cannot be placed reliably from local ideal geometry.
The initial targets are missing atoms in the flexible MLY side chain and any
TPO gap that lacks a validated geometric placement. The route should produce
plausible, explicitly qualified coordinates from a suitable energy model while
preserving the exact residue chemistry and observed coordinates.

## How

Start with a component-specific chemical template and a complete parameter
inventory for the chosen force field, including protonation and formal charge.
Enumerate plausible conformers and chemically equivalent label assignments;
minimize each candidate with optional OpenMM in the receptor environment while
holding observed atoms fixed. Validate bond lengths, stereochemistry, steric
contacts, energy changes, and consistency across candidate minima. Return a
result only when the supported force field and the outcome meet defined checks;
otherwise keep the residue unassessed with a reason. Report the force field,
charge state, starting candidates, and energy/geometry evidence as provenance.

OpenMM provides a [residue-template generator interface](https://docs.openmm.org/development/api-python/generated/openmm.app.forcefield.ForceField.html)
for unmatched residues and a [local energy minimizer](https://docs.openmm.org/latest/api-python/generated/openmm.openmm.LocalEnergyMinimizer.html).
These mechanisms do not themselves supply validated MLY/TPO parameters or a
unique experimental structure.

## Why

The bundled PDB files contain one complete TPO residue and 14 complete MLY
residues. A leave-one-atom-out placement using CCD ideal coordinates and local
graph-neighbor Kabsch anchors gives a median error near 0.145 nm for MLY CH1
and CH2; all 14 cases of each atom exceed 0.05 nm. The same method predicts
MLY N within 0.013 nm in all 14 cases, and the observed TPO phosphate atoms
within 0.014 nm in its one available fixture. These results support only a
bounded geometric subset; they do not justify automatic repair of the
remaining atoms. MLY N was not enabled by this audit: adding a polymer N also
requires restoring its bond to the preceding residue, which the bounded
intra-residue placement route does not currently do.

## What is measured and what is assumed

**Measured:** The local audit used `2vgy.pdb` and `3c0f.pdb` for MLY and
`1atp.pdb` for TPO, with the RCSB CCD ideal conformers for those components.
For each observed heavy atom, the audit omitted that atom, selected present
template neighbors within two or three bonds, aligned them with MolSysMT's
Kabsch backend, and compared the predicted position with the deposited PDB
coordinate in nanometers. The counts and thresholds above are fixture-specific.
The methyl error bound is reproduced by:

```bash
python -m pytest --receptor=llm -q tests/build/add_missing_heavy_atoms/test_modified_residues.py::test_mly_methyl_template_error_exceeds_bound_in_all_bundled_residues
```

**Assumed:** A validated force field, explicit charge/protonation state, and
receptor context could improve a candidate placement. No energy-minimization
accuracy or force-field coverage has been measured. A local minimum is not
evidence of a unique atom-label assignment or an experimental position.

## What was refuted

Applying a single rigidly aligned CCD conformer to the flexible MLY side chain
was rejected by the leave-one-out errors. Renaming MLY to LYS or TPO to THR
would discard the modification chemistry. Choosing one of two equivalent methyl
labels by minimum energy alone cannot resolve a symmetry ambiguity.

## Scope and exclusions

The initial implementation should focus on the unsafe gaps in MLY and TPO,
then admit other modified residues only with their own parameters and
validation fixtures. This proposal is separate from residue-coverage reporting
in uibcdf/molsysmt#218 and from the bounded template route in
uibcdf/molsysmt#228. It does not promise experimental accuracy, automatic
protonation-state selection, or a universal parameterizer for all CCD entries.

## Acceptance criteria

- A supported modified residue is parameterized with its exact atoms, bonds,
  elements, stereochemistry, charge state, and a named force field before
  minimization. Missing parameters fail explicitly.
- Observed atom IDs and coordinates remain unchanged; only missing atoms are
  added. Alternative conformers and symmetry-equivalent labels are evaluated
  or reported as ambiguous.
- Independent deposited structures compare the resulting chemistry and bounded
  coordinate errors against the current unrefined template route. Energy,
  geometry, parameter coverage, and failure cases have reproducible tests.
- Unsupported residue or protonation states remain unassessed with a specific
  reason; the route never silently substitutes parent-residue chemistry.

## Dependencies and risks

OpenMM remains a soft dependency. Force-field parameters for MLY and TPO must
be sourced and validated rather than presumed to exist in a standard protein
force field. Local minima depend on initial conformers, environment, charge
state, restraints, and atom-label symmetry.

## Provenance

Local MolSysMT checkout, Python 3.13, 2026-09-28. Source coordinates are the
bundled PDB fixtures named above; component chemistry and ideal coordinates
were read from the RCSB Chemical Component Dictionary TPO and MLY entries.
The current geometry audit is a development measurement, not a published
benchmark; its source files and leave-one-out procedure are named above so it
can be reproduced and extended by the proposal's eventual guard.
