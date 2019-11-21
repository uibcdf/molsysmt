
def from_mmtf_MMTFDecoder(item, atom_indices='all', frame_indices='all'):

    from molmodmt.native.composition import Composition
    from molmodmt.native import elements
    from molmodmt.utils.composition.classification import MMTFDecoder_group_to_group_class_type
    from molmodmt.utils.composition.classification import MMTFDecoder_entity_to_entity_class_type
    import numpy as np

    tmp_item = Composition()

    # bioassemblies

    index_bioassembly = 0

    for mmtf_bioassembly in item.bio_assembly:

        bioassembly = elements.BioAssembly()

        bioassembly.index = index_bioassembly
        bioassembly.id = None
        bioassembly.name = mmtf_bioassembly['name']
        bioassembly.type = None

        for transformation in mmtf_bioassembly['transformList']:

            bioassembly_transformation = elements.BioAssembly_Transformation()
            bioassembly_transformation.chain_indices = transformation['chainIndexList']
            bioassembly_transformation.matrix = np.reshape(transformation['matrix'],(4,4))
            bioassembly.transformation.append(bioassembly_transformation)

        tmp_item.bioassembly.append(bioassembly)
        index_bioassembly += 1

    # chains

    for index_chain in range(item.num_chains):

        chain = elements.Chain()

        chain.index = index_chain
        chain.id = item.chain_id_list[index_chain]
        chain.name = item.chain_name_list[index_chain]
        chain.type = None

        tmp_item.chain.append(chain)

    # groups, atoms and bonds intra group

    index_atom = 0
    count_atoms = 0
    index_group = 0

    for mmtf_group_type in item.group_type_list:

        mmtf_group = item.group_list[mmtf_group_type]
        group_class_type = MMTFDecoder_group_to_group_class_type(mmtf_group)
        group = elements.group_class_initialization(group_class_type)

        group.index = index_group
        group.id = item.group_id_list[index_group]
        group.name = mmtf_group['groupName']
        group.type = group_class_type

        group.chemical_type = mmtf_group['chemCompType']
        group.formal_charge=np.sum(mmtf_group['formalChargeList'])

        if group_class_type in ['AminoAcid', 'Nucleotide']:
            group.lettercode = mmtf_group['singleLetterCode']

        # atoms

        for atom_name, atom_element, atom_formal_charge in zip(mmtf_group['atomNameList'], mmtf_group['elementList'], mmtf_group['formalChargeList']):

            atom = elements.Atom()

            atom.index = index_atom
            atom.id = item.atom_id_list[index_atom]
            atom.name = atom_name
            atom.type = atom_name

            atom.element = atom_element
            atom.formal_charge = atom_formal_charge

            atom.group = group
            group.atom.append(atom)

            tmp_item.atom.append(atom)
            index_atom+=1

        # bonds intra group

        for bond_pair, bond_order in zip(np.reshape(mmtf_group['bondAtomList'],(-1,2)), mmtf_group['bondOrderList']):

            tmp_atom_0 = tmp_item.atom[bond_pair[0]+count_atoms]
            tmp_atom_1 = tmp_item.atom[bond_pair[1]+count_atoms]
            tmp_atom_0.bonded_atoms.append(tmp_atom_1)
            tmp_atom_1.bonded_atoms.append(tmp_atom_0)

            bond = elements.Bond()
            bond.atom = [tmp_atom_0, tmp_atom_1]
            bond.order = bond_order

            tmp_item.bond.append(bond)

        count_atoms += len(group.atom)

        tmp_item.group.append(group)
        index_group += 1

    # bonds inter-groups

    for bond_pair, bond_order in zip(np.reshape(item.bond_atom_list,(-1,2)), item.bond_order_list):
        tmp_atom_0 = tmp_item.atom[bond_pair[0]]
        tmp_atom_1 = tmp_item.atom[bond_pair[1]]
        tmp_atom_0.bonded_atoms.append(tmp_atom_1)
        tmp_atom_1.bonded_atoms.append(tmp_atom_0)
        bond = elements.Bond(atoms=[tmp_atom_0, tmp_atom_1], order=bond_order)
        tmp_item.bond.append(bond)

    # components

    from networkx import empty_graph, connected_components

    G = empty_graph(len(tmp_item.atom))

    for bond in tmp_item.bond:
        G.add_edge(bond.atom[0].index, bond.atom[1].index)

    atom_indices_per_component = list(connected_components(G))
    del(G, empty_graph, connected_components)

    index_component = 0

    for atom_indices_of_component in atom_indices_per_component:

        component = elements.Component()

        component.index = index_component
        component.id = None
        component.name = None
        component.type = None

        for atom_index in atom_indices_of_component:

            atom = tmp_item.atom[atom_index]
            atom.component = component
            component.atom.append(atom)

            group = atom.group
            if group not in component.group:
                component.group.append(group)
                group.component = component

        tmp_item.component.append(component)
        index_component += 1

    # complete nested objects in chains:

    count_groups = 0
    for index_chain in range(item.num_chains):
        chain = tmp_item.chain[index_chain]
        n_groups = item.groups_per_chain[index_chain]
        for index_group in range(count_groups, count_groups+n_groups):
            group = tmp_item.group[index_group]
            chain.group.append(group)
            group.chain = chain
            for atom in group.atom:
                atom.chain = chain
                chain.atom.append(atom)
            component = group.component
            if component not in chain.component:
                chain.component.append(component)
                component.chain = chain

        count_groups+=n_groups

    # complete nested objects in bioassemblies:

    for bioassembly in tmp_item.bioassembly:
        if len(bioassembly.transformation)>1:
            raise NotImplementedError("Not prepared to work with multiple transformations")
        for index_chain in bioassembly.transformation[0].chain_indices:
            chain = tmp_item.chain[index_chain]
            bioassembly.chain.append(chain)
            bioassembly.component.extend(chain.component)
            bioassembly.group.extend(chain.group)
            bioassembly.atom.extend(chain.atom)
        for atom in bioassembly.atom:
            atom.bioassembly = bioassembly
        for group in bioassembly.group:
            group.bioassembly = group
        for component in bioassembly.component:
            component.bioassembly = component

    # entities

    index_entity = 0

    for mmtf_entity in item.entity_list:

        entity_class_type = MMTFDecoder_entity_to_entity_class_type(mmtf_entity)
        entity = elements.entity_class_initialization(entity_class_type)

        entity.index = index_entity
        entity.id = None
        entity.name = mmtf_entity['description']
        entity.type = entity_class_type

        entity.mmtf_type = mmtf_entity['type']
        entity.description = mmtf_entity['description']

        if entity.type in ['Protein']:
            entity.sequence = mmtf_entity['sequence']

        for index_chain in mmtf_entity['chainIndexList']:
            chain = tmp_item.chain[index_chain]
            entity.chain.append(chain)
            entity.component.extend(chain.component)
            entity.group.extend(chain.group)
            entity.atom.extend(chain.atom)
        for chain in entity.chain:
            chain.entity = entity
        for component in entity.component:
            component.entity = entity
        for group in entity.group:
            group.entity = entity
        for atom in entity.atom:
            atom.entity = entity

        tmp_item.entity.append(entity)
        index_entity += 1

    # molecules:

    index_molecule = 0

    for entity in tmp_item.entity:

        if entity.type == "Protein":
            molecule = elements.molecules.Protein()
            molecule.index = index_molecule
            molecule.id = None
            molecule.name = entity.name
            molecule.type = entity.type
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
            tmp_item.molecule.append(molecule)
            index_molecule += 1

        elif entity.type == "Water":
            for chain in entity.chain:
                for component in chain.component:
                    molecule = elements.molecules.Protein()
                    molecule.index = index_molecule
                    molecule.id = None
                    molecule.name = None
                    molecule.type = entity.type
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
                    tmp_item.molecule.append(molecule)
                    index_molecule += 1

        else:
            print(entity.type)
            raise NotImplementedError

    # global attributes:

    tmp_item.n_atoms = len(tmp_item.atom)
    tmp_item.n_groups = len(tmp_item.group)
    tmp_item.n_components = len(tmp_item.component)
    tmp_item.n_chains = len(tmp_item.chain)
    tmp_item.n_molecules = len(tmp_item.molecule)
    tmp_item.n_entities = len(tmp_item.entity)
    tmp_item.n_bioassemblies = len(tmp_item.bioassembly)
    tmp_item.n_bonds = len(tmp_item.bond)

    # local attributes

    for group in tmp_item.group:
        group.n_atoms = len(group.atom)

    for component in tmp_item.component:
        component.n_atoms = len(component.atom)
        component.n_groups = len(component.group)

    for chain in tmp_item.chain:
        chain.n_atoms = len(chain.atom)
        chain.n_groups = len(chain.group)
        chain.n_components = len(chain.component)
        try:
            chain.n_molecules = len(chain.molecule)
        except:
            chain.n_molecules = 0

    for molecule in tmp_item.molecule:
        molecule.n_atoms = len(molecule.atom)
        molecule.n_groups = len(molecule.group)
        molecule.n_components = len(molecule.component)
        try:
            molecule.n_chains = len(molecule.chain)
        except:
            chain.n_chains = 0

    for entity in tmp_item.entity:
        entity.n_atoms = len(entity.atom)
        entity.n_groups = len(entity.group)
        entity.n_components = len(entity.component)
        entity.n_chains = len(entity.chain)
        entity.n_molecules = len(entity.molecule)

    for bioassembly in tmp_item.bioassembly:
        bioassembly.n_atoms = len(bioassembly.atom)
        bioassembly.n_groups = len(bioassembly.group)
        bioassembly.n_components = len(bioassembly.component)
        bioassembly.n_chains = len(bioassembly.chain)
        bioassembly.n_molecules = len(bioassembly.molecule)
        bioassembly.n_entities = len(bioassembly.entity)

    tmp_item._update_dataframe()

    return tmp_item

