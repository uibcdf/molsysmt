from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import puw

def digest_water_as_surface(water_as_surface, caller=None):

    if caller=='molsysmt.basic.view.view':
        if isinstance(water_as_surface, bool):
            return water_as_surface

    raise ArgumentError('water_as_surface', value=water_as_surface, caller=caller, message=None)

