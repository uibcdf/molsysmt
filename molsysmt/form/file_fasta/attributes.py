from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {ii:False for ii in _all_attributes}

# FASTA is sequence-only: group names/indices per chain, chain and entity metadata

attributes['group_index'] = True
attributes['group_name'] = True
attributes['group_type'] = True
attributes['chain_index'] = True
attributes['chain_id'] = True
attributes['chain_name'] = True
attributes['chain_type'] = True
attributes['entity_index'] = True
attributes['entity_id'] = True
attributes['entity_name'] = True
attributes['entity_type'] = True
attributes['n_groups'] = True
attributes['n_chains'] = True
attributes['n_entities'] = True
attributes['n_amino_acids'] = True

del(_all_attributes)
