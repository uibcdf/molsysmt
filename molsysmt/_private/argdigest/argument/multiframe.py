"""Validating the external PDB writer's structure-series switch."""

from molsysmt._private.smonitor import ArgumentError


def digest_multiframe(multiframe, caller=None):
    if isinstance(multiframe, bool):
        return multiframe
    raise ArgumentError("multiframe", value=multiframe, caller=caller)
