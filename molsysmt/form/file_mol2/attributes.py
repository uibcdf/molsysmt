from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {ii:False for ii in _all_attributes}

attributes['atom_index'] = True
attributes['atom_id'] = True
attributes['atom_name'] = True
attributes['atom_type'] = True
attributes['bond_index'] = True
attributes['bond_id'] = True
attributes['bond_type'] = True
attributes['bond_order'] = True
attributes['fractional_bond_order'] = True
attributes['bond_is_aromatic'] = True
attributes['bond_joins_components'] = True
attributes['bond_evidence'] = True
attributes['group_index'] = True
attributes['group_id'] = True
attributes['group_name'] = True
attributes['group_type'] = True
attributes['component_index'] = True
attributes['molecule_index'] = True
attributes['molecule_id'] = True
attributes['molecule_name'] = True
attributes['molecule_type'] = True
attributes['chain_index'] = True
attributes['chain_id'] = True
attributes['chain_name'] = True
attributes['chain_type'] = True
attributes['coordinates'] = True
attributes['structure_index'] = True
attributes['structure_id'] = True
attributes['n_structures'] = True
attributes['box'] = True
attributes['partial_charge'] = True

for attribute in (
    'n_atoms', 'n_groups', 'n_components', 'n_molecules', 'n_chains',
    'n_entities', 'n_bonds', 'n_amino_acids', 'n_nucleotides', 'n_ions',
    'n_waters', 'n_small_molecules', 'n_peptides', 'n_proteins', 'n_dnas',
    'n_rnas', 'n_lipids', 'n_polysaccharides', 'n_saccharides',
):
    attributes[attribute] = True

del(_all_attributes)
