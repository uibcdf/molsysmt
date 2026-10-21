"""Validate the native independent-copy allocation option."""

from molsysmt._private.smonitor import ArgumentError


def digest_deep(deep, caller=None):
    if isinstance(deep, bool):
        return deep
    raise ArgumentError("deep", value=deep, caller=caller)
