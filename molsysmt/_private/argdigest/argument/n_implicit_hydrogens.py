import numpy as np
import pandas as pd

from molsysmt._private.smonitor import ArgumentError


def digest_n_implicit_hydrogens(n_implicit_hydrogens, caller=None):
    if isinstance(n_implicit_hydrogens, bool):
        return n_implicit_hydrogens
    if isinstance(n_implicit_hydrogens, (int, np.integer)) and n_implicit_hydrogens >= 0:
        return int(n_implicit_hydrogens)
    try:
        values = list(n_implicit_hydrogens)
    except TypeError as error:
        raise ArgumentError(
            'n_implicit_hydrogens', value=n_implicit_hydrogens, caller=caller, message=None
        ) from error
    if all(
        value is None or value is pd.NA
        or isinstance(value, (int, np.integer)) and value >= 0
        for value in values
    ):
        return values
    raise ArgumentError('n_implicit_hydrogens', value=n_implicit_hydrogens, caller=caller, message=None)
