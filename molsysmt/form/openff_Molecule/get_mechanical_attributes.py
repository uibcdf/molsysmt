"""Delivering optional OpenFF molecular-mechanics atom metadata."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form='openff.Molecule')
def get_partial_charge_from_atom(
    item, indices='all', skip_digestion=False
):
    """Returning available partial charges in elementary-charge units."""

    if item.partial_charges is None:
        return None
    values = np.asarray(
        item.partial_charges.m_as('elementary_charge'), dtype=np.float64
    )
    if not is_all(indices):
        values = values[indices]
    return puw.quantity(values, 'elementary_charge', standardized=True)


@arg_digest(form='openff.Molecule')
def get_partial_charge_from_system(item, skip_digestion=False):
    """Returning all available partial charges in elementary-charge units."""

    return get_partial_charge_from_atom(item, skip_digestion=True)
