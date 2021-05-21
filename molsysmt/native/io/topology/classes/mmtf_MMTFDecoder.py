
def from_mmtf_MMTFDecoder(item, molecular_system=None, atom_indices='all', frame_indices='all', bioassembly_index=0, bioassembly_name=None):

    from molsysmt.native import Topology
    import numpy as np
    from molsysmt.elements.group import name_to_type as group_name_to_group_type
    from molsysmt.elements.entity import type_from_MMTFDecoder_entity as entity_type_from_MMTFDecoder_entity

    tmp_item = Topology()

    # sanity checks

    if len(item.bio_assembly)>0:

        mmtf_bioassembly = item.bio_assembly[bioassembly_index]

        if len(mmtf_bioassembly['transformList'])>1:
            raise NotImplementedError("The bioassembly has more than a transformation.")

        for n_chain_per_model in item.chains_per_model:
            if n_chain_per_model != item.num_chains:
                raise NotImplementedError("The bioassembly has models with different number of chains")

        if len(mmtf_bioassembly['transformList'][0]['chainIndexList']) != item.num_chains:
            raise NotImplementedError("The bioassembly has a different number of chains than the total amount of chains")

        if len(item.group_type_list)!=item.num_groups:
            raise NotImplementedError("The mmtf file has a group_type_list with different number of groups than the num_groups")

    # atoms, groups and bonds intra group

    n_atoms = item.num_atoms
    n_bonds = item.num_bonds

    tmp_item.atoms_dataframe["atom_index"] = np.arange(n_atoms, dtype=int)

    atom_name_array = np.empty(n_atoms, dtype=object)
    atom_id_array = np.empty(n_atoms, dtype=int)
    atom_type_array = np.empty(n_atoms, dtype=object)
    atom_bonded_atom_indices_array = np.empty(n_atoms, dtype=object)
    atom_formal_charge_array = np.empty(n_atoms, dtype=float)

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
        group_type = group_name_to_group_type(group_name)

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
            group_name_array[atom_index] = group_name
            group_id_array[atom_index] = group_id
            group_type_array[atom_index] = group_type

            atom_index+=1

    tmp_item.atoms_dataframe["atom_name"] = atom_name_array
    tmp_item.atoms_dataframe["atom_id"] = atom_id_array
    tmp_item.atoms_dataframe["atom_type"] = atom_type_array
    #tmp_item.atoms_dataframe["atom_formal_charge"] = atom_formal_charge_array
    del(atom_name_array, atom_id_array, atom_type_array, atom_formal_charge_array)

    tmp_item.atoms_dataframe["group_index"] = group_index_array
    tmp_item.atoms_dataframe["group_name"] = group_name_array
    tmp_item.atoms_dataframe["group_id"] = group_id_array
    tmp_item.atoms_dataframe["group_type"] = group_type_array
    del(group_name_array, group_id_array, group_type_array)

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

    # entities and molecules

    entity_index_array = np.empty(n_atoms, dtype=int)
    entity_name_array = np.empty(n_atoms, dtype=object)
    entity_id_array = np.empty(n_atoms, dtype=object)
    entity_type_array = np.empty(n_atoms, dtype=object)

    molecule_index_array = np.empty(n_atoms, dtype=int)
    molecule_name_array = np.empty(n_atoms, dtype=object)
    molecule_id_array = np.empty(n_atoms, dtype=object)
    molecule_type_array = np.empty(n_atoms, dtype=object)

    molecule_name_array.fill(np.nan)
    molecule_type_array.fill(np.nan)

    entity_index = 0
    molecule_index = 0

    for mmtf_entity in item.entity_list:

        entity_type = entity_type_from_MMTFDecoder_entity(mmtf_entity)
        entity_name = mmtf_entity['description']

        for chain_index in mmtf_entity['chainIndexList']:

            for atom_index in np.where(chain_index_array==chain_index)[0]:

                entity_index_array[atom_index] = entity_index
                entity_name_array[atom_index] = entity_name
                entity_type_array[atom_index] = entity_type
                entity_id_array[atom_index] = entity_index

        if entity_type == "protein":

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

            molecule_type = "ion"
            molecule_name = entity_name

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

        elif entity_type == "cosolute":

            molecule_type = "cosolute"
            molecule_name = entity_name

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

        elif entity_type == "small_molecule":

            molecule_type = "small_molecule"
            molecule_name = entity_name

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
        else:
            print(entity_name, entity_type, mmtf_entity)
            raise ValueError("Entity type not recognized")

        entity_index += 1

    tmp_item.atoms_dataframe["entity_index"] = entity_index_array
    tmp_item.atoms_dataframe["entity_name"] = entity_name_array
    tmp_item.atoms_dataframe["entity_type"] = entity_type_array
    tmp_item.atoms_dataframe["entity_id"] = entity_id_array

    del(entity_index_array, entity_name_array, entity_type_array, entity_id_array)

    tmp_item.atoms_dataframe["molecule_index"] = molecule_index_array
    tmp_item.atoms_dataframe["molecule_name"] = molecule_name_array
    tmp_item.atoms_dataframe["molecule_type"] = molecule_type_array
    tmp_item.atoms_dataframe["molecule_id"] = molecule_id_array

    del(molecule_index_array, molecule_name_array, molecule_type_array, molecule_id_array)

    del(group_index_array, chain_index_array, component_index_array)

    if atom_indices is not 'all':
        tmp_item = tmp_item.extract(atom_indices)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

