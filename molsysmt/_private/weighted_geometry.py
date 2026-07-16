"""Internal validation helpers for weighted structural observables."""

from __future__ import annotations

import numpy as np

from molsysmt._private.smonitor import ArgumentError, ArgumentLengthError


def prepare_weights(
    weights,
    n_atoms,
    *,
    molecular_system=None,
    selection="all",
    syntax="MolSysMT",
    group_sizes=None,
    caller=None,
):
    """Return finite, non-negative float64 weights with non-zero group sums."""

    if n_atoms < 1:
        raise ArgumentError(
            "selection",
            value=selection,
            caller=caller,
            message="The atom selection must contain at least one atom.",
        )

    if weights is None:
        output = np.ones(n_atoms, dtype=np.float64)
    elif isinstance(weights, str) and weights == "masses":
        from molsysmt import pyunitwizard as puw
        from molsysmt.physchem import get_mass

        masses = get_mass(
            molecular_system,
            element="atom",
            selection=selection,
            syntax=syntax,
        )
        output = np.asarray(puw.get_value(masses), dtype=np.float64)
    else:
        from molsysmt import pyunitwizard as puw

        if puw.is_quantity(weights):
            weights = puw.get_value(weights)
        output = np.asarray(weights, dtype=np.float64)

    output = np.ravel(output)
    if output.size != n_atoms:
        raise ArgumentLengthError(
            argument="weights",
            expected=n_atoms,
            actual=output.size,
            caller=caller,
        )
    if not np.all(np.isfinite(output)):
        raise ArgumentError(
            "weights",
            value=weights,
            caller=caller,
            message="Weights must contain only finite values.",
        )
    if np.any(output < 0.0):
        raise ArgumentError(
            "weights",
            value=weights,
            caller=caller,
            message="Weights must be non-negative.",
        )

    if group_sizes is None:
        sums = np.array([np.sum(output, dtype=np.float64)])
    else:
        boundaries = np.cumsum(np.asarray(group_sizes, dtype=np.int64))[:-1]
        sums = np.array(
            [np.sum(group, dtype=np.float64) for group in np.split(output, boundaries)]
        )
    if np.any(sums <= 0.0):
        raise ArgumentError(
            "weights",
            value=weights,
            caller=caller,
            message="The weights of every atom group must have a positive sum.",
        )

    return np.ascontiguousarray(output, dtype=np.float64)
