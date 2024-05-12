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

    index_att = {jj:ii for ii,jj in enumerate(item.getObj('atom_site').getAttributeList())}

    n_atoms = len(data_atom_site)

    atom_name_array = np.empty(n_atoms, dtype=object)
    atom_id_array = np.empty(n_atoms, dtype=int)
    atom_type_array = np.empty(n_atoms, dtype=object)
    atom_group_index_array = np.empty(n_atoms, dtype=int)
    atom_chain_index_array = np.empty(n_atoms, dtype=int)
    atom_entity_id_array = np.empty(n_atoms, dtype=int)

    coordinates_array = np.empty([1,n_atoms,3],dtype=float)
    occupancy_array = np.empty(n_atoms,dtype=float)
    alternate_location_array = np.empty(n_atoms,dtype=object)
    b_factor_array = np.empty(n_atoms,dtype=float)

    bond_atom1_index_array = []
    bond_atom2_index_array = []

    model_num_array = np.empty(n_atoms, dtype=int)

    group_name_array = []
    group_id_array = []

    chain_id_array = []
    chain_name_array = []

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
        alternate_location_array[atom_index] = atom_record['label_alt_id']
        b_factor_array[atom_index] = atom_record['B_iso_or_equiv']

        model_num_array[atom_index] = atom_record['pdbx_PDB_model_num']

        group_id = atom_record[index_att['auth_seq_id']]
        group_name = atom_record[index_att['auth_comp_id']]
        chain_id = atom_record[index_att['label_asym_id']]
        chain_name = atom_record[index_att['auth_asym_id']]
        entity_id = atom_record[index_att['label_entity_id']]

        if former_group_id!=group_id:
            group_name_list.append(group_name)
            group_id_list.append(group_id)
            former_group_id=group_id
            group_index+=1

        if former_chain_name!=chain_name:
            chain_name_list.append(chain_name)
            former_chain_name=chain_name
            chain_index+=1

        atom_group_index_array[atom_index] = group_index
        atom_chain_index_array[atom_index] = chain_index
        atom_entity_id_array[atom_index] = entity_id

    group_name_array = np.array(group_name_array, dtype='object')
    group_id_array = np.array(group_id_array, dtype=int)
    chain_name_array = np.array(chain_name_array, dtype='object')
    chain_id_array = np.array(chain_id_array, dtype='object')

    bonds_intra_group = {}

    for record in item.getObj('chem_comp_bond'):
        try:
            bonds_intra_group[record[0]].append([record[1], record[2]])
        except:
            bonds_intra_group[record[0]]=[[record[1], record[2]]]

    aux_series = pd.Series(atom_group_index_array)
    group_index_to_atom_indices = {key: list(group.index) for key, group in aux_series.groupby(aux_series)}
    for group_index, atom_indices in group_index_to_atom_indices.items():
        atom_names = atom_name_array[atom_indices]
        group_name = group_name_array[group_index]
    
    alt_atom_indices = np.where(alternate_location_array!='.')[0]

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
            alt_occupancy = occupancy[same_atoms]
            alt_loc = alternate_location[same_atoms]
            if np.allclose(alt_occupancy, alt_occupancy[0]):
                chosen = same_atoms[np.where(alt_loc=='A')[0][0]]
            else:
                chosen = same_atoms[np.argmax(alt_occupancy)]
            chosen_with_alt_loc.append(chosen)
            atoms_to_be_removed_with_alt_loc += [ii for ii in same_atoms if ii !=chosen]

        atom_indices_to_be_kept = np.setdiff1d(np.arange(n_atoms), atoms_to_be_removed_with_alt_loc)
        dict_old_to_new_atom_indices = {jj: ii for ii, jj in enumerate(atom_indices_to_be_kept)}

        aux_alternate_location = [{}]
        for chosen, same_atoms in zip(chosen_with_alt_loc, aux_dict.values()):
            atom_index = dict_old_to_new_atom_indices[chosen]
            aux_dict={
                    'location_id':alternate_location_array[same_atoms],
                    'occupancy':occupancy_array[same_atoms],
                    'b_factor':b_factor_array[same_atoms],
                    'atom_id':atom_id_array[same_atoms],
                    'coordinates':coordinates_array[0,same_atoms,:]
                    }
            aux_alternate_location[0][atom_index]=aux_dict

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

    else:

        alternate_location = None

