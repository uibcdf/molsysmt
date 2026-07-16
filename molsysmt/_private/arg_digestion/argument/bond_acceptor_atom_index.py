from ._bond_state_attribute import digest_bond_state_attribute


def digest_bond_acceptor_atom_index(bond_acceptor_atom_index, caller=None):
    return digest_bond_state_attribute(
        'bond_acceptor_atom_index', bond_acceptor_atom_index, caller, 'integer'
    )
