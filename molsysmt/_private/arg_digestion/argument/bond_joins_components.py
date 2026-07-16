from ._bond_state_attribute import digest_bond_state_attribute


def digest_bond_joins_components(bond_joins_components, caller=None):
    return digest_bond_state_attribute(
        'bond_joins_components', bond_joins_components, caller, 'boolean'
    )
