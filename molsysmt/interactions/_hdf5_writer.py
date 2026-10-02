"""Writing packed or edited analyses without packing all active occurrences."""

import json

import numpy as np

_WINDOW_BYTES = 1024 * 1024


def _window_bytes():
    from molsysmt import configure

    fraction = configure.chunk_memory_fraction
    fraction = 0.1 if fraction is None or fraction <= 0 else fraction
    return max(16, min(_WINDOW_BYTES, int(configure.max_ram_usage * fraction)))


def _dataset(group, name, shape, dtype):
    return group.create_dataset(
        name, shape=shape, dtype=dtype, compression="gzip" if np.prod(shape) else None
    )


def _write_array(group, name, array, window):
    """Write an existing numeric buffer in bounded first-axis windows."""
    dataset = _dataset(group, name, array.shape, array.dtype)
    _copy(dataset, 0, array, window)
    return dataset


def _copy(dataset, offset, array, window):
    row_bytes = array.dtype.itemsize * int(np.prod(array.shape[1:]))
    step = max(1, window // row_bytes)
    for first in range(0, len(array), step):
        last = min(first + step, len(array))
        dataset[offset + first : offset + last] = array[first:last]


def _identity(values, window):
    step = max(1, window // 8)
    return all(
        np.array_equal(
            values[first : first + step],
            np.arange(first, min(first + step, len(values)), dtype=np.int64),
        )
        for first in range(0, len(values), step)
    )


def _ranges(base, frames):
    starts = np.searchsorted(base.occurrence_structures, frames, side="left")
    stops = np.searchsorted(base.occurrence_structures, frames, side="right")
    first = last = None
    for begin, end in zip(starts, stops):
        if begin == end:
            continue
        if last is not None and begin != last:
            yield int(first), int(last)
            first = None
        if first is None:
            first = begin
        last = end
    if first is not None:
        yield int(first), int(last)


def _spans(result):
    """Traverse contiguous active slices in canonical frame/row order."""
    if hasattr(result, "_segments"):
        frames = np.sort(result.evaluated_structure_indices)
        owners = result._frame_owners[frames]
        breaks = np.r_[0, np.flatnonzero(np.diff(owners)) + 1, len(frames)]
        for first, last in zip(breaks[:-1], breaks[1:]):
            if first == last:
                continue
            base, _, relations, evidence = result._segments[int(owners[first])]
            for begin, end in _ranges(base, frames[first:last]):
                yield base, begin, end, relations, evidence
    elif hasattr(result, "_root"):
        for first, last in _ranges(
            result._root, np.sort(result.evaluated_structure_indices)
        ):
            yield result._root, first, last, None, None
    elif result.n_interactions:
        yield result, 0, result.n_interactions, None, None


def _frame_offsets(result):
    if hasattr(result, "_frame_offsets"):
        return result._frame_offsets
    base = result._root if hasattr(result, "_root") else result
    frames = result.evaluated_structure_indices
    offsets = np.zeros(result.n_structures + 1, dtype=np.int64)
    offsets[frames + 1] = np.searchsorted(
        base.occurrence_structures, frames, side="right"
    ) - np.searchsorted(base.occurrence_structures, frames, side="left")
    np.cumsum(offsets, out=offsets)
    return offsets


def _labels(group, result, window):
    import h5py

    labels = group.create_group("labels")
    strings = h5py.string_dtype(encoding="utf-8")
    for name, values in (
        ("relation_types", result.relation_types),
        ("participant_roles", result.participant_roles),
    ):
        unique = tuple(dict.fromkeys(values))
        lookup = {value: index for index, value in enumerate(unique)}
        labels.create_dataset(
            name,
            data=np.asarray(unique, dtype=strings),
            compression="gzip" if unique else None,
        )
        codes = _dataset(group, f"{name}_codes", (len(values),), np.uint32)
        step = max(1, window // 4)
        for first in range(0, len(values), step):
            last = min(first + step, len(values))
            codes[first:last] = np.fromiter(
                (lookup[values[index]] for index in range(first, last)),
                dtype=np.uint32,
                count=last - first,
            )
    labels.create_dataset(
        "evidence",
        data=np.asarray(result.evidence_labels, dtype=strings),
        compression="gzip" if result.evidence_labels else None,
    )


def write_group(result, group):
    """Write codec 2 using bounded occurrence windows and frame metadata."""
    if not result._is_full:
        raise ValueError("write the full result, not a query view")
    from ._execution_provenance import write_group as write_execution

    window = _window_bytes()
    count = image_count = 0
    if hasattr(result, "_segments"):
        has_images = result._has_images
    else:
        base = result._root if hasattr(result, "_root") else result
        has_images = base.image_vectors is not None
    for base, first, last, _, _ in _spans(result):
        count += last - first
        if has_images:
            image_count += int(
                base.occurrence_image_offsets[last]
                - base.occurrence_image_offsets[first]
            )
    if count != result.n_interactions:
        raise ValueError(
            "Active occurrence blocks disagree with the analysis row count"
        )

    group.attrs["format"] = "molsysmt.interactions"
    group.attrs["schema_version"] = 2
    group.attrs["metadata"] = json.dumps(
        {
            "n_atoms": result.n_atoms,
            "n_structures": result.n_structures,
            "source_n_atoms": result.source_n_atoms,
            "source_n_structures": result.source_n_structures,
            "method": result.method,
            "parameters": result.parameters,
            "source_id": result.source_id,
            "measure_units": result.measure_units,
            "software": result.software,
            "evaluation_mode": result.evaluation_mode,
        }
    )
    write_execution(group, result.execution_records)
    index = group.create_group("query_index")
    index.attrs["schema_version"] = 1
    offsets = _frame_offsets(result)
    if int(offsets[-1]) != count:
        raise ValueError("Frame offsets disagree with the active occurrence blocks")
    _write_array(index, "frame_offsets", offsets, window)
    mask = np.zeros(result.n_structures, dtype=np.bool_)
    mask[result.evaluated_structure_indices] = True
    _write_array(index, "evaluated_mask", mask, window)
    _labels(group, result, window)
    for name in (
        "evaluated_structure_indices",
        "atom_source_indices",
        "structure_source_indices",
        "relation_participant_offsets",
        "participant_atom_offsets",
        "participant_atoms",
        "evaluation_atom_indices",
        "evaluation_atom_indices_b",
        "evaluation_universe_indices",
    ):
        values = getattr(result, name)
        if values is None or (
            name in {"atom_source_indices", "structure_source_indices"}
            and _identity(values, window)
        ):
            continue
        _write_array(group, name, values, window)
    columns = {
        name: _dataset(group, name, (count,), dtype)
        for name, dtype in (
            ("occurrence_structures", np.int64),
            ("occurrence_relations", np.int64),
            ("occurrence_evidence", np.int32),
        )
    }
    measures = group.create_group("measurements")
    measure_columns = {
        name: _dataset(measures, name, (count,), np.float64)
        for name in result.measure_units
    }
    image_offsets = vectors = None
    if has_images:
        image_offsets = _dataset(
            group, "occurrence_image_offsets", (count + 1,), np.int64
        )
        vectors = _dataset(group, "image_vectors", (image_count, 3), np.int32)
        image_offsets[0] = 0
    destination = image_destination = 0
    step = max(1, window // 8)
    for base, first, last, relations, evidence in _spans(result):
        for begin in range(first, last, step):
            end = min(begin + step, last)
            stop = destination + end - begin
            columns["occurrence_structures"][destination:stop] = (
                base.occurrence_structures[begin:end]
            )
            rows = base.occurrence_relations[begin:end]
            columns["occurrence_relations"][destination:stop] = (
                rows if relations is None else relations[rows]
            )
            rows = base.occurrence_evidence[begin:end]
            columns["occurrence_evidence"][destination:stop] = (
                rows if evidence is None else evidence[rows]
            )
            for name in result.measure_units:
                measure_columns[name][destination:stop] = base.measurements[name][
                    begin:end
                ]
            if has_images:
                image_first = int(base.occurrence_image_offsets[begin])
                image_last = int(base.occurrence_image_offsets[end])
                image_offsets[destination + 1 : stop + 1] = (
                    base.occurrence_image_offsets[begin + 1 : end + 1]
                    - image_first
                    + image_destination
                )
                _copy(
                    vectors,
                    image_destination,
                    base.image_vectors[image_first:image_last],
                    window,
                )
                image_destination += image_last - image_first
            destination = stop
    if destination != count or image_destination != image_count:
        raise ValueError(
            "Written occurrence columns disagree with their declared lengths"
        )
