"""Validating the opt-in completed-export mapping result."""

from molsysmt._private.smonitor import ArgumentError


def digest_return_atom_map(return_atom_map, caller=None):
    if isinstance(return_atom_map, bool):
        return return_atom_map
    raise ArgumentError("return_atom_map", value=return_atom_map, caller=caller)
