(Tutorial_Read_PDBQT_Poses)=
# Reading PDBQT poses against a known source

*Loading pose coordinates without inventing missing chemistry or hydrogens.*

{func}`molsysmt.form.string_pdbqt_text.read_poses` is an experimental, resident reader for
one ligand or balanced `MODEL`/`ENDMDL` pose ensembles. Supply the known source
and its completed PDBQT export map. PDBQT alone cannot recover a full ligand
graph or the coordinates of hydrogens removed during preparation.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

{func}`molsysmt.form.string_pdbqt_text.read_poses`
:::

Positional structure indices must be plain integers. Physical quantities and
explicit dimensionless quantity wrappers are rejected before reading poses.

## Keeping the known source and export map

This executable example uses optional RDKit **during preparation**. The pose
reader itself needs no RDKit, Meeko or Vina. In a real docking workflow, retain
the prepared source and the map returned by the export sent to the engine.

```python
import numpy as np
import molsysmt as msm

molsys = msm.convert(msm.systems['caffeine']['caffeine.sdf'], to_form='rdkit.Mol')
molsys = msm.build.assign_autodock_atom_types(molsys, typing_scheme='autodock4')
molsys = msm.build.assign_partial_charges(molsys, method='gasteiger_marsili')
n = molsys.get_n_atoms()
tree = dict(
    schema_version='molsysmt.pdbqt-torsion-tree@1',
    atom_ids=molsys.topology.atoms.atom_id.to_numpy(),
    fragment_atom_indices=np.arange(n), fragment_offsets=np.array([0, n]),
    branch_atom_pairs=np.empty((0, 2), dtype=int),
    branch_fragment_pairs=np.empty((0, 2), dtype=int),
    root_fragment_index=0, torsdof=0)
text, atom_map = msm.convert(molsys, to_form='string:pdbqt_text',
    typing_scheme='autodock4', torsion_tree=tree, return_atom_map=True)
```

The example explicitly puts all atoms in one rigid ROOT, with no active
torsions. It is a reader demonstration, not a recommended docking protocol.
For torsion selection, see {ref}`Tutorial_Rotatable_Bonds`. A docking client
owns that protocol and the source/export association.

## Reading structures independently of MODEL labels

The following wraps the exported coordinates as two synthetic poses. It does
not run docking; the unequal MODEL labels demonstrate that labels are not
structure indices.

```python
body = text.removeprefix('pdbqt_text:')
pose_text = 'pdbqt_text:' + ''.join(
    f'MODEL {label}\n{body}\nENDMDL\n' for label in [9, 51])
result = msm.form.string_pdbqt_text.read_poses(pose_text, molsys, atom_map,
    structure_indices=[1, 0, 1], return_report=True)
poses, report = result['molecular_system'], result['report']
assert poses.structures.coordinates.shape == (3, 24, 3)
assert poses.structures.structure_id.tolist() == ['51', '9', '51']
assert report['input_structure_indices'].tolist() == [1, 0, 1]
assert np.allclose(msm.pyunitwizard.get_value(poses.structures.coordinates,
    to_unit='angstrom')[0], msm.pyunitwizard.get_value(
    molsys.structures.coordinates, to_unit='angstrom')[0], atol=0.00051)
```

For a path ending in `.pdbqt`, use `msm.form.file_pdbqt.read_poses`.
The text-specific function requires the `pdbqt_text:`
prefix. An unwrapped ligand produces one structure with no declared MODEL ID.
Selections preserve order and repetitions; an empty list produces coordinates
of shape `(0, n_retained_atoms, 3)`. **Every pose is validated**, including
unselected ones. Structure selection reduces coordinate storage, not parsing
work. This API does not provide streaming or a large-trajectory executor.

## Validating correspondence

The source may be any form delivering the ordered element inventory and one
complete chemical state, including a native `Topology` without coordinates.
The map must have schema `molsysmt.atom_export@1`, target `file:pdbqt`, explicit
AutoDock4 typing and a ligand torsion tree. Its counts, inverse atom axes,
source IDs/names/elements, state identity and chemical digest must agree with
the known source. The source and map must describe the same preparation stage.
JSON-decoded array lists are accepted without an external array codec.

Each pose must retain the mapped written atom order, string serial IDs, names,
elements, written charges and declared tree. Available mapped/source AutoDock
types must agree, and atom identity fields/types cannot change between poses.
Nested, repeated, incomplete or mixed MODEL records and nonfinite coordinates
are rejected. A valid source and map constitute a **declaration of
correspondence**, not authentication of the external engine's output. The
reader never discovers correspondence from spatial proximity or name guessing.

The returned atom axis is **sorted retained source indices**, not sorted
serial IDs and not necessarily PDBQT line order. The detached report has schema
`molsysmt.pdbqt_pose_read@1`:

| Field | Meaning |
| --- | --- |
| `output_to_source_atom_indices` | Source index of each returned atom. |
| `source_to_output_atom_indices` | Returned index, or -1 for an absent source atom. |
| `pdbqt_to_output_atom_indices` | Returned atom index for each PDBQT written position. |
| `input_structure_indices` | Selected pose positions, with order/repetitions. |
| `model_ids` | Selected MODEL labels, independent of their positions. |
| `omitted_source_atom_indices` | Source atoms for which the export contains no position. |
| `export_map` | Detached export map and its producer provenance. |
| `partial_charge`, `charge_unit` | Written charges in returned order, explicitly elementary charge. |
| `atom_ff_type`, `typing_scheme` | Written AutoDock4 labels in returned order. |
| `remarks` | Opaque selected remarks; no score or rank interpretation. |

The report also records the reader version, input payload SHA-256 and input
structure count. It does not identify experiments, infer rank or generate a
new chemical/charge calculation. Those operations belong to the calling
workflow.

## Handling atoms absent from the export

The default `missing_atoms='error'` rejects an export that omits source atoms.
Use `missing_atoms='omit'` only when you intend to return the **retained source
subsystem**. Omitted atoms have no coordinate row, and bonds incident on them
are removed through native extraction. Existing virtual-H declarations are
retained; this policy does not replace omitted indexed H with virtual H or
claim the result is the original full ligand. Request a report to keep the
omitted-index list and both atom axes.

Prefer {func}`molsysmt.build.merge_nonpolar_hydrogens` **before export** when
the workflow calls for merging typed nonpolar H. That prepared reduced source
has its own chemistry and charge aggregation. Use it with its own writer map;
keep the separate projection map to refer back to the earlier all-atom system.
An export map alone cannot account for atoms generated before that stage.

The reader never reuses original source positions for omitted H, places them
at their parent or performs a named reconstruction. Returned coordinates are
only those in the pose, converted from angstroms to native nm with
PyUnitWizard, independent of session units. Source structures, boxes, times,
velocities, observables and named interaction analyses are not copied.
MolecularMechanics is empty; written types/charges remain explicit report data.

The independent result can be written as H5MSM 0.5 to preserve its known
chemistry and new structures. The sidecar pose report is not a native H5MSM
domain; save it separately if needed. Generic `msm.convert()` and `msm.get()`
on PDBQT also support homogeneous MODEL ensembles, but retain only declared
partial chemistry. They do not implicitly use the known-source reader.
For selected coordinate blocks, see {ref}`Tutorial_Form_PDBQTFileHandler`.

:::{seealso}
:class: dropdown

- {ref}`cookbook-native-pdbqt`
- {ref}`Tutorial_Merge_Nonpolar_Hydrogens`
- {ref}`Tutorial_Rotatable_Bonds`
:::

File paths use {func}`molsysmt.form.file_pdbqt.read_poses`; explicit text uses
{func}`molsysmt.form.string_pdbqt_text.read_poses`. An open
{class}`molsysmt.native.PDBQTFileHandler` exposes the same operation as
`handler.read_poses()`. See {ref}`Tutorial_Form_PDBQTFileHandler` for block iteration.
