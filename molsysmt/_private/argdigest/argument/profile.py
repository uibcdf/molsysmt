"""Validate the interaction calculation profile without resolving chemistry."""

from molsysmt._private.smonitor import ArgumentError


def digest_profile(profile, caller=None):
    if profile is None or isinstance(profile, str):
        return profile
    raise ArgumentError("profile", value=profile, caller=caller)
