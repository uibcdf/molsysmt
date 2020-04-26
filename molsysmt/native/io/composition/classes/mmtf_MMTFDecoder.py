def from_mmtf_MMTFDecoder(item, atom_indices='all', frame_indices='all', bioassembly_index=0, bioassembly_name=None):


    from molsysmt.native.io.dataframe.classes import from_mmtf_MMTFDecoder as molsysmt_dataframe_from_mmtf_MMTFDecoder
    from molsysmt.native.io.composition.classes import from_molsysmt_DataFrame as molsysmt_composition_from_molsysmt_DataFrame
    from numpy import reshape, sum

    dataframe = molsysmt_dataframe_from_mmtf_MMTFDecoder(item, atom_indices='all',
            frame_indices='all', bioassembly_index=bioassembly_index,
            bioassembly_name=bioassembly_name)

    tmp_item = molsysmt_composition_from_molsysmt_DataFrame(dataframe)

    from  molsysmt.native.elements import BioAssembly_Transformation

    bioassembly_index = tmp_item.bioassembly[0].index
    mmtf_bioassembly = item.bio_assembly[bioassembly_index]

    # bioassembly transformation

    for transformation in mmtf_bioassembly['transformList']:

        bioassembly_transformation = BioAssembly_Transformation()
        bioassembly_transformation.chain_indices = transformation['chainIndexList']
        bioassembly_transformation.matrix = reshape(transformation['matrix'],(4,4))
        tmp_item.bioassembly[bioassembly_index].transformation.append(bioassembly_transformation)

    # groups

    count_atoms = 0

    for mmtf_group_type, group_index in zip(item.group_type_list, range(item.num_groups)):

        mmtf_group = item.group_list[mmtf_group_type]
        group = tmp_item.group[group_index]
        group.chemical_type = mmtf_group['chemCompType']
        group.formal_charge = sum(mmtf_group['formalChargeList'])
        if group.type in ['aminoacid', 'nucleotide']:
            group.lettercode = mmtf_group['singleLetterCode']

        ## bonds intra-group
        #for bond_pair, bond_order in zip(reshape(mmtf_group['bondAtomList'],(-1,2)), mmtf_group['bondOrderList']):

        #    atom_index_0 = bond_pair[0]+count_atoms
        #    atom_index_1 = bond_pair[1]+count_atoms

        #    bond = tmp_item.atom[atom_index_0].bond_with_atom_index[atom_index_1]
        #    bond.order = bond_order

        #count_atoms += len(group.atom)

    # bonds inter-groups

    #for bond_pair, bond_order in zip(reshape(item.bond_atom_list,(-1,2)), item.bond_order_list):

    #    atom_index_0 = bond_pair[0]
    #    atom_index_1 = bond_pair[1]

    #    bond = tmp_item.atom[atom_index_0].bond_with_atom_index[atom_index_1]
    #    bond.order = bond_order

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

    tmp_item = tmp_item.extract(atom_indices=atom_indices)

    return tmp_item

