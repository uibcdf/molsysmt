import numpy as np
from molsysmt import puw
from ...exceptions import ArgumentError

def digest_shifts(shifts, caller=None):

    if caller=='molsysmt.structure.shift_dihedral_angles.shift_dihedral_angles':

        from .angles import digest_angles

        try:
            return digest_angles(shifts, caller=caller)
        except:
            raise ArgumentError('shifts', value=shifts, caller=caller, message=None)


    raise ArgumentError('shifts', value=shifts, caller=caller, message=None)

