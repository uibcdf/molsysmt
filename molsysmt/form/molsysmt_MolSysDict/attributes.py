from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {ii: False for ii in _all_attributes}

for attribute in [
    'atom_index', 'atom_id', 'atom_name', 'atom_type',
    'group_index', 'group_id', 'group_name', 'group_type',
    'component_index', 'component_id', 'component_name', 'component_type',
    'molecule_index', 'molecule_id', 'molecule_name', 'molecule_type',
    'chain_index', 'chain_id', 'chain_name', 'chain_type',
    'entity_index', 'entity_id', 'entity_name', 'entity_type',
    'n_atoms', 'n_groups', 'n_components', 'n_molecules', 'n_chains', 'n_entities',
    'bond_index', 'bond_type', 'bond_order', 'bonded_atoms', 'bonded_atom_pairs',
    'inner_bond_index', 'inner_bonded_atoms', 'inner_bonded_atom_pairs', 'n_bonds', 'n_inner_bonds',
    'structure_index', 'structure_id', 'time', 'box', 'box_shape', 'box_angles', 'box_lengths',
    'box_volume', 'coordinates', 'n_structures'
]:
    attributes[attribute] = True

del _all_attributes
