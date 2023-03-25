from molsysmt._private.digestion import digest
import numpy as np
from molsysmt import pyunitwizard as puw

@digest(form='mmtf.MMTFDecoder')
def to_molsysmt_MolecularMechanics(item, atom_indices='all'):

    from molsysmt.native.molecular_mechanics import MolecularMechanics

    tmp_item = MolecularMechanics()

    n_atoms = item.num_atoms

    atom_index_array = np.arange(n_atoms, dtype=int)
    atom_name_array = np.empty(n_atoms, dtype=object)
    atom_id_array = np.empty(n_atoms, dtype=int)
    group_index_array = np.arange(n_atoms, dtype=int)
    group_id_array = np.empty(n_atoms, dtype=int)
    chain_id_array = np.empty(n_atoms, dtype=object)

    formal_charge_array = np.empty(n_atoms, dtype=float)

    atom_index = 0

    for mmtf_group_type, group_index, group_id in zip(item.group_type_list, range(item.num_groups), item.group_id_list):

        mmtf_group = item.group_list[mmtf_group_type]

        for atom_name, atom_formal_charge in zip(mmtf_group['atomNameList'], mmtf_group['formalChargeList']):

            atom_name_array[atom_index] = atom_name
            atom_id_array[atom_index] = item.atom_id_list[atom_index]
            group_index_array[atom_index] = group_index
            group_id_array[atom_index] = group_id
            formal_charge_array[atom_index] = atom_formal_charge

            atom_index+=1

    count_groups = 0

    for chain_index, chain_id in zip(range(item.num_chains), item.chain_id_list):

        n_groups_chain = item.groups_per_chain[chain_index]

        for group_index in range(count_groups, count_groups+n_groups_chain):
            for atom_index in np.where(group_index_array==group_index)[0]:

                chain_id_array[atom_index] = chain_id

        count_groups+=n_groups_chain

    occupancy_array = np.array(item.occupancy_list)
    alternate_location_array = np.array(item.alt_loc_list)
    formal_charge_array = puw.quantity(formal_charge_array, unit='e', standardized=True)

    ## If atoms with alternate location the highest occupancy or A is taken
    ## other pseudo-atoms are removed

    alt_atom_indices = np.where(alternate_location_array!='')[0]

    if len(alt_atom_indices):
        alt_atom_names = atom_name_array[alt_atom_indices]
        alt_group_ids = group_id_array[alt_atom_indices]
        alt_chain_ids = chain_id_array[alt_atom_indices]
        aux_dict = {}
        for aux_atom_index, aux_atom_name, aux_group_id, aux_chain_id in zip(alt_atom_indices, alt_atom_names, alt_group_ids, alt_chain_ids):
            aux_key = tuple([aux_atom_name, aux_group_id, aux_chain_id])
            if aux_key in aux_dict:
                aux_dict[aux_key].append(aux_atom_index)
            else:
                aux_dict[aux_key]=[aux_atom_index]

    atoms_to_be_removed_with_alt_loc=[]
    chosen_with_alt_loc = []
    for same_atoms in aux_dict.values():
        alt_occupancy = occupancy_array[same_atoms]
        alt_loc = alternate_location_array[same_atoms]
        if np.allclose(alt_occupancy, alt_occupancy[0]):
            chosen = same_atoms[np.where(alt_loc=='A')[0][0]]
        else:
            chosen = same_atoms[np.argmax(alt_occupancy)]
        chosen_with_alt_loc.append(chosen)
        atoms_to_be_removed_with_alt_loc += [ii for ii in same_atoms if ii !=chosen]

    atom_indices_to_be_kept = list(set(np.arange(n_atoms))-set(atoms_to_be_removed_with_alt_loc))

    tmp_item.formal_charge = formal_charge_array[atom_indices_to_be_kept]

    del(atom_index_array, atom_name_array, atom_id_array,
            group_index_array, group_id_array, chain_id_array,
            formal_charge_array)

    return tmp_item
