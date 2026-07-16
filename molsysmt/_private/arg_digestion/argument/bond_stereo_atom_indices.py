from ._bond_state_attribute import digest_stereo_atom_indices


def digest_bond_stereo_atom_indices(bond_stereo_atom_indices, caller=None):
    return digest_stereo_atom_indices(
        'bond_stereo_atom_indices', bond_stereo_atom_indices, caller
    )
