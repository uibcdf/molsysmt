import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_n_unpaired_electrons(n_unpaired_electrons, caller=None):
    # Imported here, not at module level: ArgDigest loads every digester in this
    # package when it initializes, so a top-level import made any digested call pay
    # for a heavy library that most calls never need.
    import pandas as pd

    if isinstance(n_unpaired_electrons, bool):
        return n_unpaired_electrons
    if isinstance(n_unpaired_electrons, (int, np.integer)) and n_unpaired_electrons >= 0:
        return int(n_unpaired_electrons)
    try:
        values = list(n_unpaired_electrons)
    except TypeError as error:
        raise ArgumentError(
            'n_unpaired_electrons', value=n_unpaired_electrons, caller=caller, message=None
        ) from error
    if all(
        value is None or value is pd.NA
        or isinstance(value, (int, np.integer)) and value >= 0
        for value in values
    ):
        return values
    raise ArgumentError('n_unpaired_electrons', value=n_unpaired_electrons, caller=caller, message=None)
