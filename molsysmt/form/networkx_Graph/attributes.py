from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {ii:False for ii in _all_attributes}

attributes['atom_index'] = True
attributes['atom_id'] = True
attributes['atom_name'] = True
attributes['atom_type'] = True
attributes['isotope'] = True
attributes['group_index'] = True
attributes['chain_index'] = True
attributes['component_index'] = True
attributes['formal_charge'] = True
attributes['atom_is_aromatic'] = True
attributes['n_unpaired_electrons'] = True
attributes['n_implicit_hydrogens'] = True
attributes['allows_implicit_hydrogens'] = True
attributes['atom_stereochemistry'] = True
attributes['bond_index'] = True
attributes['bonded_atoms'] = True
attributes['bond_id'] = True
attributes['bond_order'] = True
attributes['fractional_bond_order'] = True
attributes['bond_type'] = True
attributes['bond_is_aromatic'] = True
attributes['bond_is_conjugated'] = True
attributes['bond_stereochemistry'] = True
attributes['bond_stereo_atom_indices'] = True
attributes['bond_donor_atom_index'] = True
attributes['bond_acceptor_atom_index'] = True
attributes['bond_joins_components'] = True
attributes['bond_evidence'] = True
attributes['connectivity_completeness'] = True
attributes['component_completeness'] = True
attributes['component_evidence'] = True
attributes['n_atoms'] = True
attributes['n_bonds'] = True

del(_all_attributes)
