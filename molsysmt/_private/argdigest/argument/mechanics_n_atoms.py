"""Validate the explicitly declared mechanical atom domain."""

from molsysmt._private.smonitor import ArgumentError


def digest_mechanics_n_atoms(mechanics_n_atoms, caller=None):
    if mechanics_n_atoms is None:
        return None
    from molsysmt._private.h5msm_storage.mechanics import _atom_count

    try:
        return _atom_count(mechanics_n_atoms)
    except ValueError as error:
        raise ArgumentError(
            "mechanics_n_atoms", value=mechanics_n_atoms, caller=caller
        ) from error
