from molsysmt.attribute import attributes as _all_attributes

attributes = {ii: False for ii in _all_attributes.keys()}

# file:smi exposes the same topological attributes as string:smiles
# (piped through molsysmt.Topology via rdkit.Mol)
for ii, jj in _all_attributes.items():
    if jj['topological']:
        attributes[ii] = True

attributes['formal_charge'] = True
attributes['partial_charge'] = False
attributes['isotope'] = False

del _all_attributes
