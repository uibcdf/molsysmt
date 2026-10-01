"""Validate explicit acceptor indices without silently coercing numeric values."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_acceptor_atom_indices(acceptor_atom_indices, caller=None):
    if acceptor_atom_indices is None:
        return None
    try:
        array = np.asarray(acceptor_atom_indices)
    except (TypeError, ValueError):
        raise ArgumentError("acceptor_atom_indices", value=acceptor_atom_indices, caller=caller) from None
    if isinstance(acceptor_atom_indices, (list, tuple)) and any(
        isinstance(item, (bool, np.bool_)) for item in np.asarray(acceptor_atom_indices, dtype=object).flat
    ):
        raise ArgumentError("acceptor_atom_indices", value=acceptor_atom_indices, caller=caller)
    if array.shape == (0,):
        return np.empty(0, dtype=np.int64)
    if array.ndim == 1 and array.dtype.kind in "iu" and np.all(array >= 0) and np.all(array < 2**63):
        return np.unique(array.astype(np.int64))
    raise ArgumentError("acceptor_atom_indices", value=acceptor_atom_indices, caller=caller)
