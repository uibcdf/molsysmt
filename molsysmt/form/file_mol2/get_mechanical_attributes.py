"""Delivering optional MOL2 partial charges through native normalization."""

from molsysmt._private.argdigest import arg_digest


@arg_digest(form='file:mol2')
def get_partial_charge_from_atom(
    item, indices='all', skip_digestion=False
):
    """Returning MOL2 partial charges in elementary-charge units."""

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
    """Returning all available MOL2 partial charges."""

    return get_partial_charge_from_atom(item, skip_digestion=True)
