"""Reduce distance slabs without materializing a disk-backed trajectory."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.execution.persistent_result import PersistentResultHandle
from molsysmt._private.smonitor import ArgumentConflictError, ArgumentError


def validate(first, second, paired, caller):
    if (not first and not second) or (paired and (not first or not second)):
        raise ArgumentConflictError(
            arg1="as_entity",
            arg2="as_entity_2",
            caller=caller,
            reason="Reduce at least one population; paired distances require both entity flags.",
        )


def reduce(distances, first, second, paired, maximum, caller):
    values, unit = puw.get_value(distances), puw.get_unit(distances)
    try:
        if any(size == 0 for size in values.shape[1:]):
            raise ArgumentError(
                "selection",
                caller=caller,
                message="Extrema require nonempty endpoint populations.",
            )
        ns = values.shape[0]
        shape = (
            (ns,)
            if paired
            else (ns, 2)
            if first and second
            else (ns, values.shape[1] if not first else values.shape[2])
        )
        indices = np.empty(shape, dtype=np.int64)
        output = np.empty((ns,) if first and second else shape, dtype=float)
        choose = np.argmax if maximum else np.argmin
        for structure in range(ns):
            slab = values[structure]
            if paired:
                index = choose(slab)
                indices[structure] = index
                output[structure] = slab[index]
            elif first and second:
                index = np.unravel_index(choose(slab), slab.shape)
                indices[structure] = index
                output[structure] = slab[index]
            else:
                axis = 1 if not first else 0
                index = choose(slab, axis=axis)
                indices[structure] = index
                output[structure] = np.take_along_axis(
                    slab, np.expand_dims(index, axis), axis=axis
                ).squeeze(axis)
        return indices, puw.quantity(output, unit)
    finally:
        if isinstance(values, PersistentResultHandle):
            slab = None
            values.cleanup()
