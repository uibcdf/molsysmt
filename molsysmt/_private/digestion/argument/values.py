from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_values(values, caller=None):

    if values is None:
        return values

    if isinstance(values, (list, tuple, range, np.ndarray)):
        return values

    if puw.is_quantity(values):
            values

    raise ArgumentError('values', value=values, caller=caller, message=None)

