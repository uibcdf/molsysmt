"""Typed sparse H5MSM 0.5 codec for alternate atom locations."""

from collections.abc import Mapping

import h5py
import numpy as np

from molsysmt import pyunitwizard as puw

_FIELDS = frozenset({
    "frame_offsets", "atom_indices", "site_offsets", "present", "location_id",
    "atom_id", "atom_id_kind", "occupancy", "b_factor", "coordinates",
})


def _strings(value, count, name):
    values = [value] if isinstance(value, str) else list(value)
    if len(values) != count or any(
        not isinstance(item, str) or "\x00" in item for item in values
    ):
        raise ValueError(f"Alternate-location {name} must contain {count} strings.")
    return values


def _numeric(value, shape, name, unit=None):
    if value is None:
        return None
    if unit is not None:
        if not puw.is_quantity(value):
            raise ValueError(f"Alternate-location {name} must carry units of {unit}.")
        value = puw.get_value(value, to_unit=unit)
    array = np.asarray(value, dtype=np.float64)
    if array.shape != shape or np.isinf(array).any():
        raise ValueError(f"Alternate-location {name} has an invalid shape or value.")
    if name == "coordinates" and not np.isfinite(array).all():
        raise ValueError("Alternate-location coordinates must be finite.")
    return array


def prepare_alternate_location(value, n_structures, n_atoms):
    """Flatten validated alternate sites into sparse, typed columns."""
    if value is None:
        return None
    if not isinstance(value, (list, tuple, np.ndarray)) or len(value) != n_structures:
        raise ValueError("Alternate locations must contain one mapping per structure.")
    frame_offsets = [0]
    atom_indices = []
    site_offsets = [0]
    present = []
    location_ids = []
    atom_ids = []
    atom_id_kinds = []
    occupancy = []
    b_factor = []
    coordinates = []

    for frame in value:
        if not isinstance(frame, Mapping):
            raise ValueError("Alternate-location frames must be mappings of atom indices.")
        if frame and n_atoms < 0:
            raise ValueError("Alternate locations require a known atom axis.")
        if any(
            not isinstance(index, (int, np.integer)) or isinstance(index, (bool, np.bool_))
            or index < 0 or index >= n_atoms for index in frame
        ):
            raise ValueError("Alternate-location atom indices are outside the atom axis.")
        for atom_index in sorted(frame):
            entry = frame[atom_index]
            if not isinstance(entry, Mapping) or set(entry) != {
                "location_id", "occupancy", "b_factor", "atom_id", "coordinates"
            }:
                raise ValueError("Alternate-location entries require five named fields.")
            location = entry["location_id"]
            location = [location] if isinstance(location, str) else list(location)
            if not location:
                raise ValueError("Alternate-location entries require at least one site.")
            location = _strings(location, len(location), "location_id")
            count = len(location)
            occ = _numeric(entry["occupancy"], (count,), "occupancy")
            bfac = _numeric(entry["b_factor"], (count,), "b_factor", "nm**2")
            coords = _numeric(entry["coordinates"], (count, 3), "coordinates", "nm")

            ids = entry["atom_id"]
            if ids is not None:
                ids = list(ids)
                if len(ids) != count:
                    raise ValueError("Alternate-location atom_id length does not match sites.")
            for site in range(count):
                if ids is None:
                    atom_ids.append("")
                    atom_id_kinds.append(255)
                elif isinstance(ids[site], str):
                    atom_ids.append(_strings([ids[site]], 1, "atom_id")[0])
                    atom_id_kinds.append(0)
                elif isinstance(ids[site], (int, np.integer)) and not isinstance(
                    ids[site], (bool, np.bool_)
                ):
                    number = int(ids[site])
                    if not np.iinfo(np.int64).min <= number <= np.iinfo(np.int64).max:
                        raise ValueError("Alternate-location atom_id exceeds int64 range.")
                    atom_ids.append(str(number))
                    atom_id_kinds.append(1)
                else:
                    raise ValueError("Alternate-location atom_id values must be strings or integers.")
            atom_indices.append(int(atom_index))
            site_offsets.append(site_offsets[-1] + count)
            present.append([occ is not None, bfac is not None, ids is not None, coords is not None])
            location_ids.extend(location)
            occupancy.extend(occ if occ is not None else np.full(count, np.nan))
            b_factor.extend(bfac if bfac is not None else np.full(count, np.nan))
            coordinates.extend(coords if coords is not None else np.full((count, 3), np.nan))
        frame_offsets.append(len(atom_indices))

    return {
        "frame_offsets": np.asarray(frame_offsets, dtype=np.int64),
        "atom_indices": np.asarray(atom_indices, dtype=np.int64),
        "site_offsets": np.asarray(site_offsets, dtype=np.int64),
        "present": np.asarray(present, dtype=np.uint8).reshape(-1, 4),
        "location_id": location_ids,
        "atom_id": atom_ids,
        "atom_id_kind": np.asarray(atom_id_kinds, dtype=np.uint8),
        "occupancy": np.asarray(occupancy, dtype=np.float64),
        "b_factor": np.asarray(b_factor, dtype=np.float64),
        "coordinates": np.asarray(coordinates, dtype=np.float64).reshape(-1, 3),
    }


def write_alternate_location(group, prepared):
    """Write a validated sparse alternate-location payload."""
    child = group.create_group("alternate_location")
    child.attrs["schema_version"] = 1
    string_dtype = h5py.string_dtype(encoding="utf-8")
    for name, values in prepared.items():
        dtype = string_dtype if name in {"location_id", "atom_id"} else None
        shape = np.shape(values)
        dataset = child.create_dataset(
            name, data=values, dtype=dtype, compression="gzip",
            maxshape=(None, *shape[1:]),
        )
        if name == "coordinates":
            dataset.attrs["unit"] = "nm"
        elif name == "b_factor":
            dataset.attrs["unit"] = "nm**2"


def _check_dataset(child, name, dtype, shape):
    dataset = child[name]
    if dataset.shape != shape or dataset.dtype != np.dtype(dtype):
        raise ValueError(f"Alternate-location {name} has an invalid shape or type.")
    return dataset


def read_alternate_location(group, n_structures, n_atoms, frame_selection=None,
                            atom_selection=None):
    """Read only requested frames and remap their sparse atom keys."""
    if "alternate_location" not in group:
        return None
    child = group["alternate_location"]
    if child.attrs.get("schema_version") != 1 or set(child) != _FIELDS:
        raise ValueError("Unsupported H5MSM 0.5 alternate-location schema.")
    frame_offsets = _check_dataset(child, "frame_offsets", "int64", (n_structures + 1,))[:]
    n_entries = len(child["atom_indices"])
    n_sites = len(child["location_id"])
    atoms = _check_dataset(child, "atom_indices", "int64", (n_entries,))
    sites = _check_dataset(child, "site_offsets", "int64", (n_entries + 1,))
    present = _check_dataset(child, "present", "uint8", (n_entries, 4))
    kinds = _check_dataset(child, "atom_id_kind", "uint8", (n_sites,))
    occupancy = _check_dataset(child, "occupancy", "float64", (n_sites,))
    b_factor = _check_dataset(child, "b_factor", "float64", (n_sites,))
    coordinates = _check_dataset(child, "coordinates", "float64", (n_sites, 3))
    for name in ("location_id", "atom_id"):
        dataset = child[name]
        if dataset.shape != (n_sites,) or h5py.check_string_dtype(dataset.dtype) is None:
            raise ValueError(f"Alternate-location {name} has an invalid shape or type.")
    if coordinates.attrs.get("unit") != "nm" or b_factor.attrs.get("unit") != "nm**2":
        raise ValueError("Alternate-location coordinates or B factors have an unsupported unit.")
    if (frame_offsets[0] != 0 or frame_offsets[-1] != n_entries
            or np.any(np.diff(frame_offsets) < 0)
            or sites[0] != 0 or sites[-1] != n_sites):
        raise ValueError("Alternate-location offsets are inconsistent.")

    frames = range(n_structures) if frame_selection is None else frame_selection
    atom_map = None
    if atom_selection is not None:
        atom_map = {}
        for new_index, old_index in enumerate(atom_selection):
            atom_map.setdefault(int(old_index), []).append(new_index)
    result = []
    for frame_index in frames:
        start, stop = frame_offsets[int(frame_index):int(frame_index) + 2]
        frame_atoms = atoms[start:stop]
        frame_sites = sites[start:stop + 1]
        frame_present = present[start:stop]
        if (np.any(frame_atoms < 0) or (n_atoms >= 0 and np.any(frame_atoms >= n_atoms))
                or np.any(np.diff(frame_atoms) <= 0)
                or np.any(np.diff(frame_sites) <= 0)):
            raise ValueError("Alternate-location atom indices or site offsets are invalid.")
        site_start, site_stop = frame_sites[0], frame_sites[-1]
        if site_start < 0 or site_stop > n_sites:
            raise ValueError("Alternate-location site offsets are outside the site axis.")
        ids = child["atom_id"].asstr()[site_start:site_stop]
        locations = child["location_id"].asstr()[site_start:site_stop]
        site_kinds = kinds[site_start:site_stop]
        occ = occupancy[site_start:site_stop]
        bfac = b_factor[site_start:site_stop]
        coords = coordinates[site_start:site_stop]
        output = {}
        for position, old_atom in enumerate(frame_atoms):
            targets = [int(old_atom)] if atom_map is None else atom_map.get(int(old_atom), [])
            if not targets:
                continue
            flags = frame_present[position]
            if np.any(flags > 1):
                raise ValueError("Alternate-location presence flags are invalid.")
            first = frame_sites[position] - site_start
            last = frame_sites[position + 1] - site_start
            kinds_for_entry = site_kinds[first:last]
            if np.any(~np.isin(kinds_for_entry, [0, 1, 255])) or (
                bool(flags[2]) and np.any(kinds_for_entry == 255)
            ) or (not flags[2] and np.any(kinds_for_entry != 255)):
                raise ValueError("Alternate-location atom ID types are invalid.")
            values = [
                int(identifier) if kind == 1 else identifier
                for identifier, kind in zip(ids[first:last], kinds_for_entry)
            ]
            entry = {
                "location_id": np.asarray(locations[first:last], dtype=object),
                "occupancy": occ[first:last].copy() if flags[0] else None,
                "b_factor": puw.quantity(bfac[first:last].copy(), "nm**2") if flags[1] else None,
                "atom_id": np.asarray(values, dtype=object) if flags[2] else None,
                "coordinates": puw.quantity(coords[first:last].copy(), "nm") if flags[3] else None,
            }
            for new_atom in targets:
                output[new_atom] = entry.copy()
        result.append(output)
    return result


def validate_alternate_location_append(group, old_n_structures, n_atoms):
    """Validate the stored sparse columns before resizing any series."""
    read_alternate_location(
        group, old_n_structures, n_atoms,
        frame_selection=np.asarray([], dtype=np.int64),
    )
    child = group["alternate_location"]
    for name in _FIELDS:
        if child[name].maxshape[0] is not None:
            raise ValueError(f"Stored alternate-location {name} is not appendable.")
    old_entries = len(child["atom_indices"])
    if np.any(np.diff(child["site_offsets"][:]) <= 0) and old_entries:
        raise ValueError("Stored alternate-location site offsets are invalid.")


def append_alternate_location(group, prepared):
    """Extend sparse alternate sites after all append checks pass."""
    child = group["alternate_location"]
    old_entries = len(child["atom_indices"])
    old_sites = len(child["location_id"])

    data = dict(prepared)
    data["frame_offsets"] = old_entries + data["frame_offsets"][1:]
    data["site_offsets"] = old_sites + data["site_offsets"][1:]
    for name in sorted(_FIELDS):
        values = data[name]
        dataset = child[name]
        start = len(dataset)
        dataset.resize(start + len(values), axis=0)
        dataset[start:] = values
