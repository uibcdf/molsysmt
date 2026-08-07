from ._bond_state_attribute import digest_bond_state_attribute


def digest_fractional_bond_order(fractional_bond_order, caller=None):
    return digest_bond_state_attribute(
        'fractional_bond_order', fractional_bond_order, caller, 'float'
    )
