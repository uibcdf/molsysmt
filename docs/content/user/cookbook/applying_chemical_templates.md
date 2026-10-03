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

The bounded public regression workflow covers reordered atoms, multiple frames
and states, nondefault units, H5MSM roundtrips and an independent methanol
recognition control in `tests/physchem/test_chemical_template.py`. Consumer-specific
biological acceptance, including ERalpha preparation, remains separate evidence.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Chemical_Templates` — complete public example and report contract.
- {ref}`cookbook-native-sdf` — native SDF inspection before preparation.
- {ref}`Cookbook_Auditing_Residue_Chemistry` — bounded receptor-residue assessment.
:::
