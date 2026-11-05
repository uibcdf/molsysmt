import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_location_id(location_id, caller=None):

    if caller is not None:
        if caller.endswith("solve_atoms_with_alternate_location"):
            if isinstance(location_id, str):
                if location_id == "occupancy":
                    return location_id

    if isinstance(location_id, str):
        if len(location_id) == 1:
            return location_id

    if isinstance(location_id, (tuple, list)):
        location_id = np.array(location_id)

    if isinstance(location_id, np.ndarray):
        if location_id.ndim == 1 and all(
            isinstance(value, str) and len(value) == 1 for value in location_id
        ):
            return location_id

    raise ArgumentError("location_id", caller=caller, message=None)
