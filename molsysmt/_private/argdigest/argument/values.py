from molsysmt._private.smonitor import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw
from ._quantity_parsing import parse_quantity_string

def digest_values(values, caller=None):

    if isinstance(values, str):
        values = parse_quantity_string('values', values, caller=caller)

    if values is None:
        return values

    if isinstance(values, (list, tuple, range, np.ndarray)):
        return values

    if puw.is_quantity(values):
        return puw.get_value(values)

    raise ArgumentError('values', value=values, caller=caller, message=None)

