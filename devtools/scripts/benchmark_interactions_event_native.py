#!/usr/bin/env python3
"""Write and read a full-field occurrence-native HDF5 candidate.

This standalone probe keeps all required single-method fields and a direct
atom index. It is neither an H5MSM schema nor a public Interactions backend.
"""

from __future__ import annotations

import json
from collections import Counter

import h5py
import numpy as np
from benchmark_interactions_contract import UNITS, _signature
from benchmark_interactions_indexed_files import _write_probe_index


def write_event_native(path, result):
    """Write complete occurrence descriptors instead of a relation dictionary."""
    type_labels = tuple(dict.fromkeys(result.relation_types))
    role_labels = tuple(dict.fromkeys(result.participant_roles))
    type_lookup = {label: index for index, label in enumerate(type_labels)}
    role_lookup = {label: index for index, label in enumerate(role_labels)}
    type_codes = []
    part_offsets = [0]
    role_codes = []
    atom_offsets = [0]
    atoms = []
    for relation_id in result.occurrence_relations:
        type_codes.append(type_lookup[result.relation_types[relation_id]])
        part_first = int(result.relation_participant_offsets[relation_id])
        part_last = int(result.relation_participant_offsets[relation_id + 1])
        for part in range(part_first, part_last):
            role_codes.append(role_lookup[result.participant_roles[part]])
            atom_first = int(result.participant_atom_offsets[part])
            atom_last = int(result.participant_atom_offsets[part + 1])
            atoms.extend(result.participant_atoms[atom_first:atom_last])
            atom_offsets.append(len(atoms))
        part_offsets.append(len(role_codes))
    arrays = {
        "evaluated_structure_indices": result.evaluated_structure_indices,
        "occurrence_structures": result.occurrence_structures,
        "occurrence_type_codes": np.asarray(type_codes, dtype=np.uint32),
        "occurrence_evidence": result.occurrence_evidence,
        "occurrence_participant_offsets": np.asarray(part_offsets, dtype=np.int64),
        "participant_role_codes": np.asarray(role_codes, dtype=np.uint32),
        "participant_atom_offsets": np.asarray(atom_offsets, dtype=np.int64),
        "participant_atoms": np.asarray(atoms, dtype=np.int64),
        "occurrence_image_offsets": result.occurrence_image_offsets,
        "image_vectors": result.image_vectors,
    }
    with h5py.File(path, "w") as file:
        file.attrs["format"] = "molsysmt.interactions.event_probe"
        file.attrs["schema_version"] = 1
        file.attrs["metadata"] = json.dumps({
            "n_atoms": result.n_atoms, "n_structures": result.n_structures,
            "method": result.method, "parameters": result.parameters,
            "source_id": result.source_id, "measure_units": result.measure_units,
        })
        labels = file.create_group("labels")
        string_dtype = h5py.string_dtype(encoding="utf-8")
        for name, values in (
            ("types", type_labels), ("roles", role_labels),
            ("evidence", result.evidence_labels),
        ):
            labels.create_dataset(name, data=np.asarray(values, dtype=string_dtype))
        for name, array in arrays.items():
            file.create_dataset(
                name, data=array, compression="gzip" if array.size else None
            )
        measures = file.create_group("measurements")
        for name, array in result.measurements.items():
            measures.create_dataset(
                name, data=array, compression="gzip" if array.size else None
            )
    _write_probe_index(path, result)


def query_event_native(path, kind, index, *, page_size=128):
    """Return complete requested records through bounded event-page reads."""
    with h5py.File(path, "r") as file:
        if file.attrs.get("format") != "molsysmt.interactions.event_probe":
            raise ValueError("unsupported occurrence-native probe file")
        metadata = json.loads(file.attrs["metadata"])
        if metadata["measure_units"] != UNITS:
            raise ValueError("unexpected measure units")
        evaluated = file["evaluated_structure_indices"][:].tolist()
        indexes = file["probe_indexes"]
        if kind == "frame":
            coverage = [index] if index in set(evaluated) else []
            first, last = indexes["frame_offsets"][index:index + 2]
            ids = np.arange(int(first), int(last), dtype=np.int64)
        else:
            coverage = evaluated
            first, last = indexes["atom_offsets"][index:index + 2]
            ids = indexes["atom_occurrences"][int(first):int(last)].astype(np.int64)
        if not len(ids):
            return coverage, Counter()
        labels = {
            "types": file["labels/types"].asstr()[:],
            "roles": file["labels/roles"].asstr()[:],
            "evidence": file["labels/evidence"].asstr()[:],
        }
        output = []
        pages = ids // page_size
        n_events = len(file["occurrence_structures"])
        for page in np.unique(pages):
            selected = ids[pages == page]
            first = int(page) * page_size
            last = min(first + page_size, n_events)
            structures = file["occurrence_structures"][first:last]
            types = file["occurrence_type_codes"][first:last]
            evidence = file["occurrence_evidence"][first:last]
            measures = {name: file[f"measurements/{name}"][first:last]
                        for name in UNITS}
            part_offsets = file["occurrence_participant_offsets"][first:last + 1]
            part_first, part_last = int(part_offsets[0]), int(part_offsets[-1])
            roles = file["participant_role_codes"][part_first:part_last]
            atom_offsets = file["participant_atom_offsets"][part_first:part_last + 1]
            atom_first, atom_last = int(atom_offsets[0]), int(atom_offsets[-1])
            atoms = file["participant_atoms"][atom_first:atom_last]
            image_offsets = file["occurrence_image_offsets"][first:last + 1]
            image_first, image_last = int(image_offsets[0]), int(image_offsets[-1])
            images = file["image_vectors"][image_first:image_last]
            for occurrence_id in selected:
                local = int(occurrence_id) - first
                participants = []
                for part in range(int(part_offsets[local]),
                                  int(part_offsets[local + 1])):
                    part_local = part - part_first
                    participants.append({
                        "role": labels["roles"][int(roles[part_local])],
                        "atom_indices": atoms[
                            int(atom_offsets[part_local]) - atom_first:
                            int(atom_offsets[part_local + 1]) - atom_first
                        ].tolist(),
                    })
                output.append(_signature({
                    "structure_index": structures[local],
                    "interaction_type": labels["types"][int(types[local])],
                    "participants": participants,
                    "evidence": labels["evidence"][int(evidence[local])],
                    "measurements": {name: values[local]
                                     for name, values in measures.items()},
                    "images": images[
                        int(image_offsets[local]) - image_first:
                        int(image_offsets[local + 1]) - image_first
                    ],
                }))
        return coverage, Counter(output)
