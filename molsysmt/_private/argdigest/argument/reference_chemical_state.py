"""Validate independently selected reference chemical states."""

from .chemical_state import digest_chemical_state


def digest_reference_chemical_state(reference_chemical_state, caller=None):
    return digest_chemical_state(reference_chemical_state, caller=caller)
