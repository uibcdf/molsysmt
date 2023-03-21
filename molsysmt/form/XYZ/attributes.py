from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {ii:False for ii in _all_attributes}

###
### TOPOLOGICAL ATTRIBUTES
###

attributes['atom_index'] = True
attributes['n_atoms'] = True

###
### STRUCTURAL ATTRIBUTES
###

attributes['structure_index'] = True
attributes['n_structures'] = True
attributes['coordinates'] = True

del(_all_attributes)
