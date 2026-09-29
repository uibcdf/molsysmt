"""Validate a native H5MSM structural-series payload."""

from argdigest.core.caller import caller_matches

from molsysmt._private.smonitor import ArgumentError


def digest_structures(structures, caller=None):
    if not caller_matches(caller, "write_layers", "append_structures"):
        return structures
    from molsysmt.native import Structures

    if structures is None and caller_matches(caller, "write_layers"):
        return None
    if not isinstance(structures, Structures):
        raise ArgumentError("structures", value=structures, caller=caller)
    return structures
