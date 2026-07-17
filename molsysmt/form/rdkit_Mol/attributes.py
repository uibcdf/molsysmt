from molsysmt.attribute import attributes as _all_attributes

attributes = {ii: False for ii in _all_attributes.keys()}

# RDKit molecules expose their chemical graph through the native topology seam.
for ii, jj in _all_attributes.items():
    if jj['topological'] or jj['chemical_state']:
        attributes[ii] = True

# Conformers contain coordinates but no time, box, velocities, or per-frame
# thermodynamic metadata.
for ii in ('coordinates', 'structure_id', 'structure_index', 'n_structures'):
    attributes[ii] = True

# Partial charge is optional per-atom metadata rather than intrinsic RDKit
# graph state. The instance-aware adapter checks supported property names.
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

del _all_attributes
