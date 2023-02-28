from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {ii:False for ii in _all_attributes}

attributes['coordinates'] = True
attributes['box'] = True

del(_all_attributes)
