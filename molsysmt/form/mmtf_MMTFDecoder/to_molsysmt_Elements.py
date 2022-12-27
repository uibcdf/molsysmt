from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='mmtf.MMTFDecoder')
def to_molsysmt_Elements(item, atom_indices='all', structure_indices='all', bioassembly_index=0,
                         bioassembly_name=None):

    import warnings
    from molsysmt.native import Elements
    import numpy as np
    from molsysmt.element.group import get_group_type_from_group_name
    from molsysmt.element.entity import get_entity_type_from_MMTFDecoder_entity

    tmp_item = Elements()

    # sanity checks
    for n_chain_per_model in item.chains_per_model:
        if n_chain_per_model != item.num_chains:
            raise NotImplementedMethodError("The bioassembly has models with different number of chains")

    if len(item.group_type_list)!=item.num_groups:
        raise NotImplementedMethodError("The mmtf file has a group_type_list with different number of groups than the num_groups")

    if len(item.bio_assembly)>0:

        warning_message = ("The structure in the PDB has biological assemblies. "
        "There are geometrical transformations proposed in the structure. "
        "See the following issue in the source code repository: https://github.com/uibcdf/MolSysMT/issues/33")

        warnings.warn(warning_message)

        mmtf_bioassembly = item.bio_assembly[bioassembly_index]

        if len(mmtf_bioassembly['transformList'])>1:
            warning_message = ("The structure in the PDB has biological assemblies. "
            "There are geometrical transformations proposed in the structure. "
            "See the following issue in the source code repository: https://github.com/uibcdf/MolSysMT/issues/33")

            print(warning_message)
            warnings.warn(warning_message)

        if len(mmtf_bioassembly['transformList'][0]['chainIndexList']) != item.num_chains:
            warning_message = ("The bioassembly has a different number of chains than the total amount of chains")
            warnings.warn(warning_message)

    # atoms, groups and bonds intra group

    n_atoms = item.num_atoms
    n_bonds = item.num_bonds
    n_groups = item.num_groups
    n_chains = item.num_chains
    n_entities = len(item.entity_list)

    atom_name_array = np.empty(n_atoms, dtype=object)
    atom_id_array = np.empty(n_atoms, dtype=int)
    atom_type_array = np.empty(n_atoms, dtype=object)
    atom_formal_charge_array = np.empty(n_atoms, dtype=float)
    atom_b_factors_array = np.empty(n_atoms, dtype=float)
    group_index_array = np.empty(n_atoms, dtype=int)

    group_name_array = np.empty(n_groups, dtype=object)
    group_id_array = np.empty(n_groups, dtype=int)
    group_type_array = np.empty(n_groups, dtype=object)

    bond_atom1_index_array = np.empty(n_bonds, dtype=int)
    bond_atom2_index_array = np.empty(n_bonds, dtype=int)
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
            atom_formal_charge_array[atom_index] = atom_formal_charge

            group_index_array[atom_index] = group_index

            atom_index+=1

        group_name_array[group_index] = group_name
        group_id_array[group_index] = group_id
        group_type_array[group_index] = group_type


    tmp_item.atoms["atom_name"] = atom_name_array
    tmp_item.atoms["atom_id"] = atom_id_array
    tmp_item.atoms["atom_type"] = atom_type_array
    tmp_item.atoms["formal_charge"] = atom_formal_charge_array
    del(atom_name_array, atom_id_array, atom_type_array, atom_formal_charge_array)

    tmp_item.atoms["group_index"] = group_index_array
    tmp_item.groups["group_name"] = group_name_array
    tmp_item.groups["group_id"] = group_id_array
    tmp_item.groups["group_type"] = group_type_array
    del(group_name_array, group_id_array, group_type_array)

    # bonds inter-groups in graph

    for bond_pair, bond_order in zip(np.reshape(item.bond_atom_list,(-1,2)), item.bond_order_list):
        bond_atom1_index_array[bond_index]=bond_pair[0]
        bond_atom2_index_array[bond_index]=bond_pair[1]
        bond_order_array[bond_index]=bond_order
        bond_index+=1

    #### bonds

    tmp_item.bonds["atom1_index"] = bond_atom1_index_array
    tmp_item.bonds["atom2_index"] = bond_atom2_index_array
    tmp_item.bonds["order"] = bond_order_array
    del(bond_atom1_index_array, bond_atom2_index_array, bond_order_array)

    #### components

    tmp_item.build_components()
    component_index_array=tmp_item.atoms['component_index'].to_numpy(dtype=int,copy=True)

    #### chains

    chain_index_array = np.empty(n_atoms, dtype=int)
    chain_name_array = np.empty(n_chains, dtype=object)
    chain_id_array = np.empty(n_chains, dtype=object)
    #chain_type_array = np.empty(n_atoms, dtype=object)

    count_groups = 0

    for chain_index, chain_id, chain_name in zip(range(item.num_chains), item.chain_id_list, item.chain_name_list):

        n_groups_chain = item.groups_per_chain[chain_index]

        for group_index in range(count_groups, count_groups+n_groups_chain):
            for atom_index in np.where(group_index_array==group_index)[0]:

                chain_index_array[atom_index] = chain_index
        chain_name_array[chain_index] = chain_name
        chain_id_array[chain_index] = chain_id

        count_groups+=n_groups_chain

    tmp_item.atoms["chain_index"] = chain_index_array
    tmp_item.chains["chain_name"] = chain_name_array
    tmp_item.chains["chain_id"] = chain_id_array

    del(chain_name_array, chain_id_array)

    # entities and molecules

    entity_index_array = np.empty(n_atoms, dtype=int)
    entity_name_array = np.empty(n_entities, dtype=object)
    entity_id_array = np.empty(n_entities, dtype=object)
    entity_type_array = np.empty(n_entities, dtype=object)

    molecule_index_array = np.empty(n_atoms, dtype=int)
    molecule_name_array = []
    molecule_type_array = []

    entity_index = 0
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
                    entity_index_array[atom_index] = entity_index

                molecule_name_array.append(molecule_name)
                molecule_type_array.append(molecule_type)
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
                        entity_index_array[atom_index] = entity_index

                    molecule_name_array.append(molecule_name)
                    molecule_type_array.append(molecule_type)
                    molecule_index += 1

        elif entity_type == "ion":

            entity_name = entity_name.capitalize()

            molecule_type = "ion"
            molecule_name = entity_name

            for chain_index in mmtf_entity['chainIndexList']:
                for atom_index in np.where(chain_index_array==chain_index)[0]:

                    molecule_index_array[atom_index] = molecule_index
                    entity_index_array[atom_index] = entity_index

                molecule_name_array.append(molecule_name)
                molecule_type_array.append(molecule_type)
                molecule_index += 1

        elif entity_type == "small molecule":

            entity_name = entity_name.capitalize()

            molecule_type = "small molecule"
            molecule_name = entity_name

            for chain_index in mmtf_entity['chainIndexList']:
                for atom_index in np.where(chain_index_array==chain_index)[0]:

                    molecule_index_array[atom_index] = molecule_index
                    entity_index_array[atom_index] = entity_index

                molecule_name_array.append(molecule_name)
                molecule_type_array.append(molecule_type)
                molecule_index += 1

        elif entity_type == "oligosaccharide":

            entity_name = entity_name.capitalize()

            molecule_type = "oligosaccharide"
            molecule_name = entity_name

            for chain_index in mmtf_entity['chainIndexList']:
                for atom_index in np.where(chain_index_array==chain_index)[0]:

                    molecule_index_array[atom_index] = molecule_index
                    entity_index_array[atom_index] = entity_index

                molecule_name_array.append(molecule_name)
                molecule_type_array.append(molecule_type)
                molecule_index += 1

        else:

            raise ValueError("Entity type not recognized")

        entity_name_array[entity_index] = entity_name
        entity_type_array[entity_index] = entity_type
        entity_index += 1

    tmp_item.atoms["molecule_index"] = molecule_index_array
    tmp_item.molecules["molecule_name"] = np.array(molecule_name_array, dtype=object)
    tmp_item.molecules["molecule_type"] = np.array(molecule_type_array, dtype=object)

    del(molecule_index_array, molecule_name_array, molecule_type_array)

    tmp_item.atoms["entity_index"] = entity_index_array
    tmp_item.entities["entity_name"] = entity_name_array
    tmp_item.entities["entity_type"] = entity_type_array

    del(entity_index_array, entity_name_array, entity_type_array, entity_id_array)

    del(group_index_array, chain_index_array, component_index_array)

    tmp_item._nan_to_None()

    if not is_all(atom_indices):
        tmp_item = tmp_item.extract(atom_indices)

    return tmp_item

