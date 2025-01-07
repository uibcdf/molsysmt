import numpy as np
from ...exceptions import ArgumentError

functions_where_boolean = (
    'molsysmt.basic.get.get',
    'molsysmt.basic.compare.compare',
    'molsysmt.basic.iterator.__init__',
    '.iterators.__init__',
    )

def digest_occupancy(occupancy, caller=None):

    if caller is not None:

        if caller.endswith(functions_where_boolean):
            if isinstance(occupancy, bool):
                return occupancy
            else:
                raise ArgumentError('occupancy', value=occupancy, caller=caller, message=None)

    if occupancy is None:
        return None

    if isinstance(occupancy, (list, tuple)):
        occupancy = np.array(occupancy)

    if isinstance(occupancy, np.ndarray):
        if len(occupancy.shape) == 1:
            return occupancy[np.newaxis, :]
        elif len(occupancy.shape) == 2:
            return occupancy


    raise ArgumentError('occupancy', value=occupancy, caller=caller, message=None)
