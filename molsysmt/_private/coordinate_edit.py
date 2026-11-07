"""Prepare owned arithmetic and independent publication targets for coordinate edits."""

import numpy as np


def editable_coordinate_values(values):
    """Copy the selected magnitude, promoting integer arithmetic to float64."""
    dtype = np.float64 if np.asarray(values).dtype.kind in "iu" else None
    return np.array(values, dtype=dtype, copy=True)


def copy_for_coordinate_edit(molecular_system):
    """Copy a system, promoting integer XYZ storage without changing basic.copy."""
    from molsysmt import pyunitwizard as puw
    from molsysmt.basic import copy, get_form

    form = get_form(molecular_system)
    if isinstance(form, (list, tuple)):
        items = [copy_for_coordinate_edit(item) for item in molecular_system]
        return items[0] if len(items) == 1 else items
    if form == "XYZ":
        values, unit = puw.get_value_and_unit(molecular_system)
        if np.asarray(values).dtype.kind in "iu":
            return puw.quantity(
                editable_coordinate_values(values),
                unit=unit,
                form=puw.get_form(molecular_system),
                standardized=False,
            )
    return copy(molecular_system)
