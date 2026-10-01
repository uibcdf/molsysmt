"""Validate the operand of a native interaction frame replacement."""

from molsysmt._private.smonitor import ArgumentError


def digest_replacement(replacement, caller=None):
    from molsysmt.interactions.result import Interactions

    if not isinstance(replacement, Interactions):
        raise ArgumentError("replacement", value=replacement, caller=caller)
    return replacement
