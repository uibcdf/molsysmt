"""Validating structure-aligned chemical-state association arguments."""

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import ArgumentError


def digest_structure_chemical_state_index(
    structure_chemical_state_index, caller=None
):
    """Return a query flag or nullable non-negative integer association values."""

    if caller in {'molsysmt.basic.get.get', 'molsysmt.basic.compare.compare'}:
        if isinstance(structure_chemical_state_index, bool):
            return structure_chemical_state_index
        raise ArgumentError(
            'structure_chemical_state_index',
            value=structure_chemical_state_index,
            caller=caller,
            message=None,
        )

    if structure_chemical_state_index is None or structure_chemical_state_index is pd.NA:
        return structure_chemical_state_index
    if isinstance(structure_chemical_state_index, (int, np.integer)) and not isinstance(
        structure_chemical_state_index, (bool, np.bool_)
    ):
        if int(structure_chemical_state_index) >= 0:
            return int(structure_chemical_state_index)
    if isinstance(structure_chemical_state_index, (list, tuple, np.ndarray)):
        values = list(structure_chemical_state_index)
        if all(
            value is None
            or value is pd.NA
            or isinstance(value, (int, np.integer))
            and not isinstance(value, (bool, np.bool_))
            and int(value) >= 0
            for value in values
        ):
            return values
    raise ArgumentError(
        'structure_chemical_state_index',
        value=structure_chemical_state_index,
        caller=caller,
        message=None,
    )
