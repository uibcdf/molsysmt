
def from_mmtf_MMTFDecoder(item, atom_indices='all', frame_indices='all'):

    from molmodmt.native.composition import Composition
    from molmodmt.native import elements
    from molmodmt.utils.composition.classification import MMTFDecoder_group_to_group_class
    from molmodmt.utils.composition.classification import MMTFDecoder_entity_to_entity_class
    import numpy as np


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
        for chain_id in entity_mmtf['chainIndexList']:
            tmp_chain = tmp_item.chain[chain_id]
            tmp_chain.entity = entity
            entity.chain.append(tmp_chain)
            for tmp_group in tmp_chain.group:
                tmp_group.entity=entity
                entity.group.append(tmp_group)
                for tmp_atom in tmp_group.atom:
                    entity.atom.append(tmp_atom)
                    tmp_atom.entity=entity
        tmp_item.entity.append(entity)

    n_bioassembly = len(item.bio_assembly)
    for id in range(n_bioassembly):
            tmp_chain = tmp_item.chain[chain_id]
            tmp_chain.bioassembly = bioassembly
            bioassembly.chain.append(tmp_chain)
            for tmp_group in tmp_chain.group:
                tmp_group.bioassembly=bioassembly
                bioassembly.group.append(tmp_group)
                for tmp_atom in tmp_group.atom:
                    bioassembly.atom.append(tmp_atom)
                    tmp_atom.bioassembly=bioassembly
        tmp_item.bioassembly.append(bioassembly)


    # Inter group bonds
    #if hasattr(mmtf, 'bond_atom_list'):

    #https://github.com/rcsb/mmtf/blob/master/spec.md#bondatomlist
    #https://mmtf.rcsb.org/faq.html
    #https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5473584/
    #https://github.com/rcsb/mmtf/issues/34

    tmp_item.n_atoms = len(tmp_item.atom)
    tmp_item.n_groups = len(tmp_item.group)
    tmp_item.n_chains = len(tmp_item.chain)
    tmp_item.n_molecules = len(tmp_item.molecule)
    tmp_item.n_entities = len(tmp_item.entity)
    tmp_item.n_bioassemblies = len(tmp_item.bioassembly)
    tmp_item.n_bonds = len(tmp_item.bond)

    return tmp_item

