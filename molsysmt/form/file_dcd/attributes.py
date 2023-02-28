from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {ii:False for ii in _all_attributes}

form_attributes['coordinates'] = True
form_attributes['box'] = True

del(_all_attributes)
