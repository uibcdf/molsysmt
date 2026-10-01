"""Validating the units of a lateral geometric cutoff."""

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError

from ._quantity_parsing import parse_quantity_string


def digest_offset_threshold(offset_threshold, caller=None):
    if offset_threshold is None and caller == "molsysmt.interactions.cation_pi.get_cation_pi_interactions.get_cation_pi_interactions":
        return None
    if isinstance(offset_threshold, str):
        offset_threshold = parse_quantity_string("offset_threshold", offset_threshold, caller=caller)
    if puw.is_quantity(offset_threshold) and puw.check(offset_threshold, dimensionality={"[L]": 1}):
        return puw.standardize(offset_threshold)
    raise ArgumentError("offset_threshold", value=offset_threshold, caller=caller)
