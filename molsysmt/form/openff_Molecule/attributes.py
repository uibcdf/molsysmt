from molsysmt.attribute import attributes as _all_attributes

attributes = {ii: False for ii in _all_attributes.keys()}

for ii, jj in _all_attributes.items():
    if jj['topological']:
        attributes[ii] = True

attributes['formal_charge'] = True
attributes['partial_charge'] = True

del _all_attributes
