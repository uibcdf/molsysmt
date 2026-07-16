from ._bond_state_attribute import digest_bond_state_attribute


def digest_bond_is_aromatic(bond_is_aromatic, caller=None):
    return digest_bond_state_attribute(
        'bond_is_aromatic', bond_is_aromatic, caller, 'boolean'
    )
