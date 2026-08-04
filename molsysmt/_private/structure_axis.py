"""Resolving the structure axis of a composite molecular system.

A molecular system may be spread over complementary items, and those items need not
cover the same number of structures: a topology file holding one reference
conformation beside a trajectory file is an ordinary composition. The structure axis
of the system is therefore a property of the system, not of whichever item happens
to be listed last.

The rule, recorded in
``devguide/pending_bugs/structural_attribute_resolution_ignores_the_structure_axis.md``:

1. The axis is the largest structure count among the items carrying structural
   data. It does not depend on item order.
2. Only items spanning the axis may deliver a structural attribute.
3. An item below the axis holding no structures or a single one is a reference
   conformation; its structural series are dropped and the drop is reported.
4. Two items each holding more than one structure, of different lengths, give no
   basis for choosing and are rejected.
"""

from __future__ import annotations


def item_n_structures(item, form):
    """Returning the structure count of one item, or None if it carries no structures.

    This deliberately calls the form getter instead of the public ``get``. The axis is
    needed by ``where_is_attribute``, which is what ``get`` uses to resolve every
    attribute, so asking publicly here would re-enter the same resolution path.
    """

    from molsysmt.form import _dict_modules

    getter = getattr(_dict_modules[form], 'get_n_structures_from_system', None)
    if getter is None:
        return None

    try:
        value = getter(item, structure_indices='all', skip_digestion=True)
    except Exception:
        # An item whose count cannot be established does not define the axis. It is
        # still free to deliver attributes if no other item constrains the system.
        return None

    return None if value is None else int(value)


def structure_axis(items, forms, caller=None):
    """Returning the structure axis of the system and the count of every item.

    Raises
    ------
    StructuralInconsistencyError
        If two items each hold more than one structure and their counts differ.
    """

    counts = [item_n_structures(item, form) for item, form in zip(items, forms)]

    trajectory_counts = sorted({count for count in counts if count is not None and count > 1})
    if len(trajectory_counts) > 1:
        from molsysmt._private.smonitor import StructuralInconsistencyError

        detail = ', '.join(
            f'{form!r} spans {count} structures'
            for form, count in zip(forms, counts)
            if count is not None
        )
        raise StructuralInconsistencyError(
            reason=(
                f'Items providing structural data cover different structure axes: {detail}. '
                'A single structure beside a trajectory is a reference conformation and is '
                'accepted, but two trajectories of different lengths give no basis for '
                "choosing which one defines the system's structure axis. If the intention "
                'is to join them along that axis, use molsysmt.concatenate_structures, '
                'which takes exactly this list of molecular systems.'
            ),
            caller=caller,
        )

    axis = max((count for count in counts if count is not None), default=None)

    return axis, counts
