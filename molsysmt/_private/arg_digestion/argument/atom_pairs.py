from ...exceptions import ArgumentError
from ...variables import is_iterable_of_integers, is_iterable_of_pairs
import numpy as np

def digest_atom_pairs(atom_pairs, caller=None):

    if caller.endswith('add_harmonic_bond_force'):
        if is_iterable_of_integers(atom_pairs):
            if isinstance(atom_pairs, (list,tuple)) and len(atom_pairs) == 2:
                return [[atom_pairs[0], atom_pairs[1]]]
            elif isinstance(atom_pairs, np.ndarray) and len(atom_pairs) == 2:
                return [[atom_pairs[0], atom_pairs[1]]]
        elif is_iterable_of_pairs(atom_pairs):
            return [[ii, jj] for ii,jj in atom_pairs]
    elif caller.endswith('add_contacts'):
        if atom_pairs is None:
            return None
        if is_iterable_of_integers(atom_pairs):
            if isinstance(atom_pairs, (list,tuple)) and len(atom_pairs) == 2:
                return np.array([[atom_pairs[0], atom_pairs[1]]])
            elif isinstance(atom_pairs, np.ndarray) and len(atom_pairs) == 2:
                return np.array([[atom_pairs[0], atom_pairs[1]]])
        elif is_iterable_of_pairs(atom_pairs):
            if isinstance(atom_pairs, (list,tuple)):
                return np.array([[ii, jj] for ii,jj in atom_pairs])
            elif isinstance(atom_pairs, np.ndarray):
                return atom_pairs

    raise ArgumentError('atom_pairs', value=atom_pairs, caller=caller, message=None)

