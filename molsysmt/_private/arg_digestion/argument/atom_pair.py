from ...exceptions import ArgumentError
import numpy as np
from ...variables import is_iterable_of_integers, is_iterable_of_pairs

functions_with_boolean = (
        )

functions_with_list_as_output = (
    'add_harmonic_bond_force',
        )

def digest_atom_pair(atom_pair, caller=None):


    if caller is not None:
        if caller.endswith(functions_with_list_as_output):
            if is_iterable_of_integers(atom_pair):
                if isinstance(atom_pair, (list,tuple)) and len(atom_pair) == 2:
                    return [[atom_pair[0], atom_pair[1]]]
                elif isinstance(atom_pair, np.ndarray) and len(atom_pair) == 2:
                    return [[atom_pair[0], atom_pair[1]]]
            elif is_iterable_pairs(atom_pair):
                return [[ii, jj] for ii,jj in atom_pair]

    raise ArgumentError('atom_pair', value=atom_pair, caller=caller, message=None)

