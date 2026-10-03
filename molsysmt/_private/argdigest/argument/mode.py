"""Validating the explicit chemistry mode of hydrogen addition."""

from molsysmt._private.smonitor import ArgumentError


def digest_mode(mode, caller=None):
    if caller == 'molsysmt.build.add_missing_hydrogens.add_missing_hydrogens':
        if isinstance(mode, str) and mode in {'pH', 'fixed_chemical_state'}:
            return mode
        raise ArgumentError('mode', value=mode, caller=caller)
    # Unrelated mode arguments retain their existing owner-defined validation.
    return mode
