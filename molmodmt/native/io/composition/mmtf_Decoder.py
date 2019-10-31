
def import_mmtf_Decoder(item):

    from molmodmt.native.composition import Composition
    from molmodmt.native.elements import Atom, Group, Component, Chain, Molecule, Entity, BioAssembly
    from molmodmt.native.elements.molecules import Ion, Water, Cosolute, SmallMolecule, Peptide, Protein, DNA, RNA

    tmp_item = Composition()

    tmp_item.atom = []
    tmp_item.group = []
    tmp_item.chain = []

    for id, index in zip(range(item.num_atoms), item.atom_id_list):
        atom = Atom(id=id, index=index)
        tmp_item.atom.append(atom)

    for id, index in zip(range(item.num_atoms), item.group_id_list):
        group = Group(id=id, index=index)
        tmp_item.group.append(group)

    for id, index, name in zip(range(item.num_chains), item.chain_id_list, item.chain_name_list):
        chain = Chain(id=id, index=index, name=name)
        tmp_item.chain.append(chain)

    #https://github.com/rcsb/mmtf/blob/master/spec.md#bondatomlist
    #https://mmtf.rcsb.org/faq.html
    #https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5473584/
    #https://github.com/rcsb/mmtf/issues/34

    tmp_item.n_atoms = len(tmp_item.atom)
    tmp_item.n_groups = len(tmp_item.group)
    tmp_item.n_chains = len(tmp_item.chain)

    return tmp_item

