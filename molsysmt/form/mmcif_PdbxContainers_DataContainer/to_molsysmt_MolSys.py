from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import pandas as pd

# https://github.com/rcsb/mmtf/blob/master/spec.md

@digest(form='mmcif.PdbxContainers.DataContainer')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import MolSys
    from molsysmt.element.group import get_bonded_atom_pairs

    index_att = {jj:ii for ii,jj in enumerate(item.getObj('atom_site').getAttributeList())}

    n_atoms = len(item.getObj('atom_site').data)

    atom_name_array = np.empty(n_atoms, dtype=object)
    atom_id_array = np.empty(n_atoms, dtype=int)
    atom_type_array = np.empty(n_atoms, dtype=object)
    atom_group_index_array = np.empty(n_atoms, dtype=int)
    atom_chain_index_array = np.empty(n_atoms, dtype=int)

    coordinates_array = np.empty([1,n_atoms,3],dtype=float)
    occupancy_array = np.empty(n_atoms,dtype=float)
    alternate_location_array = np.empty(n_atoms,dtype=object)
    b_factor_array = np.empty(n_atoms,dtype=float)

    atom_pairs_bonded = []

    model_num_array = np.empty(n_atoms, dtype=int)

    group_name_array = []
    group_id_array = []
    group_entity_id_array = []
    group_chain_id_array = []

    chain_name_array = []
    chain_id_array = []

    former_group_id = None
    group_index = -1
    former_chain_id = None
    chain_index = -1

    for atom_index, atom_record in enumerate(item.getObj('atom_site').data):

        atom_id_array[atom_index] = atom_record[index_att['id']]
        atom_type_array[atom_index] = atom_record[index_att['type_symbol']]
        atom_name_array[atom_index] = atom_record[index_att['auth_atom_id']]

        coordinates_array[0,atom_index,0] = atom_record[index_att['Cartn_x']]
        coordinates_array[0,atom_index,1] = atom_record[index_att['Cartn_y']]
        coordinates_array[0,atom_index,2] = atom_record[index_att['Cartn_z']]

        occupancy_array[atom_index] = atom_record[index_att['occupancy']]
        alternate_location_array[atom_index] = atom_record[index_att['label_alt_id']]
        b_factor_array[atom_index] = atom_record[index_att['B_iso_or_equiv']]

        model_num_array[atom_index] = atom_record[index_att['pdbx_PDB_model_num']]

        group_id = atom_record[index_att['auth_seq_id']]
        group_name = atom_record[index_att['auth_comp_id']]
        chain_id = atom_record[index_att['label_asym_id']]
        chain_name = atom_record[index_att['auth_asym_id']]
        entity_id = atom_record[index_att['label_entity_id']]

        if former_group_id!=group_id:
            group_name_array.append(group_name)
            group_id_array.append(group_id)
            group_entity_id_array.append(entity_id)
            group_chain_id_array.append(chain_id)
            former_group_id=group_id
            group_index+=1

        if former_chain_id!=chain_id:
            chain_name_array.append(chain_name)
            chain_id_array.append(chain_id)
            former_chain_id=chain_id
            chain_index+=1

        atom_group_index_array[atom_index] = group_index
        atom_chain_index_array[atom_index] = chain_index

    group_name_array = np.array(group_name_array, dtype='object')
    group_id_array = np.array(group_id_array, dtype=int)
    chain_name_array = np.array(chain_name_array, dtype='object')
    chain_id_array = np.array(chain_id_array, dtype='object')

    aux_series = pd.Series(atom_group_index_array)
    group_index_to_atom_indices = {key: list(group.index) for key, group in aux_series.groupby(aux_series)}
    del(aux_series)

    # bonds intra-group

    if item.exists('chem_comp_bond'):

        bonds_intra_group = {}

        for record in item.getObj('chem_comp_bond'):
            try:
                bonds_intra_group[record[0]].append([record[1], record[2]])
            except:
                bonds_intra_group[record[0]]=[[record[1], record[2]]]

        for group_index, atom_indices in group_index_to_atom_indices.items():

            atom_names = atom_name_array[atom_indices]
            group_name = group_name_array[group_index]

            dict_aux = {ii:jj for ii,jj in zip(atom_names,atom_indices)}
            dict_mask = {ii:False for ii in atom_names}

            aux_atom_pairs_bonded = []

            for at1, at2 in bonds_intra_group[group_name]:
                try:
                    aux_atom_pairs_bonded.append(sorted([dict_aux[at1],dict_aux[at2]]))
                    dict_mask[at1]=True
                    dict_mask[at2]=True
                except:
                    pass

            remains = [ii for ii,jj in dict_mask.items() if not jj]

            if len(remains):
                if set(remains)==set(['H1','H3']):
                    for at1, at2 in [['N', 'H1'], ['N', 'H3']]:
                        aux_atom_pairs_bonded.append(sorted([dict_aux[at1],dict_aux[at2]]))
                    atom_pairs_bonded += aux_atom_pairs_bonded
                elif len(atom_indices)==1:
                    atom_pairs_bonded += []
                else:
                    print(f'Warning! The bonds of group {group_name} were recalculated by MolSysMT.')
                    aux_pairs_bonded = get_bonded_atom_pairs(group_name, atom_names, atom_indices)
                    atom_pairs_bonded += aux_atom_pairs_bonded
            else:
                atom_pairs_bonded += aux_atom_pairs_bonded

    else:

        aux_series = pd.Series(atom_group_index_array)
        group_index_to_atom_indices = {key: list(group.index) for key, group in aux_series.groupby(aux_series)}

        for group_index, atom_indices in group_index_to_atom_indices.items():

            atom_names = atom_name_array[atom_indices].tolist()
            group_name = group_name_array[group_index]
            aux_atom_pairs_bonded = get_bonded_atom_pairs(group_name, atom_names, atom_indices)
            atom_pairs_bonded += aux_atom_pairs_bonded

    atom_pairs_bonded = np.array(sorted(atom_pairs_bonded))
    bond_atom1_index_array = atom_pairs_bonded[:,0]
    bond_atom2_index_array = atom_pairs_bonded[:,1]
    del(atom_pairs_bonded)

    # components, molecules and entities, and bonds extra-group

    entity_id_array = []
    entity_name_array = []
    entity_type_array = []
    entity_id_to_entity_index = {}

    index_att = {jj:ii for ii,jj in enumerate(item.getObj('entity').getAttributeList())}

    for entity_index, entity_record in enumerate(item.getObj('entity').data):

        entity_id_array.append(entity_record[index_att['id']])
        entity_name_array.append(entity_record[index_att['pdbx_description']])
        entity_type_array.append(entity_record[index_att['pdbx_description']])

    for group_index, atom_indices in group_index_to_atom_indices.items():



    # alternate locations

    alt_atom_indices = np.where(alternate_location_array!='.')[0]
    alternate_location = None

    if len(alt_atom_indices):

        alt_atom_names = atom_name_array[alt_atom_indices]
        alt_group_indices = atom_group_index_array[alt_atom_indices]
        alt_chain_indices = atom_chain_index_array[alt_atom_indices]
        alt_group_ids = group_id_array[alt_group_indices]
        alt_chain_ids = chain_id_array[alt_chain_indices]

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
            alt_occupancy = occupancy_array[same_atoms]
            alt_loc = alternate_location_array[same_atoms]
            if np.allclose(alt_occupancy, alt_occupancy[0]):
                chosen = same_atoms[np.where(alt_loc=='A')[0][0]]
            else:
                chosen = same_atoms[np.argmax(alt_occupancy)]
            chosen_with_alt_loc.append(chosen)
            atoms_to_be_removed_with_alt_loc += [ii for ii in same_atoms if ii !=chosen]

        atom_indices_to_be_kept = np.setdiff1d(np.arange(n_atoms), atoms_to_be_removed_with_alt_loc)
        dict_old_to_new_atom_indices = {jj: ii for ii, jj in enumerate(atom_indices_to_be_kept)}

        alternate_location = [{}]
        for chosen, same_atoms in zip(chosen_with_alt_loc, aux_dict.values()):
            atom_index = dict_old_to_new_atom_indices[chosen]
            aux_dict={
                    'location_id':alternate_location_array[same_atoms],
                    'occupancy':occupancy_array[same_atoms],
                    'b_factor':b_factor_array[same_atoms],
                    'atom_id':atom_id_array[same_atoms],
                    'coordinates':coordinates_array[0,same_atoms,:]
                    }
            alternate_location[0][atom_index]=aux_dict

        atom_name_array = atom_name_array[atom_indices_to_be_kept]
        atom_id_array = atom_id_array[atom_indices_to_be_kept]
        atom_type_array = atom_type_array[atom_indices_to_be_kept]
        atom_group_index_array = atom_group_index_array[atom_indices_to_be_kept]
        atom_chain_index_array = atom_chain_index_array[atom_indices_to_be_kept]

        mask1 = np.isin(bond_atom1_index_array, atom_indices_to_be_kept)
        mask2 = np.isin(bond_atom2_index_array, atom_indices_to_be_kept)
        mask = mask1*mask2

        vaux_dict = np.vectorize(dict_old_to_new_atom_indices.__getitem__)
        bond_atom1_index_array = bond_atom1_index_array[mask]
        bond_atom1_index_array = vaux_dict(bond_atom1_index_array)
        bond_atom2_index_array = bond_atom2_index_array[mask]
        bond_atom2_index_array = vaux_dict(bond_atom2_index_array)
        
        coordinates_array = coordinates_array[:,atom_indices_to_be_kept,:]
        b_factor_array = b_factor_array[atom_indices_to_be_kept]


    return alternate_location
