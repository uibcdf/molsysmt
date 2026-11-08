"""Validate a geometric cluster representative rule."""

from molsysmt._private.smonitor import ArgumentError


def digest_representative(representative, caller=None):
    if isinstance(representative, str) and representative in {"medoid", "first"}:
        return representative
    raise ArgumentError("representative", caller=caller)
