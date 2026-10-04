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

1. Extract the atoms of one intended component; retain their map to the complete
   system. The default requires its stored graph to be connected.
2. Identify the intended source and template chemical states explicitly.
3. Curate the template's identity, revision, source URI/checksum and hydrogen policy.
4. Supply an exhaustive map from template indices to source indices, including all
   existing explicit H atoms. Names alone do not validate correspondence.
5. Run `msm.physchem.assess_chemical_template()` and review every indexed issue.

For a heavy-only deposited ligand, a heavy-only template with declared stored H
counts is a different input from a hydrogen-complete template. Applying it does
not create donor-H coordinates. Hydrogen placement must be a separate fixed-state
operation; importing ideal template coordinates would change the observed pose.

## Declaring missing connectivity

If the source graph is incomplete, you can explicitly pass
`connectivity_policy='complete_from_template'` to both assessment and application.
Supply a connected, chemically prepared template with exhaustive correspondence
over the existing atoms. Review its proposed `added_bonds` before applying. No
extra source edge is removed, known assignment overwritten, or missing atom created.
Keep `require_same_graph` when missing bonds are not part of your preparation decision.

For a linear peptide, construct a coordinate-free reference with
`msm.physchem.get_peptide_chemical_template()` and explicit ordered residue states,
terminal chemistry and any disulfide group pairs. Inspect the
{ref}`factory contract <Tutorial_Get_Peptide_Chemical_Template>` before mapping
observed atoms. HIS alone is insufficient: choose HID, HIE or HIP explicitly.
The factory includes terminal OXT and no indexed H; missing observed heavy atoms
must be repaired separately. It leaves stereochemistry unspecified and does not
certify L residues or peptide cis/trans. Use a separately prepared template when
your workflow requires those assignments.

An extracted
pocket is not necessarily a chemically closed polymer: decide its boundary chemistry
explicitly rather than treating cut peptide bonds as complete residues. The tools
transfer the prepared template; a compatible local map does not certify chemistry
of the remainder of a receptor. Preserve the factory provenance and application
report as two distinct records alongside the original observed system.

After adding bonds, inspect the old-to-final `source_bond_correspondence` and new
edge indices in the detached report. Connected-component indices/IDs are rebuilt
in the selected state; component names/types become unknown. Group and molecule
inventory, other states, existing structure/state associations and pose remain intact.

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
missing, the graph needs unsupported reconciliation or aromatic/stereo normalization is not
supported. Application raises a catalog-backed structural error containing that
report and changes neither input. Do not hide it with an empty interaction result,
neutral-charge fallback or an unconditional `complete` assignment.

## Preparing a bounded observed peptide

The pinned 1QKU receptor control uses label chain A. Residues with IDs 301–303
have missing heavy atoms and are excluded from this scenario. The contiguous
304–550 fragment contains 247 residues, 1,975 observed heavy atoms and 2,013
stored bonds, including terminal OXT. Keep the extraction's source atom-index
map: those residue IDs are strings, not group or atom indices.

Declare the fragment's chemistry explicitly: the regression chooses HIE for
every HIS, ammonium at the artificial N-terminal cut at residue 304, and
carboxylate at residue 550. These are scenario choices, not an assignment of the
receptor's environmental protonation. Build that reference with
`msm.physchem.get_peptide_chemical_template()`.

The deposited aromatic bonds use an encoding that differs from the reference.
Call {ref}`the aromatic normalization tool <Tutorial_Normalize_Aromatic_Bond_Orders>`
as a separate recorded representation choice before assessment. For the eleven
ARG groups, explicitly map template NH1 to source NH2 and template NH2 to source
NH1: their equivalent terminal guanidinium nitrogens use opposite single/double
drawings. This map does not rename or move observed atoms, and the tool does not
guess it. Other atoms use the declared group/name correspondence. Review the
exhaustive map and assessment; the default identical-graph policy suffices and
no missing edge is added in this fragment.

Applying the reference retains every heavy atom's ID and pose. Recognition finds
31 aromatic rings. Use `get_hbond_sites(method='smarts_donor_acceptor')` when you
need the attributed chemical rules; the default elemental N/O method deliberately
includes amide and positively charged nitrogens as candidate acceptors.

The separate `build.add_missing_hydrogens()` fixed-state operation adds 2,028 H
with RDKit, preserving the 1,975 heavy-atom coordinates. It reports the loss of
observed B-factors under the intersection attribute policy. H5MSM retains the
resulting chemical state and coordinates. New H geometry has no environmental
optimization; stereo and biological acceptance remain unvalidated. Native to
RDKit conversion retains declared prohibitions of implicit H after sanitation,
including aromatic NH; do not relax the fixed-state checks to bypass conflicts.

This offline path is protected by
`tests/physchem/test_chemical_template_receptor.py`. It does not repair excluded
residues, prepare the complete receptor, or reinsert the fragment into the source.
Keep normalization, template and hydrogen-placement reports separately alongside
the extraction map and your explicit boundary/protonation choices.

## Checking a deposited ligand

The offline EST control from RCSB entry 1QKU illustrates the distinction between
chemical assignment and coordinate generation. A separately curated heavy-only
template fills the 20 observed atoms, retaining their pose and 23 heavy bonds.
Recognition yields the six-atom aromatic ring and acceptors O3/O17. Its 24 stored
H counts do not provide explicit donor-H pairs or H positions.

After selecting that chemical state, request the separate
{ref}`fixed-state hydrogen operation <Tutorial_Fixed_State_Hydrogens>` with
`mode='fixed_chemical_state'`, `pH=None`, `engine='RDKit'` and `return_report=True`.
For the pinned EST pose, the regression produces 44 atoms and 47 bonds, retains
all 20 original coordinate values and five CIP centers, and exposes donor-H
pairs for O3/O17. Those new H positions are modeled local geometry; no receptor
optimization or minimization has been performed. The roundtrip is protected by
`tests/build/add_missing_hydrogens/test_fixed_state.py`. B-factors are reported
as dropped when expanding this observed structure; strict attribute policy
rejects that loss. Keep both detached preparation reports with the input provenance.

The same public template-to-H composition accepts observed 181L BNZ with an
explicitly mapped heavy-only benzene template. Its six aromatic bonds retain
their flags and fractional orders of 1.5 without guessed integer Kekule orders.
H addition produces C6H6 with the six observed carbon IDs and positions unchanged.
This provider control validates the prepared ligand representation and local H
placement; final DockingMT scoring and receptor preparation remain separate.

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

The bounded public regression workflow covers reordered atoms, multiple structures
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
