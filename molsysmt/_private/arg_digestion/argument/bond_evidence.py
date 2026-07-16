from ._bond_state_attribute import digest_bond_state_attribute


def digest_bond_evidence(bond_evidence, caller=None):
    return digest_bond_state_attribute(
        'bond_evidence', bond_evidence, caller, 'choice',
        choices={'explicit', 'inferred', 'user_defined', 'unknown'},
    )
