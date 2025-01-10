from ...exceptions import ArgumentError

def digest_atom_pair(atom_pair, caller=None):

    if caller.endswith('add_harmonic_bond_force'):
        if isinstance(atom_pair, (list, tuple)) and len(atom_pair) == 2:
            return atom_pair

    raise ArgumentError('atom_pair', value=pairs, caller=caller, message=None)

