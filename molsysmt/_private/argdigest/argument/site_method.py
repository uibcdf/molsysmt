"""Validate the chemical recognition rule used before directional geometry."""

from molsysmt._private.interaction_methods import supported_methods
from molsysmt._private.smonitor import ArgumentError


def digest_site_method(site_method, caller=None):
    if isinstance(site_method, str) and site_method in supported_methods("hbond_sites"):
        return site_method
    raise ArgumentError("site_method", value=site_method, caller=caller)
