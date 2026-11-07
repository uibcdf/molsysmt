"""Delivering ParmEd per-atom partial charges."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="parmed.Structure")
def get_partial_charge_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting partial charge from atom in form parmed.Structure.


    Parameters
    ----------
    item : molecular system
        ParmEd structure with optional atom or assigned AtomType charges.
    indices : object, default='all'
        Atom indices (0-based) to retain. The default includes every atom.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity or none
        Assigned partial charges in elementary charge units, or None when all
        selected atoms lack assignments. An explicit zero is a known charge.

    Raises
    ------
    NotWithThisFormError
        If selected atoms mix known and unknown assignments. Select the known
        atoms or convert to native MolSys to retain a nullable mechanics column.


    .. versionadded:: 1.0.0
    """

    from ._mechanical import assigned_partial_charges

    values = assigned_partial_charges(item)
    if not is_all(indices):
        values = [values[index] for index in indices]
    if not values or all(value is None for value in values):
        return None
    if any(value is None for value in values):
        from molsysmt._private.smonitor import NotWithThisFormError

        raise NotWithThisFormError(
            form="parmed.Structure",
            requested_attribute="partial_charge",
            message="Selected ParmEd atoms mix assigned and unknown partial charges; no zero substitution or missing-number convention is applied.",
        )
    return puw.quantity(
        np.asarray(values, dtype=float), "elementary_charge", standardized=True
    )


@arg_digest(form="parmed.Structure")
def get_partial_charge_from_system(item, skip_digestion=False):
    """
    Getting partial charge from system in form parmed.Structure.


    Parameters
    ----------
    item : molecular system
        ParmEd structure with optional atom or assigned AtomType charges.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity or none
        Assigned atom charges in elementary charge units, or None when absent.

    Raises
    ------
    NotWithThisFormError
        If the atoms mix known and unknown assignments. No zero is inferred.


    .. versionadded:: 1.0.0
    """

    return get_partial_charge_from_atom(item, skip_digestion=True)
