import numpy as np
from molsysmt import puw
from ...exceptions import ArgumentError

def digest_angles_shifts(angles_shifts, caller=None):

    if caller=='molsysmt.structure.shift_dihedral_angles.shift_dihedral_angles':

        from .angles import digest_angles

        try:
            return digest_angles(angles_shifts, caller=caller)
        except:
            raise ArgumentError('angles_shifts', value=angles_shifts, caller=caller, message=None)


    raise ArgumentError('angles_shifts', value=angles_shifts, caller=caller, message=None)

