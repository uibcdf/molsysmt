from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {ii:False for ii in _all_attributes}


###
### STRUCTURAL ATTRIBUTES
###

attributes['structure_index'] = True
attributes['structure_id'] = True
attributes['time'] = True
attributes['box'] = True
attributes['box_shape'] = True
attributes['box_angles'] = True
attributes['box_lengths'] = True
attributes['box_volume'] = True
attributes['coordinates'] = True
attributes['occupancy'] = True
attributes['alternate_location'] = True
attributes['b_factor'] = True
attributes['n_structures'] = True


del(_all_attributes)
