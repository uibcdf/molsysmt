import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_atom_is_aromatic(atom_is_aromatic, caller=None):
    # Imported here, not at module level: ArgDigest loads every digester in this
    # package when it initializes, so a top-level import made any digested call pay
    # for a heavy library that most calls never need.
    import pandas as pd

    if isinstance(atom_is_aromatic, (bool, np.bool_)):
        return bool(atom_is_aromatic)
    values = np.asarray(atom_is_aromatic, dtype=object)
    if values.ndim == 1 and all(
        value is None or value is pd.NA or isinstance(value, (bool, np.bool_))
        for value in values
    ):
        return values.tolist()
    raise ArgumentError('atom_is_aromatic', value=atom_is_aromatic, caller=caller, message=None)
