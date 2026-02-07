import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError

def digest_rotations(rotations, caller=None):

    if caller is not None:
        if caller.endswith('digest_bioassembly'):
            from .rotation import arg_digest_rotation
            if isinstance(rotations, (np.ndarray, list, tuple)):
                return [digest_rotation(ii) for ii in rotations]

    raise ArgumentError('rotations', value=rotation, caller=caller, message=None)


