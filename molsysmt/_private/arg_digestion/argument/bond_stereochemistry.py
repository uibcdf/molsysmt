from ._bond_state_attribute import digest_bond_state_attribute


def digest_bond_stereochemistry(bond_stereochemistry, caller=None):
    return digest_bond_state_attribute(
        'bond_stereochemistry', bond_stereochemistry, caller, 'string'
    )
