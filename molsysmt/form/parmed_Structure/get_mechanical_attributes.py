"""Delivering ParmEd per-atom partial charges."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form='parmed.Structure')
def get_partial_charge_from_atom(
    item, indices='all', skip_digestion=False
):
    """Returning ParmEd partial charges in elementary-charge units."""

    values = np.asarray([atom.charge for atom in item.atoms], dtype=np.float64)
    if not is_all(indices):
        values = values[indices]
    return puw.quantity(values, 'elementary_charge', standardized=True)


@arg_digest(form='parmed.Structure')
def get_partial_charge_from_system(item, skip_digestion=False):
    """Returning all ParmEd partial charges."""

    return get_partial_charge_from_atom(item, skip_digestion=True)
