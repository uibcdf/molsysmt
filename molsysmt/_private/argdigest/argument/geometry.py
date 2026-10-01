"""Validating requested geometric classes of aromatic ring contacts."""

from molsysmt._private.smonitor import ArgumentError


def digest_geometry(geometry, caller=None):
    if isinstance(geometry, str) and geometry in {"parallel", "edge_to_face", "both"}:
        return geometry
    raise ArgumentError("geometry", value=geometry, caller=caller)
