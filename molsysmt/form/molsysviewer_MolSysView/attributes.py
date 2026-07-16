from molsysmt.attribute import attributes as _all_attributes

attributes = {ii: False for ii in _all_attributes.keys()}

for ii, jj in _all_attributes.items():
    if jj['topological'] or jj['structural']:
        attributes[ii] = True

attributes['bond_id'] = False
attributes['isotope'] = False
