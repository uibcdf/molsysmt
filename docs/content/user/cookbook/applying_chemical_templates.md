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

1. Extract one intended component and retain its map to the complete system, or
   select that component explicitly inside the original system. The default
   requires its stored graph to be connected; stored external edges are unassessed.
2. Identify the intended source and template chemical states explicitly.
3. Curate the template's identity, revision, source URI/checksum and hydrogen policy.
4. Supply an exhaustive map from template indices to source indices, including all
   existing explicit H atoms. Names alone do not validate correspondence.
5. Run `msm.physchem.assess_chemical_template()` and review every indexed issue.

For a heavy-only deposited ligand, a heavy-only template with declared stored H
counts is a different input from a hydrogen-complete template. Applying it does
not create donor-H coordinates. Hydrogen placement must be a separate fixed-state
operation; importing ideal template coordinates would change the observed pose.

(cookbook-component-chemical-transfer)=
## Retaining the original complex

To update the observed complex instead of keeping only an extracted ligand,
compose the previously reviewed template-to-ligand map with the retained
ligand-to-source map. In the continuation below, `molsys` is the original system,
`template` is the curated same-atom template, `source_atom_indices` contains the
original indices in extracted-ligand order, and `atom_correspondence` is the
exhaustive template-to-extracted-ligand map. All maps contain indices, not IDs.

```python
full_map = atom_correspondence.copy()
full_map[:, 1] = source_atom_indices[atom_correspondence[:, 1]]
options = dict(
    template=template, atom_correspondence=full_map,
    template_provenance=template_provenance, selection=source_atom_indices,
)
assessment = msm.physchem.assess_chemical_template(molsys, **options)
# Inspect issues and coverage before the transactional application.
result = msm.physchem.apply_chemical_template(molsys, **options)
molsys_A = result['molecular_system']
msm.convert(molsys_A, to_form='file:h5msm',
            output_filename='chemically_updated_complex.h5msm')
```

The pinned EST control applies 20 heavy atoms to full-source indices 5,940–5,959
of 1QKU, retaining all 6,596 atoms, their original positions and every unrelated
relationship. The remaining chemical atom fields stay unknown; global connectivity
stays `partial`. Native and H5MSM inputs, full-complex persistence, and extraction
of the assigned EST are checked in `tests/physchem/test_chemical_template_est.py`.
The extracted ligand still inherits `partial`; explicitly applying the reviewed
whole-ligand template again justifies its own complete connectivity for recognition.

The default requires the same stored internal atom pairs. To fill a reviewed
missing selected bond, explicitly choose `complete_from_template`. Inspect the
proposed edges first. Rebuilding can renumber component indices but preserves
IDs, names and types of unchanged atom sets, including unrelated components.
Merged or split selected components have missing labels. An inconsistent unrelated
stored partition remains unassessed; resolve it separately before scoped completion.
This route transfers chemical assignments to existing atoms. It does not insert
generated H or missing heavy atoms, reconcile representation differences, or
prepare excluded receptor regions. A peptide fragment whose stored bonds reach
outside the selection remains unassessed; its artificial terminal chemistry
cannot be inserted across that cut. Retain the detached preparation report with
the map. Named observations are invalidated on a changed output copy, while the
original complex remains unchanged. Full-graph interaction recognizers can still
reject this partially prepared complex even if participants select only EST.

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
edge indices in the detached report. Connected-component indices are rebuilt
in the selected state. Whole-input completion regenerates IDs; scoped completion
preserves them for unchanged atom sets. Names/types of unchanged atom sets are
preserved; labels of merged or split components become missing. Group and molecule
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
output_filename=...)`. H5MSM 0.5 preserves chemical values, structures and
template-application history. On reload, inspect
the stored chemical state and pose, rather than interpreting the installed
software version as the original producer version. Retrieve template history with
`molsys.chemical_states.get_preparation_history()`. Each record's `report` holds
the provider report and `output` holds the original output dimensions.

These are the original operation's indices, even if you later extract, reorder,
merge or edit the system. Retain intervening maps separately; history is evidence
of the operation, not a certificate for current assignments. Fixed-state
hydrogen-generation and terminal-attachment reports also attach automatically
to their own results. Archive a component's selected historical records in a
destination explicitly when reinserting its generated H.

(cookbook-component-hydrogen-reinsertion)=
## Reinserting generated H

You can append a prepared component's generated H to the original atom domain
using existing public tools. The following continuation assumes `molsys_A` is
the chemically updated complex from {ref}`Retaining the original complex
<cookbook-component-chemical-transfer>`, with **one chemical state and one
structure**. The reviewed template and the two retained index maps are the same
as in that example. They declare correspondence; neither matching atom IDs nor
matching axis lengths proves it.

Extract the component and explicitly apply its exhaustive template again:
extraction conservatively inherits the parent connectivity status. Fixed-state
H generation requires a declared complete isolated graph. The `intersection`
policy below deliberately accepts reported attribute removal. On observed
1QKU it removes `b_factor`; choose `strict` to reject that loss instead.

```python
import numpy as np

prepared_complex = molsys_A
isolated = msm.extract(prepared_complex, selection=source_atom_indices)
isolated = msm.physchem.apply_chemical_template(
    isolated, template=template, atom_correspondence=atom_correspondence,
    template_provenance=template_provenance,
)['molecular_system']
generated = msm.build.add_missing_hydrogens(
    isolated, pH=None, engine='RDKit', mode='fixed_chemical_state',
    return_report=True, attribute_policy='intersection',
)
hydrogenated = generated['molecular_system']
generation_report = generated['report']
pairs = generation_report['parent_hydrogen_pairs']
n_original = len(source_atom_indices)
np.testing.assert_array_equal(
    generation_report['atom_correspondence'],
    np.column_stack((np.arange(n_original), np.arange(n_original))),
)
np.testing.assert_array_equal(
    pairs[:, 1], np.arange(n_original, msm.get(hydrogenated, n_atoms=True)),
)
if (len(np.unique(source_atom_indices)) != n_original
        or np.any(source_atom_indices < 0)
        or np.any(source_atom_indices >= msm.get(prepared_complex, n_atoms=True))):
    raise ValueError('The declared component-to-source map is not one-to-one.')
original_pose = msm.get(prepared_complex, selection=source_atom_indices,
                       coordinates=True)
retained_pose = msm.get(hydrogenated, selection=np.arange(n_original),
                       coordinates=True)
np.testing.assert_array_equal(
    msm.pyunitwizard.get_value(original_pose, to_unit='nm'),
    msm.pyunitwizard.get_value(retained_pose, to_unit='nm'),
)
implicit, explicit = msm.get(
    prepared_complex, selection=source_atom_indices,
    n_implicit_hydrogens=True, n_explicit_hydrogens=True,
)
np.testing.assert_array_equal(
    np.asarray(implicit, dtype=int) + np.asarray(explicit, dtype=int),
    np.bincount(pairs[:, 0], minlength=n_original),
)
```

Map each generated H's parent through the retained source indices and copy its
declared chemical fields from the producer result. Omit the isolated system's
atom IDs: the attachment tool synthesizes unique string IDs in the destination.
It appends atoms without moving or reordering the existing atom axis.

```python
fields = {
    'formal_charge': 'formal_charge', 'atom_is_aromatic': 'is_aromatic',
    'n_unpaired_electrons': 'n_unpaired_electrons',
    'n_implicit_hydrogens': 'n_implicit_hydrogens',
    'n_explicit_hydrogens': 'n_explicit_hydrogens',
    'allows_implicit_hydrogens': 'allows_implicit_hydrogens',
    'atom_stereochemistry': 'stereochemistry',
}
values = msm.get(hydrogenated, selection=pairs[:, 1],
                 **{field: True for field in fields})
types, names = msm.get(hydrogenated, selection=pairs[:, 1],
                      atom_type=True, atom_name=True)
records = [
    dict(parent_atom_index=int(source_atom_indices[parent]),
         atom_type=types[k], atom_name=names[k],
         chemical_attributes={field: column[k]
                              for field, column in zip(fields.values(), values)})
    for k, (parent, _) in enumerate(pairs)
]
attached = msm.build.add_terminal_atoms(
    prepared_complex, records,
    msm.get(hydrogenated, selection=pairs[:, 1], coordinates=True),
    attribute_policy='intersection',
)
molsys_B = attached['molecular_system']
parents = np.unique(source_atom_indices[pairs[:, 0]])
if len(parents):
    msm.set(molsys_B, selection=parents,
            n_implicit_hydrogens=np.zeros(len(parents), dtype=int),
            n_explicit_hydrogens=np.zeros(len(parents), dtype=int))
# Retain the isolated producer's original report in the destination history.
molsys_B.chemical_states.append_preparation_history(
    hydrogenated.chemical_states.get_preparation_history()[-1:])
msm.convert(molsys_B, to_form='file:h5msm',
            output_filename='complex_with_generated_hydrogens.h5msm')
```

The indexed H now replace their parents' virtual counts: leaving both in place
would count the same H twice. Only parents whose complete virtual inventory was
materialized are updated; unrelated chemical assignments stay unchanged.
The attachment preserves the parent global connectivity status. A prepared
ligand does not establish complete chemistry for the rest of the complex.
Named analyses become unevaluated, and each new atom has source index `-1`.
No additions preserve evaluated coverage. This workflow has no implicit alignment,
protonation choice or environmental minimization.

The observed EST control appends 24 H to 6,596 existing atoms, yielding 6,620,
with every deposited coordinate retained and global connectivity still partial.
Its extracted 44-atom ligand has the known six-member aromatic ring and no
remaining virtual H after an explicit complete-template reassessment. Synthetic
methanol and ammonium controls cover implicit/explicit counts, charged chemistry,
ID collisions, native/H5MSM inputs, invalid maps/inventories and no-op repetition.
See `tests/build/add_terminal_atoms/test_component_hydrogen_reinsertion.py`.

The attachment result already retains its report. The explicit
`append_preparation_history()` above also archives the isolated producer's last
H-generation record, so H5MSM 0.5 retains **both** reports with original units
and producer versions. On reload, inspect `molsys_B.chemical_states.get_preparation_history()`.
The final generation record still describes a 44-atom output with 20 original
ligand atoms; the preceding attachment record describes the 6,620-atom complex
with 6,596 original atoms. Record order is append order, including imports.
Their indices are historical and are not remapped or certified as current.
Retain `source_atom_indices` separately: generation describes local geometry,
attachment destination parents/new indices, IDs and dropped attributes. The
reports store no duplicate coordinate arrays. This is a bounded terminal-H
workflow; arbitrary heavy-atom replacement, bonds between new atoms, multiple
states/structures and receptor-fragment boundary reconciliation require separate
contracts. A cut peptide's artificial terminal H cannot be reinserted into the
uncut chain through this recipe.

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
Template and fixed-state H-placement reports accompany their output in H5MSM
preparation history. Keep normalization/factory reports separately alongside
the extraction map and explicit boundary/protonation choices. Historical reports
retain original indices; importing them does not reconcile the fragment boundary.

(cookbook-polymer-context-template)=
## Preparing a receptor selection with context

For the observed 1QKU receptor, a ligand shell is an inspection selection inside
the full chain. Keep its peptide links to external residues. Assume `molsys` is
the observed complete source loaded as a native MolSys. The following scenario
choices declare HIE for every HIS, ammonium at residue 301, carboxylate at 550,
and no disulfides. They are not environmental protonation predictions.

Build a reference for all 250 residues, without reconstructing the nine missing
heavy atoms in SER301/LYS302/LYS303. Explicitly declare the ARG NH1/NH2 map as in
the bounded fragment scenario. The separate aromatic normalization acts on the
entire extracted receptor and returns its own representation report. Context
application preserves outside assignments relative to that normalized input.

```python
import numpy as np

receptor_selection = 'molecule_type == "protein" and chain_id == "A"'
source_atom_indices = msm.select(molsys, selection=receptor_selection)
receptor = msm.extract(molsys, selection=source_atom_indices)
assert receptor.topology.groups.group_id.tolist() == [str(i) for i in range(301, 551)]
names = receptor.topology.groups.group_name.tolist()
definition = msm.physchem.get_peptide_chemical_template(
    ['HIE' if name == 'HIS' else name for name in names],
    'ammonium', 'carboxylate')
normalization = msm.physchem.normalize_aromatic_bond_orders(receptor)
molsys_A = normalization['molecular_system']

lookup = {(int(row.group_index), row.atom_name): int(index)
          for index, row in receptor.topology.atoms.iterrows()}
mapped_pairs = []
for index, row in definition['template'].topology.atoms.iterrows():
    name = row.atom_name
    if names[int(row.group_index)] == 'ARG' and name in {'NH1', 'NH2'}:
        name = 'NH2' if name == 'NH1' else 'NH1'
    source_index = lookup.get((int(row.group_index), name))
    if source_index is not None:
        mapped_pairs.append((int(index), source_index))
mapped_pairs = np.asarray(mapped_pairs, dtype=np.int64)

shell_groups = np.asarray(msm.select(
    molsys, selection=f'({receptor_selection}) within 0.5 nm without pbc of '
                      '(group_name == "EST" and chain_id == "D")', element='group'), dtype=np.int64)
shell_source_atoms = msm.select(molsys, selection=f'group_index in {shell_groups.tolist()}')
source_to_local = np.full(msm.get(molsys, n_atoms=True), -1, dtype=np.int64)
source_to_local[source_atom_indices] = np.arange(msm.get(receptor, n_atoms=True))
selected = source_to_local[shell_source_atoms]
assert np.all(selected >= 0)
inside = np.isin(mapped_pairs[:, 1], selected)
result = msm.physchem.apply_chemical_template(
    molsys_A, template=definition['template'], selection=selected,
    atom_correspondence=mapped_pairs[inside],
    context_atom_correspondence=mapped_pairs[~inside],
    template_provenance=definition['template_provenance'])
molsys_B = result['molecular_system']
assert result['report']['coverage']['scope'] == 'selected_with_context'
assert result['report']['coverage']['unmapped_template_atom_indices'].size == 9
msm.convert(molsys_B, to_form='file:h5msm', output_filename='receptor_with_prepared_shell.h5msm')
```

The primary map covers every selected atom; the context map covers other observed
reference/source atoms. Missing reference atoms can be left unmapped only when
they are not required neighbors or stereo references of the selection. Selecting
an incomplete residue instead would fail, rather than making its missing neighbors
disappear. This recipe uses an explicitly inspected name/group map for the pinned
case; it does not provide general atom matching or alias/resonance reconciliation.
Retain `source_atom_indices`, reference factory and normalization reports separately.

The 0.5 nm shell contains 19 whole residues; 0.4/0.6 nm variants contain 12/23.
No atom is added or moved. Only selected atom fields and incident bonds are
assigned, including peptide links crossing the selection. Unknown outside atom
fields remain unknown, and outside-only bonds remain as supplied. H5MSM retains
the historical context/assignment maps and coverage report. The 1,990-atom receptor
remains globally partial; no H geometry is generated, and full-graph recognition
still rejects it. Additional preparation, repair and consumer acceptance are
required before treating it as a complete receptor. Executed recipe and native/H5MSM
controls live in `tests/physchem/test_chemical_template_context.py`.

## Assessing excluded residue gaps

Before expanding the bounded fragment, audit the full label-chain A inventory.
Native `msm.build.add_missing_heavy_atoms()` reconstructs SER301 OG as an initial
local-template estimate, retaining observed coordinates and IDs. Its four-atom
gaps in each of LYS302 and LYS303 remain unassessed; a guessed lysine rotamer is
not a validated reconstruction. Query `get_missing_heavy_atoms()` again and retain
the warnings. This is not preparation of the complete receptor.

If you already assigned chemistry, native expansion preserves known fields and
state provenance but leaves added fields unknown and connectivity partial.
Reassess and apply your explicit chemical template after reconstruction. Named
interactions become pending for recalculation, with their definitions and axes
preserved. Under `attribute_policy='intersection'`, missing values for added
atoms cause existing B-factors or force-field atom parameters to be reported as
dropped. Use `attribute_policy='strict'` to reject such loss transactionally.
The source is unchanged in either case. The bounds above still deliberately
exclude all three residues and retain their original regression evidence.

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

(cookbook-prepared-interface)=
## Composing a prepared interface

You can compose the separately prepared receptor fragment and ligand with
`msm.merge()` and calculate interactions on that new system. This gives the
recognizers a declared chemical graph for every included atom. A selection of
participants alone does not restrict full-graph chemical recognition on the raw
complex; unprepared components can still prevent that calculation.

For the bounded 1QKU scenario above, fixed-state H addition followed by merging
produces 4,047 atoms: 4,003 in the receptor fragment and 44 in EST. All 1,995
deposited heavy-atom coordinates remain unchanged. The included chemical graph
has 4,088 bonds and 32 aromatic rings. Connectivity completeness applies to
this new system, not to the original 6,596-atom complex or excluded residues.

The following continuation assumes `molsys_A` and `molsys_B` are those prepared,
H-added native systems, and `molsys` is the original observed complex. Retain
each extraction's source atom indices and extend its map with `-1` for each
appended H. The supplied `atom_source_indices_A` and `atom_source_indices_B`
therefore map every local atom, including generated atoms, to that same original
index domain. String atom IDs can repeat across independently expanded systems;
IDs do not establish this correspondence. Use matching structures and compatible
states when merging, and retain the separate preparation reports.

```python
import numpy as np

n_A = molsys_A.get_n_atoms()
n_B = molsys_B.get_n_atoms()
molsys_C = msm.merge([molsys_A, molsys_B], to_form='molsysmt.MolSys')
indices_A = np.arange(n_A)
indices_B = np.arange(n_A, n_A + n_B)
analysis = msm.interactions.hydrophobic.get_hydrophobic_interactions(
    molsys_C, selection=indices_A, selection_2=indices_B,
    selection_mode='between', structure_indices=[0], pbc=False,
)

# Declare the inspected local-to-source map through the typed public form.
payload = msm.convert(analysis, to_form='molsysmt.InteractionsDict')
payload.data['atom_source_indices'] = np.concatenate(
    [atom_source_indices_A, atom_source_indices_B]
)
payload.data['source_n_atoms'] = molsys.get_n_atoms()
payload.data['source_id'] = 'rcsb:1QKU:deposited-atom-order'
analysis = msm.convert(payload, to_form='molsysmt.Interactions')
molsys_C.interactions = {**molsys_C.interactions, 'hydrophobic': analysis}

visible = analysis.query(
    structure_indices=[0], atom_indices=indices_B, mode='incident'
)
msm.convert(molsys_C, to_form='file:h5msm',
            output_filename='prepared_interface.h5msm')
```

This source label is a caller declaration, not authentication. Typed conversion
checks map bounds and uniqueness of known source indices; it retains the local
participant indices, evaluated coverage and original producer versions. A
missing source index (`-1`) does not make a generated atom an observed atom.

The offline control produces 12 hydrophobic observations using the default
`atom_pair_distance` method and its chemical profile. H-bond detection with
`method='donor_acceptor_distance_angle', profile='smarts_donor_acceptor'` and
π–π detection with `method='plane_angle_intersection', profile='smarts_5_6'`
produce zero observations for this locally H-added geometry, with structure 0
explicitly evaluated. Store these as separate named analyses using the same
source map; zero observations must remain distinct from an unevaluated structure.
Local H geometry has not been refined in the environment, so these counts do not
establish biological absence. Future refinement is tracked by
[MolSysMT #323](https://github.com/uibcdf/molsysmt/issues/323).

The native and H5MSM-input controls verify queries by structure and atoms, between
selections, independent hydrophobic pair distances, named-result roundtrips,
occurrence indices, source maps, parameters, units and producer attribution in
`tests/physchem/test_chemical_template_receptor.py`. H5MSM saves the new system
and its analyses, including histories of applied chemical templates; it does not
reinsert chemistry into the raw complex or attach detached H-placement reports.
Complete receptor preparation and consumer
biological acceptance remain separate work.

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
