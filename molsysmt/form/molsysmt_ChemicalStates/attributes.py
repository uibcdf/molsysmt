from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {name: False for name in _all_attributes}
for name in ("n_atoms", "n_chemical_states", "reference_chemical_state_index"):
    attributes[name] = True
