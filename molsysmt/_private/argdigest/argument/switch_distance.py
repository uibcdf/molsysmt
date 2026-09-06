import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from ._quantity_parsing import parse_quantity_string

def digest_switch_distance(switch_distance, caller=None):

    if isinstance(switch_distance, str):
        switch_distance = parse_quantity_string('switch_distance', switch_distance, caller=caller)

    if caller is not None and caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        if switch_distance is None:
            return switch_distance

    if switch_distance is None:
        return switch_distance

    if puw.is_quantity(switch_distance):
        if puw.check(switch_distance, dimensionality={'[L]':1}):
            return puw.standardize(switch_distance)

    raise ArgumentError('switch_distance', value=switch_distance, caller=caller, message=None)

