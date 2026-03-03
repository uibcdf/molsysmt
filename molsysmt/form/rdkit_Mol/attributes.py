from molsysmt.attribute import attributes as _all_attributes

attributes = {ii: False for ii in _all_attributes.keys()}

# rdkit.Mol supports topological and structural attributes
for ii, jj in _all_attributes.items():
    if jj['topological'] or jj['structural']:
        attributes[ii] = True

# Mechanical attributes are partially supported via properties
attributes['formal_charge'] = True
attributes['partial_charge'] = True
