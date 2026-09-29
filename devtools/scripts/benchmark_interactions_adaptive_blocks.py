#!/usr/bin/env python3
"""Compare full-field global, event, and projected-choice HDF5 blocks.

The writer materializes the source records and both candidate descriptors per
block. It measures snapshot size and checks the complete payload and atom
postings, but does not establish bounded streaming construction or fast reads.
"""

from __future__ import annotations

import argparse
import json
import platform
import tempfile
from collections import Counter
from pathlib import Path

import h5py
import numpy as np
from benchmark_interactions_contract import (
    METHOD,
    UNITS,
    _direct_postings,
    _signature,
    expected,
    generate_fixture,
)
from benchmark_interactions_indexed_files import _smallest_unsigned

import molsysmt as msm


def _write_arrays(group, arrays):
    for name, array in arrays.items():
        group.create_dataset(
            name, data=array, compression="gzip" if array.size else None
        )


def _descriptor_arrays(result, labels, mode):
    type_codes = {label: index for index, label in enumerate(labels["types"])}
    role_codes = {label: index for index, label in enumerate(labels["roles"])}
    if mode == "global":
        return {
            "relation_type_codes": np.asarray(
                [type_codes[value] for value in result.relation_types],
                dtype=np.uint32,
            ),
            "relation_participant_offsets": result.relation_participant_offsets,
            "participant_role_codes": np.asarray(
                [role_codes[value] for value in result.participant_roles],
                dtype=np.uint32,
            ),
            "participant_atom_offsets": result.participant_atom_offsets,
            "participant_atoms": result.participant_atoms,
            "occurrence_relations": result.occurrence_relations,
        }
    occurrence_types = []
    occurrence_participant_offsets = [0]
    roles = []
    atom_offsets = [0]
    atoms = []
    for relation in result.occurrence_relations:
        occurrence_types.append(type_codes[result.relation_types[relation]])
        first = int(result.relation_participant_offsets[relation])
        last = int(result.relation_participant_offsets[relation + 1])
        for part in range(first, last):
            roles.append(role_codes[result.participant_roles[part]])
            atom_first = int(result.participant_atom_offsets[part])
            atom_last = int(result.participant_atom_offsets[part + 1])
            atoms.extend(result.participant_atoms[atom_first:atom_last])
            atom_offsets.append(len(atoms))
        occurrence_participant_offsets.append(len(roles))
    return {
        "occurrence_type_codes": np.asarray(occurrence_types, dtype=np.uint32),
        "occurrence_participant_offsets": np.asarray(
            occurrence_participant_offsets, dtype=np.int64
        ),
        "participant_role_codes": np.asarray(roles, dtype=np.uint32),
        "participant_atom_offsets": np.asarray(atom_offsets, dtype=np.int64),
        "participant_atoms": np.asarray(atoms, dtype=np.int64),
    }


def _common_arrays(result, labels, start, stop):
    evidence_codes = {label: index for index, label in enumerate(labels["evidence"])}
    return {
        "occurrence_structures": result.occurrence_structures,
        "occurrence_evidence": np.asarray([
            evidence_codes[result.evidence_labels[code]]
            for code in result.occurrence_evidence
        ], dtype=np.int32),
        "occurrence_image_offsets": (
            np.asarray([0], dtype=np.int64)
            if result.image_vectors is None and result.n_interactions == 0
            else result.occurrence_image_offsets
        ),
        "image_vectors": (
            np.empty((0, 3), dtype=np.int32)
            if result.image_vectors is None and result.n_interactions == 0
            else result.image_vectors
        ),
        "frame_offsets": np.searchsorted(
            result.occurrence_structures, np.arange(start, stop + 1), side="left"
        ).astype(np.int64),
        "occurrence_atom_count": np.fromiter(
            (len(np.unique(result._relation_atoms(relation)))
             for relation in result.occurrence_relations),
            dtype=np.int64, count=result.n_interactions,
        ),
        **{f"measure_{name}": values for name, values in result.measurements.items()},
    }


def _labels(records):
    return {
        "types": tuple(dict.fromkeys(row["interaction_type"] for row in records)),
        "roles": tuple(dict.fromkeys(
            participant["role"] for row in records
            for participant in row["participants"]
        )),
        "evidence": tuple(dict.fromkeys(row["evidence"] for row in records)),
    }


def _write_file(path, records, evaluated, n_frames, n_atoms, block_size, policy):
    labels = _labels(records)
    choices = []
    projected_descriptor_bytes = {"global": 0, "event": 0}
    postings = [[] for _ in range(n_atoms)]
    block_event_offsets = [0]
    with h5py.File(path, "w") as file:
        file.attrs["format"] = "molsysmt.interactions.block_probe"
        file.attrs["schema_version"] = 1
        file.attrs["metadata"] = json.dumps({
            "n_atoms": n_atoms, "n_structures": n_frames,
            "method": METHOD, "parameters": {"seed": 251},
            "source_id": "synthetic_contract", "measure_units": UNITS,
            "block_size": block_size,
        })
        string_dtype = h5py.string_dtype(encoding="utf-8")
        label_group = file.create_group("labels")
        for name, values in labels.items():
            label_group.create_dataset(
                name, data=np.asarray(values, dtype=string_dtype)
            )
        file.create_dataset(
            "evaluated_structure_indices",
            data=np.asarray(evaluated, dtype=np.int64), compression="gzip",
        )
        blocks = file.create_group("blocks")
        for start in range(0, n_frames, block_size):
            stop = min(start + block_size, n_frames)
            block_id = start // block_size
            rows = [row for row in records
                    if start <= row["structure_index"] < stop]
            coverage = [frame for frame in evaluated if start <= frame < stop]
            result = msm.Interactions.from_records(
                rows, n_atoms=n_atoms, n_structures=n_frames,
                evaluated_structure_indices=coverage, method=METHOD,
                measure_units=UNITS, parameters={"seed": 251},
                source_id="synthetic_contract",
            )
            descriptors = {
                mode: _descriptor_arrays(result, labels, mode)
                for mode in ("global", "event")
            }
            projected = {
                mode: sum(array.nbytes for array in arrays.values())
                for mode, arrays in descriptors.items()
            }
            for mode in projected:
                projected_descriptor_bytes[mode] += projected[mode]
            mode = (min(projected, key=projected.get)
                    if policy == "adaptive" else policy)
            choices.append(mode)
            block = blocks.create_group(str(block_id))
            block.attrs["scope"] = mode
            block.attrs["source_start"] = start
            block.attrs["source_stop"] = stop
            _write_arrays(block.create_group("common"),
                          _common_arrays(result, labels, start, stop))
            _write_arrays(block.create_group("descriptors"), descriptors[mode])
            atom_offsets, atom_occurrences, _ = _direct_postings(result)
            for atom in range(n_atoms):
                postings[atom].extend(
                    block_event_offsets[-1] + int(event)
                    for event in atom_occurrences[
                        atom_offsets[atom]:atom_offsets[atom + 1]
                    ]
                )
            block_event_offsets.append(
                block_event_offsets[-1] + result.n_interactions
            )
        atom_offsets = np.r_[0, np.cumsum([len(group) for group in postings])]
        index = file.create_group("index")
        _write_arrays(index, {
            "atom_offsets": _smallest_unsigned(atom_offsets),
            "atom_occurrences": _smallest_unsigned(
                [event for group in postings for event in group]
            ),
            "block_event_offsets": _smallest_unsigned(block_event_offsets),
        })
    with h5py.File(path, "r") as file:
        storage = []
        file.visititems(lambda _name, item: storage.append(item.id.get_storage_size())
                        if isinstance(item, h5py.Dataset) else None)
    file_bytes = path.stat().st_size
    return {
        "choices": choices,
        "projected_descriptor_bytes": projected_descriptor_bytes,
        "postings": sum(map(len, postings)),
        "file_bytes": file_bytes,
        "dataset_storage_bytes": sum(storage),
        "hdf_metadata_and_padding_bytes": file_bytes - sum(storage),
    }


def _read_block(block, labels):
    common = {name: dataset[:] for name, dataset in block["common"].items()}
    descriptors = {name: dataset[:] for name, dataset in block["descriptors"].items()}
    output = []
    for event in range(len(common["occurrence_structures"])):
        relation = (int(descriptors["occurrence_relations"][event])
                    if block.attrs["scope"] == "global" else event)
        if block.attrs["scope"] == "global":
            type_code = descriptors["relation_type_codes"][relation]
            part_offsets = descriptors["relation_participant_offsets"]
        else:
            type_code = descriptors["occurrence_type_codes"][relation]
            part_offsets = descriptors["occurrence_participant_offsets"]
        participants = []
        for part in range(int(part_offsets[relation]),
                          int(part_offsets[relation + 1])):
            first = int(descriptors["participant_atom_offsets"][part])
            last = int(descriptors["participant_atom_offsets"][part + 1])
            participants.append({
                "role": labels["roles"][int(descriptors["participant_role_codes"][part])],
                "atom_indices": descriptors["participant_atoms"][first:last].tolist(),
            })
        first = int(common["occurrence_image_offsets"][event])
        last = int(common["occurrence_image_offsets"][event + 1])
        output.append(_signature({
            "structure_index": common["occurrence_structures"][event],
            "interaction_type": labels["types"][int(type_code)],
            "participants": participants,
            "evidence": labels["evidence"][int(common["occurrence_evidence"][event])],
            "measurements": {name: common[f"measure_{name}"][event]
                             for name in UNITS},
            "images": common["image_vectors"][first:last],
        }))
    return output


def _verify_file(path, records, evaluated, n_atoms):
    with h5py.File(path, "r") as file:
        if file.attrs.get("format") != "molsysmt.interactions.block_probe":
            raise AssertionError("unexpected block file format")
        metadata = json.loads(file.attrs["metadata"])
        if metadata["method"] != METHOD or metadata["measure_units"] != UNITS:
            raise AssertionError("analysis metadata changed")
        coverage = file["evaluated_structure_indices"][:].tolist()
        labels = {name: file[f"labels/{name}"].asstr()[:]
                  for name in ("types", "roles", "evidence")}
        decoded = {}
        for name, block in file["blocks"].items():
            decoded[int(name)] = _read_block(block, labels)
        actual = Counter(signature for rows in decoded.values()
                         for signature in rows)
        if (coverage, actual) != expected(records, evaluated):
            raise AssertionError("block payload differs from full-field oracle")
        index = file["index"]
        offsets = index["atom_offsets"][:]
        event_ids = index["atom_occurrences"][:]
        block_offsets = index["block_event_offsets"][:]
        for atom in range(n_atoms):
            actual_postings = event_ids[
                offsets[atom]:offsets[atom + 1]
            ].tolist()
            expected_postings = [
                int(block_offsets[block]) + event
                for block, rows in sorted(decoded.items())
                for event, row in enumerate(rows)
                if any(atom in participant_atoms for _, participant_atoms
                       in row[2])
            ]
            if actual_postings != expected_postings:
                raise AssertionError(f"block atom postings differ for atom {atom}")
        return len(actual), len(event_ids)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=1000)
    parser.add_argument("--atoms", type=int, default=500)
    parser.add_argument("--per-frame", type=int, default=8)
    parser.add_argument("--block-size", type=int, default=100)
    parser.add_argument("--distribution", choices=("stable", "churn", "mixed"),
                        default="mixed")
    parser.add_argument("--switch-frame", type=int,
                        help="Use an unaligned stable-to-churn transition")
    args = parser.parse_args()
    if args.frames < 30 or args.atoms < 30 or args.block_size < 1:
        parser.error("frames and atoms must be >=30; block size must be positive")
    if args.switch_frame is not None:
        if args.distribution != "mixed" or not 0 < args.switch_frame < args.frames:
            parser.error("switch-frame requires mixed input and an interior frame")
        stable, evaluated = generate_fixture(
            args.frames, args.atoms, args.per_frame, "stable", 251
        )
        churn, churn_evaluated = generate_fixture(
            args.frames, args.atoms, args.per_frame, "churn", 251
        )
        if evaluated != churn_evaluated:
            raise AssertionError("phase fixtures have different evaluated coverage")
        records = ([row for row in stable
                    if row["structure_index"] < args.switch_frame]
                   + [row for row in churn
                      if row["structure_index"] >= args.switch_frame])
    else:
        records, evaluated = generate_fixture(
            args.frames, args.atoms, args.per_frame, args.distribution, 251
        )
    with tempfile.TemporaryDirectory() as directory:
        results = {}
        for policy in ("global", "event", "adaptive"):
            path = Path(directory) / f"{policy}.h5i"
            result = _write_file(
                path, records, evaluated, args.frames, args.atoms,
                args.block_size, policy,
            )
            checked_rows, checked_postings = _verify_file(
                path, records, evaluated, args.atoms
            )
            result["oracle_rows"] = checked_rows
            result["checked_postings"] = checked_postings
            results[policy] = result
        print(json.dumps({
            "platform": platform.platform(), "h5py": h5py.__version__,
            "frames": args.frames, "atoms": args.atoms,
            "per_frame": args.per_frame, "block_size": args.block_size,
            "distribution": args.distribution,
            "switch_frame": args.switch_frame,
            "evaluated_frames": len(evaluated), "occurrences": len(records),
            "results": results,
        }, indent=2))


if __name__ == "__main__":
    main()
