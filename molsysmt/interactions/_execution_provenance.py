"""Frame-scoped execution provenance, independent of scientific criteria."""

from copy import deepcopy

import numpy as np


def normalize(records, execution, coverage, size):
    from .result import _immutable_array, _indices

    if records is not None and execution is not None:
        raise ValueError("Supply execution or execution_records, not both")
    if records is None:
        records = [{"structure_indices": coverage, "details": dict(execution or {})}]
    result = []
    seen = []
    for record in records:
        frames = _indices(record["structure_indices"], size, "execution structure_indices")
        if np.unique(frames).size != frames.size:
            raise ValueError("Execution structure indices must be unique")
        details = deepcopy(dict(record["details"]))
        if len(frames):
            result.append((_immutable_array(np.sort(frames)), details))
            seen.append(frames)
    frames = np.concatenate(seen) if seen else np.empty(0, dtype=np.int64)
    if not np.array_equal(np.sort(frames), np.sort(coverage)):
        raise ValueError("Execution records must partition evaluated structures exactly")
    return tuple(result)


def project(records, coverage):
    """Export independent records for the current query's evaluated frames."""
    result = []
    requested = np.unique(coverage)
    for frames, details in records:
        positions = np.searchsorted(frames, requested)
        valid = positions < len(frames)
        selected = requested[valid][frames[positions[valid]] == requested[valid]]
        if len(selected):
            result.append({"structure_indices": selected, "details": deepcopy(details)})
    return tuple(result)


def replace(source, incoming, frames):
    from .result import _immutable_array

    records = []
    for active, details in source._execution_records:
        mask = np.isin(active, source._coverage) & ~np.isin(active, frames)
        if mask.all():
            records.append((active, details))
        elif mask.any():
            records.append((_immutable_array(active[mask]), details))
    for record in incoming.execution_records:
        records.append((_immutable_array(record["structure_indices"]), record["details"]))
    return tuple(records)


def remap(source, frames):
    result = []
    for record in source.execution_records:
        selected = np.flatnonzero(np.isin(frames, record["structure_indices"]))
        if len(selected):
            result.append({"structure_indices": selected, "details": record["details"]})
    return tuple(result)


def legacy(parameters):
    """Migrate only the documented runtime keys of version-1 payloads."""
    parameters = deepcopy(parameters)
    keys = ("execution", "execution_chunks", "memory_policy")
    execution = {key: parameters.pop(key) for key in keys if key in parameters}
    legs = parameters.get("hbond_parameters")
    if isinstance(legs, dict):
        nested = {key: legs.pop(key) for key in keys if key in legs}
        if nested:
            execution["hbond_execution"] = nested
    return parameters, execution


def write_group(group, records):
    import json

    import h5py

    child = group.create_group("execution")
    child.create_dataset("details", data=np.asarray(
        [json.dumps(record["details"]) for record in records],
        dtype=h5py.string_dtype(encoding="utf-8")))
    offsets = np.r_[0, np.cumsum([len(record["structure_indices"]) for record in records])].astype(np.int64)
    frames = np.concatenate([record["structure_indices"] for record in records]) if records else np.empty(0, dtype=np.int64)
    child.create_dataset("structure_offsets", data=offsets)
    child.create_dataset("structure_indices", data=frames, compression="gzip" if frames.size else None)


def read_group(group):
    import json

    child = group["execution"]
    details = child["details"].asstr()[:]
    offsets = child["structure_offsets"][:]
    frames = child["structure_indices"][:]
    if (offsets.shape != (len(details) + 1,) or offsets[0] != 0
            or offsets[-1] != len(frames) or np.any(np.diff(offsets) < 0)):
        raise ValueError("Invalid execution provenance offsets")
    return tuple({"structure_indices": frames[first:last], "details": json.loads(value)}
                 for value, first, last in zip(details, offsets[:-1], offsets[1:]))
