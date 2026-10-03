(cookbook-native-pdbqt)=
# Reading and writing prepared PDBQT

The experimental `file:pdbqt` and `string:pdbqt_text` forms read a rigid
receptor or one ligand with a balanced ROOT/BRANCH tree. They require no RDKit,
Meeko or Vina installation. A string is explicit: prepend `pdbqt_text:` to its
raw contents. Raw text without that prefix is not promised as PDBQT; its
PDB-like atom records can otherwise be confused with ordinary PDB.

## Reading explicit data

The input in this recipe is a **previously prepared** ligand. It must already
carry valid AutoDock4 labels and finite partial charges.

```python
import molsysmt as msm
from molsysmt.form.file_pdbqt import get_torsion_tree

source = 'prepared_ligand.pdbqt'
tree = get_torsion_tree(source)
molsys, report = msm.convert(source, to_form='molsysmt.MolSys',
                            discard_torsion_tree=True, return_report=True)
data = msm.get(source, element='atom', atom_type=True, atom_ff_type=True,
               partial_charge=True, coordinates=True, output_type='dictionary')
coordinates = data['coordinates']
labels = data['atom_ff_type']
charges = data['partial_charge']
```

Coordinates become native lengths through PyUnitWizard and charges are native
values in elementary charge. Atom serials become string IDs; atom indices
follow source line order, independently of serial values. Atom names,
residue/chain identity, present occupancy and B factors are retained. B factors
are explicitly read as angstrom squared and converted to native area units.
`atom_type` is a chemical element decoded from the declared AutoDock label;
`atom_ff_type` retains the label. An `A` label does not create a separate
stored aromaticity assignment.

Only BRANCH endpoints provide declared covalent bonds, with unknown orders.
The graph is marked **partial** even for a rigid receptor containing no
BRANCH records. Absence of a listed edge does not mean absence of a chemical
bond. Formal charges, aromaticity and implicit hydrogen assignments are not
inferred. Graph-dependent scientific tools requiring complete connectivity
must obtain that chemistry from another explicit source.

## Keeping the tree separately

The torsion tree has schema `molsysmt.pdbqt-torsion-tree@1`. It contains the
exact source `atom_ids` axis, packed `fragment_atom_indices` and
`fragment_offsets`, oriented `branch_atom_pairs` and `branch_fragment_pairs`,
`root_fragment_index=0`, `torsdof` and explicit evidence. Branch pairs use
**indices**, not atom serial IDs. The child endpoint belongs to the child
fragment. TORSDOF is the source value and need not equal the number of active
BRANCH records. The dictionary has detached NumPy arrays, with no hidden
mutation of the source. A rigid receptor without ROOT yields `None`.

Native MolSys has no general torsion-tree domain. A full ligand conversion
therefore requires explicit `discard_torsion_tree=True`; save the tree
separately first. Reduced Topology, Structures and MolecularMechanics
projections omit format metadata by default. Attribute queries use those
reduced projections without requiring authorization to discard an entire
MolSys result. The string adapter offers the equivalent public
`molsysmt.form.string_pdbqt_text.get_torsion_tree` tool.

## Writing supplied assignments

```python
msm.convert(molsys, to_form='roundtrip.pdbqt',
            typing_scheme='autodock4', torsion_tree=tree)
payload = msm.convert(molsys, to_form='string:pdbqt_text',
                      typing_scheme='autodock4', torsion_tree=tree)
```

The writer requires exactly one selected structure, topology, atom names,
unique canonical integer string atom IDs in `[1, 99999]`, explicit partial
charges and supported AutoDock4 labels matching the chemical elements. Supply
`typing_scheme='autodock4'` explicitly. `torsion_tree=None` requests rigid
receptor layout; a supplied tree requests ligand layout. Do not omit a saved
ligand tree when you intend to preserve its flexibility.

The tree must partition the selected atom inventory, connect every fragment
to ROOT without cycles, and match the **exact atom ID order**. If complete
native chemistry is present, branches and rigid fragments are checked against
that graph using {func}`molsysmt.topology.get_rigid_fragments`. The writer
neither infers nor chemically classifies rotatable bonds.

Serialization converts lengths explicitly to angstroms, including under a
non-default unit policy. Coordinates and charges use three decimal places;
occupancy and B factors use two. Rooted tree traversal may reorder atoms;
retained serial IDs provide correspondence. Output atom records use ATOM.
Validation finishes before opening the destination. Unsupported assignments,
field overflows, missing data and stale trees raise clear errors.

## Hydrogen and loss policy

Every source hydrogen is retained. There is **no** automatic preparation,
nonpolar hydrogen merging, charge aggregation, label assignment or protonation.
Merging is a separate future preparation operation with an explicit projection
map, tracked in [MolSysMT #223](https://github.com/uibcdf/molsysmt/issues/223).
AutoDock charge/type assignment and chemical torsion perception remain separate
work in [#222](https://github.com/uibcdf/molsysmt/issues/222) and
[#224](https://github.com/uibcdf/molsysmt/issues/224).

A native projection drops arbitrary REMARK records and the ATOM/HETATM record
kind. Writing native data cannot preserve the complete chemical graph, bond
orders, general mechanics settings, structures beyond one frame, or named
interactions. Inspect {func}`molsysmt.basic.get_conversion_report` or use
`return_report=True`. `strict=True` rejects known losses; authorization to
omit a tree does not disable strict mode. Reports are conservative and do not
claim exhaustive auditing of native PDBQT output. H5MSM 0.5 does not persist
MolecularMechanics; storing the native MolSys there does not preserve the
PDBQT labels and charges for subsequent PDBQT serialization.

File/string identity bridges preserve the original payload, including remarks,
trees, line endings and atom order. Rigid subsets are supported through native
projection. Tree subsets require explicit remapping through the native writer;
the adapter rejects implicit tree projection. Flexible-receptor BEGIN_RES,
MODEL ensembles, alternate locations, insertion codes, macrocycle glue types,
hydrated-ligand pseudoatoms and custom labels remain unsupported.

## Format references

The supported layout follows the
[AutoDock4.2.6 manual](https://autodock.scripps.edu/wp-content/uploads/sites/56/2021/10/AutoDock4.2.6_UserGuide.pdf)
and was checked against [Vina's PDBQT parser](https://github.com/ccsb-scripps/AutoDock-Vina/blob/develop/src/lib/parse_pdbqt.cpp).
These are format references, not method names or required software providers.
