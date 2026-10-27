"""Validating explicitly requested reference conformation categories."""

from molsysmt._private.smonitor import ArgumentError


def digest_conformation(conformation, caller=None):
    if isinstance(conformation, str) and conformation in {
        "alpha_helix",
        "beta_sheet",
        "reverse_turn",
    }:
        return conformation
    raise ArgumentError("conformation", value=conformation, caller=caller)
