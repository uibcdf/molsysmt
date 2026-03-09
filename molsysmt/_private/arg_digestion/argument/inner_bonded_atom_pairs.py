from molsysmt._private.smonitor import ArgumentError
import numpy as np

def digest_inner_bonded_atom_pairs(inner_bonded_atom_pairs, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(inner_bonded_atom_pairs, bool):
            return inner_bonded_atom_pairs
    elif caller=='molsysmt.basic.compare.compare':
        if isinstance(inner_bonded_atom_pairs, bool):
            return inner_bonded_atom_pairs

    raise ArgumentError('inner_bonded_atom_pairs', value=inner_bonded_atom_pairs, caller=caller, message=None)
