from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw



def digest_value(value, caller=None):

    if caller.endswith('set_coordinates_to_atom'):
        from .coordinates import digest_coordinates
        return digest_coordinates(value, caller=caller)

    if caller.endswith('set_structure_id_to_system'):
        from .structure_id import digest_structure_id
        return digest_structure_id(value, caller=caller)

    if caller.endswith('set_time_to_system'):
        from .time import digest_time
        return digest_time(value, caller=caller)

    if caller.endswith('set_box_to_system'):
        from .box import digest_box
        return digest_box(value, caller=caller)

    if caller.endswith('set_coordinates_to_system'):
        from .coordinates import digest_coordinates
        return digest_coordinates(value, caller=caller)

    if value is not None:
        if puw.is_quantity(value):
            return puw.standardize(value)

    raise ArgumentError('value', value=value, caller=caller, message=None)
