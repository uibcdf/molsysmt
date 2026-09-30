"""Validating an explicit interaction calculation scope."""

from molsysmt._private.smonitor import ArgumentError


def digest_selection_mode(selection_mode, caller=None):
    if isinstance(selection_mode, str) and selection_mode in {
        "internal",
        "incident",
        "between",
    }:
        return selection_mode
    raise ArgumentError("selection_mode", value=selection_mode, caller=caller)
