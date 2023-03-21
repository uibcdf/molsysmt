from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {ii:False for ii in _all_attributes}

attributes['atom_index'] = True
attributes['bond_index'] = True
attributes['bonded_atoms'] = True

del(_all_attributes)
