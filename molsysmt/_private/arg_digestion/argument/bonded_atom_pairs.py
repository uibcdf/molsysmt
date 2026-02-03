from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_bonded_atom_pairs(bonded_atom_pairs, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(bonded_atom_pairs, bool):
            return bonded_atom_pairs
    elif caller.endswith('add_bonds.add_bonds'):
        if isinstance(bonded_atom_pairs, list):
            for sublist in bonded_atom_pairs:
                if not (isinstance(sublist, list) and len(sublist) == 2):
                    raise ArgumentError('bonded_atom_pairs', value=bonded_atom_pairs, caller=caller, message=None)
                if not all(isinstance(item, (int, np.integer)) for item in sublist):
                    print('aa')
                    raise ArgumentError('bonded_atom_pairs', value=bonded_atom_pairs, caller=caller, message=None)
            return np.array(bonded_atom_pairs)
        elif isinstance(bonded_atom_pairs, np.ndarray):
            if len(bonded_atom_pairs.shape)==2 and bonded_atom_pairs.shape[1]==2:
                return bonded_atom_pairs
            else:
                raise ArgumentError('bonded_atom_pairs', value=bonded_atom_pairs, caller=caller, message=None)

    raise ArgumentError('bonded_atom_pairs', value=bonded_atom_pairs, caller=caller, message=None)

