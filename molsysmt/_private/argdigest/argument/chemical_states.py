"""Validate the independent H5MSM chemical-state layer."""

from argdigest.core.caller import caller_matches

from molsysmt._private.smonitor import ArgumentError


def digest_chemical_states(chemical_states, caller=None):
    if not caller_matches(caller, "write_layers") or chemical_states is None:
        return chemical_states
    from molsysmt.native import ChemicalStates

    if not isinstance(chemical_states, ChemicalStates):
        raise ArgumentError("chemical_states", value=chemical_states, caller=caller)
    return chemical_states
