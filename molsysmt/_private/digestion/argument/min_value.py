from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_min_value(min_value, caller=None):

    if min_value is None:
        return None

    if isinstance(min_value, [int, float]):
        return min_value

    if puw.is_quantity(min_value):
        return min_value

    raise ArgumentError('min_value', value=min_value, caller=caller, message=None)
