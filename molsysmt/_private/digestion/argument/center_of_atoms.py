from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_center_of_atoms(center_of_atoms, syntax="MolSysMT", caller=None):

    if isinstance(center_of_atoms, bool):

        return center_of_atoms

    raise ArgumentError('center_of_atoms', value=center_of_atoms, caller=caller, message=None)

