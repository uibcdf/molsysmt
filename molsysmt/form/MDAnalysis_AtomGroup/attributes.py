from molsysmt.attribute import attributes as _all_attributes

attributes = {ii: False for ii in _all_attributes.keys()}

# MDAnalysis.AtomGroup supports most topological and structural attributes
# because it can delegate to its parent universe.

for ii, jj in _all_attributes.items():
    if jj['topological'] or jj['structural']:
        attributes[ii] = True

# Mechanical attributes might be restricted depending on the universe
attributes['formal_charge'] = True
attributes['partial_charge'] = True
attributes['isotope'] = False
