"""Validating explicit coordinate-based stereo inference."""

from molsysmt._private.smonitor import ArgumentError


def digest_from_coordinates(from_coordinates, caller=None):
    if isinstance(from_coordinates, bool):
        return from_coordinates
    raise ArgumentError("from_coordinates", value=from_coordinates, caller=caller)
