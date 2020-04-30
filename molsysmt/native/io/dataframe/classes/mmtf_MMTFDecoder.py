
def from_mmtf_MMTFDecoder(item, atom_indices='all', frame_indices='all', bioassembly_index=0, bioassembly_name=None):

    from molsysmt.native import DataFrame
    from numpy import empty, array, arange, reshape, where, unique, nan
    from molsysmt.elements.group import name_to_type as group_name_to_group_type
    from molsysmt.elements.entity import type_from_MMTFDecoder_entity as entity_type_from_MMTFDecoder_entity
    from networkx import empty_graph, connected_components

    tmp_item = DataFrame()

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

    # atoms, groups and bonds intra group in graph

    n_atoms = item.num_atoms

    tmp_item["atom.index"] = arange(n_atoms, dtype=int)

    atom_name_array = empty(n_atoms, dtype=object)
    atom_id_array = empty(n_atoms, dtype=int)
    atom_type_array = empty(n_atoms, dtype=object)
    atom_bonded_atom_indices_array = empty(n_atoms, dtype=object)
    atom_formal_charge_array = empty(n_atoms, dtype=float)

    group_index_array = empty(n_atoms, dtype=int)
    group_name_array = empty(n_atoms, dtype=object)
    group_id_array = empty(n_atoms, dtype=int)
    group_type_array = empty(n_atoms, dtype=object)

    G = empty_graph(n_atoms)

    atom_index = 0

    for mmtf_group_type, group_index, group_id in zip(item.group_type_list, range(item.num_groups), item.group_id_list):

        mmtf_group = item.group_list[mmtf_group_type]
        group_name = mmtf_group['groupName']
        group_type = group_name_to_group_type(group_name)

        # bonds intra-groups in graph

        for bond_pair, bond_order in zip(reshape(mmtf_group['bondAtomList'],(-1,2)), mmtf_group['bondOrderList']):

            G.add_edge(bond_pair[0]+atom_index, bond_pair[1]+atom_index)

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

    tmp_item["atom.name"] = atom_name_array
    tmp_item["atom.id"] = atom_id_array
    tmp_item["atom.type"] = atom_type_array
    tmp_item["atom.formal_charge"] = atom_formal_charge_array
    del(atom_name_array, atom_id_array, atom_type_array, atom_formal_charge_array)

    tmp_item["group.index"] = group_index_array
    tmp_item["group.name"] = group_name_array
    tmp_item["group.id"] = group_id_array
    tmp_item["group.type"] = group_type_array
    del(group_name_array, group_id_array, group_type_array)

    # bonds inter-groups in graph

    for bond_pair, bond_order in zip(reshape(item.bond_atom_list,(-1,2)), item.bond_order_list):
        G.add_edge(bond_pair[0], bond_pair[1])

    #### bonds

    for atom_index in range(item.num_atoms):
        atom_bonded_atom_indices_array[atom_index] = list(G.neighbors(atom_index))

    tmp_item["atom.bonded_atom_indices"] = atom_bonded_atom_indices_array
    del(atom_bonded_atom_indices_array)

    #### components

    atom_indices_per_component = list(connected_components(G))
    del(G)

    component_index_array = empty(n_atoms, dtype=int)
    #component_name_array = empty(n_atoms, dtype=object)
    #component_id_array = empty(n_atoms, dtype=int)
    #component_type_array = empty(n_atoms, dtype=object)

    component_index = 0

    for atom_indices_of_component in atom_indices_per_component:
        for atom_index in atom_indices_of_component:

            component_index_array[atom_index] = component_index

        component_index += 1

    tmp_item["component.index"] = component_index_array

    #### chains

    chain_index_array = empty(n_atoms, dtype=int)
    chain_name_array = empty(n_atoms, dtype=object)
    chain_id_array = empty(n_atoms, dtype=object)
    #chain_type_array = empty(n_atoms, dtype=object)

    count_groups = 0

    for chain_index, chain_id, chain_name in zip(range(item.num_chains), item.chain_id_list, item.chain_name_list):

        n_groups_chain = item.groups_per_chain[chain_index]

        for group_index in range(count_groups, count_groups+n_groups_chain):
            for atom_index in where(group_index_array==group_index)[0]:

                chain_index_array[atom_index] = chain_index
                chain_name_array[atom_index] = chain_name
                chain_id_array[atom_index] = chain_id

        count_groups+=n_groups_chain

    tmp_item["chain.index"] = chain_index_array
    tmp_item["chain.name"] = chain_name_array
    tmp_item["chain.id"] = chain_id_array

    del(chain_name_array, chain_id_array)

    # entities and molecules

    entity_index_array = empty(n_atoms, dtype=int)
    entity_name_array = empty(n_atoms, dtype=object)
    entity_id_array = empty(n_atoms, dtype=object)
    entity_type_array = empty(n_atoms, dtype=object)

    molecule_index_array = empty(n_atoms, dtype=int)
    molecule_name_array = empty(n_atoms, dtype=object)
    molecule_id_array = empty(n_atoms, dtype=object)
    molecule_type_array = empty(n_atoms, dtype=object)

    molecule_name_array.fill(nan)
    molecule_type_array.fill(nan)

    entity_index = 0
    molecule_index = 0

    for mmtf_entity in item.entity_list:

        entity_type = entity_type_from_MMTFDecoder_entity(mmtf_entity)
        entity_name = mmtf_entity['description']

        for chain_index in mmtf_entity['chainIndexList']:

            for atom_index in where(chain_index_array==chain_index)[0]:

                entity_index_array[atom_index] = entity_index
                entity_name_array[atom_index] = entity_name
                entity_type_array[atom_index] = entity_type
                entity_id_array[atom_index] = entity_index

        if entity_type == "protein":

            molecule_type = "protein"
            molecule_name = entity_name

            for chain_index in mmtf_entity['chainIndexList']:
                for atom_index in where(chain_index_array==chain_index)[0]:

                    molecule_index_array[atom_index] = molecule_index
                    molecule_name_array[atom_index] = molecule_name
                    molecule_type_array[atom_index] = molecule_type
                    molecule_id_array[atom_index] = molecule_index

            molecule_index += 1

        elif entity_type == "water":

            molecule_type = "water"
            molecule_name = "water"

            for chain_index in mmtf_entity['chainIndexList']:
                atom_indices_in_chain = where(chain_index_array==chain_index)[0]
                component_indices_in_chain = unique(component_index_array[atom_indices_in_chain])
                for component_index in component_indices_in_chain:
                    for atom_index in where(component_index_array==component_index)[0]:

                        molecule_index_array[atom_index] = molecule_index
                        molecule_name_array[atom_index] = molecule_name
                        molecule_type_array[atom_index] = molecule_type
                        molecule_id_array[atom_index] = molecule_index

                    molecule_index += 1

        elif entity_type == "ion":

            molecule_type = "ion"
            molecule_name = entity_name

            for chain_index in mmtf_entity['chainIndexList']:
                atom_indices_in_chain = where(chain_index_array==chain_index)[0]
                component_indices_in_chain = unique(component_index_array[atom_indices_in_chain])
                for component_index in component_indices_in_chain:
                    for atom_index in where(component_index_array==component_index)[0]:

                        molecule_index_array[atom_index] = molecule_index
                        molecule_name_array[atom_index] = molecule_name
                        molecule_type_array[atom_index] = molecule_type
                        molecule_id_array[atom_index] = molecule_index

                    molecule_index += 1

        else:
            print(entity_type)
            raise ValueError("Entity type not recognized")

        entity_index += 1

    tmp_item["entity.index"] = entity_index_array
    tmp_item["entity.name"] = entity_name_array
    tmp_item["entity.type"] = entity_type_array
    tmp_item["entity.id"] = entity_id_array

    del(entity_index_array, entity_name_array, entity_type_array, entity_id_array)

    tmp_item["molecule.index"] = molecule_index_array
    tmp_item["molecule.name"] = molecule_name_array
    tmp_item["molecule.type"] = molecule_type_array
    tmp_item["molecule.id"] = molecule_id_array

    del(molecule_index_array, molecule_name_array, molecule_type_array, molecule_id_array)

    del(group_index_array, chain_index_array, component_index_array)

    tmp_item = tmp_item.extract(atom_indices)

    return tmp_item

