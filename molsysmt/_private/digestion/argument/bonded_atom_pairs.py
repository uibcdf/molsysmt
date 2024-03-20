from molsysmt._private.exceptions import ArgumentError
from numpy import ndarray

def digest_bonded_atom_pairs(bonded_atom_pairs, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(bonded_atom_pairs, bool):
            return bonded_atom_pairs
    elif caller=='molsysmt.build.add_bonds.add_bonds':
        if isinstance(bonded_atom_pairs, list):
            for sublist in bonded_atom_pairs:
                if not (isinstance(sublist, list) and len(sublist) == 2):
                    raise ArgumentError('bonded_atom_pairs', value=bonded_atom_pairs, caller=caller, message=None)
                if not all(isinstance(item, int) for item in sublist):
                    raise ArgumentError('bonded_atom_pairs', value=bonded_atom_pairs, caller=caller, message=None)
            return bonded_atom_pairs
        elif isinstance(bonded_atom_pairs, ndarray):
            if


    raise ArgumentError('bonded_atom_pairs', value=bonded_atom_pairs, caller=caller, message=None)

