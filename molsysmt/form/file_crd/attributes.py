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
attributes['coordinates'] = True
attributes['box'] = True
attributes['time'] = True
attributes['structure_id'] = True
attributes['n_atoms'] = True
attributes['n_groups'] = True
attributes['n_structures'] = True

del(_all_attributes)

