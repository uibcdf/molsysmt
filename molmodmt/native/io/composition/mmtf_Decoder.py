
def import_mmtf_Decoder(item):

    from molmodmt.native.composition import Composition
    from molmodmt.native import elements
    from molmodmt.utils.groups.classification import MMTFDecoder_group_to_group_class
    import numpy as np

    tmp_item = Composition()

    tmp_item.atom = []
    tmp_item.group = []
    tmp_item.chain = []
    tmp_item.bond = []

    for id, index in zip(range(item.num_atoms), item.atom_id_list):
        atom = elements.Atom(id=id, index=index)
        tmp_item.atom.append(atom)

    count_atoms = 0
    for id, index, id_type in zip(range(item.num_groups), item.group_id_list, item.group_type_list):
        group_mmtf = item.group_list[id_type]
        group_class = MMTFDecoder_group_to_group_class(group_mmtf)
        if group_class is None:
            group = elements.Group(id=id, index=index)
        else:
            group = getattr(elements.groups,group_class)(id=id, index=index)
        group.name = group_mmtf['groupName']
        group.chemical_type = group_mmtf['chemCompType']
        if group_mmtf['singleLetterCode']!='?':
            group.lettercode=group_mmtf['singleLetterCode']
        group.formal_charge=np.sum(group_mmtf['formalChargeList'])
        for bond_pair, bond_order in zip(np.reshape(group_mmtf['bondAtomList'],(-1,2)), group_mmtf['bondOrderList']):
            tmp_atom_0 = tmp_item.atom[bond_pair[0]+count_atoms]
            tmp_atom_1 = tmp_item.atom[bond_pair[1]+count_atoms]
            tmp_atom_0.bonded_atoms.append(tmp_atom_1)
            tmp_atom_1.bonded_atoms.append(tmp_atom_0)
            bond = elements.Bond(atoms=[tmp_atom_0, tmp_atom_1], order=bond_order)
            tmp_item.bond.append(bond)
        for atom_name, atom_element, atom_formal_charge in zip(group_mmtf['atomNameList'], group_mmtf['elementList'], group_mmtf['formalChargeList']):
            atom_id = count_atoms
            tmp_atom = tmp_item.atom[atom_id]
            tmp_atom.name = atom_name
            tmp_atom.type = atom_name
            tmp_atom.element = atom_element
            tmp_atom.formal_charge = atom_formal_charge
            tmp_atom.group = group
            group.atom.append(tmp_atom)
            count_atoms+=1
        tmp_item.group.append(group)

    for bond_pair, bond_order in zip(np.reshape(item.bond_atom_list,(-1,2)), item.bond_order_list):
        tmp_atom_0 = tmp_item.atom[bond_pair[0]]
        tmp_atom_1 = tmp_item.atom[bond_pair[1]]
        tmp_atom_0.bonded_atoms.append(tmp_atom_1)
        tmp_atom_1.bonded_atoms.append(tmp_atom_0)
        bond = elements.Bond(atoms=[tmp_atom_0, tmp_atom_1], order=bond_order)
        tmp_item.bond.append(bond)

    count_groups=0
    for id, index, name, n_groups in zip(range(item.num_chains), item.chain_id_list, item.chain_name_list, item.groups_per_chain):
        chain = elements.Chain(id=id, index=index, name=name)
        for group_id in range(count_groups, n_groups):
            tmp_group = tmp_item.group[group_id]
            tmp_group.chain=chain
            chain.group.append(tmp_group)
            for tmp_atom in tmp_group.atom:
                tmp_atom.chain=chain
                chain.atom.append(tmp_atom)
        tmp_item.chain.append(chain)
        count_groups+=n_groups

    n_entities = len(item.entity_list)
    for id, entity_mmtf in zip(range(n_entities), item.entity_list):
        name = entity_mmtf['description']
        type = entity_mmtf['type']
        entity_class = MMTFDecoder_entity_to_entity_class(entity_mmtf)
        if entity_class is None:
            entity = elements.Entity(id=id, name=name)
        else:
            entity = getattr(elements.entities, group_class)(id=id, name=name)
        entity.mmtf_type = type
        for chain_id in entity_mmtf['chainIndexList']:
            tmp_chain = tmp_item.chain[chain_id]
            entity.chain.append(tmp_chain)
        tmp_item.entity.append(entity)

    # Inter group bonds
    #if hasattr(mmtf, 'bond_atom_list'):

    #https://github.com/rcsb/mmtf/blob/master/spec.md#bondatomlist
    #https://mmtf.rcsb.org/faq.html
    #https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5473584/
    #https://github.com/rcsb/mmtf/issues/34

    tmp_item.n_atoms = len(tmp_item.atom)
    tmp_item.n_groups = len(tmp_item.group)
    tmp_item.n_chains = len(tmp_item.chain)
    tmp_item.n_entities = len(tmp_item.entity)
    tmp_item.n_bonds = len(tmp_item.bond)

    return tmp_item

