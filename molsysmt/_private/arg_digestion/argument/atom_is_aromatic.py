import numpy as np
import pandas as pd

from molsysmt._private.smonitor import ArgumentError


def digest_atom_is_aromatic(atom_is_aromatic, caller=None):
    if isinstance(atom_is_aromatic, (bool, np.bool_)):
        return bool(atom_is_aromatic)
    values = np.asarray(atom_is_aromatic, dtype=object)
    if values.ndim == 1 and all(
        value is None or value is pd.NA or isinstance(value, (bool, np.bool_))
        for value in values
    ):
        return values.tolist()
    raise ArgumentError('atom_is_aromatic', value=atom_is_aromatic, caller=caller, message=None)
