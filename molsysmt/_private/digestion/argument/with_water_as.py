from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_with_water_as(with_water_as, caller=None):

    if caller=='molsysmt.basic.view.view':
        if isinstance(with_water_as, str):
            if with_water_as in ['surface', 'licorice']:
                return with_water_as

    raise ArgumentError('with_water_as', value=with_water_as, caller=caller, message=None)

