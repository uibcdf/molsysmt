(Tutorial_Chemical_Templates)=
# Assessing and applying chemical templates

*Transferring declared chemical assignments through an explicit atom correspondence.*

Use `msm.physchem.assess_chemical_template()` to check a prepared template against
one isolated component, either as the full input or selected inside a larger
system. Use `msm.physchem.apply_chemical_template()` to fill missing
assignments on an independent native system after the same preflight succeeds.
Both experimental functions accept supported molecular forms. Native templates
need neither coordinates nor RDKit. Converting other forms retains their existing
dependency requirements.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

- {func}`molsysmt.physchem.assess_chemical_template`
- {func}`molsysmt.physchem.apply_chemical_template`
- {func}`molsysmt.physchem.get_peptide_chemical_template`
- {func}`molsysmt.physchem.normalize_aromatic_bond_orders`
:::

## Declaring the correspondence

`atom_correspondence` is an exhaustive integer array of shape `(n_selected_atoms, 2)`.
Column zero contains **template atom indices**; column one contains **source atom
indices**. Both refer to the full respective inputs, starting at zero. Each atom
in the selected source scope and every template atom occurs exactly once in its
column, including every explicit H atom. Names and
IDs do not substitute for indices. An identity map is valid only when you know
the orders correspond; neither function performs automatic matching.

Elements and declared isotopes must agree. The default
`connectivity_policy='require_same_graph'` requires the same stored covalent graph
and one connected component within the scope. The default `selection='all'`
retains the whole-input contract. You can extract a ligand and retain its source
map, or explicitly select its complete stored component in the original complex.
Explicit template completion can add missing covalent edges as described below.
Dative relationships, component-cut bonds and unexpected source edges remain
outside the supported repair boundary.

(Tutorial_Selected_Chemical_Template)=
## Updating a selected component

Pass `selection` and optionally `syntax` to both assessment and application when
the source contains other components. Numeric selections are deduplicated;
strings use topological selections in the requested chemical state. The map's
second column still uses **full source indices**, not indices in an extracted
ligand. Every template atom and exactly the selected source atoms must be mapped.
Nested selections, mismatched coverage and stored relationships crossing the
selection are rejected or remain explicitly unassessed before any application.
Coordinate-dependent selections are outside this coordinate-independent operation.

Only selected atom assignments and internal bond fields can be filled. Unrelated
atoms and relationships, other states, original atom order/IDs and all structures
remain unchanged. A proper subset retains the source state's global connectivity
completeness, including `partial` or `unavailable`. The detached report records
`source.atom_indices`, original completeness, `coverage.scope`, boundary evidence
and result completeness. The initial subset route requires the same stored internal atom pairs; even
`complete_from_template` leaves missing selected bonds unassessed. Complete an
extracted component instead. Global component rebuilding after new edges needs
separate preservation of unrelated component metadata. Scoped template evidence
does not become a new native
per-component completeness store. H5MSM persists the updated assignments and
global status, while this preparation report remains a separate record.

Changing chemistry conservatively invalidates named interaction coverage on the
returned copy. Repeating an unchanged application retains coverage. Applying
chemistry to a ligand does not make the complete raw complex recognizable; the
unprepared receptor and other components still need their own assessments.
An extraction preserves its parent's conservative completeness flag. You can
explicitly reassess/apply the same exhaustive template to the extracted component
to justify its whole-input connectivity coverage. See the
{ref}`full-complex recipe <cookbook-component-chemical-transfer>` for map composition.

`template_provenance` must be JSON compatible and declare nonempty `identity`,
`version`, `source_uri`, `checksum` and `hydrogen_policy` strings. Supply the
identity and checksum of the actual template you used. These values record your
declaration; MolSysMT does not authenticate the template or verify the checksum.

| Hydrogen policy | Required interpretation |
| --- | --- |
| `explicit_atoms` | Both stored virtual H-count fields are zero; observed H atoms participate in the map. |
| `stored_counts` | The template explicitly declares virtual/implicit H counts over its existing atoms. No H atoms or coordinates are generated. |

A hydrogen-complete template cannot map onto a heavy-only source. Choose an
explicitly prepared heavy-only template with `stored_counts` if that is the
chemical state you intend to transfer. Counts do not supply donor–H geometry.

(Tutorial_Normalize_Aromatic_Bond_Orders)=
## Normalizing declared aromatic bond orders

Use `msm.physchem.normalize_aromatic_bond_orders(molsys)` when already declared
aromatic bonds carry integer single/double orders and your chosen template uses
fractional orders. This experimental representation operation returns a copy in
`molecular_system` and a detached `report`. It replaces integer orders only on
bonds marked `is_aromatic=True`, setting their fractional order to 1.5. Unknown
aromatic flags remain unknown; it does not perceive aromaticity or certify valence.

```python
import molsysmt as msm
molsys = msm.physchem.get_peptide_chemical_template(
    ['PHE'], 'ammonium', 'carboxylate')['template']
normalization = msm.physchem.normalize_aromatic_bond_orders(molsys)
assert normalization['report']['status'] == 'unchanged'
assert normalization['report']['bonded_atom_pairs'].shape == (6, 2)
```

Native systems, topologies and chemical-state domains do not require RDKit.
Other forms must supply the stored declarations through their existing adapters.
Choose a state index or the resolved reference; coordinates do not select states
in this operation. Nonselected states and the source remain unchanged. A known
nonaromatic endpoint, unsupported bond stereo, noncovalent aromatic relationship,
invalid endpoints or incompatible orders cause an error before mutation.

The report keeps source bond indices/pairs, original orders, changed indices,
unknown aromatic flags and producer version. Bond orders are dimensionless.
Normalization retains coordinates and units, atom identity, all atom assignments
and connectivity completeness. Changed chemistry invalidates named interactions
on the returned copy. Repeating it on a canonical representation makes no changes.
H5MSM stores normalized chemical values; retain this report separately to recover
the original encoding. Guanidinium/carboxylate resonance and unknown chemistry
require separate decisions; template assessment still rejects known conflicts.

(Tutorial_Get_Peptide_Chemical_Template)=
## Constructing a peptide template

`msm.physchem.get_peptide_chemical_template()` constructs one linear peptide's
heavy graph from bundled, versioned residue fragments. You supply ordered states
and both terminal choices. It returns a coordinate-free native template,
`template_provenance` and a construction report. No source atoms are matched,
no coordinates generated, and no chemical state chosen from pH or a residue alias.

```python
import molsysmt as msm

peptide_definition = msm.physchem.get_peptide_chemical_template(
    ['GLY', 'GLY'], n_terminal_state='ammonium',
    c_terminal_state='carboxylate')
assert peptide_definition['template'].get_n_atoms() == 9
assert peptide_definition['report']['n_stored_hydrogens'] == 8
assert peptide_definition['report']['n_indexed_hydrogens'] == 0
```

This declares C4H8N2O3 with charged termini. The eight H are counts on its nine
heavy atoms, not coordinate rows. The template always contains a terminal OXT;
an absent source OXT or sidechain atom requires a separate repair before an
exhaustive correspondence can succeed.

Supported exact, case-sensitive states are:

| Residue family | Explicit state names |
| --- | --- |
| Histidine | HID (ND1 H), HIE (NE2 H), HIP (both H, charge +1). HIS is ambiguous and rejected. |
| Aspartate / glutamate | ASP / GLU (carboxylate, −1), ASH / GLH (carboxylic acid, neutral). |
| Lysine | LYS (ammonium, +1), LYN (amine, neutral). |
| Cysteine | CYS (thiol), CYM (thiolate, −1), CYX (declared disulfide). |
| Arginine | ARG (guanidinium, +1). |
| Other supported states | ALA, ASN, GLN, GLY, ILE, LEU, MET, PHE, PRO, SER, THR, TRP, TYR and VAL. |

The first amino terminus is explicitly `ammonium` or `amine`; the last carboxyl
terminus is `carboxylate` or `carboxylic_acid`. Proline uses the corresponding
secondary-amine H inventory. These choices apply even for one residue. This
factory does not add caps, model an unobserved biological terminus or select
histidine tautomers from their environment.

For disulfides, declare pairs of **template group indices**, starting at zero:

```python
disulfide_definition = msm.physchem.get_peptide_chemical_template(
    ['CYX', 'GLY', 'CYX'], n_terminal_state='ammonium',
    c_terminal_state='carboxylate', disulfide_group_pairs=[[0, 2]])
assert disulfide_definition['report']['disulfide_bond_pairs'].shape == (1, 2)
```

Every CYX must be paired exactly once; CYS/CYM cannot be silently turned into
CYX. Sulfur proximity is not a bond declaration. Pair order is normalized for a
deterministic result. The report gives actual template atom pairs for peptide and
disulfide links, with empty int64 arrays of shape `(0, 2)` when appropriate.

The factory uses a pinned Meeko data snapshot and native assembly; neither Meeko
nor RDKit is needed at runtime. Snapshot identity/hash, the curated fragment hash,
offline curation software and the requested assembly are retained separately.
`checksum` hashes the declared assembled graph definition, not an H5MSM file.
The copied/derived source data retain their separate upstream license under
`molsysmt/data/databases/peptide_templates/`. Backbone amide/carboxyl conjugation
is declared during assembly; other assignments use the curated fragment model.

**Stereochemistry remains unspecified**, including residue enantiomers and
peptide cis/trans: this factory does not certify an L peptide. An already declared
source stereo assignment needs a compatible, explicitly prepared template rather
than being overwritten. Modified residues, caps, cyclic backbones, arbitrary
crosslinks and multiple chains are outside this factory's current scope.

Supply `peptide_definition['template']` and its `template_provenance` to the
existing assessment/application tools, together with your independently accepted
exhaustive map. Their source remains form agnostic. Counts alone still cannot
supply donor-H geometry; use the separately chosen fixed-state H operation after
chemical preparation and pose validation.

Successful factory construction credits MolSysMT as executed software and the
reference snapshot as data in an optional Ackredit scope. RDKit's offline curation
version is provenance, not an executed runtime credit. The report/provenance stay
detached sidecars; H5MSM stores chemical values and states.

## Preparing an independent example

This small methanol control uses optional RDKit **only to construct the prepared
template**. Its atom order is C, O, three carbon H atoms, then the oxygen H atom.
The source below independently declares those atoms and edges without chemical
orders. You can instead load a prepared native template supplied by another tool.

```python
import numpy as np
import molsysmt as msm
from rdkit import Chem, rdBase

template = Chem.AddHs(Chem.MolFromSmiles('CO'))
builder = msm.MolSysBuilder()
for index, element in enumerate(['C', 'O', 'H', 'H', 'H', 'H']):
    builder.add_atom(atom_id=str(index), atom_name=f'{element}{index}',
                     atom_type=element)
for first, second in [(0, 1), (0, 2), (0, 3), (0, 4), (1, 5)]:
    builder.add_bond(first, second)
builder.set_coordinates(msm.pyunitwizard.quantity(
    np.arange(36, dtype=float).reshape(2, 6, 3) / 10, 'angstrom'))
molsys = builder.build()
correspondence = np.column_stack((np.arange(6), np.arange(6)))
provenance = dict(
    identity='methanol illustrative RDKit template', version=rdBase.rdkitVersion,
    source_uri='smiles:CO', checksum='caller-declared illustrative fixture',
    hydrogen_policy='explicit_atoms')
assessment = msm.physchem.assess_chemical_template(
    molsys, template=template, atom_correspondence=correspondence,
    template_provenance=provenance)
assert assessment['status'] == 'compatible'
```

The illustrative coordinates are a preservation control, not an optimized
conformer or a docking pose. The assessment does not inspect coordinates.

## Completing a declared graph

Choose `connectivity_policy='complete_from_template'` explicitly when the source
has missing edges and declares incomplete or unknown connectivity. The template
must still declare a complete connected covalent graph over **all mapped atoms**.
The source may contain disconnected fragments of that graph. A source claiming
complete connectivity cannot have its missing edges silently reconciled.

For example, remove the oxygen–hydrogen bond from the independent source above:

```python
molsys_fragmented = molsys.copy()
molsys_fragmented.topology.remove_bonds([4])
completion = msm.physchem.assess_chemical_template(
    molsys_fragmented, template=template, atom_correspondence=correspondence,
    template_provenance=provenance, connectivity_policy='complete_from_template')
assert completion['status'] == 'compatible'
assert len(completion['added_bonds']) == 1
assert completion['added_bonds'][0]['atom1_index'] == 1
assert completion['added_bonds'][0]['atom2_index'] == 5
completed = msm.physchem.apply_chemical_template(
    molsys_fragmented, template=template, atom_correspondence=correspondence,
    template_provenance=provenance, connectivity_policy='complete_from_template')
assert completed['molecular_system'].get_n_atoms() == 6
assert msm.get(completed['molecular_system'], n_bonds=True) == 5
```

The operation adds declared edges, not atoms or coordinates. It retains existing
edge evidence and records new edges as `user_defined`, backed by your detached
template declaration. Known chemical conflicts still fail before application.
The same boundary can transfer a caller-prepared peptide or disulfide link; it
does not choose terminal/protonation states or supply curated polymer templates.

New edges can reorder the canonical bond table. In an applied report,
`source_bond_correspondence` is an integer array `(n_original_bonds, 2)` mapping
old to final bond indices. Each `added_bonds` record contains the original
`template_bond_index`, mapped atom pair, chemical fields and final `bond_index`.
After adding edges, the selected state's components are rebuilt: component
indices and IDs can change, and component names/types are left unknown. Stable
atom order, group/molecule inventory and other states remain unchanged. Retain
the map when referring to original bond indices after this operation.

## Applying and inspecting the result

```python
original_coordinates = msm.pyunitwizard.get_value(
    molsys.structures.coordinates, to_unit='nm').copy()
result = msm.physchem.apply_chemical_template(
    molsys, template=template, atom_correspondence=correspondence,
    template_provenance=provenance)
prepared = result['molecular_system']
assert prepared is not molsys
assert result['report']['status'] == 'applied'
np.testing.assert_array_equal(
    msm.pyunitwizard.get_value(prepared.structures.coordinates, to_unit='nm'),
    original_coordinates)
sites = msm.physchem.get_hbond_sites(prepared)
assert sites['donor_hydrogen_pairs'].tolist() == [[1, 5]]
assert sites['acceptor_atom_indices'].tolist() == [1]
```

The source and template remain unchanged. The result preserves source atom
order, string IDs, membership, all coordinate structures, units, box and structure/state
associations. Only absent supported chemical fields in the chosen state are
filled. Existing mechanical parameters are copied, without reparameterization.

If chemistry or its completeness declaration changes, every named interaction
analysis on the returned copy loses its observations and evaluated-structure coverage.
The names remain available for recalculation. The original system's analyses
remain intact. `report['invalidated_analysis_names']` identifies the affected
analyses. An identical application with no chemical changes preserves analyses.

## Choosing states and interpreting failures

Choose source and template states independently with `chemical_state=index` and
`template_chemical_state=index`. The default `'reference'` uses each input's
resolved reference; `None` has the same meaning. Ambiguous references are
`unassessed`, and invalid explicit indices raise. `'structure'` is unavailable:
this operation selects chemical states independently of structures. Unselected states
and existing structure-to-state associations remain unchanged.

The assessment uses schema `molsysmt.chemical_template@1`:

| Status | Meaning |
| --- | --- |
| `compatible` | All supported correspondence checks passed and required template fields are declared. |
| `conflict` | An explicit assignment, graph or element correspondence conflicts. |
| `unassessed` | Required information, supported scope or representation normalization is unavailable. |
| `applied` | Application completed on an independent system. |

Malformed maps or provenance raise argument diagnostics. An unresolved assessment
is inspectable; application raises `msm.StructuralInconsistencyError` with the
detached assessment in `error.report`. Inspect indexed `issues` and their
`reason_code`, `side`, `field` and `diagnostic_code`. Failure changes neither input.

Missing assignments are distinguished from declared single bonds or neutral
charges. Existing explicit values cannot be overwritten. Differing aromatic/
Kekule encodings and stereo-reference encodings requiring normalization stay
unassessed; equality of chemical states is not guessed. Supported stereo-reference
atoms are remapped with the orientation of each stored bond endpoint.

## Retaining provenance and saving chemistry

The report retains the exact detached map, original state indices, assigned and
preserved fields, graph/completeness justification, template declaration and
producer version. Formal charge uses elementary charge units. Stored inferred
edge evidence remains inferred after assignment; it does not become an explicit
bond declaration. `unassessed_checks` records limits including valence, environmental
protonation, stereogenicity, conformer quality and force-field/docking readiness.

Public conversion of the prepared system to H5MSM 0.5 preserves the chemical
values, states and structures. **The preparation report is currently returned
separately and is not embedded in MolSys or H5MSM.** Keep it with your workflow
record if you need template-specific provenance. The report contains NumPy arrays
and is not directly JSON serializable.

After preparing components separately, you can use `msm.merge()` to construct a
new analysis system. Its atom indices differ from the original complex; retain
the extraction maps and mark generated atoms as having no deposited source index.
Full-graph recognizers can then examine the included declared chemistry before
filtering an interface. The {ref}`prepared-interface recipe
<cookbook-prepared-interface>` demonstrates named interactions and H5MSM
roundtrips. This does not extend the exhaustive template-map contract to partial
assignment on an arbitrary complex, certify excluded chemistry or refine H
geometry in the environment.

Successful application returns portable executed-MolSysMT attribution and credits
it inside an optional Ackredit scope. Assessment and failed application do not
credit completed preparation. Loading chemistry or inspecting a saved report
does not repeat the calculation. Optional Ackredit absence/failure cannot change
the scientific result. Template declarations and software credit have distinct
roles; template correctness is the responsibility of its selected provider.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Chemical_Readiness` for stored-field inspection.
- {ref}`Cookbook_Applying_Chemical_Templates` for the workflow and save boundary.
- {ref}`Tutorial_Get_CIP_stereochemistry` for explicit stereochemical analysis.
:::
