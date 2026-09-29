"""Private explicit axis links between optional H5MSM 0.5 layers."""

import json

import numpy as np

_LAYERS = frozenset({"topology", "chemical_states", "structures", "interactions"})
_AXIS_PAIRS = {
    "atom": ("atom", "atom"),
    "structure": ("structure", "structure"),
    "structure_state": ("structure", "state"),
}


def _axis_sizes(topology, chemical_states, structures, interactions):
    sizes = {}
    if topology is not None:
        sizes[("topology", None, "atom")] = topology.n_atoms
    if chemical_states is not None:
        sizes[("chemical_states", None, "atom")] = chemical_states.n_atoms
        sizes[("chemical_states", None, "state")] = chemical_states.n_chemical_states
    if structures is not None:
        sizes[("structures", None, "structure")] = structures.n_structures
        payload = structures._frame_payload()
        if any(payload[name] is not None for name in
               ("coordinates", "velocities", "b_factor", "occupancy")):
            sizes[("structures", None, "atom")] = structures.n_atoms
    if interactions is not None:
        for name, result in interactions.items():
            sizes[("interactions", name, "atom")] = result.n_atoms
            sizes[("interactions", name, "structure")] = result.n_structures
    return sizes


def _axis_sizes_from_file(root):
    """Read axis cardinalities without loading any domain payload arrays."""
    sizes = {}
    if "topology" in root:
        sizes[("topology", None, "atom")] = int(root["topology/atoms"].attrs["n_rows"])
    if "chemical_states" in root:
        group = root["chemical_states"]
        sizes[("chemical_states", None, "atom")] = int(group.attrs["n_atoms"])
        sizes[("chemical_states", None, "state")] = int(group.attrs["n_chemical_states"])
    if "structures" in root:
        group = root["structures"]
        sizes[("structures", None, "structure")] = int(group.attrs["n_structures"])
        n_atoms = int(group.attrs["n_atoms"])
        if n_atoms >= 0:
            sizes[("structures", None, "atom")] = n_atoms
    if "interactions" in root:
        collection = root["interactions"]
        for child in collection.values():
            name = child.attrs["name"]
            metadata = json.loads(child.attrs["metadata"])
            sizes[("interactions", name, "atom")] = int(metadata["n_atoms"])
            sizes[("interactions", name, "structure")] = int(metadata["n_structures"])
    return sizes


def _normalize_link(link, sizes):
    if not isinstance(link, dict):
        raise TypeError("Each axis link must be a dictionary.")
    if set(link) != {"axis", "source", "target", "indices", "source_name", "target_name"}:
        raise ValueError("Axis links require axis, source, target, names, and indices.")
    axis = link["axis"]
    source = link["source"]
    target = link["target"]
    source_name = link["source_name"]
    target_name = link["target_name"]
    if axis not in _AXIS_PAIRS or source not in _LAYERS or target not in _LAYERS:
        raise ValueError("Axis link has an unsupported axis or layer.")
    if source == target and source_name == target_name:
        raise ValueError("An axis link must connect distinct domains.")
    for layer, name in ((source, source_name), (target, target_name)):
        if layer == "interactions":
            if not isinstance(name, str) or not name:
                raise ValueError("An interaction endpoint requires an analysis name.")
        elif name is not None:
            raise ValueError("Only interaction endpoints have analysis names.")
    source_axis, target_axis = _AXIS_PAIRS[axis]
    source_key = (source, source_name, source_axis)
    target_key = (target, target_name, target_axis)
    if source_key not in sizes or target_key not in sizes:
        raise ValueError("Axis link refers to an absent or unknown layer axis.")
    source_size, target_size = sizes[source_key], sizes[target_key]
    indices = link["indices"]
    if isinstance(indices, str) and indices == "identity":
        if source_size != target_size:
            raise ValueError("Identity axis link requires equal cardinalities.")
        normalized = "identity"
    else:
        values = np.asarray(indices)
        if values.size == 0:
            values = np.asarray(indices, dtype=np.int64)
        if values.ndim != 1 or values.shape != (source_size,) or values.dtype.kind not in "iu":
            raise ValueError("Axis link indices must match the source axis length.")
        values = values.astype(np.int64, copy=True)
        if np.any(values < -1) or np.any(values >= target_size):
            raise ValueError("Axis link indices are outside the target axis.")
        known = values[values >= 0]
        if axis == "atom" and np.unique(known).size != known.size:
            raise ValueError("Atom axis links cannot map distinct atoms to one atom.")
        normalized = "identity" if np.array_equal(values, np.arange(source_size)) else values
    return {
        "axis": axis, "source": source, "target": target,
        "source_name": source_name, "target_name": target_name,
        "indices": normalized,
    }


def normalize_associations(links, sizes):
    """Validate links without mutating an HDF5 file."""
    if links is None:
        return None
    normalized = [_normalize_link(link, sizes) for link in links]
    identities = [
        (item["axis"], item["source"], item["source_name"],
         item["target"], item["target_name"])
        for item in normalized
    ]
    if len(set(identities)) != len(identities):
        raise ValueError("Duplicate axis link endpoints are ambiguous.")
    _check_redundant_paths(normalized, sizes)
    return normalized


def _link_array(link, sizes):
    """Materialize only the map needed for one consistency comparison."""
    indices = link["indices"]
    if isinstance(indices, str):
        source_axis = _AXIS_PAIRS[link["axis"]][0]
        size = sizes[(link["source"], link["source_name"], source_axis)]
        return np.arange(size, dtype=np.int64)
    return indices


def _check_redundant_paths(links, sizes):
    """Reject contradictory direct, reverse, and two-step axis mappings."""
    for axis in ("atom", "structure"):
        edges = {
            ((link["source"], link["source_name"]),
             (link["target"], link["target_name"])): link
            for link in links if link["axis"] == axis
        }
        for (source, middle), first in edges.items():
            forward = _link_array(first, sizes)
            reverse = edges.get((middle, source))
            if reverse is not None:
                backward = _link_array(reverse, sizes)
                known = forward >= 0
                mapped = np.full(len(forward), -1, dtype=np.int64)
                mapped[known] = backward[forward[known]]
                conflict = known & (mapped >= 0) & (mapped != np.arange(len(forward)))
                if np.any(conflict):
                    raise ValueError("Reverse axis links disagree on an index.")
            for (second_source, target), second in edges.items():
                if second_source != middle or target == source:
                    continue
                direct = edges.get((source, target))
                if direct is None:
                    continue
                second_map = _link_array(second, sizes)
                composed = np.full(len(forward), -1, dtype=np.int64)
                known = forward >= 0
                composed[known] = second_map[forward[known]]
                direct_map = _link_array(direct, sizes)
                conflict = (
                    (composed >= 0) & (direct_map >= 0)
                    & (composed != direct_map)
                )
                if np.any(conflict):
                    raise ValueError("Direct and composed axis links disagree on an index.")


def write_associations(root, links):
    """Store already validated links as a versioned metadata group."""
    if links is None:
        return
    group = root.create_group("associations")
    group.attrs["schema_version"] = 1
    group.attrs["n_links"] = len(links)
    for index, link in enumerate(links):
        child = group.create_group(str(index))
        for key in ("axis", "source", "target"):
            child.attrs[key] = link[key]
        for key in ("source_name", "target_name"):
            if link[key] is not None:
                child.attrs[key] = link[key]
        indices = link["indices"]
        if isinstance(indices, str):
            child.attrs["mapping"] = "identity"
        else:
            child.attrs["mapping"] = "explicit"
            options = {"maxshape": (None,)} if link["axis"] == "structure_state" else {}
            child.create_dataset("indices", data=indices, compression="gzip", **options)


def read_associations(root, sizes):
    """Read and revalidate optional cross-layer links."""
    if "associations" not in root:
        return None
    group = root["associations"]
    if group.attrs.get("schema_version") != 1:
        raise ValueError("Unsupported H5MSM 0.5 association schema.")
    count = int(group.attrs["n_links"])
    if count < 0 or set(group) != {str(index) for index in range(count)}:
        raise ValueError("Association link groups are inconsistent.")
    links = []
    for index in range(count):
        child = group[str(index)]
        mapping = child.attrs["mapping"]
        if mapping == "identity":
            if len(child):
                raise ValueError("Identity axis link must not contain a dataset.")
            indices = "identity"
        elif mapping == "explicit" and set(child) == {"indices"}:
            indices = child["indices"][:]
        else:
            raise ValueError("Axis link has an invalid mapping encoding.")
        links.append({
            "axis": child.attrs["axis"],
            "source": child.attrs["source"],
            "target": child.attrs["target"],
            "source_name": child.attrs.get("source_name"),
            "target_name": child.attrs.get("target_name"),
            "indices": indices,
        })
    return normalize_associations(links, sizes)
