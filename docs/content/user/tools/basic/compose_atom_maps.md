(Tutorial_Compose_Atom_Maps)=
# Composing atom maps

*Keeping declared atom correspondence across preparation and lossy exports.*

{func}`molsysmt.basic.compose_atom_maps` joins completed operation reports in
their actual execution order. It is experimental and performs index arithmetic;
it does not match molecules, identify atoms by proximity or generate coordinates.
The typed `molsysmt.atom_map@1` result uses one-dimensional NumPy arrays and a
small list of normalized stages. It never creates an atom-pair matrix.

For an explicit export rename, use
{func}`molsysmt.build.project_atom_names` and insert its report at the actual
renaming step. Original and projected labels remain separate; selected/renamed
source indices survive typed stage normalization and JSON restoration.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

{func}`molsysmt.basic.compose_atom_maps`
:::

## Reading direct correspondence

A generated atom can have coordinates without an atom index in the original
system. Here one operation adds an atom, and another removes and reorders atoms.
These small records explicitly declare the axes; they are not molecular forms.

```python
import molsysmt as msm

addition = dict(schema='molsysmt.atom_map@1', n_source_atoms=2, n_output_atoms=3,
    source_to_output_atom_indices=[0, 1], output_to_source_atom_indices=[0, 1, -1])
selection = dict(schema='molsysmt.atom_map@1', n_source_atoms=3, n_output_atoms=2,
    source_to_output_atom_indices=[1, -1, 0], output_to_source_atom_indices=[2, 0])
mapped = msm.basic.compose_atom_maps([addition, selection])
assert mapped['source_to_output_atom_indices'].tolist() == [1, -1]
assert mapped['output_to_source_atom_indices'].tolist() == [-1, 0]
assert mapped['generated_output_atom_indices'].tolist() == [0]
```

Both direct maps use `-1` for absent correspondence. Mask that value before
indexing an array: NumPy's ordinary `array[-1]` means its last row, not absence.
Source/output IDs remain string labels; no ID is interpreted as an index.

## Separating fusion from positions

`source_to_representative_atom_indices` is a **separate** array. An original H
merged into a retained atom has no direct coordinate correspondence, while this
array can identify the final atom representing its contribution. This is not a
hydrogen position. Repeated merges follow the representative; if that atom is
later omitted, the original contribution has no final representative either.
The earlier merge evidence remains in the normalized stages.

`source_atom_status` describes the final result: `retained`, `merged` or
`omitted`. `generated_output_atom_indices` identifies final atoms with no
pre-operation source index. The tool does not add up or calculate new charges.
Stage charge totals, conservation/rounding bounds and `charge_transfers` retain
their original operation domains and
explicit `charge_unit='elementary_charge'`; transfers from different stages
must not be summed as if they were independent original atoms.

## Following a preparation workflow

This executable example uses optional RDKit to prepare methanol and its H
coordinates. The map-composition tool itself uses no chemical engine. The
single rigid ROOT is a correspondence demonstration, not a docking protocol.

```python
import numpy as np
from rdkit import Chem

molecule = Chem.MolFromSmiles('CO')
conformer = Chem.Conformer(2)
conformer.SetPositions(np.array([[0., 0., 0.], [1.4, 0., 0.]]))
conformer.Set3D(True)
molecule.AddConformer(conformer)
molsys = msm.convert(molecule, to_form='molsysmt.MolSys')
msm.set(molsys, element='atom', atom_id=['17', '3'])
added = msm.build.add_missing_hydrogens(molsys, pH=None, engine='RDKit',
    mode='fixed_chemical_state', return_report=True)
molsys = msm.build.assign_autodock_atom_types(added['molecular_system'],
    typing_scheme='autodock4')
molsys = msm.build.assign_partial_charges(molsys, method='gasteiger_marsili')
projected = msm.build.merge_nonpolar_hydrogens(molsys,
    typing_scheme='autodock4', return_report=True)
molsys = projected['molecular_system']
tree = dict(schema_version='molsysmt.pdbqt-torsion-tree@1',
    atom_ids=molsys.topology.atoms.atom_id.to_numpy(),
    fragment_atom_indices=np.array([1, 0, 2]), fragment_offsets=np.array([0, 3]),
    branch_atom_pairs=np.empty((0, 2), dtype=int),
    branch_fragment_pairs=np.empty((0, 2), dtype=int), root_fragment_index=0, torsdof=0)
text, exported = msm.convert(molsys, to_form='string:pdbqt_text',
    typing_scheme='autodock4', torsion_tree=tree, return_atom_map=True)
poses = msm.form.string_pdbqt_text.read_poses(text, molsys, exported, return_report=True)
lineage = msm.basic.compose_atom_maps([
    added['report'], projected['report'], exported, poses['report']])
assert lineage['n_source_atoms'] == 2
assert lineage['output_to_source_atom_indices'].tolist() == [0, 1, -1]
assert lineage['generated_output_atom_indices'].tolist() == [2]
assert len(lineage['stages']) == 4
```

The surviving polar H has a real returned position and no original heavy-only
source index. The generated nonpolar H were merged; their source-stage parent
pairs and charge-transfer evidence remain explicit. None receives its parent's
position or an invented original ID/index.

The supported completed report schemas are `molsysmt.terminal_attachment@1`,
`molsysmt.hydrogen_addition@1`, `molsysmt.atom_projection@1`,
`molsysmt.atom_export@1`, `molsysmt.pdbqt_pose_read@1` and `molsysmt.atom_map@1`.
Pass reports, not the enclosing `molecular_system`/`report` return dictionaries.
For a pose-read stage, the sequential input is the **PDBQT written order** and
the output is the reader's native atom order. This adaptation also works when
the writer selected fewer atoms than the known source. Include its writer map;
the reader's source-to-output array alone uses a different source domain.

## Validating and saving maps

Adjacent counts and available ordered IDs/names must agree. The pose stage's
declared export SHA-256 must match the preceding writer binding when supplied.
These checks validate declared axes, not authenticity or common origin. Missing
labels are not invented; unknown labels cannot prove identity. Intentional
renaming needs its own declared identity-index stage carrying old source labels
and new output labels. Chemistry changes and structure selections are outside
this atom-only map; keep the original reports for those domains.

You can append stages to an existing composed map. Its stage lineage is flattened
and checked against its aggregate arrays before use. Original inputs remain
unchanged, and the result owns detached arrays/metadata. NumPy arrays serialize
to JSON lists and are restored by this same typed boundary:

```python
import json

encoded = json.dumps(lineage, default=lambda value: value.tolist())
restored = msm.basic.compose_atom_maps([json.loads(encoded)])
assert restored['output_to_source_atom_indices'].tolist() == [0, 1, -1]
```

Normalized stages preserve method/engine/parameters, software, references and
attribution when present, plus local map and merge/creation evidence. Writer
stages retain ordered ROOT members, first ROOT atom and oriented source branches
on that stage's input axis; the typed torsion tree uses its written output axis.
The existing PDBQT tree validator checks that representation without inferring
chemical connectivity. Original structure-selection fields remain stage-local
provenance; this atom-only tool does not compose those structure axes. They do
not embed coordinates or the full readiness/inventory reports. No original
scientific calculation is credited as running again. Keep the original records
for complete preparation evidence; this compact sidecar is not an H5MSM 0.5
domain and does not change the public molecular forms or the H5MSM schema.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Merge_Nonpolar_Hydrogens`
- {ref}`Tutorial_Read_PDBQT_Poses`
- {ref}`Tutorial_Fixed_State_Hydrogens`
- {ref}`cookbook-native-pdbqt`
:::
