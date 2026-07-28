from molsysmt.attribute import attributes as _all_attributes

attributes = {ii: False for ii in _all_attributes.keys()}

for ii, jj in _all_attributes.items():
    if jj['topological'] or jj['structural']:
        attributes[ii] = True

attributes['kinetic_energy'] = False
attributes['occupancy'] = False
attributes['potential_energy'] = False
attributes['structure_chemical_state_index'] = False
attributes['temperature'] = False
attributes['total_energy'] = False
