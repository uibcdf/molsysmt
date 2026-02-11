import numpy as np
from molsysmt._private.smonitor import ArgumentError
from .rotation import digest_rotation

def digest_rotations(rotations, caller=None):

    if caller is not None:
        if caller.endswith('digest_bioassembly'):
            if isinstance(rotations, (np.ndarray, list, tuple)):
                return [digest_rotation(ii) for ii in rotations]

    raise ArgumentError('rotations', value=rotations, caller=caller, message=None)

