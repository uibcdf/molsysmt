from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_center_of_atoms_2(center_of_atoms_2, syntax="MolSysMT", caller=None):

    if center_of_atoms_2 is None:
        return None

    from .center_of_atoms import digest_center_of_atoms

    try:
        return digest_center_of_atoms(center_of_atoms_2, syntax=syntax, caller=caller)
    except:
        raise ArgumentError('center_of_atoms_2', value=center_of_atoms_2, caller=caller, message=None)

