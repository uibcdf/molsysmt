from ...exceptions import ArgumentError
from ...variables import is_all
import numpy as np

def digest_location_id(location_id, caller=None):

    if caller is not None:
        if caller.endswith('solve_atoms_with_alternate_location'):
            if isinstance(location_id, str):
                if location_id=='occupancy':
                    return location_id

    if isinstance(location_id, str):
        if len(location_id)==1:
            return location_id

    if isinstance(location_id, (tuple, list)):
        location_id=np.array(location_id)

    if isinstance(location_id, np.ndarray):
        for ii in location_id:
            ok=False
            if isinstance(ii, str):
                if len(ii)==1:
                    ok=True
            if not ok:
                break
        if ok:
            return location_id

    raise ArgumentError('location_id', caller=caller, message=None)

