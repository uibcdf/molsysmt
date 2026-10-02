"""Packing active source spans without a whole-analysis query projection."""

from types import MappingProxyType

import numpy as np

from ._frame_validity import _metadata
from ._hdf5_writer import _spans, _window_bytes
from .result import _STORAGE_FIELDS, Interactions, _immutable_array


def _owned(shape, dtype, fill):
    # Freeze one destination column at a time. At most this column, rather
    # than all observations, is duplicated while making its immutable owner.
    array = np.empty(shape, dtype=dtype)
    fill(array)
    return _immutable_array(array)


def compact(source):
    """Return a packed snapshot preserving the existing registry and handles."""
    if not source._is_full:
        raise ValueError("compact the full result, not a query view")
    count = source.n_interactions
    window = _window_bytes()
    edited = hasattr(source, "_root") or hasattr(source, "_segments")
    if hasattr(source, "_segments"):
        has_images = source._has_images
    else:
        base = source._root if hasattr(source, "_root") else source
        has_images = base.image_vectors is not None
    observation_fields = {"occurrence_structures", "occurrence_relations", "occurrence_evidence",
                          "occurrence_image_offsets", "image_vectors", "measurements"}
    result = object.__new__(Interactions)
    result.__dict__ = {name: getattr(source, name)
                       for name in _STORAGE_FIELDS - observation_fields}
    result.__dict__.update(_metadata(source))
    result._coverage = source.evaluated_structure_indices
    from ._execution_provenance import normalize

    result._execution_records = normalize(source.execution_records, None,
                                          result._coverage, source.n_structures)
    result._is_full = True
    for name in ("_atom_relation_offsets", "_atom_relation_ids",
                 "_relation_occurrence_offsets", "_relation_occurrence_ids"):
        result.__dict__[name] = None

    def fill_column(destination, name, measurement=False):
        position = 0
        step = max(1, window // destination.dtype.itemsize)
        for base, first, last, relations, evidence in _spans(source):
            for begin in range(first, last, step):
                end = min(begin + step, last)
                values = base.measurements[name][begin:end] if measurement else getattr(base, name)[begin:end]
                mapping = relations if name == "occurrence_relations" and not measurement else None
                if name == "occurrence_evidence" and not measurement:
                    mapping = evidence
                destination[position:position + end - begin] = values if mapping is None else mapping[values]
                position += end - begin
        if position != count:
            raise ValueError("Active occurrence blocks disagree with the analysis row count")

    for name, dtype in (("occurrence_structures", np.int64),
                        ("occurrence_relations", np.int64), ("occurrence_evidence", np.int32)):
        result.__dict__[name] = (_owned((count,), dtype, lambda array, column=name: fill_column(array, column))
                                 if edited else getattr(source, name))
    result.__dict__["measurements"] = MappingProxyType({
        name: (_owned((count,), np.float64, lambda array, column=name: fill_column(array, column, True))
               if edited else source.measurements[name]) for name in source.measure_units
    })
    if has_images and edited:
        image_count = sum(int(base.occurrence_image_offsets[last] - base.occurrence_image_offsets[first])
                          for base, first, last, _, _ in _spans(source))

        def fill_offsets(destination):
            destination[0] = 0
            position = image_position = 0
            for base, first, last, _, _ in _spans(source):
                image_first = int(base.occurrence_image_offsets[first])
                for begin in range(first, last, max(1, window // 8)):
                    end = min(begin + max(1, window // 8), last)
                    destination[position + 1:position + end - begin + 1] = (
                        base.occurrence_image_offsets[begin + 1:end + 1] - image_first + image_position)
                    position += end - begin
                image_position += int(base.occurrence_image_offsets[last]) - image_first

        def fill_images(destination):
            position = 0
            for base, first, last, _, _ in _spans(source):
                begin, end = map(int, base.occurrence_image_offsets[[first, last]])
                for start in range(begin, end, max(1, window // 12)):
                    stop = min(start + max(1, window // 12), end)
                    destination[position:position + stop - start] = base.image_vectors[start:stop]
                    position += stop - start

        result.__dict__["occurrence_image_offsets"] = _owned((count + 1,), np.int64, fill_offsets)
        result.__dict__["image_vectors"] = _owned((image_count, 3), np.int32, fill_images)
    else:
        result.__dict__["occurrence_image_offsets"] = base.occurrence_image_offsets if has_images else None
        result.__dict__["image_vectors"] = base.image_vectors if has_images else None

    def fill_positions(destination):
        for first in range(0, count, max(1, window // 8)):
            last = min(first + max(1, window // 8), count)
            destination[first:last] = np.arange(first, last, dtype=np.int64)

    result._positions = _owned((count,), np.int64, fill_positions) if edited else source._positions
    result._storage_locked = True
    return result
