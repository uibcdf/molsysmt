
def from_mmtf_MMTFDecoder(item, atom_indices='all', frame_indices='all', bioassembly_index=0,
        bioassembly_name=None):

    from molmodmt.native.composition import Composition
    from molmodmt.native import elements
    from molmodmt.utils.composition.classification import MMTFDecoder_group_to_group_class_type
    from molmodmt.utils.composition.classification import MMTFDecoder_entity_to_entity_class_type
    import numpy as np

    # bioassembly from mmtf

    if bioassembly_name is not None:
        name_found = False
        index_bioassembly = 0
        for mmtf_bioassembly in item.bio_assembly:
            if bioassembly_name == mmtf_bioassembly['name']:
                name_found = True
                break
            else:
                index_bioassembly += 1
        if not name_found:
            raise ValueError("Bioassembly name not found in mmtf item.")
    else:
        bioassembly_name = item.bio_assembly[bioassembly_index]['name']

    mmtf_bioassembly = item.bio_assembly[bioassembly_index]

    # sanity checks

    if len(bioassembly.transformation)>1:
        raise NotImplementedError("The bioassembly has more than a transformation.")

    for n_chain_per_model in mmtf_bioassembly.chains_per_model:
        if n_chain_per_model != mmtf_bioassembly.num_chains:
            raise NotImplementedError("The bioassembly has models with different number of chains")

    if len(bioassembly_transformation.chain_indices) != mmtf_bioassembly.num_chains:
        raise NotImplementedError("The bioassembly has a different number of chains than the total amount of chains")

    if len(item.group_type_list)!=item.num_groups:
        raise NotImplementedError("The mmtf file has a group_type_list with different number of groups than the num_groups")

    # composition

    tmp_item = Composition()

    # bioassembly

    bioassembly = elements.BioAssembly(index=bioassembly_index, id=bioassembly_name, name=bioassembly_name)

    for transformation in mmtf_bioassembly['transformList']:

        bioassembly_transformation = elements.BioAssembly_Transformation()
        bioassembly_transformation.chain_indices = transformation['chainIndexList']
        bioassembly_transformation.matrix = np.reshape(transformation['matrix'],(4,4))
        bioassembly.transformation.append(bioassembly_transformation)

    # groups, atoms and bonds intra group

    atom_index = 0
    count_atoms = 0

    for mmtf_group_type, group_index, group_id in zip(item.group_type_list, range(item.num_groups), item.group_id_list):

        mmtf_group = item.group_list[mmtf_group_type]
        group_type = MMTFDecoder_group_to_group_class_type(mmtf_group)
        group = elements.group_initialization_wizard(index=group_index, id=group_id, name=mmtf_group['groupName'], type=group_type)

        group.chemical_type = mmtf_group['chemCompType']
        group.formal_charge=np.sum(mmtf_group['formalChargeList'])

        if group_type in ['aminoacid', 'nucleotide']:
            group.lettercode = mmtf_group['singleLetterCode']

        # atoms

        for atom_name, atom_element, atom_formal_charge in zip(mmtf_group['atomNameList'], mmtf_group['elementList'], mmtf_group['formalChargeList']):

            atom_id = item.atom_id_list[atom_index]

            atom = elements.Atom(index=atom_index, id=atom_id, name=atom_name, type=atom_element)

            atom.formal_charge = atom_formal_charge

            group.atom.append(atom)
            atom.group = group
            bioassembly.atom.append(atom)

            atom_index+=1

        group.bioassembly = bioassembly
        bioassembly.group.append(group)

        # bonds intra-group

        for bond_pair, bond_order in zip(np.reshape(mmtf_group['bondAtomList'],(-1,2)), mmtf_group['bondOrderList']):

            tmp_atom_0 = tmp_item.atom[bond_pair[0]+count_atoms]
            tmp_atom_1 = tmp_item.atom[bond_pair[1]+count_atoms]

            bond = elements.Bond(atoms=[tmp_atom_0, tmp_atom_1], order=bond_order)

            tmp_item.bond.append(bond)

        count_atoms += len(group.atom)


    # bonds inter-groups

    for bond_pair, bond_order in zip(np.reshape(item.bond_atom_list,(-1,2)), item.bond_order_list):
        tmp_atom_0 = tmp_item.atom[bond_pair[0]]
        tmp_atom_1 = tmp_item.atom[bond_pair[1]]
        bond = elements.Bond(atoms=[tmp_atom_0, tmp_atom_1], order=bond_order)
        tmp_item.bond.append(bond)

    # components

    from networkx import empty_graph, connected_components

    G = empty_graph(len(tmp_item.atom))

    for bond in tmp_item.bond:
        G.add_edge(bond.atom[0].index, bond.atom[1].index)

    atom_indices_per_component = list(connected_components(G))
    del(G, empty_graph, connected_components)

    component_index = 0

    for atom_indices_of_component in atom_indices_per_component:

        component = elements.Component(index=component_index)

        for atom_index in atom_indices_of_component:

            atom = bioassembly.atom[atom_index]
            atom.component = component
            component.atom.append(atom)

            group = atom.group
            if group.component is None:
                group.component = component
                component.group.append(group)

        component.bioassembly = component
        bioassembly.component.append(component)
        component_index += 1

    # chains

    count_groups = 0

    for chain_index, chain_id, chain_name in zip(range(item.num_chains), item.chain_id_list, item.chain_name_list):

        chain = elements.Chain(index=chain_index, id=chain_id, name=chain_name)
        n_groups_chain = item.groups_per_chain[index_chain]

        for index_group in range(count_groups, count_groups+n_groups_chain):
            group = tmp_item.group[index_group]
            group.chain = chain
            chain.group.append(group)
            for atom in group.atom:
                atom.chain = chain
                chain.atom.append(atom)
            component = group.component
            if component.chain is None:
                chain.component.append(component)
                component.chain = chain

        count_groups+=n_groups

        bioassembly.chain.append(chain)

    # entities

    entity_index = 0

    for mmtf_entity in item.entity_list:

        entity_type = MMTFDecoder_entity_to_entity_class_type(mmtf_entity)
        entity_name = mmtf_entity['description']
        entity = elements.entity_initialization_wizard(index=entity_index, id=None, name=entity_name, type=entity_type)

        entity.mmtf_type = mmtf_entity['type']
        entity.description = mmtf_entity['description']

        if entity.type in ['protein']:
            entity.sequence = mmtf_entity['sequence']

        for index_chain in mmtf_entity['chainIndexList']:
            chain = tmp_item.chain[index_chain]
            entity.chain.append(chain)
            entity.component.extend(chain.component)
            entity.group.extend(chain.group)
            entity.atom.extend(chain.atom)
        #for chain in entity.chain:
        #    chain.entity = entity
        for component in entity.component:
            component.entity = entity
        for group in entity.group:
            group.entity = entity
        for atom in entity.atom:
            atom.entity = entity

        bioassembly.entity.append(entity)
        index_entity += 1

    # molecules:

    molecule_index = 0

    for entity in tmp_item.entity:

        if entity.type == "protein":
            molecule = molecule_initalization_wizard(index=molecule_index, id=None, name=entity.name, type="protein")
            molecule.sequence = entity.sequence
            for chain in entity.chain:
                molecule.chain.append(chain)
                chain.molecule = molecule
                for component in chain.component:
                    molecule.component.append(component)
                    component.molecule = molecule
                    for group in component.group:
                        molecule.group.append(group)
                        group.molecule = molecule
                        for atom in group.atom:
                            molecule.atom.append(atom)
                            atom.molecule = molecule
            bioassembly.molecule.append(molecule)
            index_molecule += 1

        elif entity.type == "water":
            for chain in entity.chain:
                for component in chain.component:
                    molecule = molecule_initalization_wizard(index=molecule_index, id=None, name="water", type="water")
                    molecule.chain = chain
                    molecule.component.append(component)
                    component.molecule = molecule
                    chain.molecule.append(molecule)
                    for group in component.group:
                        molecule.group.append(group)
                        group.molecule = molecule
                        for atom in group.atom:
                            molecule.atom.append(atom)
                            atom.molecule = molecule
                    bioassembly.molecule.append(molecule)
                    index_molecule += 1

        else:
            print(entity.type)
            raise ValueError("Entity type not recognized")



    # End

    tmp_item.bioassembly=bioassembly

#
#    # complete nested objects in bioassemblies:
#
#    for bioassembly in tmp_item.bioassembly:
#        if len(bioassembly.transformation)>1:
#            raise NotImplementedError("Not prepared to work with multiple transformations")
#        for index_chain in bioassembly.transformation[0].chain_indices:
#            chain = tmp_item.chain[index_chain]
#            bioassembly.chain.append(chain)
#            bioassembly.component.extend(chain.component)
#            bioassembly.group.extend(chain.group)
#            bioassembly.atom.extend(chain.atom)
#        for atom in bioassembly.atom:
#            atom.bioassembly = bioassembly
#        for group in bioassembly.group:
#            group.bioassembly = group
#        for component in bioassembly.component:
#            component.bioassembly = component
#    # local attributes
#
#    for bioassembly in tmp_item.bioassembly:
#        bioassembly.n_atoms = len(bioassembly.atom)
#        bioassembly.n_groups = len(bioassembly.group)
#        bioassembly.n_components = len(bioassembly.component)
#        bioassembly.n_chains = len(bioassembly.chain)
#        bioassembly.n_molecules = len(bioassembly.molecule)
#        bioassembly.n_entities = len(bioassembly.entity)

    return tmp_item

