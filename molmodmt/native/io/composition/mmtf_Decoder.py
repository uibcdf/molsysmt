
def import_mmtf_Decoder(item):

    from molmodmt.native.composition import Composition
    from molmodmt.native import elements
    from molmodmt.topology.groups_classification import MMTFDecoder_group_to_group_class

    tmp_item = Composition()

    tmp_item.atom = []
    tmp_item.group = []
    tmp_item.chain = []

    for id, index in zip(range(item.num_atoms), item.atom_id_list):
        atom = element.Atom(id=id, index=index)
        tmp_item.atom.append(atom)

    for id, index, id_type in zip(range(item.num_groups), item.group_id_list, item.group_type_list):
        group_mmtf = item.group_list[id_type]
        group_class = MMTFDecoder_group_to_group_class(group_mmtf)
        if group_class is None:
            group = element.Group(id=id, index=index)
        else:
            group = getattr(element.groups,group_class)(id=id, index=index)

    for id, index, name in zip(range(item.num_chains), item.chain_id_list, item.chain_name_list):
        chain = element.Chain(id=id, index=index, name=name)
        tmp_item.chain.append(chain)


    # Inter group bonds
    #if hasattr(mmtf, 'bond_atom_list'):


    #https://github.com/rcsb/mmtf/blob/master/spec.md#bondatomlist
    #https://mmtf.rcsb.org/faq.html
    #https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5473584/
    #https://github.com/rcsb/mmtf/issues/34

    tmp_item.n_atoms = len(tmp_item.atom)
    tmp_item.n_groups = len(tmp_item.group)
    tmp_item.n_chains = len(tmp_item.chain)
    tmp_item.n_bonds = len(tmp_item.bond)

    return tmp_item

