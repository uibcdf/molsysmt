"""Typed H5MSM 0.5 codec for system-level biological assemblies."""

from collections.abc import Mapping

import numpy as np

from molsysmt import pyunitwizard as puw


def _chain_indices(values):
    array = np.asarray(values)
    if array.size == 0:
        array = np.asarray([], dtype=np.int64)
    if array.ndim != 1 or array.dtype.kind not in "iu":
        raise ValueError("Bioassembly chain indices must be one-dimensional integers.")
    if array.dtype.kind == "u" and np.any(array > np.iinfo(np.int64).max):
        raise ValueError("Bioassembly chain indices exceed the supported range.")
    array = array.astype(np.int64, copy=False)
    if np.any(array < 0):
        raise ValueError("Bioassembly chain indices must be nonnegative.")
    return array


def prepare_bioassembly(value):
    """Validate assembly operations and convert translations explicitly to nm."""
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise ValueError("Bioassembly must be a mapping of assembly IDs to operations.")

    prepared = []
    seen = set()
    for key, assembly in value.items():
        assembly_id = str(key)
        if not assembly_id or assembly_id in seen:
            raise ValueError("Bioassembly IDs must be unique nonempty strings.")
        seen.add(assembly_id)
        if not isinstance(assembly, Mapping) or set(assembly) != {
            "chain_indices", "rotations", "translations"
        }:
            raise ValueError("Bioassembly operations require chain_indices, rotations, and translations.")

        rotations = np.asarray(assembly["rotations"], dtype=np.float64)
        if rotations.size == 0:
            rotations = np.empty((0, 3, 3), dtype=np.float64)
        if rotations.ndim != 3 or rotations.shape[1:] != (3, 3):
            raise ValueError("Bioassembly rotations must have shape (n_operations, 3, 3).")
        if not np.isfinite(rotations).all():
            raise ValueError("Bioassembly rotations must be finite.")
        n_operations = rotations.shape[0]

        raw_translations = assembly["translations"]
        if isinstance(raw_translations, (list, tuple)):
            if not all(puw.is_quantity(entry) for entry in raw_translations):
                raise ValueError("Bioassembly translations must carry length units.")
            translations = np.asarray([
                puw.get_value(entry, to_unit="nm") for entry in raw_translations
            ], dtype=np.float64)
        elif puw.is_quantity(raw_translations):
            translations = np.asarray(
                puw.get_value(raw_translations, to_unit="nm"), dtype=np.float64
            )
        else:
            raise ValueError("Bioassembly translations must carry length units.")
        if n_operations == 0 and translations.size == 0:
            translations = np.empty((0, 3), dtype=np.float64)
        if translations.shape != (n_operations, 3) or not np.isfinite(translations).all():
            raise ValueError("Bioassembly translations must have finite shape (n_operations, 3).")

        raw_chains = assembly["chain_indices"]
        if not isinstance(raw_chains, (list, tuple, np.ndarray)):
            raise ValueError("Bioassembly chain indices must be a sequence.")
        if len(raw_chains) and isinstance(raw_chains[0], (list, tuple, np.ndarray)):
            scope = "per_operation"
            if len(raw_chains) != n_operations:
                raise ValueError("Bioassembly chain sets must match the operation count.")
            sets = [_chain_indices(indices) for indices in raw_chains]
        else:
            scope = "common"
            sets = [_chain_indices(raw_chains)]
        offsets = np.zeros(len(sets) + 1, dtype=np.int64)
        offsets[1:] = np.cumsum([len(indices) for indices in sets])
        indices = np.concatenate(sets) if sets else np.empty(0, dtype=np.int64)
        prepared.append((assembly_id, scope, indices, offsets, rotations, translations))
    return prepared


def write_bioassembly(group, prepared):
    """Write one validated system-level assembly collection."""
    collection = group.create_group("bioassembly")
    collection.attrs["schema_version"] = 1
    collection.attrs["n_assemblies"] = len(prepared)
    for index, (assembly_id, scope, chains, offsets, rotations, translations) in enumerate(prepared):
        child = collection.create_group(str(index))
        child.attrs["assembly_id"] = assembly_id
        child.attrs["chain_scope"] = scope
        child.create_dataset("chain_indices", data=chains)
        child.create_dataset("chain_offsets", data=offsets)
        child.create_dataset("rotations", data=rotations)
        dataset = child.create_dataset("translations", data=translations)
        dataset.attrs["unit"] = "nm"


def same_bioassembly(left, right):
    """Compare two validated assembly collections in canonical units."""
    left_prepared = prepare_bioassembly(left)
    right_prepared = prepare_bioassembly(right)
    if left_prepared is None or right_prepared is None:
        return left_prepared is right_prepared
    if len(left_prepared) != len(right_prepared):
        return False
    right_by_id = {entry[0]: entry[1:] for entry in right_prepared}
    for assembly_id, scope, chains, offsets, rotations, translations in left_prepared:
        other = right_by_id.get(assembly_id)
        if other is None or other[0] != scope:
            return False
        if not all(np.array_equal(a, b) for a, b in zip(
            (chains, offsets, rotations, translations), other[1:]
        )):
            return False
    return True


def read_bioassembly(group):
    """Read and validate one typed system-level assembly collection."""
    if "bioassembly" not in group:
        return None
    collection = group["bioassembly"]
    if collection.attrs.get("schema_version") != 1:
        raise ValueError("Unsupported H5MSM 0.5 bioassembly schema.")
    n_assemblies = int(collection.attrs.get("n_assemblies", -1))
    if n_assemblies < 0 or set(collection) != {str(index) for index in range(n_assemblies)}:
        raise ValueError("Bioassembly collection indices are inconsistent.")
    result = {}
    for index in range(n_assemblies):
        child = collection[str(index)]
        if set(child) != {"chain_indices", "chain_offsets", "rotations", "translations"}:
            raise ValueError("Bioassembly operation fields are incomplete.")
        assembly_id = child.attrs.get("assembly_id")
        if isinstance(assembly_id, bytes):
            assembly_id = assembly_id.decode()
        scope = child.attrs.get("chain_scope")
        if isinstance(scope, bytes):
            scope = scope.decode()
        if not isinstance(assembly_id, str) or not assembly_id or assembly_id in result:
            raise ValueError("Bioassembly IDs are invalid or duplicated.")
        if scope not in {"common", "per_operation"}:
            raise ValueError("Bioassembly chain scope is invalid.")
        chains = child["chain_indices"][:]
        offsets = child["chain_offsets"][:]
        rotations = child["rotations"][:]
        translations = child["translations"][:]
        if (
            chains.dtype != np.dtype("int64") or chains.ndim != 1
            or offsets.dtype != np.dtype("int64") or offsets.ndim != 1
            or rotations.dtype != np.dtype("float64")
            or translations.dtype != np.dtype("float64")
            or rotations.ndim != 3 or rotations.shape[1:] != (3, 3)
            or translations.shape != (len(rotations), 3)
            or child["translations"].attrs.get("unit") != "nm"
            or len(offsets) != (2 if scope == "common" else len(rotations) + 1)
            or offsets[0] != 0 or offsets[-1] != len(chains)
            or np.any(np.diff(offsets) < 0) or np.any(chains < 0)
            or not np.isfinite(rotations).all() or not np.isfinite(translations).all()
        ):
            raise ValueError("Bioassembly operation data are invalid.")
        chain_sets = [
            chains[offsets[pos]:offsets[pos + 1]].tolist()
            for pos in range(len(offsets) - 1)
        ]
        result[assembly_id] = {
            "chain_indices": chain_sets[0] if scope == "common" else chain_sets,
            "rotations": rotations,
            "translations": puw.quantity(translations, "nm"),
        }
    return result
