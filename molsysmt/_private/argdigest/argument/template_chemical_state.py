"""Validating the independently selected template chemical state."""

from molsysmt._private.smonitor import ArgumentError

from .chemical_state import digest_chemical_state


def digest_template_chemical_state(template_chemical_state, caller=None):
    try:
        return digest_chemical_state(template_chemical_state, caller=caller)
    except ArgumentError as error:
        raise ArgumentError(
            "template_chemical_state", value=template_chemical_state, caller=caller
        ) from error
