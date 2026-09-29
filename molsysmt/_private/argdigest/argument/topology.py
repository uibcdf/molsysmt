"""Validate the independent H5MSM topology layer."""

from argdigest.core.caller import caller_matches

from molsysmt._private.smonitor import ArgumentError


def digest_topology(topology, caller=None):
    if not caller_matches(caller, "write_layers") or topology is None:
        return topology
    from molsysmt.native import Topology

    if not isinstance(topology, Topology):
        raise ArgumentError("topology", value=topology, caller=caller)
    return topology
