import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt._private.variables import is_all

###### Set

## Atom


@arg_digest(form="XYZ")
def set_coordinates_to_atom(
    item, indices="all", structure_indices="all", value=None, skip_digestion=False
):
    """
    Setting coordinates to atom on form XYZ.


    Parameters
    ----------
    item : molecular system
        Coordinate quantity of shape (3,), (n_atoms, 3), or
        (n_structures, n_atoms, 3), retaining its quantity library and units.
    indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) in destination order, or all atoms.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    value : quantity, default=None
        New coordinates with length units, broadcastable to the selected
        (n_structures, n_atoms, 3) shape. Conversion uses destination units.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Raises
    ------
    StructuralInconsistencyError
        If floating or narrowing values would be assigned to integer storage.
        Rejection occurs before writing any coordinate. Use floating storage
        for physical coordinate edits.

    Notes
    -----
    Assignment preserves the original XYZ rank and converts through the
    destination quantity owner independently of application unit policy.
    Empty selections make no change. Floating destinations retain their dtype;
    this function does not resize or replace the caller's quantity.

    .. versionadded:: 1.0.0
    """
    shape = np.shape(item)
    normalized_shape = (1,) * (3 - len(shape)) + shape
    atom_count = normalized_shape[1] if is_all(indices) else len(indices)
    structure_count = (
        normalized_shape[0] if is_all(structure_indices) else len(structure_indices)
    )
    if atom_count == 0 or structure_count == 0:
        return

    # Conversion belongs to the destination quantity owner, not the session policy.
    unit = puw.get_unit(item)
    values = puw.get_value(value, to_unit=unit)
    dtype = np.asarray(puw.get_value(item)).dtype
    if dtype.kind in "iu" and not np.can_cast(np.asarray(values).dtype, dtype, "safe"):
        raise StructuralInconsistencyError(
            reason=(
                "Floating or narrowing coordinate updates cannot be published into "
                "integer XYZ storage. Use floating coordinates for an in-place edit "
                "or request an independent transform, which promotes integer storage."
            ),
            caller="molsysmt.form.XYZ.set_coordinates_to_atom",
        )
    values = np.broadcast_to(values, (structure_count, atom_count, 3))
    value = puw.quantity(values, unit=unit, form=puw.get_form(item), standardized=False)

    if len(shape) == 1:
        # Indexing these singleton axes also rejects invalid direct-adapter indices.
        if not is_all(indices):
            np.arange(1)[indices]
        if not is_all(structure_indices):
            np.arange(1)[structure_indices]
        item[:] = value[-1, -1, :]
    elif len(shape) == 2:
        if not is_all(structure_indices):
            np.arange(1)[structure_indices]
        atom_indices = slice(None) if is_all(indices) else indices
        item[atom_indices, :] = value[-1, :, :]
    else:
        if is_all(indices):
            if is_all(structure_indices):
                item[:, :, :] = value[:, :, :]
            else:
                item[structure_indices, :, :] = value[:, :, :]
        else:
            if is_all(structure_indices):
                item[:, indices, :] = value[:, :, :]
            else:
                item[np.ix_(structure_indices, indices)] = value[:, :, :]


## System


@arg_digest(form="XYZ")
def set_coordinates_to_system(
    item, indices="all", structure_indices="all", value=None, skip_digestion=False
):
    """
    Setting coordinates to system on form XYZ.


    Parameters
    ----------
    item : molecular system
        Coordinate quantity of shape (3,), (n_atoms, 3), or
        (n_structures, n_atoms, 3), retaining its quantity library and units.
    indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) in destination order, or all atoms.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    value : quantity, default=None
        New coordinates with length units, broadcastable to the selected
        (n_structures, n_atoms, 3) shape. Conversion uses destination units.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Raises
    ------
    StructuralInconsistencyError
        If floating or narrowing values would be assigned to integer storage.
        Rejection occurs before writing any coordinate. Use floating storage
        for physical coordinate edits.

    Notes
    -----
    Assignment preserves the original XYZ rank and converts through the
    destination quantity owner independently of application unit policy.
    Empty selections make no change. Floating destinations retain their dtype;
    this function does not resize or replace the caller's quantity.

    .. versionadded:: 1.0.0
    """
    return set_coordinates_to_atom(
        item, indices="all", structure_indices=structure_indices, value=value
    )
