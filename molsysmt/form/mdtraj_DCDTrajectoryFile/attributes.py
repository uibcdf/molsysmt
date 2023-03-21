from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {ii:False for ii in _all_attributes}

attributes['atom_index'] = True
attributes['n_atoms'] = True

attributes['structure_index'] = True
attributes['time'] = True
attributes['coordinates'] = True
attributes['box'] = True
attributes['box_shape'] = True
attributes['box_volume'] = True
attributes['box_lengths'] = True
attributes['box_angles'] = True
attributes['n_structures'] = True

del(_all_attributes)
