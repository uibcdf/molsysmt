from molsysmt._private.digestion import digest
import numpy as np
from molsysmt import pyunitwizard as puw

@digest(form='mmtf.MMTFDecoder')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    if item.num_models>1:
        print('molsys.form.mmtf_MMTFDecoder.to_molsysmt_Structures needs to be fixed')

    from molsysmt.native.structures import Structures

    # atoms, groups and bonds intra group

    n_atoms = item.num_atoms

    coordinates = np.column_stack([item.x_coord_list, item.y_coord_list, item.z_coord_list])
    coordinates = xyz.reshape([-1, item.num_atoms, 3])
    coordinates = puw.quantity(xyz, 'angstroms')
    coordinates = puw.standardize(xyz)

    atom_index_array = np.arange(n_atoms, dtype=int)
    atom_name_array = np.empty(n_atoms, dtype=object)
    atom_id_array = np.empty(n_atoms, dtype=int)
    group_index_array = np.arange(n_atoms, dtype=int)
    group_id_array = np.empty(n_atoms, dtype=int)
    chain_id_array = np.empty(n_atoms, dtype=object)

    #formal_charge_array = np.empty(n_atoms, dtype=float)

    atom_index = 0

    for mmtf_group_type, group_index, group_id in zip(item.group_type_list, range(item.num_groups), item.group_id_list):

        mmtf_group = item.group_list[mmtf_group_type]

        for atom_name, atom_formal_charge in zip(mmtf_group['atomNameList'], mmtf_group['formalChargeList']):

            atom_name_array[atom_index] = atom_name
            atom_id_array[atom_index] = item.atom_id_list[atom_index]
            #formal_charge_array[atom_index] = atom_formal_charge
            group_index_array[atom_index] = group_index
            group_id_array[atom_index] = group_id

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
    b_factor_array = puw.quantity(np.array(item.b_factor_list), unit='angstroms**2', standardized=True)
    #formal_charge_array = puw.quantity(formal_charge_array, unit='e', standardized=True)

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

    alternate_location = [{}]
    for chosen, same_atoms in zip(chosen_with_alt_loc, aux_dict.values()):
        atom_index = np.where(atom_indices_to_be_kept==chosen)[0][0]
        aux_dict={
                'alternate_location':alternate_location_array[same_atoms],
                'occupancy':occupancy_array[same_atoms],
                'b_factor':b_factor_array[same_atoms],
                'atom_id':atom_id_array[same_atoms],
                }
        alternate_location[0][atom_index]=aux_dict

    structure_id = None
    time = None


    if not is_all(structure_indices):
        xyz = xyz[structure_indices,:,:]

    if not is_all(indices):
        xyz = xyz[:,indices,:]

    return xyz


    #coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices)
    #box = get_box_from_system(item, structure_indices=structure_indices)
    #occupancy = get_occupancy_from_atom(item, atom_indices=atom_indices, structure_indices=structure_indices)
    #b_factor = get_b_factor_from_atom(item, atom_indices=atom_indices, structure_indices=structure_indices)
    #formal_charge = get_formal_charge_from_atom(item, atom_indices=atom_indices, structure_indices=structure_indices)
    #alternate_location = get_alternate_location_from_atom(item, structure_indices=structure_indices)

    #tmp_item = Structures()
    #tmp_item.append_structures(structure_id=structure_id, time=time, coordinates=coordinates, box=box,
    #        occupancy=occupancy, b_factor=b_factor, formal_charge=formal_charge, alternate_location=alternate_location)

    return tmp_item

