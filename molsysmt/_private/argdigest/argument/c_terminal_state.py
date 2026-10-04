"""Validating an explicitly declared carboxyl-terminal state."""

from molsysmt._private.smonitor import ArgumentError


def digest_c_terminal_state(c_terminal_state, caller=None):
    if isinstance(c_terminal_state, str) and c_terminal_state in {
        "carboxylate",
        "carboxylic_acid",
    }:
        return c_terminal_state
    raise ArgumentError("c_terminal_state", value=c_terminal_state, caller=caller)
