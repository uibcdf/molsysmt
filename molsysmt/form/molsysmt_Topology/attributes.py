from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {ii:False for ii in _all_attributes}

attributes['atom_index'] = True
attributes['atom_id'] = True
attributes['atom_name'] = True
attributes['atom_type'] = True
attributes['group_index'] = True
attributes['group_id'] = True
attributes['group_name'] = True
attributes['group_type'] = True
attributes['component_index'] = True
attributes['component_id'] = True
attributes['component_name'] = True
attributes['component_type'] = True
attributes['molecule_index'] = True
attributes['molecule_id'] = True
attributes['molecule_name'] = True
attributes['molecule_type'] = True
attributes['chain_index'] = True
attributes['chain_id'] = True
attributes['chain_name'] = True
attributes['chain_type'] = True
attributes['entity_index'] = True
attributes['entity_id'] = True
attributes['entity_name'] = True
attributes['entity_type'] = True
attributes['n_atoms'] = True
attributes['n_groups'] = True
attributes['n_components'] = True
attributes['n_molecules'] = True
attributes['n_chains'] = True
attributes['n_entities'] = True
attributes['n_amino_acids'] = True
attributes['n_nucleotides'] = True
attributes['n_ions'] = True
attributes['n_waters'] = True
attributes['n_small_molecules'] = True
attributes['n_peptides'] = True
attributes['n_proteins'] = True
attributes['n_dnas'] = True
attributes['n_rnas'] = True
attributes['n_lipids'] = True
attributes['n_oligosaccharides'] = True
attributes['n_saccharides'] = True


attributes['bond_index'] = True
attributes['bond_id'] = False
attributes['bond_type'] = True
attributes['bond_order'] = True
attributes['bonded_atoms'] = True
attributes['bonded_atom_pairs'] = True
attributes['inner_bond_index'] = True
attributes['inner_bonded_atoms'] = True
attributes['inner_bonded_atom_pairs'] = True
attributes['n_bonds'] = True
attributes['n_inner_bonds'] = True

del(_all_attributes)
