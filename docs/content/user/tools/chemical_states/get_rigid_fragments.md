(Tutorial_Rigid_Fragments)=
# Deriving rigid fragments

Use {func}`molsysmt.chemical_states.get_rigid_fragments` to partition a complete
covalent graph at explicitly chosen source **bond indices**. This identifies
connected fragments after those cuts; chemical rotatable-bond classification
is provided separately by {func}`molsysmt.chemical_states.get_rotatable_bonds`.

```python
import molsysmt as msm
molsys = msm.ChemicalStates(n_atoms=4)
molsys.append_state()
molsys.add_bonds([[0, 1], [1, 2], [2, 3]])
msm.set(molsys, element='bond', bond_type='covalent')

# This example declares all bonds, not an incomplete subset.
columns = msm.convert(molsys, to_form='molsysmt.ChemicalStatesDict')
columns.data['states'][0]['connectivity_completeness'] = 'complete'
molsys = msm.convert(columns, to_form='molsysmt.ChemicalStates')
fragments = msm.chemical_states.get_rigid_fragments(molsys, bond_indices=[1])
assert fragments['fragment_atom_indices'].tolist() == [0, 1, 2, 3]
assert fragments['fragment_offsets'].tolist() == [0, 2, 4]
assert fragments['atom_fragment_indices'].tolist() == [0, 0, 1, 1]
assert fragments['fragment_pairs'].tolist() == [[0, 1]]
```

The input may be any supported form carrying the required complete chemical
connectivity, including standalone `ChemicalStates` and `ChemicalStatesDict`.
A format that loses completeness metadata must supply it explicitly before
this operation; the function does not assume that its listed bonds are all
bonds. Here the complete-graph declaration is made in the public typed transport
payload, then validated by conversion back to `ChemicalStates`. Adding bonds
alone declares partial connectivity. Declare completeness only when you know
the entire graph; `Topology` stores the stable inventory and has no chemical
attributes. `chemical_state` selects one state, and `structure_indices` resolves
state assignments when `chemical_state='structure'`. Coordinates are unused.

Memberships are packed int64 arrays with offsets. Source atom and bond indices
are retained; fragment indices are assigned by their smallest source atom
index. Disconnected components and isolated atoms become separate fragments.
Repeated cuts are deduplicated. An empty atom domain gives offsets `[0]`,
empty memberships and branch arrays of shape `(0, 2)`.

Every chosen bond must be covalent and a bridge in the **original** graph.
Ring bonds fail even when several simultaneous ring cuts would disconnect the
graph. Dative bonds, invalid indices and incomplete graphs also fail. No
chemical state or coordinate array is changed. This tool does not choose a
root, declare TORSDOF, or construct PDBQT records.

:::{seealso}
{func}`molsysmt.chemical_states.get_covalent_blocks` for general hypothetical bond cuts;
{ref}`cookbook-native-pdbqt` for the separate, declared PDBQT torsion tree.
:::
