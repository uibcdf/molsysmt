(Tutorial_Chemical_Templates)=
# Assessing and applying chemical templates

*Transferring declared chemical assignments through an explicit atom correspondence.*

Use `msm.physchem.assess_chemical_template()` to check a prepared template against
one isolated component. Use `msm.physchem.apply_chemical_template()` to fill missing
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
:::

## Declaring the correspondence

`atom_correspondence` is an exhaustive integer array of shape `(n_atoms, 2)`.
Column zero contains **template atom indices**; column one contains **source atom
indices**. Both refer to the full respective inputs, starting at zero. Each atom
occurs exactly once in each column, including every explicit H atom. Names and
IDs do not substitute for indices. An identity map is valid only when you know
the orders correspond; neither function performs automatic matching.

Elements and declared isotopes must agree. The default
`connectivity_policy='require_same_graph'` requires the same stored covalent graph
and one connected component. Extract a ligand from its complex first if you need
this bounded operation; keep the extraction's map back to the full system.
Explicit template completion can add missing covalent edges as described below.
Dative relationships, component-cut bonds and unexpected source edges remain
outside the supported repair boundary.

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
order, string IDs, membership, all coordinate frames, units, box and frame/state
associations. Only absent supported chemical fields in the chosen state are
filled. Existing mechanical parameters are copied, without reparameterization.

If chemistry or its completeness declaration changes, every named interaction
analysis on the returned copy loses its observations and evaluated-frame coverage.
The names remain available for recalculation. The original system's analyses
remain intact. `report['invalidated_analysis_names']` identifies the affected
analyses. An identical application with no chemical changes preserves analyses.

## Choosing states and interpreting failures

Choose source and template states independently with `chemical_state=index` and
`template_chemical_state=index`. The default `'reference'` uses each input's
resolved reference; `None` has the same meaning. Ambiguous references are
`unassessed`, and invalid explicit indices raise. `'structure'` is unavailable:
this operation selects chemical states independently of frames. Unselected states
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
