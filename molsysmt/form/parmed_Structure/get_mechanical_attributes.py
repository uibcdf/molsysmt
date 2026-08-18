"""Delivering ParmEd per-atom partial charges."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form='parmed.Structure')
def get_partial_charge_from_atom(
    item, indices='all', skip_digestion=False
):
    """
    Getting partial charge from atom in form parmed.Structure.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """

    values = np.asarray([atom.charge for atom in item.atoms], dtype=np.float64)
    if not is_all(indices):
        values = values[indices]
    return puw.quantity(values, 'elementary_charge', standardized=True)


@arg_digest(form='parmed.Structure')
def get_partial_charge_from_system(item, skip_digestion=False):
    """
    Getting partial charge from system in form parmed.Structure.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """

    return get_partial_charge_from_atom(item, skip_digestion=True)
