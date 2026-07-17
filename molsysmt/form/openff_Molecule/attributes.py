from molsysmt.attribute import attributes as _all_attributes

attributes = {ii: False for ii in _all_attributes.keys()}

for ii, jj in _all_attributes.items():
    if jj['topological']:
        attributes[ii] = True

attributes['formal_charge'] = True
attributes['partial_charge'] = True
attributes['atom_is_aromatic'] = True
attributes['atom_stereochemistry'] = True
attributes['bond_id'] = True
attributes['fractional_bond_order'] = True
attributes['bond_is_aromatic'] = True
attributes['bond_joins_components'] = True
attributes['bond_evidence'] = True
attributes['isotope'] = False
attributes['coordinates'] = True
attributes['structure_id'] = True
attributes['structure_index'] = True
attributes['n_structures'] = True

del _all_attributes
