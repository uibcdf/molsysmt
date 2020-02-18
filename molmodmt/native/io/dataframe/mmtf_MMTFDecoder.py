
def from_mmtf_MMTFDecoder(item, atom_indices='all', frame_indices='all', bioassembly_index=0,
        bioassembly_name=None):

    from molmodmt.native import DataFrame
    from numpy import arange
    from molmodmt.utils.composition.classification import MMTFDecoder_group_to_group_class_type
    from molmodmt.utils.composition.classification import MMTFDecoder_entity_to_entity_class_type
    from networkx import empty_graph, connected_components

    tmp_item = DataFrame()

    # sanity checks

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

    tmp_item['atom.index'] = arange(item.num_atoms)
    G = empty_graph(item.num_atoms)

    atom_index = 0
    count_atoms = 0

    aux_col_names=['atom.name', 'atom.id', 'atom.type', 'atom.formal_charge', 'group.index', 'group.name', 'group.id', 'group.type']

    for mmtf_group_type, group_index, group_id in zip(item.group_type_list, range(item.num_groups), item.group_id_list):

        mmtf_group = item.group_list[mmtf_group_type]
        group_type = MMTFDecoder_group_to_group_class_type(mmtf_group)

        for atom_name, atom_type, atom_formal_charge in zip(mmtf_group['atomNameList'], mmtf_group['elementList'], mmtf_group['formalChargeList']):

            atom_id = item.atom_id_list[atom_index]

            tmp_item.at[atom_index, aux_col_names] = [atom_name, atom_id, atom_type, atom_formal_charge, group_index, group_name, group_id, group_type]

            atom_index+=1

        # bonds intra-group

        for bond_pair, bond_order in zip(np.reshape(mmtf_group['bondAtomList'],(-1,2)), mmtf_group['bondOrderList']):

            G.add_edge(bond_pair[0]+count_atoms, bond_pair[1]+count_atoms)

        count_atoms += len(group.atom)


    # bonds inter-groups in graph

    for bond_pair, bond_order in zip(np.reshape(item.bond_atom_list,(-1,2)), item.bond_order_list):
        G.add_edge(bond_pair[0], bond_pair[1])

    # bonds

    for atom_index in range(item.num_atoms):
        tmp_item.at[atom_index, 'atom.bonded_atom_indices'] = list(G.neighbors(atom_index))

    # components

    atom_indices_per_component = list(connected_components(G))
    del(G)

    component_index = 0

    for atom_indices_of_component in atom_indices_per_component:
        for atom_index in atom_indices_of_component:

            tmp_item.at[atom_index, 'component.index'] = component_index

        component_index += 1

    # chains

    count_groups = 0
    group_indices = tmp_item['group.index']
    aux_col_names=['chain.index', 'chain.name', 'chain.id']

    for chain_index, chain_id, chain_name in zip(range(item.num_chains), item.chain_id_list, item.chain_name_list):

        n_groups_chain = item.groups_per_chain[chain_index]

        for group_index in range(count_groups, count_groups+n_groups_chain):
            for atom_index in group_indices.index[group_indices==group_index]:

                tmp_item.at[atom_index,aux_col_names]=[chain_index,chain_name,chain_id]

        count_groups+=n_groups_chain

    del(group_indices)

    # entities

    entity_index = 0
    chain_indices = tmp_item['group.index']
    aux_col_names=['entity.index', 'entity.name', 'entity.type']

    for mmtf_entity in item.entity_list:

        entity_type = MMTFDecoder_entity_to_entity_class_type(mmtf_entity)
        entity_name = mmtf_entity['description']

        for chain_index in mmtf_entity['chainIndexList']:
            for atom_index in chain_indices.index[chain_indices==chain_index]:

                tmp_item.at[atom_index,aux_col_names]=[entity_index,entity_name,entity_type]

        entity_index += 1

    del(chain_indices)

    # molecules:

    molecule_index = 0

    for entity in bioassembly.entity:

        if entity.type == "protein":
            molecule = elements.molecule_initialization_wizard(index=molecule_index, id=None, name=entity.name, type="protein")
            molecule.sequence = entity.sequence
            molecule.entity = entity
            entity.molecule.append(molecule)
            for chain in entity.chain:
                for component in chain.component:
                    molecule.component.append(component)
                    component.molecule = molecule
                    for group in component.group:
                        molecule.group.append(group)
                        group.molecule = molecule
                        for atom in group.atom:
                            molecule.atom.append(atom)
                            atom.molecule = molecule
            molecule.bioassembly = bioassembly
            bioassembly.molecule.append(molecule)
            molecule_index += 1

        elif entity.type == "water":
            for chain in entity.chain:
                for component in chain.component:
                    molecule = elements.molecule_initialization_wizard(index=molecule_index, id=None, name="water", type="water")
                    molecule.component.append(component)
                    component.molecule = molecule
                    molecule.entity = entity
                    entity.molecule.append(molecule)
                    for group in component.group:
                        molecule.group.append(group)
                        group.molecule = molecule
                        for atom in group.atom:
                            molecule.atom.append(atom)
                            atom.molecule = molecule
                    molecule.bioassembly = bioassembly
                    bioassembly.molecule.append(molecule)
                    molecule_index += 1

        elif entity.type == "ion":
            for chain in entity.chain:
                for component in chain.component:
                    molecule = elements.molecule_initialization_wizard(index=molecule_index, id=None, name=component.group[0].name, type="ion")
                    molecule.component.append(component)
                    component.molecule = molecule
                    molecule.entity = entity
                    entity.molecule.append(molecule)
                    for group in component.group:
                        molecule.group.append(group)
                        group.molecule = molecule
                        for atom in group.atom:
                            molecule.atom.append(atom)
                            atom.molecule = molecule
                    molecule.bioassembly = bioassembly
                    bioassembly.molecule.append(molecule)
                    molecule_index += 1

        else:
            print(entity.type)
            raise ValueError("Entity type not recognized")

    # sanity_check and update

    bioassembly._sanity_check(children_elements=True)
    bioassembly._update_all(children_elements=True)

    # End

    tmp_item = Composition()
    tmp_item.bioassembly=bioassembly
    tmp_item._update_from_bioassembly()
    tmp_item._update_dataframe()

    return tmp_item

