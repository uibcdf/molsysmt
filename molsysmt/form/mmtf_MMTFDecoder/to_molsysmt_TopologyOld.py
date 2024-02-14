from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='mmtf.MMTFDecoder')
def to_molsysmt_TopologyOld(item, atom_indices='all', skip_digestion=False):

    import warnings
    from molsysmt.native import TopologyOld
    from molsysmt.element.group import get_group_type_from_group_name
    from molsysmt.element.entity import get_entity_type_from_MMTFDecoder_entity

    tmp_item = TopologyOld()

    if len(item.group_type_list)!=item.num_groups:
        raise NotImplementedMethodError("The mmtf file has a group_type_list with different number of groups than the num_groups")

    # atoms, groups and bonds intra group

    n_atoms = item.num_atoms
    n_bonds = item.num_bonds

    tmp_item.atoms_dataframe["atom_index"] = np.arange(n_atoms, dtype=int)

    atom_name_array = np.empty(n_atoms, dtype=object)
    atom_id_array = np.empty(n_atoms, dtype=int)
    atom_type_array = np.empty(n_atoms, dtype=object)
    atom_bonded_atom_indices_array = np.empty(n_atoms, dtype=object)
    formal_charge_array = np.empty(n_atoms, dtype=float)

    group_index_array = np.empty(n_atoms, dtype=int)
    group_name_array = np.empty(n_atoms, dtype=object)
    group_id_array = np.empty(n_atoms, dtype=int)
    group_type_array = np.empty(n_atoms, dtype=object)

    bond_atom1_index_array = np.empty(n_bonds, dtype=int)
    bond_atom2_index_array = np.empty(n_bonds, dtype=int)
    #bond_type_array = np.empty(n_bonds, dtype=object)
    bond_order_array = np.empty(n_bonds, dtype=int)

    atom_index = 0
    bond_index = 0

    for mmtf_group_type, group_index, group_id in zip(item.group_type_list, range(item.num_groups), item.group_id_list):

        mmtf_group = item.group_list[mmtf_group_type]
        group_name = mmtf_group['groupName']
        group_type = get_group_type_from_group_name(group_name)

        # bonds intra-groups

        for bond_pair, bond_order in zip(np.reshape(mmtf_group['bondAtomList'],(-1,2)), mmtf_group['bondOrderList']):

            bond_atom1_index_array[bond_index]=bond_pair[0]+atom_index
            bond_atom2_index_array[bond_index]=bond_pair[1]+atom_index
            bond_order_array[bond_index]=bond_order
            bond_index+=1

        for atom_name, atom_type, atom_formal_charge in zip(mmtf_group['atomNameList'], mmtf_group['elementList'], mmtf_group['formalChargeList']):

            atom_name_array[atom_index] = atom_name
            atom_id_array[atom_index] = item.atom_id_list[atom_index]
            atom_type_array[atom_index] = atom_type
            formal_charge_array[atom_index] = atom_formal_charge

            group_index_array[atom_index] = group_index
            group_name_array[atom_index] = group_name
            group_id_array[atom_index] = group_id
            group_type_array[atom_index] = group_type

            atom_index+=1

    tmp_item.atoms_dataframe["atom_name"] = atom_name_array
    tmp_item.atoms_dataframe["atom_id"] = atom_id_array
    tmp_item.atoms_dataframe["atom_type"] = atom_type_array
    tmp_item.atoms_dataframe["occupancy"] = item.occupancy_list

    tmp_item.atoms_dataframe["alternate_location"] = np.array(item.alt_loc_list)
    tmp_item.atoms_dataframe["alternate_location"].replace({'':None}, inplace=True)

    del(atom_name_array, atom_id_array, atom_type_array)

    tmp_item.atoms_dataframe["group_index"] = group_index_array
    tmp_item.atoms_dataframe["group_name"] = group_name_array
    tmp_item.atoms_dataframe["group_id"] = group_id_array
    tmp_item.atoms_dataframe["group_type"] = group_type_array
    del(group_name_array, group_id_array, group_type_array)

    b_factor_array = puw.quantity(np.array(item.b_factor_list), unit='angstroms**2', standardized=True)
    tmp_item.atoms_dataframe["b_factor"] = puw.get_value(b_factor_array)

    formal_charge_array = puw.quantity(formal_charge_array, unit='e', standardized=True)
    tmp_item.atoms_dataframe["formal_charge"] = puw.get_value(formal_charge_array)
    del(formal_charge_array, b_factor_array)

    # bonds inter-groups in graph

    for bond_pair, bond_order in zip(np.reshape(item.bond_atom_list,(-1,2)), item.bond_order_list):
        bond_atom1_index_array[bond_index]=bond_pair[0]
        bond_atom2_index_array[bond_index]=bond_pair[1]
        bond_order_array[bond_index]=bond_order
        bond_index+=1

    #### bonds

    tmp_item.bonds_dataframe["atom1_index"] = bond_atom1_index_array
    tmp_item.bonds_dataframe["atom2_index"] = bond_atom2_index_array
    tmp_item.bonds_dataframe["order"] = bond_order_array
    del(bond_atom1_index_array, bond_atom2_index_array, bond_order_array)

    #### components

    tmp_item._build_components()
    component_index_array=tmp_item.atoms_dataframe['component_index'].to_numpy(dtype=int,copy=True)

    #### chains

    chain_index_array = np.empty(n_atoms, dtype=int)
    chain_name_array = np.empty(n_atoms, dtype=object)
    chain_id_array = np.empty(n_atoms, dtype=object)
    #chain_type_array = np.empty(n_atoms, dtype=object)

    count_groups = 0

    for chain_index, chain_id, chain_name in zip(range(item.num_chains), item.chain_id_list, item.chain_name_list):

        n_groups_chain = item.groups_per_chain[chain_index]

        for group_index in range(count_groups, count_groups+n_groups_chain):
            for atom_index in np.where(group_index_array==group_index)[0]:

                chain_index_array[atom_index] = chain_index
                chain_name_array[atom_index] = chain_name
                chain_id_array[atom_index] = chain_id

        count_groups+=n_groups_chain

    tmp_item.atoms_dataframe["chain_index"] = chain_index_array
    tmp_item.atoms_dataframe["chain_name"] = chain_name_array
    tmp_item.atoms_dataframe["chain_id"] = chain_id_array

    del(chain_name_array, chain_id_array)

    # molecules

    molecule_index_array = np.empty(n_atoms, dtype=int)
    molecule_name_array = np.empty(n_atoms, dtype=object)
    molecule_id_array = np.empty(n_atoms, dtype=object)
    molecule_type_array = np.empty(n_atoms, dtype=object)

    molecule_name_array.fill(np.nan)
    molecule_type_array.fill(np.nan)

    molecule_index = 0

    for mmtf_entity in item.entity_list:

        entity_type = get_entity_type_from_MMTFDecoder_entity(mmtf_entity)
        entity_name = mmtf_entity['description']

        if entity_type == "protein":

            entity_name = entity_name.capitalize()

            molecule_type = "protein"
            molecule_name = entity_name

            for chain_index in mmtf_entity['chainIndexList']:
                for atom_index in np.where(chain_index_array==chain_index)[0]:

                    molecule_index_array[atom_index] = molecule_index
                    molecule_name_array[atom_index] = molecule_name
                    molecule_type_array[atom_index] = molecule_type
                    molecule_id_array[atom_index] = molecule_index

                molecule_index += 1

        elif entity_type == "water":

            molecule_type = "water"
            molecule_name = "water"

            for chain_index in mmtf_entity['chainIndexList']:
                atom_indices_in_chain = np.where(chain_index_array==chain_index)[0]
                component_indices_in_chain = np.unique(component_index_array[atom_indices_in_chain])
                for component_index in component_indices_in_chain:
                    for atom_index in np.where(component_index_array==component_index)[0]:

                        molecule_index_array[atom_index] = molecule_index
                        molecule_name_array[atom_index] = molecule_name
                        molecule_type_array[atom_index] = molecule_type
                        molecule_id_array[atom_index] = molecule_index

                    molecule_index += 1

        elif entity_type == "ion":

            entity_name = entity_name.capitalize()

            molecule_type = "ion"
            molecule_name = entity_name

            for chain_index in mmtf_entity['chainIndexList']:
                for atom_index in np.where(chain_index_array==chain_index)[0]:

                    molecule_index_array[atom_index] = molecule_index
                    molecule_name_array[atom_index] = molecule_name
                    molecule_type_array[atom_index] = molecule_type
                    molecule_id_array[atom_index] = molecule_index

                molecule_index += 1

        elif entity_type == "small molecule":

            entity_name = entity_name.capitalize()

            molecule_type = "small molecule"
            molecule_name = entity_name

            for chain_index in mmtf_entity['chainIndexList']:
                for atom_index in np.where(chain_index_array==chain_index)[0]:

                    molecule_index_array[atom_index] = molecule_index
                    molecule_name_array[atom_index] = molecule_name
                    molecule_type_array[atom_index] = molecule_type
                    molecule_id_array[atom_index] = molecule_index

                molecule_index += 1

        elif entity_type == "oligosaccharide":

            entity_name = entity_name.capitalize()

            molecule_type = "oligosaccharide"
            molecule_name = entity_name

            for chain_index in mmtf_entity['chainIndexList']:
                for atom_index in np.where(chain_index_array==chain_index)[0]:

                    molecule_index_array[atom_index] = molecule_index
                    molecule_name_array[atom_index] = molecule_name
                    molecule_type_array[atom_index] = molecule_type
                    molecule_id_array[atom_index] = molecule_index

                molecule_index += 1

        else:

            raise ValueError("Entity type not recognized")

    tmp_item.atoms_dataframe["molecule_index"] = molecule_index_array
    tmp_item.atoms_dataframe["molecule_name"] = molecule_name_array
    tmp_item.atoms_dataframe["molecule_type"] = molecule_type_array
    tmp_item.atoms_dataframe["molecule_id"] = molecule_id_array

    del(molecule_index_array, molecule_name_array, molecule_type_array, molecule_id_array)

    del(group_index_array, chain_index_array, component_index_array)

    # molecules

    tmp_item._build_entities()

    ## nan to None

    tmp_item._nan_to_None()

    ## If atoms with alternate location the highest occupancy or A is taken
    ## other pseudo-atoms are removed

    if not np.all(tmp_item.atoms_dataframe["alternate_location"]==None):
        alt_loc = tmp_item.atoms_dataframe["alternate_location"].to_numpy()
        alt_atom_indices = np.where(alt_loc!=None)[0]
        alt_atom_names = tmp_item.atoms_dataframe["atom_name"][alt_atom_indices].to_numpy()
        alt_group_ids = tmp_item.atoms_dataframe["group_id"][alt_atom_indices].to_numpy()
        alt_chain_ids = tmp_item.atoms_dataframe["chain_id"][alt_atom_indices].to_numpy()
        aux_dict = {}
        for aux_atom_index, aux_atom_name, aux_group_id, aux_chain_id in zip(alt_atom_indices, alt_atom_names, alt_group_ids, alt_chain_ids):
            aux_key = tuple([aux_atom_name, aux_group_id, aux_chain_id])
            if aux_key in aux_dict:
                aux_dict[aux_key].append(aux_atom_index)
            else:
                aux_dict[aux_key]=[aux_atom_index]

    atoms_to_be_removed_with_alt_loc=[]
    for same_atoms in aux_dict.values():
        alt_occupancy = tmp_item.atoms_dataframe["occupancy"][same_atoms].to_numpy()
        alt_loc = tmp_item.atoms_dataframe["alternate_location"][same_atoms].to_numpy()
        if np.allclose(alt_occupancy, alt_occupancy[0]):
            chosen = np.where(alt_loc=='A')[0][0]
        else:
            chosen = np.argmax(alt_occupancy)
        chosen = same_atoms.pop(chosen)
        atoms_to_be_removed_with_alt_loc += same_atoms

    tmp_item.atoms_dataframe.__delitem__('alternate_location')
    tmp_item.atoms_dataframe.__delitem__('occupancy')
    tmp_item.atoms_dataframe.__delitem__('b_factor')
    tmp_item.atoms_dataframe.__delitem__('formal_charge')
    tmp_item.atoms_dataframe.__delitem__('partial_charge')

    if not is_all(atom_indices):
        atom_indices = list(set(atom_indices)-set(atoms_to_be_removed_with_alt_loc))
        tmp_item = tmp_item.extract(atom_indices)
    else:
        if len(atoms_to_be_removed_with_alt_loc):
            atom_indices = list(set(np.arange(n_atoms))-set(atoms_to_be_removed_with_alt_loc))
            tmp_item = tmp_item.extract(atom_indices)

    return tmp_item

