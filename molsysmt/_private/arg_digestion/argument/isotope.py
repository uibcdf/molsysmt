"""Validating nullable atomic mass numbers."""

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import ArgumentError


def digest_isotope(isotope, caller=None):
    if caller in {'molsysmt.basic.get.get', 'molsysmt.basic.compare.compare'}:
        if isinstance(isotope, (bool, np.bool_)):
            return bool(isotope)
    elif caller == 'molsysmt.basic.set.set' or caller.endswith('set_isotope_to_atom'):
        if isotope is None or isotope is pd.NA:
            return isotope
        values = [isotope] if np.isscalar(isotope) else list(isotope)
        if all(
            value is None or value is pd.NA
            or (
                isinstance(value, (int, np.integer))
                and not isinstance(value, (bool, np.bool_))
                and 1 <= int(value) <= 65535
            )
            for value in values
        ):
            normalized = [
                value if value is None or value is pd.NA else int(value)
                for value in values
            ]
            return normalized[0] if np.isscalar(isotope) else normalized
    raise ArgumentError('isotope', value=isotope, caller=caller, message=None)
