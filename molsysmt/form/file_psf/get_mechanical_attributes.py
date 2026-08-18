"""Delivering CHARMM PSF per-atom force-field attributes."""

from molsysmt._private.argdigest import arg_digest


def _get_native(item):
    """Return the PSF normalized through the native mechanics seam."""

    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    return to_molsysmt_MolSys(item, skip_digestion=True)


@arg_digest(form='file:psf')
def get_partial_charge_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting partial charge from atom in form file:psf.


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

    from molsysmt.form.molsysmt_MolSys import get_partial_charge_from_atom

    return get_partial_charge_from_atom(
        _get_native(item), indices=indices, skip_digestion=True
    )


@arg_digest(form='file:psf')
def get_partial_charge_from_system(item, skip_digestion=False):
    """
    Getting partial charge from system in form file:psf.


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


@arg_digest(form='file:psf')
def get_atom_ff_type_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting atom ff type from atom in form file:psf.


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

    from molsysmt.form.molsysmt_MolSys import get_atom_ff_type_from_atom

    return get_atom_ff_type_from_atom(
        _get_native(item), indices=indices, skip_digestion=True
    )


@arg_digest(form='file:psf')
def get_atom_ff_type_from_system(item, skip_digestion=False):
    """
    Getting atom ff type from system in form file:psf.


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

    return get_atom_ff_type_from_atom(item, skip_digestion=True)
