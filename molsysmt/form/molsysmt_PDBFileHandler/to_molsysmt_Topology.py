from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import pandas as pd
import numpy as np

@digest(form='molsysmt.PDBFileHandler')
def to_molsysmt_Topology(item, atom_indices='all', get_missing_bonds=True, skip_digestion=False):

    from molsysmt.native import Topology
    from molsysmt.build import get_missing_bonds as _get_missing_bonds

    tmp_item = Topology()

    atom_id_array = []
    atom_name_array = []
    group_index_array = []
    group_id_array = []
    group_name_array = []
    chain_index_array = []
    chain_name_array = []

    occupancy_array = []
    alternate_location_array = []

    group_index = -1
    former_group_id = None

    chain_index = -1
    former_chain_name = None
    aux_dict_chain = {}



    for atom_record in item.entry.coordinate.model[0].record:

        atom_id_array.append(atom_record.serial)
        atom_name_array.append(atom_record.name)

        occupancy_array.append(atom_record.occupancy)
        alternate_location_array.append(atom_record.altLoc)

        if former_group_id!=atom_record.resSeq:
            group_id_array.append(int(atom_record.resSeq))
            group_name_array.append(atom_record.resName)
            group_index += 1
            former_group_id = atom_record.resSeq

        group_index_array.append(group_index)

        if former_chain_name!=atom_record.chainId:
            if atom_record.chainId in aux_dict_chain:
                chain_index = aux_dict_chain[atom_record.chainId]
            else:
                chain_index += 1
                aux_dict_chain[atom_record.chainId]=chain_index
                chain_name_array.append(atom_record.chainId)

        chain_index_array.append(chain_index)

    atom_id_array = np.array(atom_id_array, dtype=int)
    atom_name_array = np.array(atom_name_array, dtype=str)
    group_index_array = np.array(group_index_array, dtype=int)
    chain_index_array = np.array(chain_index_array, dtype=int)
    group_id_array = np.array(group_id_array, dtype=int)
    group_name_array = np.array(group_name_array, dtype=str)
    chain_name_array = np.array(chain_name_array, dtype=str)

    occupancy_array = np.array(occupancy_array, dtype=float)
    alternate_location_array = np.array(alternate_location_array, dtype=str)

    alt_atom_indices = np.where(alternate_location_array!=' ')[0]
    aux_dict = {}

    if len(alt_atom_indices):

        alt_atom_names = atom_name_array[alt_atom_indices].to_numpy()
        alt_group_index = tmp_item.atoms["group_index"][alt_atom_indices].to_numpy()
        alt_chain_index = tmp_item.atoms["chain_index"][alt_atom_indices].to_numpy()
        for aux_atom_index, aux_atom_name, aux_group_index, aux_chain_index in zip(alt_atom_indices,
                                                                             alt_atom_names, alt_group_index,
                                                                             alt_chain_index):
            aux_key = tuple([aux_atom_name, aux_group_index, aux_chain_index])
            if aux_key in aux_dict:
                aux_dict[aux_key].append(aux_atom_index)
            else:
                aux_dict[aux_key]=[aux_atom_index]

    atoms_to_be_removed_with_alt_loc=[]
    for same_atoms in aux_dict.values():
        alt_occupancy = occupancy[same_atoms]
        alt_loc = alternate_location[same_atoms]
        if np.allclose(alt_occupancy, alt_occupancy[0]):
            chosen = np.where(alt_loc=='A')[0][0]
        else:
            chosen = np.argmax(alt_occupancy)
        chosen = same_atoms.pop(chosen)
        atoms_to_be_removed_with_alt_loc += same_atoms
    
    atom_id_array = np.delete(atom_id_array, atoms_to_be_removed_with_alt_loc)
    atom_name_array = np.delete(atom_name_array, atoms_to_be_removed_with_alt_loc)
    group_index_array = np.delete(group_index_array, atoms_to_be_removed_with_alt_loc)
    chain_index_array = np.delete(chain_index_array, atoms_to_be_removed_with_alt_loc)

    n_atoms = atom_id_array.shape[0]
    n_groups = group_name_array.shape[0]
    n_chains = chain_name_array.shape[0]

    tmp_item.reset_atoms(n_atoms=n_atoms)
    tmp_item.reset_groups(n_groups=n_groups)
    tmp_item.reset_chains(n_chains=n_chains)

    tmp_item.atoms.atom_id = atom_id_array
    tmp_item.atoms.atom_name = atom_name_array
    tmp_item.atoms.group_index = group_index_array
    tmp_item.atoms.chain_index = chain_index_array

    tmp_item.rebuild_atoms(redefine_ids=False, redefine_types=True)

    tmp_item.groups.group_id = group_id_array
    tmp_item.groups.group_name = group_name_array

    tmp_item.rebuild_groups(redefine_ids=False, redefine_types=True)

    tmp_item.chains.chain_name = chain_name_array

    tmp_item.rebuild_chains(redefine_ids=True, redefine_types=False )

    if get_missing_bonds:

        bonds = _get_missing_bonds(tmp_item, with_distances=True)
        bonds = np.array(bonds)
        tmp_item.reset_bonds(n_bonds=bonds.shape[0])
        tmp_item.bonds.drop(['order', 'type'], axis=1, inplace=True)
        tmp_item.bonds.atom1_index=bonds[:,0]
        tmp_item.bonds.atom2_index=bonds[:,1]

        tmp_item.rebuild_components()
        tmp_item.rebuild_molecules()
        tmp_item.rebuild_chains(redefine_ids=False, redefine_types=True)
        tmp_item.rebuild_entities()

    tmp_item = tmp_item.extract(atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item

