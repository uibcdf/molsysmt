from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {ii: False for ii in _all_attributes}

# Topological coverage
attributes['atom_index'] = True
attributes['atom_id'] = True
attributes['atom_name'] = True
attributes['group_id'] = True
attributes['group_name'] = True
attributes['chain_id'] = True
attributes['entity_id'] = True
attributes['formal_charge'] = True
attributes['n_atoms'] = True
attributes['n_bonds'] = True
attributes['bond_index'] = True
attributes['bonded_atoms'] = True

# Structural coverage
attributes['coordinates'] = True
attributes['time'] = True
attributes['n_structures'] = True

del _all_attributes
