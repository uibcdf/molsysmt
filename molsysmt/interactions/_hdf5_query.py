"""Private selective queries over versioned HDF5 interaction groups."""

import json

import numpy as np

from .result import _indices, _software_versions, _unique_in_order


def _dataset(group, path, cache=None):
    if cache is None:
        return group[path]
    datasets = cache.setdefault("datasets", {})
    if path not in datasets:
        datasets[path] = group[path]
    return datasets[path]


def _take(dataset, indices):
    """Read selected rows in requested order, including repeats."""
    positions = np.asarray(indices, dtype=np.int64)
    if not len(positions):
        return np.empty((0, *dataset.shape[1:]), dtype=dataset.dtype)
    unique, inverse = np.unique(positions, return_inverse=True)
    return dataset[unique][inverse]


def _legacy_bounds(dataset, frame, right=False):
    """Binary-search one sorted on-disk occurrence column."""
    low, high = 0, len(dataset)
    while low < high:
        middle = (low + high) // 2
        value = int(dataset[middle])
        if value < frame or (right and value == frame):
            low = middle + 1
        else:
            high = middle
    return low


def _frame_bounds(group, frame, n_structures):
    occurrences = group["occurrence_structures"]
    if "query_index" not in group:
        return (
            _legacy_bounds(occurrences, frame),
            _legacy_bounds(occurrences, frame, right=True),
        )
    index = group["query_index"]
    if index.attrs.get("schema_version") != 1:
        raise ValueError("Unsupported interaction query index version.")
    offsets = index["frame_offsets"]
    mask = index["evaluated_mask"]
    if offsets.shape != (n_structures + 1,) or mask.shape != (n_structures,):
        raise ValueError("Interaction query index has invalid axis lengths.")
    begin, end = (int(value) for value in offsets[frame:frame + 2])
    if begin < 0 or end < begin or end > len(occurrences):
        raise ValueError("Interaction frame offsets are inconsistent.")
    if (begin > 0 and int(occurrences[begin - 1]) >= frame) or (
        end < len(occurrences) and int(occurrences[end]) <= frame
    ) or (begin < end and (
        int(occurrences[begin]) != frame
        or int(occurrences[end - 1]) != frame
    )):
        raise ValueError("Interaction frame offsets disagree with occurrences.")
    return begin, end


def _coverage(group, requested, n_structures):
    if "query_index" in group:
        index = group["query_index"]
        if index.attrs.get("schema_version") != 1:
            raise ValueError("Unsupported interaction query index version.")
        mask = index["evaluated_mask"]
        if mask.shape != (n_structures,):
            raise ValueError("Interaction evaluated mask has an invalid length.")
        return requested[_take(mask, requested).astype(bool)]
    evaluated = group["evaluated_structure_indices"][:]
    return requested[np.isin(requested, evaluated)]


def _relation(group, relation, type_labels, role_labels, cache=None):
    relation = int(relation)
    part_first, part_last = (int(value) for value in
                             _dataset(group, "relation_participant_offsets", cache)[relation:relation + 2])
    atom_offsets = _dataset(group, "participant_atom_offsets", cache)[part_first:part_last + 1]
    atoms = _dataset(group, "participant_atoms", cache)[
        int(atom_offsets[0]):int(atom_offsets[-1])
    ]
    role_codes = _dataset(group, "participant_roles_codes", cache)[part_first:part_last]
    participants = []
    for index, role_code in enumerate(role_codes):
        start = int(atom_offsets[index] - atom_offsets[0])
        stop = int(atom_offsets[index + 1] - atom_offsets[0])
        participants.append({
            "role": role_labels[int(role_code)],
            "atom_indices": atoms[start:stop].astype(np.int64, copy=True),
        })
    type_code = int(_dataset(group, "relation_types_codes", cache)[relation])
    return {
        "interaction_type": type_labels[type_code],
        "participants": participants,
    }


def query_interactions_group(group, structure_indices, *, atom_indices=None,
                             mode="incident", interaction_types=None,
                             _cache=None):
    """Read only requested frames and their relevant relation descriptions."""
    if group.attrs.get("format") != "molsysmt.interactions" or group.attrs.get(
        "schema_version"
    ) not in (1, 2):
        raise ValueError("Unsupported Interactions group schema or version.")
    metadata = (
        _cache["metadata"] if _cache is not None
        else json.loads(group.attrs["metadata"])
    )
    from ._execution_provenance import legacy, normalize, project, read_group

    if _cache is not None and "execution_records" in _cache:
        records = _cache["execution_records"]
    else:
        if group.attrs["schema_version"] == 1:
            metadata = dict(metadata)
            metadata["parameters"], execution = legacy(metadata["parameters"])
            incoming = None
        else:
            execution, incoming = None, read_group(group)
        records = normalize(incoming, execution,
                            group["evaluated_structure_indices"][:], int(metadata["n_structures"]))
        if _cache is not None:
            _cache.update(execution_records=records, metadata=metadata)
    n_atoms = int(metadata["n_atoms"])
    n_structures = int(metadata["n_structures"])
    frames = _unique_in_order(_indices(
        structure_indices, n_structures, "structure_indices"
    ))
    if mode not in {"incident", "internal", "cross"}:
        raise ValueError("mode must be 'incident', 'internal', or 'cross'.")
    atoms = None if atom_indices is None else np.unique(
        _indices(atom_indices, n_atoms, "atom_indices")
    )
    allowed_types = (
        None if interaction_types is None else
        {interaction_types} if isinstance(interaction_types, str) else
        set(interaction_types)
    )
    if _cache is not None and _cache.get("evaluated_mask") is not None:
        coverage = frames[_cache["evaluated_mask"][frames]]
    else:
        coverage = _coverage(group, frames, n_structures)
    chunks = []
    expected_frames = []
    for frame in coverage:
        if _cache is not None and _cache.get("frame_offsets") is not None:
            begin, end = (int(value) for value in
                          _cache["frame_offsets"][int(frame):int(frame) + 2])
        else:
            begin, end = _frame_bounds(group, int(frame), n_structures)
        if begin < end:
            chunks.append(np.arange(begin, end, dtype=np.int64))
            expected_frames.append(np.full(end - begin, frame, dtype=np.int64))
    positions = np.concatenate(chunks) if chunks else np.empty(0, dtype=np.int64)
    expected = (
        np.concatenate(expected_frames) if expected_frames
        else np.empty(0, dtype=np.int64)
    )
    relations = _take(_dataset(group, "occurrence_relations", _cache), positions).astype(np.int64)

    descriptors = {}
    if len(relations):
        type_labels = (
            _cache["type_labels"] if _cache is not None
            else _dataset(group, "labels/relation_types").asstr()[:]
        )
        role_labels = (
            _cache["role_labels"] if _cache is not None
            else _dataset(group, "labels/participant_roles").asstr()[:]
        )
        allowed_relations = set()
        for relation in np.unique(relations):
            relation = int(relation)
            relation_cache = None if _cache is None else _cache["relations"]
            if relation_cache is not None and relation in relation_cache:
                descriptor = relation_cache[relation]
            else:
                descriptor = _relation(
                    group, relation, type_labels, role_labels, _cache
                )
                if relation_cache is not None:
                    relation_cache[relation] = descriptor
            if allowed_types is not None and descriptor["interaction_type"] not in allowed_types:
                continue
            if atoms is not None:
                involved = np.unique(np.concatenate([
                    part["atom_indices"] for part in descriptor["participants"]
                ]))
                matches = np.isin(involved, atoms)
                if mode == "incident" and not matches.any():
                    continue
                if mode == "internal" and not matches.all():
                    continue
                if mode == "cross" and (not matches.any() or matches.all()):
                    continue
            allowed_relations.add(relation)
            descriptors[relation] = descriptor
        keep = np.isin(relations, list(allowed_relations))
        positions = positions[keep]
        relations = relations[keep]
        expected = expected[keep]

    evidence_codes = _take(_dataset(group, "occurrence_evidence", _cache), positions)
    evidence_labels = (
        _cache["evidence_labels"] if _cache is not None
        else _dataset(group, "labels/evidence").asstr()[:]
    )
    evidence = np.asarray(evidence_labels, dtype=str)[evidence_codes]
    measures = {
        name: _take(dataset, positions).astype(np.float64)
        for name, dataset in (
            _cache["measurements"].items() if _cache is not None
            else group["measurements"].items()
        )
    }
    if "occurrence_image_offsets" in group:
        offsets = _dataset(group, "occurrence_image_offsets", _cache)
        starts = _take(offsets, positions)
        stops = _take(offsets, positions + 1)
        lengths = stops - starts
        image_offsets = np.r_[0, np.cumsum(lengths, dtype=np.int64)]
        vectors = _dataset(group, "image_vectors", _cache)
        pieces = [vectors[int(first):int(last)]
                  for first, last in zip(starts, stops)]
        image_vectors = (
            np.concatenate(pieces) if pieces else np.empty((0, 3), dtype=np.int32)
        )
    else:
        image_offsets = None
        image_vectors = None
    structure_values = _take(
        _dataset(group, "occurrence_structures", _cache), positions
    ).astype(np.int64)
    if not np.array_equal(structure_values, expected):
        raise ValueError("Interaction frame index disagrees with stored occurrences.")
    participant_atoms = (
        np.unique(np.concatenate([
            participant["atom_indices"]
            for descriptor in descriptors.values()
            for participant in descriptor["participants"]
        ])) if descriptors else np.empty(0, dtype=np.int64)
    )
    atom_sources = (
        _take(_dataset(group, "atom_source_indices", _cache), participant_atoms)
        if "atom_source_indices" in group else participant_atoms.copy()
    )
    structure_sources = (
        _take(_dataset(group, "structure_source_indices", _cache), coverage)
        if "structure_source_indices" in group else coverage.copy()
    )
    return {
        "n_atoms": n_atoms,
        "n_structures": n_structures,
        "source_n_atoms": int(metadata.get("source_n_atoms", n_atoms)),
        "source_n_structures": int(metadata.get("source_n_structures", n_structures)),
        "source_id": metadata.get("source_id"),
        "software": _software_versions(metadata.get("software")),
        "execution_records": project(records, coverage),
        "method": metadata["method"],
        "parameters": metadata["parameters"],
        "evaluation_mode": metadata["evaluation_mode"],
        "evaluated_structure_indices": coverage,
        "evaluated_structure_source_indices": structure_sources,
        "occurrence_indices": positions,
        "participant_atom_indices": participant_atoms,
        "participant_atom_source_indices": atom_sources,
        "structure_indices": structure_values,
        "relation_indices": relations,
        "relations": descriptors,
        "evidence": evidence,
        "measurements": measures,
        "measure_units": metadata["measure_units"],
        "image_offsets": image_offsets,
        "image_vectors": image_vectors,
    }


def query_named_interactions_file(filename, analysis_name, structure_indices,
                                  *, atom_indices=None, mode="incident",
                                  interaction_types=None):
    """Query one named analysis in an H5MSM 0.5 file by requested frames."""
    with HDF5InteractionsReader(filename, analysis_name) as reader:
        return reader.query(
            structure_indices, atom_indices=atom_indices, mode=mode,
            interaction_types=interaction_types,
        )


class HDF5InteractionsReader:
    """Hold one named H5MSM 0.5 analysis open for repeated selective queries."""

    def __init__(self, filename, analysis_name):
        import h5py

        if not isinstance(analysis_name, str) or not analysis_name:
            raise ValueError("analysis_name must be a nonempty string.")
        self.file = h5py.File(filename, "r")
        self.group = None
        self._cache = None
        try:
            if self.file.attrs.get("type") != "h5msm" or self.file.attrs.get("version") != "0.5":
                raise ValueError("Expected an H5MSM 0.5 file.")
            if "interactions" not in self.file:
                raise KeyError("The file has no interaction analyses.")
            collection = self.file["interactions"]
            if (collection.attrs.get("schema") != "molsysmt.interactions_collection"
                    or collection.attrs.get("schema_version") != 1):
                raise ValueError("Unsupported interaction collection schema or version.")
            count = int(collection.attrs["n_analyses"])
            if count < 0 or set(collection) != {str(index) for index in range(count)}:
                raise ValueError("Interaction collection groups are inconsistent.")
            for index in range(count):
                group = collection[str(index)]
                if group.attrs.get("name") == analysis_name:
                    self.group = group
                    break
            if self.group is None:
                raise KeyError(f"Unknown interaction analysis {analysis_name!r}.")
            if (self.group.attrs.get("format") != "molsysmt.interactions"
                    or self.group.attrs.get("schema_version") not in (1, 2)):
                raise ValueError("Unsupported Interactions group schema or version.")
            metadata = json.loads(self.group.attrs["metadata"])
            self._cache = {
                "metadata": metadata,
                "type_labels": self.group["labels/relation_types"].asstr()[:],
                "role_labels": self.group["labels/participant_roles"].asstr()[:],
                "evidence_labels": self.group["labels/evidence"].asstr()[:],
                "measurements": dict(self.group["measurements"].items()),
                "relations": {},
                "datasets": {},
                "frame_offsets": None,
                "evaluated_mask": None,
            }
            n_structures = int(metadata["n_structures"])
            if "query_index" in self.group and n_structures <= 200_000:
                index = self.group["query_index"]
                if index.attrs.get("schema_version") != 1:
                    raise ValueError("Unsupported interaction query index version.")
                offsets = index["frame_offsets"][:]
                mask = index["evaluated_mask"][:]
                if (offsets.shape != (n_structures + 1,)
                        or mask.shape != (n_structures,)
                        or int(offsets[0]) != 0
                        or int(offsets[-1]) != len(self.group["occurrence_structures"])
                        or np.any(np.diff(offsets) < 0)):
                    raise ValueError("Interaction frame offsets are inconsistent.")
                self._cache["frame_offsets"] = offsets
                self._cache["evaluated_mask"] = mask
        except Exception:
            self.close()
            raise

    def query(self, structure_indices, *, atom_indices=None, mode="incident",
              interaction_types=None):
        """Read matching occurrences from the open analysis."""
        if self.group is None:
            raise ValueError("The HDF5 interaction reader is closed.")
        return query_interactions_group(
            self.group, structure_indices, atom_indices=atom_indices,
            mode=mode, interaction_types=interaction_types, _cache=self._cache,
        )

    def close(self):
        """Close the underlying file handle."""
        if self.file is not None:
            self.file.close()
        self.file = None
        self.group = None
        self._cache = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
