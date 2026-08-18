"""Delivering optional MOL2 partial charges through native normalization."""

from molsysmt._private.argdigest import arg_digest


@arg_digest(form='file:mol2')
def get_partial_charge_from_atom(
    item, indices='all', skip_digestion=False
):
    """
    Getting partial charge from atom in form file:mol2.

    Parameters
    ----------
    item : file:mol2
        Source item in file:mol2 form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.molsysmt_MolSys import get_partial_charge_from_atom
    import numpy as np

    from molsysmt import pyunitwizard as puw
    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    native = to_molsysmt_MolSys(item, skip_digestion=True)
    values = get_partial_charge_from_atom(
        native, indices=indices, skip_digestion=True
    )
    if values is None:
        return None
    return puw.quantity(
        np.asarray(values, dtype=np.float64),
        'elementary_charge',
        standardized=True,
    )


@arg_digest(form='file:mol2')
def get_partial_charge_from_system(item, skip_digestion=False):
    """
    Getting partial charge from system in form file:mol2.

    Parameters
    ----------
    item : file:mol2
        Source item in file:mol2 form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """

    return get_partial_charge_from_atom(item, skip_digestion=True)
