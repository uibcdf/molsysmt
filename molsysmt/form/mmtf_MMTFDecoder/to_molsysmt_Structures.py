from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np
from molsysmt import pyunitwizard as puw

@digest(form='mmtf.MMTFDecoder')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    from molsysmt.native.structures import Structures
    from molsysmt.pbc import get_box_from_lengths_and_angles

    n_atoms = item.num_atoms
    n_structures = item.num_models

    if item.num_models>1:
        print('molsys.form.mmtf_MMTFDecoder.to_molsysmt_Structures needs to be fixed')
        print('to include more than a single structure')

    coordinates = np.column_stack([item.x_coord_list, item.y_coord_list, item.z_coord_list])
    coordinates = coordinates.reshape([-1, item.num_atoms, 3])
    coordinates = puw.quantity(coordinates, 'angstroms')
    coordinates = puw.standardize(coordinates)

    atom_index = np.arange(n_atoms, dtype=int)
    atom_name = np.empty(n_atoms, dtype=object)
    atom_id = np.empty(n_atoms, dtype=int)
    group_index = np.arange(n_atoms, dtype=int)
    group_id = np.empty(n_atoms, dtype=int)
    chain_id = np.empty(n_atoms, dtype=object)

    aux_atom_index = 0

    for mmtf_group_type, aux_group_index, aux_group_id in zip(item.group_type_list, range(item.num_groups), item.group_id_list):

        mmtf_group = item.group_list[mmtf_group_type]

        for aux_atom_name in zip(mmtf_group['atomNameList']):

            atom_name[aux_atom_index] = aux_atom_name
            atom_id[aux_atom_index] = item.atom_id_list[aux_atom_index]
            group_index[aux_atom_index] = aux_group_index
            group_id[aux_atom_index] = aux_group_id

            aux_atom_index+=1

    count_groups = 0

    for aux_chain_index, aux_chain_id in zip(range(item.num_chains), item.chain_id_list):

        n_groups_chain = item.groups_per_chain[aux_chain_index]

        for aux_group_index in range(count_groups, count_groups+n_groups_chain):
            for aux_atom_index in np.where(group_index==aux_group_index)[0]:

                chain_id[aux_atom_index] = aux_chain_id

        count_groups+=n_groups_chain

    occupancy = np.array(item.occupancy_list)
    alternate_location = np.array(item.alt_loc_list)
    b_factor = puw.quantity(np.array(item.b_factor_list), unit='angstroms**2', standardized=True)
    ## If atoms with alternate location the highest occupancy or A is taken
    ## other pseudo-atoms are removed

    alt_atom_indices = np.where(alternate_location!='')[0]

    if len(alt_atom_indices):
        alt_atom_names = atom_name[alt_atom_indices]
        alt_group_ids = group_id[alt_atom_indices]
        alt_chain_ids = chain_id[alt_atom_indices]
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
        alt_occupancy = occupancy[same_atoms]
        alt_loc = alternate_location[same_atoms]
        if np.allclose(alt_occupancy, alt_occupancy[0]):
            chosen = same_atoms[np.where(alt_loc=='A')[0][0]]
        else:
            chosen = same_atoms[np.argmax(alt_occupancy)]
        chosen_with_alt_loc.append(chosen)
        atoms_to_be_removed_with_alt_loc += [ii for ii in same_atoms if ii !=chosen]

    atom_indices_to_be_kept = list(set(np.arange(n_atoms))-set(atoms_to_be_removed_with_alt_loc))

    aux_alternate_location = [{}]
    for chosen, same_atoms in zip(chosen_with_alt_loc, aux_dict.values()):
        atom_index = np.where(atom_indices_to_be_kept==chosen)[0][0]
        aux_dict={
                'location_id':alternate_location[same_atoms],
                'occupancy':occupancy[same_atoms],
                'b_factor':b_factor[same_atoms],
                'atom_id':atom_id[same_atoms],
                'coordinates':coordinates[0,same_atoms,:]
                }
        aux_alternate_location[0][atom_index]=aux_dict

    structure_id = None
    time = None

    coordinates = coordinates[:,atom_indices_to_be_kept,:]
    occupancy = occupancy[atom_indices_to_be_kept]
    b_factor = b_factor[atom_indices_to_be_kept]
    alternate_location = aux_alternate_location

    if item.unit_cell is not None:

        cell_lengths = np.empty([n_structures,3], dtype='float64')
        cell_angles = np.empty([n_structures,3], dtype='float64')
        for ii in range(3):
            cell_lengths[:,ii] = item.unit_cell[ii]
            cell_angles[:,ii] = item.unit_cell[ii+3]

        cell_lengths = puw.quantity(cell_lengths, 'angstroms')
        cell_angles = puw.quantity(cell_angles, 'degrees')

        box = get_box_from_lengths_and_angles(cell_lengths, cell_angles)
        box = puw.standardize(box)

    else:

        box = None

    if not is_all(structure_indices):
        if box is not None:
            box = box[structure_indices,:,:]


    bioassembly = {}

    for aux_bioassembly in item.bio_assembly:

        aux = {'chain_indices': [], 'rotations': [], 'translations': []}

        for transformation in aux_bioassembly['transformList']:

            matrix_transformation = np.array(transformation['matrix']).reshape(-1,4)

            aux['chain_indices'].append(transformation['chainIndexList'])
            aux['rotations'].append(matrix_transformation[:3,:3])
            aux['translations'].append(puw.quantity(matrix_transformation[:3,3], unit='angstroms', standardized=True))

        bioassembly[aux_bioassembly['name']] = aux

    tmp_item = Structures(structure_id=structure_id, time=time, coordinates=coordinates, box=box,
            occupancy=occupancy, b_factor=b_factor, alternate_location=alternate_location, bioassembly=bioassembly)

    return tmp_item

