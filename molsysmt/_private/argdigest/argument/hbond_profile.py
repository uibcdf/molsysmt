"""Validate the optional chemical/geometric profile used for bridge legs."""

from molsysmt._private.smonitor import ArgumentError


def digest_hbond_profile(hbond_profile, caller=None):
    if hbond_profile is None or isinstance(hbond_profile, str):
        return hbond_profile
    raise ArgumentError("hbond_profile", value=hbond_profile, caller=caller)
