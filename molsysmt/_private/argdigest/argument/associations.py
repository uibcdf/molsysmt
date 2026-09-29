"""Validate the outer shape of H5MSM axis associations."""

from argdigest.core.caller import caller_matches

from molsysmt._private.smonitor import ArgumentError


def digest_associations(associations, caller=None):
    if not caller_matches(caller, "write_layers") or associations is None:
        return associations
    if not isinstance(associations, (list, tuple)) or any(
        not isinstance(link, dict) for link in associations
    ):
        raise ArgumentError("associations", value=associations, caller=caller)
    return associations
