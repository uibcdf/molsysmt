from molsysmt._private.smonitor import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_values(values, caller=None):

    if isinstance(values, str):
        values = puw.parse(values)

    if values is None:
        return values

    if isinstance(values, (list, tuple, range, np.ndarray)):
        return values

    if puw.is_quantity(values):
        return puw.get_value(values)

    raise ArgumentError('values', value=values, caller=caller, message=None)

