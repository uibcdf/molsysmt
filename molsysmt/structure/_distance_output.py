"""Encode positional distance observations while keeping both endpoint axes."""

from molsysmt import pyunitwizard as puw
from molsysmt._private.execution.persistent_result import PersistentResultHandle
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.variables import is_all


def dictionary(
    values,
    atoms,
    second_atoms,
    frames,
    second_frames,
    paired,
    indices,
    structure_indices,
    centered,
):
    raw = puw.get_value(values)
    if isinstance(raw, PersistentResultHandle):
        raw.cleanup()
        raise NotImplementedMethodError(
            caller="molsysmt.structure.get_distances",
            message="Disk-backed results require ndarray output; consume the handle in blocks.",
        )
    indices = "atom" if indices is None else indices
    if indices == "group" or (centered and indices == "atom"):
        raise NotImplementedMethodError(caller="molsysmt.structure.get_distances")
    ns = values.shape[0]
    n_first = values.shape[1]
    n_second = n_first if paired else values.shape[2]
    first_labels = list(range(n_first)) if indices == "selection" else atoms
    second_labels = (
        list(range(n_second))
        if indices == "selection"
        else atoms
        if second_atoms is None
        else second_atoms
    )
    frame_labels = (
        list(range(ns))
        if structure_indices == "selection" or is_all(frames)
        else frames
    )
    other_labels = (
        list(range(ns))
        if structure_indices == "selection" or is_all(second_frames)
        else second_frames
    )
    result = {}
    for first in range(n_first):
        for second in [first] if paired else range(n_second):
            if paired and indices == "selection":
                owner, key = result, first
            else:
                owner = result.setdefault(int(first_labels[first]), {})
                key = int(second_labels[second])
            series = values[:, first] if paired else values[:, first, second]
            if structure_indices is None:
                owner[key] = series
            else:
                entries = owner.setdefault(key, {})
                for position in range(ns):
                    frame = int(frame_labels[position])
                    if second_frames is None:
                        entries[frame] = series[position]
                    else:
                        entries.setdefault(frame, {})[int(other_labels[position])] = (
                            series[position]
                        )
    return result
