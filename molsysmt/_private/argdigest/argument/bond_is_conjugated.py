from ._bond_state_attribute import digest_bond_state_attribute


def digest_bond_is_conjugated(bond_is_conjugated, caller=None):
    return digest_bond_state_attribute(
        'bond_is_conjugated', bond_is_conjugated, caller, 'boolean'
    )
