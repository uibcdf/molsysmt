"""Validate the scientific criterion used for each water-bridge leg."""

from molsysmt._private.interaction_methods import supported_methods
from molsysmt._private.smonitor import ArgumentError


def digest_hbond_method(hbond_method, caller=None):
    if isinstance(hbond_method, str) and hbond_method in supported_methods("hbonds"):
        return hbond_method
    raise ArgumentError("hbond_method", value=hbond_method, caller=caller)
