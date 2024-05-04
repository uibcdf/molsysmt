from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

# https://github.com/rcsb/mmtf/blob/master/spec.md

@digest(form='mmtf.MMTFDecoder')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import MolSys
    from molsysmt.config import min_length_protein

    # atoms, groups and bonds intra group

    n_atoms = item.num_atoms
    n_groups = item.num_groups
    n_bonds = item.num_bonds
    n_chains = item.num_chains
    n_structures = item.num_models

    atom_name_array = np.empty(n_atoms, dtype=object)
    atom_id_array = np.empty(n_atoms, dtype=int)
    atom_type_array = np.empty(n_atoms, dtype=object)
    group_index_array = np.empty(n_atoms, dtype=int)
    chain_index_array = np.empty(n_atoms, dtype=int)

    group_name_array = np.empty(n_groups, dtype=object)
    group_id_array = np.empty(n_groups, dtype=int)

    chain_name_array = np.empty(n_chains, dtype=object)
    chain_id_array = np.empty(n_chains, dtype=int)

    bond_atom1_index_array = np.empty(n_bonds, dtype=int)
    bond_atom2_index_array = np.empty(n_bonds, dtype=int)

    formal_charge_array = np.empty(n_atoms, dtype=float)

    atom_index = 0
    bond_index = 0

    for mmtf_group_type, group_index, group_id in zip(item.group_type_list, range(item.num_groups), item.group_id_list):

        mmtf_group = item.group_list[mmtf_group_type]
        group_name_array[group_index] = mmtf_group['groupName']
        group_id_array[group_index] = group_id

        # bonds intra-groups

        if len(np.unique(mmtf_group['bondAtomList']))==len(mmtf_group['atomNameList']):

            for bond_pair in np.reshape(mmtf_group['bondAtomList'],(-1,2)):

                bond_atom1_index_array[bond_index]=bond_pair[0]+atom_index
                bond_atom2_index_array[bond_index]=bond_pair[1]+atom_index
                bond_index+=1

        else:

            aux_bonds = get_bonded_atom_pairs(mmtf_group['groupName'], mmtf_group['atomNameList'])

            print(aux_bonds)
            print('error', mmtf_group['groupName'])


        for atom_name, atom_type, atom_formal_charge in zip(mmtf_group['atomNameList'], mmtf_group['elementList'], mmtf_group['formalChargeList']):

            atom_name_array[atom_index] = atom_name
            atom_id_array[atom_index] = item.atom_id_list[atom_index]
            atom_type_array[atom_index] = atom_type
            formal_charge_array[atom_index] = atom_formal_charge

            group_index_array[atom_index] = group_index

            atom_index+=1

    # bonds inter-groups in graph

    for bond_pair, bond_order in zip(np.reshape(item.bond_atom_list,(-1,2)), item.bond_order_list):
        bond_atom1_index_array[bond_index]=bond_pair[0]
        bond_atom2_index_array[bond_index]=bond_pair[1]
        #bond_order_array[bond_index]=bond_order
        bond_index+=1

    # chains

    count_groups = 0

    dict_chain_id = {}
    aux_chain_id = 0

    for chain_index, chain_id, chain_name in zip(range(n_chains), item.chain_id_list, item.chain_name_list):

        if chain_id not in dict_chain_id:
            dict_chain_id[chain_id]=aux_chain_id
            aux_chain_id+=1

        chain_name_array[chain_index] = chain_name
        chain_id_array[chain_index] = dict_chain_id[chain_id]

        n_groups_chain = item.groups_per_chain[chain_index]

        for group_index in range(count_groups, count_groups+n_groups_chain):
            for atom_index in np.where(group_index_array==group_index)[0]:

                chain_index_array[atom_index] = chain_index

        count_groups+=n_groups_chain

    coordinates = np.column_stack([item.x_coord_list, item.y_coord_list, item.z_coord_list])
    coordinates = coordinates.reshape([-1, item.num_atoms, 3])
    coordinates = puw.quantity(coordinates, 'angstroms')
    coordinates = puw.standardize(coordinates)

    if item.unit_cell is not None:

        from molsysmt.pbc import get_box_from_lengths_and_angles

        cell_lengths = np.empty([n_structures,3], dtype='float64')
        cell_angles = np.empty([n_structures,3], dtype='float64')
        for ii in range(3):
            cell_lengths[:,ii] = item.unit_cell[ii]
            cell_angles[:,ii] = item.unit_cell[ii+3]

        cell_lengths = puw.quantity(cell_lengths, 'angstroms')
        cell_angles = puw.quantity(cell_angles, 'degrees')

        box = get_box_from_lengths_and_angles(cell_lengths, cell_angles, skip_digestion=True)
        box = puw.standardize(box)

    else:

        box = None

    bioassembly = {}

    for aux_bioassembly in item.bio_assembly:

        aux = {'chain_indices': [], 'rotations': [], 'translations': []}

        for transformation in aux_bioassembly['transformList']:

            matrix_transformation = np.array(transformation['matrix']).reshape(-1,4)

            aux['chain_indices'].append(transformation['chainIndexList'])
            aux['rotations'].append(matrix_transformation[:3,:3])
            aux['translations'].append(puw.quantity(matrix_transformation[:3,3], unit='angstroms', standardized=True))

        bioassembly[aux_bioassembly['name']] = aux

    occupancy = np.array(item.occupancy_list)
    alternate_location = np.array(item.alt_loc_list)
    b_factor = puw.quantity(np.array(item.b_factor_list), unit='angstroms**2', standardized=True)

    alt_atom_indices = np.where(alternate_location!='')[0]

    if len(alt_atom_indices):

        print('>@>',alt_atom_indices)

        alt_atom_names = atom_name[alt_atom_indices]
        alt_group_ids = group_id[alt_atom_indices]
        alt_chain_ids = chain_id[alt_atom_indices]
        aux_dict = {}
        for aux_atom_index, aux_atom_name, aux_group_id, aux_chain_id in zip(alt_atom_indices, alt_atom_names,
                                                                             alt_group_ids, alt_chain_ids):
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

        atom_indices_to_be_kept = np.setdiff1(np.arange(n_atoms), atoms_to_be_removed_with_alt_loc)
        dict_old_to_new_atom_indices = {jj: ii for ii, jj in enumerate(atom_indices_to_be_kept)}

        aux_alternate_location = [{}]
        for chosen, same_atoms in zip(chosen_with_alt_loc, aux_dict.values()):
            atom_index = dict_old_to_new_atom_indices[chosen]
            aux_dict={
                    'location_id':alternate_location[same_atoms],
                    'occupancy':occupancy[same_atoms],
                    'b_factor':b_factor[same_atoms],
                    'atom_id':atom_id[same_atoms],
                    'coordinates':coordinates[0,same_atoms,:]
                    }
            aux_alternate_location[0][atom_index]=aux_dict

        atom_name_array = atom_name_array[atom_indices_to_be_kept]
        atom_id_array = atom_id_array[atom_indices_to_be_kept]
        atom_type_array = atom_type_array[atom_indices_to_be_kept]
        group_index_array = group_index_array[atom_indices_to_be_kept]
        chain_index_array = chain_index_array[atom_indices_to_be_kept]

        mask1 = np.isin(bond_atom1_index_array, atom_indices_to_be_kept)
        mask2 = np.isin(bond_atom2_index_array, atom_indices_to_be_kept)
        mask = mask1*mask2

        vaux_dict = np.vectorize(dict_old_to_new_atom_indices.__getitem__)
        bond_atom1_index_array = bond_atom1_index_array[mask]
        bond_atom1_index_array = vaux_dict(bond_atom1_index_array)
        bond_atom2_index_array = bond_atom2_index_array[mask]
        bond_atom2_index_array = vaux_dict(bond_atom2_index_array)
        #bond_type_array = bond_type_array[mask]
        #bond_order_array = bond_order_array[mask]
        
        coordinates = coordinates[:,atom_indices_to_be_kept,:]
        b_factor = b_factor[atom_indices_to_be_kept]
        formal_charge_array = formal_charge_array[atom_indices_to_be_kept]
        alternate_location = aux_alternate_location

    n_atoms=atom_name_array.shape[0]
    n_bonds= bond_atom1_index_array.shape[0]

    tmp_item = MolSys(n_atoms=n_atoms, n_groups=n_groups, n_chains=n_chains, n_bonds=n_bonds)

    tmp_item.topology.atoms["atom_name"] = atom_name_array
    tmp_item.topology.atoms["atom_id"] = atom_id_array
    tmp_item.topology.atoms["atom_type"] = atom_type_array
    tmp_item.topology.atoms["group_index"] = group_index_array
    tmp_item.topology.atoms["chain_index"] = chain_index_array
    del(atom_name_array, atom_id_array, atom_type_array, group_index_array, chain_index_array)

    tmp_item.topology.groups["group_name"] = group_name_array
    tmp_item.topology.groups["group_id"] = group_id_array
    del(group_name_array, group_id_array)

    tmp_item.topology.chains["chain_name"] = chain_name_array
    tmp_item.topology.chains["chain_id"] = chain_id_array
    del(chain_name_array, chain_id_array)

    tmp_item.topology.bonds["atom1_index"] = bond_atom1_index_array
    tmp_item.topology.bonds["atom2_index"] = bond_atom2_index_array
    #tmp_item.topology.bonds["order"] = bond_order_array
    tmp_item.topology.bonds._remove_empty_columns()
    tmp_item.topology.bonds._sort_bonds()
    del(bond_atom1_index_array, bond_atom2_index_array)


    tmp_item.topology.rebuild_groups(redefine_ids=False, redefine_types=True)
    tmp_item.topology.rebuild_components(redefine_indices=True, redefine_ids=True,
                                         redefine_names=False, redefine_types=True)

    return tmp_item

    molecule_index = 0

    dict_chain_to_groups = tmp_item.topology.atoms.groupby('chain_index')['group_index'].unique().to_dict()

    for mmtf_entity in item.entity_list:

        entity_name = mmtf_entity['description']

        for chain_index in mmtf_entity['chainIndexList']:

            group_indices = dict_chain_to_groups[chain_index]

            first_group_type = tmp_item.topology.groups.iat[group_indices[0],2]

            if first_group_type == 'water':

                for group_index in group_indices:

                    component_index = tmp_item.topology.groups.iat[group_index,3]

                    tmp_item.topology.components.iat[component_index,3]=molecule_index
                    tmp_item.topology.components.iat[component_index,2]='water'
                    tmp_item.topology.components.iat[component_index,1]='water'
                    molecule_index+=1

            elif first_group_type == 'ion':

                for group_index in group_indices:

                    component_index = tmp_item.topology.groups.iat[group_index,3]

                    tmp_item.topology.components.iat[component_index,3]=molecule_index
                    tmp_item.topology.components.iat[component_index,2]='ion'
                    tmp_item.topology.components.iat[component_index,1]=entity_name
                    molecule_index+=1

            elif first_group_type == 'small molecule':

                for group_index in group_indices:

                    component_index = tmp_item.topology.groups.iat[group_index,3]

                    tmp_item.topology.components.iat[component_index,3]=molecule_index
                    tmp_item.topology.components.iat[component_index,2]='small molecule'
                    tmp_item.topology.components.iat[component_index,1]=entity_name
                    molecule_index+=1

            elif first_group_type == 'lipid':

                for group_index in group_indices:

                    component_index = tmp_item.topology.groups.iat[group_index,3]

                    tmp_item.topology.components.iat[component_index,3]=molecule_index
                    tmp_item.topology.components.iat[component_index,2]='lipid'
                    tmp_item.topology.components.iat[component_index,1]=entity_name
                    molecule_index+=1

            elif first_group_type in ['terminal capping', 'amino acid']:

                n_groups = len(group_indices)

                if first_group_type == 'terminal capping':
                    n_groups -= 1

                last_group_type = tmp_item.topology.groups.iat[group_indices[-1],2]

                if last_group_type == 'terminal capping':
                    n_groups -= 1

                if n_groups >= min_length_protein:
                    tmp_type = 'protein'
                else:
                    tmp_type = 'peptide'

                component_indices = tmp_item.topology.groups.iloc[group_indices,3].unique()

                for component_index in component_indices:

                    tmp_item.topology.components.iat[component_index,3]=molecule_index
                    tmp_item.topology.components.iat[component_index,2]=tmp_type
                    tmp_item.topology.components.iat[component_index,1]=entity_name

                molecule_index+=1

                pass

            elif first_group_type == 'nucleotide':

                raise ValueError("Entity type not recognized:", first_group_type)

            else:

                raise ValueError("Entity type not recognized:", first_group_type)

            del group_indices

    del dict_chain_to_groups

    aux_n_molecules = molecule_index

    # molecules

    tmp_item.topology.reset_molecules(n_molecules=aux_n_molecules)
    tmp_item.topology.rebuild_molecules(redefine_indices=False, redefine_ids=True, redefine_names=True, redefine_types=True)

    # entities

    tmp_item.topology.rebuild_entities(redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True)

    # structures

    tmp_item.structures.append(coordinates=coordinates, box=box)

    #tmp_item = tmp_item.extract(atom_indices=atom_indices, structure_indices=structure_indices,
    #                            copy_if_all=False, skip_digestion=True)

    return tmp_item

