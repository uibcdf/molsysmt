"""Validating explicit template connectivity policies."""

from molsysmt._private.smonitor import ArgumentError


def digest_connectivity_policy(connectivity_policy, caller=None):
    if not isinstance(connectivity_policy, str) or connectivity_policy not in {
        "require_same_graph",
        "complete_from_template",
    }:
        raise ArgumentError(
            "connectivity_policy", value=connectivity_policy, caller=caller
        )
    return connectivity_policy
