from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {ii:False for ii in _all_attributes}

form_attributes['group_index'] = True
form_attributes['group_name'] = True

del(_all_attributes)
