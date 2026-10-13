"""Normalize the absolute RMSD ambiguity tolerance to nanometers."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError


def digest_tie_tolerance(tie_tolerance, caller=None):
    try:
        quantity = puw.ensure_quantity(tie_tolerance, dimensionality={"[L]": 1})
        value = puw.get_value(quantity, to_unit="nm")
        if np.ndim(value) == 0 and np.isfinite(value) and value >= 0:
            return quantity
    except Exception:
        # Provider dimensionality/parser failures belong to this input boundary.
        pass
    raise ArgumentError("tie_tolerance", value=tie_tolerance, caller=caller)
