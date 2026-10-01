"""Validating the units of an orthogonal plane-deviation cutoff."""

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError

from ._quantity_parsing import parse_quantity_string


def digest_planarity_threshold(planarity_threshold, caller=None):
    if planarity_threshold is None and caller in {"molsysmt.interactions.cation_pi.get_cation_pi_interactions.get_cation_pi_interactions",
                                              "molsysmt.interactions.pi_pi.get_pi_pi_interactions.get_pi_pi_interactions"}:
        return None
    if isinstance(planarity_threshold, str):
        planarity_threshold = parse_quantity_string("planarity_threshold", planarity_threshold, caller=caller)
    if puw.is_quantity(planarity_threshold) and puw.check(planarity_threshold, dimensionality={"[L]": 1}):
        return puw.standardize(planarity_threshold)
    raise ArgumentError("planarity_threshold", value=planarity_threshold, caller=caller)
