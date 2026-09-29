from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {name: False for name in _all_attributes}
attributes["n_atoms"] = True
attributes["n_structures"] = True
