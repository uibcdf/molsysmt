"""Require explicit length units on a geometric distance population."""

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError


def digest_distances(distances, caller=None):
    if puw.is_quantity(distances) and puw.check(distances, dimensionality={"[L]": 1}):
        return distances
    raise ArgumentError("distances", caller=caller)
