
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

    # molecules

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



    # global attributes:

    tmp_item.n_atoms = len(tmp_item.atom)
    tmp_item.n_groups = len(tmp_item.group)
    tmp_item.n_components = len(tmp_item.group)
    tmp_item.n_chains = len(tmp_item.chain)
    tmp_item.n_molecules = len(tmp_item.molecule)
    tmp_item.n_entities = len(tmp_item.entity)
    tmp_item.n_bioassemblies = len(tmp_item.bioassembly)
    tmp_item.n_bonds = len(tmp_item.bond)

    # complete nested objects in chains:

    count_groups = 0
    for index_chain in range(item.num_chains):
        chain = tmp_item.chain[index_chain]
        n_groups = item.groups_per_chain[index_chain]
        for index_group in range(count_groups, count_groups+n_groups):
            group = tmp_item.group[index_group]
            chain.group.append(group)
            for atom in group.atom:
                atom.group = group
                atom.chain = chain
                chain.atom.append(atom)
        count_groups+=n_groups

    # complete nested objects in bioassemblies:

    for bioassembly in tmp_item.bioassembly:
        if len(bioassembly.transformation)>1:
            raise NotImplementedError("Not prepared to work with multiple transformations")
        for index_chain in bioassembly.transformation[0].chain_indices:
            chain = tmp_item.chain[index_chain]
            bioassembly.chain.append(chain)
            bioassembly.group.extend(chain.group)
            bioassembly.atom.extend(chain.atom)

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


    return tmp_item

