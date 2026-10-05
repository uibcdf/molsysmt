"""Validating an optional declared context map between atom-index domains."""

from molsysmt._private.argdigest.argument.atom_correspondence import (
    digest_atom_correspondence,
)
from molsysmt._private.smonitor import ArgumentError


def digest_context_atom_correspondence(context_atom_correspondence, caller=None):
    if context_atom_correspondence is None:
        return None
    try:
        return digest_atom_correspondence(context_atom_correspondence, caller=caller)
    except ArgumentError as error:
        raise ArgumentError(
            "context_atom_correspondence",
            value=context_atom_correspondence,
            caller=caller,
        ) from error
