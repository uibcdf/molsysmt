from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from ._quantity_parsing import parse_quantity_string

def digest_probe_radius(probe_radius, caller=None):

    if isinstance(probe_radius, str):
        probe_radius = parse_quantity_string('probe_radius', probe_radius, caller=caller)

    if puw.is_quantity(probe_radius):
        if puw.check(probe_radius, dimensionality={'[L]':1}):
            return puw.standardize(probe_radius)

    raise ArgumentError('probe_radius', value=probe_radius, caller=caller, message=None)
