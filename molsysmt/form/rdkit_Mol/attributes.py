from molsysmt.attribute import attributes as _all_attributes

attributes = {ii: False for ii in _all_attributes.keys()}

# rdkit.Mol supports topological and structural attributes
for ii, jj in _all_attributes.items():
    if jj['topological'] or jj['structural']:
        attributes[ii] = True

# Mechanical attributes are partially supported via properties
attributes['formal_charge'] = True
attributes['partial_charge'] = True
attributes['atom_is_aromatic'] = True
attributes['n_unpaired_electrons'] = True
attributes['n_implicit_hydrogens'] = True
attributes['allows_implicit_hydrogens'] = True
attributes['atom_stereochemistry'] = True
attributes['fractional_bond_order'] = True
attributes['bond_is_aromatic'] = True
attributes['bond_is_conjugated'] = True
attributes['bond_stereochemistry'] = True
attributes['bond_stereo_atom_indices'] = True
attributes['bond_donor_atom_index'] = True
attributes['bond_acceptor_atom_index'] = True
attributes['bond_joins_components'] = True
attributes['bond_evidence'] = True
attributes['isotope'] = True
attributes['structure_chemical_state_index'] = False
