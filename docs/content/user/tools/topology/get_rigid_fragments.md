(Tutorial_Rigid_Fragments)=
# Deriving rigid fragments

Use {func}`molsysmt.topology.get_rigid_fragments` to partition a complete
covalent graph at explicitly chosen source **bond indices**. This identifies
connected fragments after those cuts; chemical rotatable-bond classification
remains a separate preparation task.

```python
import molsysmt as msm
import pandas as pd
from molsysmt.native import Topology

molsys = Topology(n_atoms=4)
molsys.bonds = pd.DataFrame({
    'atom1_index': [0, 1, 2], 'atom2_index': [1, 2, 3],
    'bond_type': ['covalent'] * 3})
molsys._chemical_states[0].connectivity_completeness = 'complete'
fragments = msm.topology.get_rigid_fragments(molsys, bond_indices=[1])
assert fragments['fragment_atom_indices'].tolist() == [0, 1, 2, 3]
assert fragments['fragment_offsets'].tolist() == [0, 2, 4]
assert fragments['atom_fragment_indices'].tolist() == [0, 0, 1, 1]
assert fragments['fragment_pairs'].tolist() == [[0, 1]]
```

The input may be any supported form carrying the required complete chemical
connectivity, including standalone `ChemicalStates` and `ChemicalStatesDict`.
A format that loses completeness metadata must supply it explicitly before
this operation; the function does not assume that its listed bonds are all
bonds. `chemical_state` selects one state, and `structure_indices` resolves
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
{func}`molsysmt.topology.get_covalent_blocks` for general hypothetical bond cuts;
{ref}`cookbook-native-pdbqt` for the separate, declared PDBQT torsion tree.
:::
