"""Validate the outer public correspondence-result boundary."""

from molsysmt._private.smonitor import ArgumentError


def digest_correspondences(correspondences, caller=None):
    if correspondences is None or (
        isinstance(correspondences, dict)
        and correspondences.get("schema") == "molsysmt.atom_correspondences@1"
    ):
        return correspondences
    raise ArgumentError("correspondences", value=correspondences, caller=caller)
