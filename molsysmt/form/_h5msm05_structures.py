"""Private, independent structural-series probe for H5MSM 0.5."""

import h5py
import numpy as np

from molsysmt.native.structures import Structures

from ._h5msm05_alternate_location import (
    append_alternate_location,
    prepare_alternate_location,
    read_alternate_location,
    validate_alternate_location_append,
    write_alternate_location,
)
from ._h5msm05_bioassembly import (
    prepare_bioassembly,
    read_bioassembly,
    same_bioassembly,
    write_bioassembly,
)

_FIELDS = {
    "structure_id": ("structure_id", None, 1, np.int64),
    "time": ("_time", "ps", 1, np.float64),
    "coordinates": ("_coordinates", "nm", 3, np.float64),
    "velocities": ("_velocities", "nm/ps", 3, np.float64),
    "box": ("_box", "nm", 3, np.float64),
    "b_factor": ("_b_factor", "nm**2", 2, np.float64),
    "occupancy": ("_occupancy", None, 2, np.float64),
    "temperature": ("_temperature", "K", 1, np.float64),
    "potential_energy": ("_potential_energy", "kJ/mol", 1, np.float64),
    "kinetic_energy": ("_kinetic_energy", "kJ/mol", 1, np.float64),
}
_ATOM_FIELDS = frozenset({"coordinates", "velocities", "b_factor", "occupancy"})
_VECTOR_FIELDS = frozenset({"coordinates", "velocities", "box"})


def _structure_id_kind(value):
    array = np.asarray(value)
    if array.dtype.kind in "iu" and np.can_cast(array.dtype, np.int64, casting="safe"):
        return "int64"
    if array.dtype.kind == "U" or (
        array.dtype.kind == "O" and all(isinstance(item, str) for item in array)
    ):
        if all("\x00" not in str(item) for item in array):
            return "string"
    raise ValueError("Structural series 'structure_id' cannot be stored as int64 or string.")


def _selection(indices, size, name):
    if indices is None:
        return None
    values = np.asarray(indices)
    if values.ndim != 1 or values.dtype.kind not in "iu":
        raise ValueError(f"{name} must be a one-dimensional integer list.")
    if np.any(values < 0) or np.any(values >= size):
        raise IndexError(f"{name} contains an index outside the stored axis.")
    return values.astype(np.int64, copy=False)


def _rows(dataset, indices):
    if indices is None:
        return dataset[:]
    if len(indices) == 0:
        return np.empty((0, *dataset.shape[1:]), dtype=dataset.dtype)
    unique, inverse = np.unique(indices, return_inverse=True)
    return dataset[unique][inverse]


def _atom_rows(dataset, frame_indices, atom_indices):
    """Read only requested atoms, preserving both requested axis orders."""
    frames = (
        np.arange(dataset.shape[0], dtype=np.int64)
        if frame_indices is None else frame_indices
    )
    shape = (len(frames), len(atom_indices), *dataset.shape[2:])
    if not len(frames) or not len(atom_indices):
        return np.empty(shape, dtype=dataset.dtype)
    unique_frames, frame_inverse = np.unique(frames, return_inverse=True)
    unique_atoms, atom_inverse = np.unique(atom_indices, return_inverse=True)
    selected = np.stack(
        [dataset[int(frame), unique_atoms, ...] for frame in unique_frames], axis=0
    )
    return selected[frame_inverse][:, atom_inverse, ...]


def _prepared_series(structures):
    if not isinstance(structures, Structures):
        raise TypeError("The structures layer requires native Structures.")
    prepare_bioassembly(structures.bioassembly)
    n_structures, n_atoms = structures._validate_alignment()
    values = {
        name: getattr(structures, source)
        for name, (source, _, _, _) in _FIELDS.items()
    }
    atom_domain_known = any(values[name] is not None for name in _ATOM_FIELDS)
    for name, (_, _, ndim, dtype) in _FIELDS.items():
        value = values[name]
        if value is None:
            continue
        array = np.asarray(value)
        expected = (n_structures,)
        if name in _ATOM_FIELDS:
            expected += (n_atoms,)
        if name in _VECTOR_FIELDS:
            expected += (3,)
        if name == "box":
            expected += (3,)
        if array.ndim != ndim or array.shape != expected:
            raise ValueError(f"Structural series {name!r} has shape {array.shape}, expected {expected}.")
        if name == "structure_id":
            _structure_id_kind(array)
        elif array.dtype.kind not in "iuf":
            raise ValueError(f"Structural series {name!r} cannot be stored as {np.dtype(dtype)}.")
    n_atoms = n_atoms if atom_domain_known else -1
    prepare_alternate_location(structures.alternate_location, n_structures, n_atoms)
    return n_structures, n_atoms, values


def write_independent_structures(root, structures, *, compression="gzip", block_size=256):
    """Write numeric structural series without creating a topology scaffold."""
    if "structures" in root:
        raise ValueError("The structures layer already exists.")
    if not isinstance(block_size, int) or block_size < 1:
        raise ValueError("block_size must be a positive integer.")
    n_structures, n_atoms, values = _prepared_series(structures)

    group = root.create_group("structures")
    group.attrs["schema_version"] = 1
    group.attrs["n_structures"] = n_structures
    group.attrs["n_atoms"] = n_atoms
    group.attrs["constant_time_step"] = bool(structures.constant_time_step)
    id_kind = None if values["structure_id"] is None else _structure_id_kind(values["structure_id"])
    group.attrs["constant_id_step"] = bool(structures.constant_id_step) and id_kind == "int64"
    group.attrs["constant_box"] = bool(structures.constant_box)
    if structures.time_step is not None:
        group.attrs["time_step_ps"] = float(structures._time_step)
    if structures.id_step is not None and id_kind == "int64":
        group.attrs["id_step"] = int(structures.id_step)

    for name, (_, unit, _, dtype) in _FIELDS.items():
        value = values[name]
        if value is None:
            continue
        array = np.asarray(value)
        if name == "structure_id" and id_kind == "string":
            array = array.astype(object)
        options = {"compression": compression} if compression is not None else {}
        stored_dtype = h5py.string_dtype("utf-8") if name == "structure_id" and id_kind == "string" else dtype
        dataset = group.create_dataset(
            name, shape=array.shape, maxshape=(None, *array.shape[1:]),
            dtype=stored_dtype, **options
        )
        if name == "structure_id":
            dataset.attrs["value_kind"] = id_kind
        if unit is not None:
            dataset.attrs["unit"] = unit
        for start in range(0, n_structures, block_size):
            stop = min(start + block_size, n_structures)
            dataset[start:stop] = array[start:stop]
    if structures.bioassembly is not None:
        write_bioassembly(group, prepare_bioassembly(structures.bioassembly))
    if structures.alternate_location is not None:
        write_alternate_location(
            group,
            prepare_alternate_location(structures.alternate_location, n_structures, n_atoms),
        )


def _append_flags(group, structures, values, old_count):
    """Prepare conservative metadata for the joined series before resizing."""
    if old_count == 0:
        integer_ids = values["structure_id"] is not None and (
            _structure_id_kind(values["structure_id"]) == "int64"
        )
        return {
            "constant_time_step": bool(structures.constant_time_step),
            "constant_id_step": bool(structures.constant_id_step) and integer_ids,
            "constant_box": bool(structures.constant_box),
            "time_step_ps": None if structures.time_step is None else float(structures._time_step),
            "id_step": None if structures.id_step is None or not integer_ids else int(structures.id_step),
        }

    def continuous(name, flag, step_key, step):
        if not bool(group.attrs.get(flag, False)) or not bool(getattr(structures, flag)):
            return False
        if name not in group or values[name] is None or step is None:
            return False
        old_step = group.attrs.get(step_key)
        if old_step is None:
            return False
        if name == "structure_id":
            if _structure_id_kind(values[name]) != "int64":
                return False
            matches_step = int(old_step) == step
        else:
            matches_step = np.isclose(old_step, step, rtol=1e-10, atol=1e-12)
        if not matches_step:
            return False
        incoming = np.asarray(values[name])
        previous = group[name][old_count - 1]
        joined = np.concatenate(([previous], incoming))
        differences = np.diff(joined)
        if name == "structure_id":
            return bool(np.all(differences == step))
        return bool(np.all(np.isclose(differences, step, rtol=1e-10, atol=1e-12)))

    time_step = None if structures.time_step is None else float(structures._time_step)
    id_step = None if structures.id_step is None else int(structures.id_step)
    time_constant = continuous("time", "constant_time_step", "time_step_ps", time_step)
    id_constant = continuous("structure_id", "constant_id_step", "id_step", id_step)
    box_constant = (
        bool(group.attrs.get("constant_box", False))
        and bool(structures.constant_box)
        and "box" in group
        and values["box"] is not None
        and bool(np.allclose(values["box"], group["box"][old_count - 1]))
    )
    return {
        "constant_time_step": time_constant,
        "constant_id_step": id_constant,
        "constant_box": box_constant,
        "time_step_ps": time_step if time_constant else None,
        "id_step": id_step if id_constant else None,
    }


def append_independent_structures(root, structures, *, block_size=256):
    """Append complete structural rows to a resizable independent layer."""
    if "structures" not in root:
        raise ValueError("The structures layer does not exist.")
    if not isinstance(block_size, int) or block_size < 1:
        raise ValueError("block_size must be a positive integer.")
    count, n_atoms, values = _prepared_series(structures)
    group = root["structures"]
    if group.attrs.get("schema_version") != 1:
        raise ValueError("Unsupported H5MSM 0.5 structures layer schema.")
    stored_bioassembly = read_bioassembly(group)
    if structures.bioassembly is not None and not same_bioassembly(
        stored_bioassembly, structures.bioassembly
    ):
        raise ValueError("Appended bioassembly metadata differ from the stored assemblies.")
    stored_alternates = "alternate_location" in group
    incoming_alternates = structures.alternate_location is not None
    if stored_alternates != incoming_alternates:
        raise ValueError("Appending structures requires matching alternate_location presence.")
    old_count = int(group.attrs["n_structures"])
    old_atoms = int(group.attrs["n_atoms"])
    if old_count < 0 or old_atoms < -1 or old_atoms != n_atoms:
        raise ValueError("The appended structures have an incompatible atom axis.")
    fields = {name for name, value in values.items() if value is not None}
    if set(group) - {"bioassembly", "alternate_location"} != fields:
        raise ValueError("The appended structures must contain the same series as the stored layer.")
    for name in fields:
        _, unit, ndim, dtype = _FIELDS[name]
        dataset = group[name]
        array = np.asarray(values[name])
        if name == "structure_id":
            incoming_kind = _structure_id_kind(array)
            stored_kind = dataset.attrs.get("value_kind", "int64")
            if stored_kind != incoming_kind or (
                stored_kind == "string" and h5py.check_string_dtype(dataset.dtype) is None
            ):
                raise ValueError("Stored structure_id cannot be appended with a different type.")
            dtype = dataset.dtype
        if (dataset.ndim != ndim or dataset.shape != (old_count, *array.shape[1:])
                or dataset.dtype != np.dtype(dtype)
                or (unit is not None and dataset.attrs.get("unit") != unit)
                or dataset.maxshape[0] is not None):
            raise ValueError(f"Stored structural series {name!r} cannot be appended.")
    incoming_alt_prepared = None
    if stored_alternates:
        validate_alternate_location_append(group, old_count, old_atoms)
        incoming_alt_prepared = prepare_alternate_location(
            structures.alternate_location, count, n_atoms
        )
    if count == 0:
        return
    metadata = _append_flags(group, structures, values, old_count)
    for name in sorted(fields):
        dataset = group[name]
        array = np.asarray(values[name])
        if name == "structure_id" and dataset.attrs.get("value_kind") == "string":
            array = array.astype(object)
        dataset.resize(old_count + count, axis=0)
        for start in range(0, count, block_size):
            stop = min(start + block_size, count)
            dataset[old_count + start:old_count + stop] = array[start:stop]
    if stored_alternates:
        append_alternate_location(group, incoming_alt_prepared)
    group.attrs["n_structures"] = old_count + count
    for name in ("constant_time_step", "constant_id_step", "constant_box"):
        group.attrs[name] = metadata[name]
    for name in ("time_step_ps", "id_step"):
        if metadata[name] is None:
            if name in group.attrs:
                del group.attrs[name]
        else:
            group.attrs[name] = metadata[name]


def read_independent_structures(root, *, structure_indices=None, atom_indices=None):
    """Read selected structural series from an optional H5MSM 0.5 layer."""
    if "structures" not in root:
        return None
    group = root["structures"]
    if group.attrs.get("schema_version") != 1:
        raise ValueError("Unsupported H5MSM 0.5 structures layer schema.")
    n_structures = int(group.attrs["n_structures"])
    n_atoms = int(group.attrs["n_atoms"])
    if n_structures < 0 or n_atoms < -1:
        raise ValueError("Invalid structures layer axis cardinality.")
    unknown = set(group) - set(_FIELDS) - {"bioassembly", "alternate_location"}
    if unknown:
        raise ValueError(f"Unknown structural series {sorted(unknown)}.")
    frame_selection = _selection(structure_indices, n_structures, "structure_indices")
    if n_atoms == -1 and atom_indices is not None:
        raise ValueError("Cannot select atoms from an unknown atom domain.")
    atom_selection = None if atom_indices is None else _selection(atom_indices, n_atoms, "atom_indices")
    if "bioassembly" in group and atom_selection is not None and not np.array_equal(
        atom_selection, np.arange(n_atoms)
    ):
        raise ValueError("Selecting atoms cannot remap bioassembly chain indices in a structures-only read.")

    data = {}
    for name, (_, unit, ndim, _) in _FIELDS.items():
        if name not in group:
            continue
        dataset = group[name]
        expected = (n_structures,)
        if name in _ATOM_FIELDS:
            if n_atoms < 0:
                raise ValueError(f"Structural series {name!r} requires a known atom axis.")
            expected += (n_atoms,)
        if name in _VECTOR_FIELDS:
            expected += (3,)
        if name == "box":
            expected += (3,)
        if dataset.ndim != ndim or dataset.shape != expected:
            raise ValueError(f"Structural series {name!r} has an invalid shape.")
        if unit is not None and dataset.attrs.get("unit") != unit:
            raise ValueError(f"Structural series {name!r} has an unsupported unit.")
        if name == "structure_id":
            kind = dataset.attrs.get("value_kind", "int64")
            if kind == "string":
                if h5py.check_string_dtype(dataset.dtype) is None:
                    raise ValueError("Structural series 'structure_id' has an invalid string type.")
            elif kind != "int64" or dataset.dtype != np.dtype("int64"):
                raise ValueError("Structural series 'structure_id' has an invalid integer type.")
        if name in _ATOM_FIELDS and atom_selection is not None:
            values = _atom_rows(dataset, frame_selection, atom_selection)
        else:
            values = _rows(dataset, frame_selection)
        if name == "structure_id" and dataset.attrs.get("value_kind") == "string":
            values = np.asarray([
                item.decode("utf-8") if isinstance(item, bytes) else str(item)
                for item in values
            ], dtype=object)
        data[name] = values

    data["bioassembly"] = read_bioassembly(group)
    data["alternate_location"] = read_alternate_location(
        group, n_structures, n_atoms, frame_selection, atom_selection
    )
    structures = Structures(skip_digestion=True, **data)
    complete_order = frame_selection is None or np.array_equal(
        frame_selection, np.arange(n_structures)
    )
    structures.constant_time_step = complete_order and bool(
        group.attrs.get("constant_time_step", False)
    )
    structures.constant_id_step = complete_order and bool(
        group.attrs.get("constant_id_step", False)
    )
    structures.constant_box = bool(group.attrs.get("constant_box", False))
    if complete_order and "time_step_ps" in group.attrs:
        structures.time_step = float(group.attrs["time_step_ps"])
    if complete_order and "id_step" in group.attrs:
        structures.id_step = int(group.attrs["id_step"])
    return structures
