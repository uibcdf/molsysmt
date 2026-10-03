(Cookbook_Applying_Chemical_Templates)=
# Applying an explicit chemical template

*Preserving a molecular pose while filling declared missing chemical assignments.*

A ligand loaded from coordinates can have a useful pose and an incomplete chemical
description. Start with {ref}`Tutorial_Chemical_Readiness`, retain the ligand's
original indices when extracting it, and choose a prepared template independently.
The {ref}`template tutorial <Tutorial_Chemical_Templates>` demonstrates the complete
workflow with an independent methanol donor/acceptor control and optional RDKit
template construction. This narrative recipe records the decisions for real inputs.

:::{versionadded} 1.0.0
:::

## Establishing the input

1. Extract one isolated connected component; retain its map to the complete system.
2. Identify the intended source and template chemical states explicitly.
3. Curate the template's identity, revision, source URI/checksum and hydrogen policy.
4. Supply an exhaustive map from template indices to source indices, including all
   existing explicit H atoms. Names alone do not validate correspondence.
5. Run `msm.physchem.assess_chemical_template()` and review every indexed issue.

For a heavy-only deposited ligand, a heavy-only template with declared stored H
counts is a different input from a hydrogen-complete template. Applying it does
not create donor-H coordinates. Hydrogen placement must be a separate fixed-state
operation; importing ideal template coordinates would change the observed pose.

## Applying, recognizing and saving

Apply only a compatible template with `msm.physchem.apply_chemical_template()`.
Use the returned `molecular_system` for downstream recognition and retain the
detached `report` with your workflow records. Independently check the expected
chemical properties for your ligand; successful transfer is not a valence,
protonation or docking certification. Preserve the original unprepared input for
comparison. Named interactions invalidated on the returned copy require explicit
recalculation before use.

Save the prepared system through `msm.convert(..., to_form='file:h5msm',
output_filename=...)`. H5MSM 0.5 preserves its chemical values and structures;
the detached preparation report requires separate retention. On reload, inspect
the stored chemical state and pose, rather than interpreting the installed
software version as the original producer version.

## Handling unresolved cases

Keep an unresolved assessment when chemistry conflicts, required fields are
missing, the graph needs reconciliation or aromatic/stereo normalization is not
supported. Application raises a catalog-backed structural error containing that
report and changes neither input. Do not hide it with an empty interaction result,
neutral-charge fallback or an unconditional `complete` assignment.

## Checking a deposited ligand

The offline EST control from RCSB entry 1QKU illustrates the distinction between
chemical assignment and coordinate generation. A separately curated heavy-only
template fills the 20 observed atoms, retaining their pose and 23 heavy bonds.
Recognition yields the six-atom aromatic ring and acceptors O3/O17. Its 24 stored
H counts do not provide explicit donor-H pairs or H positions.

Choose the stereochemical source explicitly when reference fields disagree.
For the pinned EST definition, the CACTVS canonical descriptor and independent
CIP assignment from the deposited pose agree at five centers; the atom-level CCD
flag differs at C8. The fixture records that difference and the selected descriptor.
It does not silently substitute conflicting fields or infer the cause.

The source revisions, atom maps and checksums are recorded in
`tests/physchem/data/chemical_templates/manifest.json`; the reproducible curation
and its limits are described in the adjacent README. Native application can read
the curated H5MSM template without the RDKit used to produce it. This is evidence
for chemical transfer and pose preservation, not biological acceptance of the
consumer's complete ERalpha workflow.

The bounded public regression workflow covers reordered atoms, multiple frames
and states, nondefault units, H5MSM roundtrips and an independent methanol
recognition control in `tests/physchem/test_chemical_template.py`. Consumer-specific
biological acceptance remains separate evidence. The real EST control is in
`tests/physchem/test_chemical_template_est.py`.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Chemical_Templates` — complete public example and report contract.
- {ref}`cookbook-native-sdf` — native SDF inspection before preparation.
- {ref}`Cookbook_Auditing_Residue_Chemistry` — bounded receptor-residue assessment.
:::
