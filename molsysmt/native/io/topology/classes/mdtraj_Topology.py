def from_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe import from_mdtraj_Topology as dataframe_from_mmtf_MMTFDecoder
    from molsysmt.native.io.topology import from_molsysmt_DataFrame as topology_from_molsysmt_DataFrame
    from numpy import reshape, sum

    dataframe = dataframe_from_mmtf_MMTFDecoder(item, atom_indices=atom_indices, frame_indices=frame_indices)

    tmp_item = topology_from_molsysmt_DataFrame(dataframe)

    # groups

    atom_index=0
    count_atoms = 0

    for mmtf_group_type, group_index in zip(item.group_type_list, range(item.num_groups)):

        mmtf_group = item.group_list[mmtf_group_type]
        group = tmp_item.group[group_index]
        group.chemical_type = mmtf_group['chemCompType']
        group.formal_charge = sum(mmtf_group['formalChargeList'])
        if group.type in ['aminoacid', 'nucleotide']:
            group.lettercode = mmtf_group['singleLetterCode']

        # atoms

        for atom_formal_charge in mmtf_group['formalChargeList']:

            atom = tmp_item.atom[atom_index]
            atom.formal_charge = atom_formal_charge

            atom_index+=1

        # bonds intra-group
        for bond_pair, bond_order in zip(reshape(mmtf_group['bondAtomList'],(-1,2)), mmtf_group['bondOrderList']):

            atom_index_0 = bond_pair[0]+count_atoms
            atom_index_1 = bond_pair[1]+count_atoms

            bond = tmp_item.atom[atom_index_0].bond_with_atom_index[atom_index_1]
            bond.order = bond_order

        count_atoms += len(group.atom)

    # bonds inter-groups

    for bond_pair, bond_order in zip(reshape(item.bond_atom_list,(-1,2)), item.bond_order_list):

        atom_index_0 = bond_pair[0]
        atom_index_1 = bond_pair[1]

        bond = tmp_item.atom[atom_index_0].bond_with_atom_index[atom_index_1]
        bond.order = bond_order

    # entities

    entity_index = 0

    for mmtf_entity in item.entity_list:

        entity = tmp_item.entity[entity_index]

        entity.mmtf_type = mmtf_entity['type']
        entity.description = mmtf_entity['description']

        if entity.type in ['protein']:
            entity.sequence = mmtf_entity['sequence']


        entity_index += 1

    # molecules:

    for entity in tmp_item.entity:

        if entity.type == "protein":
            for molecule in entity.molecule:
                molecule.sequence = entity.sequence


    # End

    return tmp_item

