from ...exceptions import ArgumentError
import numpy as np

def digest_atom_pairs(atom_pairs, caller=None):

    if caller.endswith('add_harmonic_bond_force'):
        if is_iterable_of_integers(atom_pairs):
            if isinstance(atom_pairs, (list,tuple)) and len(atom_pairs) == 2:
                return [[atom_pairs[0], atom_pairs[1]]]
            elif isinstance(atom_pairs, np.ndarray) and len(atom_pairs) == 2:
                return [[atom_pairs[0], atom_pairs[1]]]
        elif is_iterable_pairs(atom_pairs):
            return [[ii, jj] for ii,jj in atom_pairs]

    raise ArgumentError('atom_pairs', value=atom_pairs, caller=caller, message=None)

