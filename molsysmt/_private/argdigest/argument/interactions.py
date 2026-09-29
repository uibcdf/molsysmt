"""Validate a named H5MSM interaction collection."""

from collections.abc import Mapping

from argdigest.core.caller import caller_matches

from molsysmt._private.smonitor import ArgumentError


def digest_interactions(interactions, caller=None):
    if not caller_matches(caller, "write_layers") or interactions is None:
        return interactions
    from molsysmt.interactions.result import Interactions

    if not isinstance(interactions, Mapping) or any(
        not isinstance(name, str) or not name or not isinstance(result, Interactions)
        for name, result in interactions.items()
    ):
        raise ArgumentError("interactions", value=interactions, caller=caller)
    return interactions
