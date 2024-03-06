from molsysmt._private.digestion import digest
import numpy as np

@digest(form='file:gro')
def to_molsysmt_Topology(item, atom_indices='all', get_missing_bonds=False, skip_digestion=False):

    from molsysmt.native import Topology
    from molsysmt.build import get_missing_bonds as _get_missing_bonds

    with open(item,'r') as fff:
        
        header = fff.readline()
        n_atoms = int(fff.readline())
    
        atom_id_array = np.ndarray(shape=[n_atoms], dtype=int)
        atom_name_array = np.ndarray(shape=[n_atoms], dtype=object)
        group_index_array = np.ndarray(shape=[n_atoms], dtype=int)
        group_id_array = []
        group_name_array = []
    
        group_index = -1
        former_group_id = -1
        
        for ii in range(n_atoms):
            line = fff.readline()
    
            group_id = int(line[:5])
            if former_group_id!=group_id:
                group_id_array.append(group_id)
                group_name_array.append(line[5:10].strip())
                group_index+=1
                former_group_id=group_id
    
            atom_id_array[ii]=int(line[15:20])
            atom_name_array[ii]=line[10:15].strip()
            group_index_array[ii]=group_index
    
    group_id_array = np.array(group_id_array, dtype=int)
    group_name_array = np.array(group_name_array, dtype=object)
    n_groups = group_id_array.shape[0]

    tmp_item = Topology()

    tmp_item.reset_atoms(n_atoms=n_atoms)
    tmp_item.reset_groups(n_groups=n_groups)
    tmp_item.reset_chains(n_chains=1)

    tmp_item.atoms.atom_id = atom_id_array
    tmp_item.atoms.atom_name = atom_name_array
    tmp_item.atoms.group_index = group_index_array
    tmp_item.atoms.chain_index = np.zeros(shape=[n_atoms], dtype=int)

    tmp_item.rebuild_atoms(redefine_ids=False, redefine_types=True)

    tmp_item.groups.group_id = group_id_array
    tmp_item.groups.group_name = group_name_array

    tmp_item.rebuild_groups(redefine_ids=False, redefine_types=True)

    tmp_item.chains.iloc[0,0] = 0
    tmp_item.chains.iloc[0,1] = 'A'

    if get_missing_bonds:

        bonds = _get_missing_bonds(tmp_item, with_distances=False)
        bonds = np.array(bonds)
        tmp_item.reset_bonds(n_bonds=bonds.shape[0])
        tmp_item.bonds.drop(['order', 'type'], axis=1, inplace=True)
        tmp_item.bonds.atom1_index=bonds[:,0]
        tmp_item.bonds.atom2_index=bonds[:,1]

        tmp_item.rebuild_components()
        tmp_item.rebuild_molecules()
        tmp_item.rebuild_chains(redefine_types=True)
        tmp_item.rebuild_entities()


    tmp_item = tmp_item.extract(atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item

