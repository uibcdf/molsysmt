"""Delivering CHARMM PSF per-atom force-field attributes."""

from molsysmt._private.arg_digestion import arg_digest


def _get_native(item):
    """Return the PSF normalized through the native mechanics seam."""

    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    return to_molsysmt_MolSys(item, skip_digestion=True)


@arg_digest(form='file:psf')
def get_partial_charge_from_atom(item, indices='all', skip_digestion=False):
    """Returning PSF partial charges in elementary-charge units."""

    from molsysmt.form.molsysmt_MolSys import get_partial_charge_from_atom

    return get_partial_charge_from_atom(
        _get_native(item), indices=indices, skip_digestion=True
    )


@arg_digest(form='file:psf')
def get_partial_charge_from_system(item, skip_digestion=False):
    """Returning all PSF partial charges."""

    return get_partial_charge_from_atom(item, skip_digestion=True)


@arg_digest(form='file:psf')
def get_atom_ff_type_from_atom(item, indices='all', skip_digestion=False):
    """Returning CHARMM force-field atom types."""

    from molsysmt.form.molsysmt_MolSys import get_atom_ff_type_from_atom

    return get_atom_ff_type_from_atom(
        _get_native(item), indices=indices, skip_digestion=True
    )


@arg_digest(form='file:psf')
def get_atom_ff_type_from_system(item, skip_digestion=False):
    """Returning all CHARMM force-field atom types."""

    return get_atom_ff_type_from_atom(item, skip_digestion=True)
