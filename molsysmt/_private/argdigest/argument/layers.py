"""Validate named H5MSM layers at the public read boundary."""

from argdigest.core.caller import caller_matches

from molsysmt._private.smonitor import ArgumentError

_NAMES = frozenset(
    {"topology", "chemical_states", "structures", "interactions", "associations"}
)


def digest_layers(layers, caller=None):
    if not caller_matches(caller, "read_layers"):
        return layers
    if layers is None:
        return None
    if isinstance(layers, str):
        values = [layers]
    elif isinstance(layers, (list, tuple)):
        values = layers
    else:
        raise ArgumentError("layers", value=layers, caller=caller)
    if any(not isinstance(value, str) or value not in _NAMES for value in values):
        raise ArgumentError("layers", value=layers, caller=caller)
    return layers
