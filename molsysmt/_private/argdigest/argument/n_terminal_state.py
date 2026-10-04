"""Validating an explicitly declared amino-terminal state."""

from molsysmt._private.smonitor import ArgumentError


def digest_n_terminal_state(n_terminal_state, caller=None):
    if isinstance(n_terminal_state, str) and n_terminal_state in {"ammonium", "amine"}:
        return n_terminal_state
    raise ArgumentError("n_terminal_state", value=n_terminal_state, caller=caller)
