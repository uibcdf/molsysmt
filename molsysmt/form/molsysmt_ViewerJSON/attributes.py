from molsysmt.attribute.attributes import attributes as _all_attributes

# Start pessimistic (everything unavailable) and toggle supported entries
attributes = {ii: False for ii in _all_attributes}

# Topological attributes we can expose
attributes['atom_index'] = True
attributes['atom_id'] = True
attributes['atom_name'] = True
attributes['group_id'] = True
attributes['group_name'] = True
attributes['chain_id'] = True
attributes['entity_id'] = True
attributes['formal_charge'] = True
attributes['partial_charge'] = True
attributes['bond_order'] = True
attributes['bond_type'] = True
attributes['n_atoms'] = True
attributes['n_bonds'] = True
attributes['bond_index'] = True
attributes['bonded_atoms'] = True

# Structural attributes we can expose
attributes['coordinates'] = True
attributes['time'] = True
attributes['n_structures'] = True

del _all_attributes
