from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {ii:False for ii in _all_attributes}

attributes['group_index'] = True
attributes['group_name'] = True

del(_all_attributes)
