"""Internal index validation helpers for public basic operations."""

from __future__ import annotations

import numpy as np

from molsysmt._private.smonitor import ArgumentError, NotWithThisFormError
from molsysmt._private.variables import is_all


def validate_element_indices(molecular_system, indices, element, argument, caller):
    """Validate and normalize element indices without invoking the public API recursively."""

    if indices is None or is_all(indices):
        return indices

    array = np.asarray(indices)
    if array.ndim == 0:
        array = array.reshape(1)
    if array.ndim == 1 and array.size == 0:
        return []
    if array.ndim != 1 or not np.issubdtype(array.dtype, np.integer):
        raise ArgumentError(
            argument=argument,
            value=indices,
            caller=caller,
            message=f"'{argument}' must be a one-dimensional collection of integer indices.",
        )

    n_elements = _get_count(molecular_system, element)
    if n_elements is None:
        return array.astype(np.int64).tolist()

    invalid = array[(array < 0) | (array >= n_elements)]
    if invalid.size:
        raise ArgumentError(
            argument=argument,
            value=indices,
            caller=caller,
            message=(
                f"'{argument}' contains out-of-range {element} indices "
                f"{invalid.astype(np.int64).tolist()}; valid indices are in [0, {n_elements})."
            ),
        )

    return array.astype(np.int64).tolist()


def normalize_mask(molecular_system, mask, element, caller):
    """Normalize a Boolean mask or validate an index-based mask."""

    if mask is None or is_all(mask) or isinstance(mask, str):
        return mask

    array = np.asarray(mask)
    if array.ndim == 1 and np.issubdtype(array.dtype, np.bool_):
        n_elements = _get_count(molecular_system, element)
        if n_elements is not None and array.size != n_elements:
            raise ArgumentError(
                argument="mask",
                value=mask,
                caller=caller,
                message=(
                    f"A Boolean 'mask' for element {element!r} must contain {n_elements} "
                    f"entries; received {array.size}."
                ),
            )
        return np.flatnonzero(array).astype(np.int64).tolist()

    return validate_element_indices(molecular_system, mask, element, "mask", caller)


def validate_structure_indices(molecular_system, structure_indices, caller):
    """Validate explicit structure indices when a structure count is available."""

    if structure_indices is None or is_all(structure_indices):
        return structure_indices

    return validate_element_indices(
        molecular_system,
        structure_indices,
        "structure",
        "structure_indices",
        caller,
    )


def _get_count(molecular_system, element):
    """Return an element count directly from the form adapter, if available."""

    from molsysmt.basic import where_is_attribute
    from molsysmt.element import _singular_element_to_plural
    from molsysmt.form import _dict_modules

    if element == "structure":
        attribute = "n_structures"
    elif element not in _singular_element_to_plural:
        return None
    else:
        attribute = "n_" + _singular_element_to_plural[element]
    item, form = where_is_attribute(
        molecular_system,
        attribute,
        include_none=False,
        skip_digestion=True,
    )
    if item is None:
        return None

    getter = getattr(_dict_modules[form], f"get_{attribute}_from_system", None)
    if getter is None:
        return None

    try:
        value = getter(item, skip_digestion=True)
    except NotWithThisFormError:
        return None
    return None if value is None else int(value)
