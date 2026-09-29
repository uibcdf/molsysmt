#!/usr/bin/env python3
"""Bound the gain from fixed-role descriptor families on full-field fixtures.

This optimistic numeric bound excludes family schema strings and any codec
dispatch/index cost. It is a triage tool, not a file or query benchmark.
"""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import tempfile
import time
from collections import defaultdict
from pathlib import Path

import h5py
import numpy as np
from benchmark_interactions_adaptive_blocks import (
    _common_arrays,
    _descriptor_arrays,
    _labels,
)
from benchmark_interactions_contract import (
    METHOD,
    UNITS,
    _direct_postings,
    generate_fixture,
)

import molsysmt as msm


def _family_key(relation):
    return (
        relation["interaction_type"],
        tuple((part["role"], len(part["atom_indices"]))
              for part in relation["participants"]),
    )


def _vary_ring_sizes(records, n_atoms):
    """Create stable five/six/seven-member ring groups within one method."""
    transformed = []
    for record in records:
        if record["interaction_type"] != "pi_pi":
            transformed.append(record)
            continue
        participants = []
        occupied = {atom for part in record["participants"]
                    for atom in part["atom_indices"]}
        for part in record["participants"]:
            atoms = list(part["atom_indices"])
            target = 5 + atoms[0] % 3
            if target == 5:
                atoms.pop()
            elif target == 7:
                added = next(atom for atom in range(n_atoms)
                             if atom not in occupied)
                atoms.append(added)
                occupied.add(added)
            participants.append({**part, "atom_indices": atoms})
        transformed.append({**record, "participants": participants})
    return transformed


def _write_file(path, result, evaluated, labels, common, index,
                descriptors, specialized=None):
    with h5py.File(path, "w") as file:
        file.attrs["format"] = "molsysmt.interactions.specialized_probe"
        file.attrs["schema_version"] = 1
        file.attrs["mode"] = "specialized" if specialized else "global"
        file.attrs["metadata"] = json.dumps({
            "n_atoms": result.n_atoms, "n_structures": result.n_structures,
            "method": METHOD, "parameters": {"seed": 251},
            "source_id": "synthetic_contract", "measure_units": UNITS,
        })
        text_dtype = h5py.string_dtype(encoding="utf-8")
        label_group = file.create_group("labels")
        for name, values in labels.items():
            label_group.create_dataset(name,
                                       data=np.asarray(values, dtype=text_dtype))
        file.create_dataset("evaluated_structure_indices",
                            data=np.asarray(evaluated, dtype=np.int64),
                            compression="gzip")
        for group_name, arrays in (("common", common), ("index", index),
                                   ("descriptors", descriptors if specialized is None
                                    else specialized)):
            group = file.create_group(group_name)
            for name, array in arrays.items():
                group.create_dataset(
                    name, data=array,
                    compression="gzip" if array.size else None,
                )
    return path.stat().st_size


def _check_specialized_file(path, result, evaluated, labels, common, index,
                            family_names):
    with h5py.File(path, "r") as file:
        if json.loads(file.attrs["metadata"])["measure_units"] != UNITS:
            raise AssertionError("measure units changed")
        if file["evaluated_structure_indices"][:].tolist() != evaluated:
            raise AssertionError("evaluated coverage changed")
        for name, values in labels.items():
            if file[f"labels/{name}"].asstr()[:].tolist() != list(values):
                raise AssertionError(f"label table {name} changed")
        for section, arrays in (("common", common), ("index", index)):
            for name, expected_array in arrays.items():
                if not np.array_equal(file[f"{section}/{name}"][:], expected_array):
                    raise AssertionError(f"{section}/{name} changed")
        group = file["descriptors"]
        if not np.array_equal(group["occurrence_relations"][:],
                              result.occurrence_relations):
            raise AssertionError("occurrence relation IDs changed")
        kind_labels = file["labels/types"].asstr()[:]
        role_labels = file["labels/roles"].asstr()[:]
        kind_codes = group["family_kind_codes"][:]
        role_offsets = group["family_role_offsets"][:]
        role_codes = group["family_role_codes"][:]
        atom_lengths = group["family_atom_lengths"][:]
        stored_families = []
        for family_id, kind_code in enumerate(kind_codes):
            start, stop = role_offsets[family_id:family_id + 2]
            pattern = tuple((role_labels[int(role_codes[part])],
                             int(atom_lengths[part]))
                            for part in range(int(start), int(stop)))
            stored_families.append((kind_labels[int(kind_code)], pattern))
        if stored_families != family_names:
            raise AssertionError("family role schema changed")
        family_codes = group["relation_family"][:]
        locals_ = group["relation_local"][:]
        if len(family_codes) != len(result.relation_types):
            raise AssertionError("relation family map has wrong size")
        for relation_id in range(len(result.relation_types)):
            family_id = int(family_codes[relation_id])
            local_id = int(locals_[relation_id])
            kind, pattern = stored_families[family_id]
            values = group[f"family_atoms_{family_id}"][local_id].tolist()
            participants = []
            offset = 0
            for role, length in pattern:
                participants.append({"role": role,
                                     "atom_indices": values[offset:offset + length]})
                offset += length
            original = result.relation(relation_id)
            if (kind != original["interaction_type"]
                    or len(participants) != len(original["participants"])) or any(
                item["role"] != other["role"]
                or item["atom_indices"] != other["atom_indices"].tolist()
                for item, other in zip(participants, original["participants"])
            ):
                raise AssertionError(f"relation {relation_id} changed")


def _load_time(path, repeats):
    samples = []
    for _ in range(repeats):
        before = time.perf_counter_ns()
        with h5py.File(path, "r") as file:
            for section in ("common", "index", "descriptors"):
                for dataset in file[section].values():
                    dataset[:]
        samples.append((time.perf_counter_ns() - before) / 1e6)
    return round(statistics.median(samples), 3)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=1000)
    parser.add_argument("--distribution", choices=("stable", "churn", "mixed"),
                        default="mixed")
    parser.add_argument("--file-probe", action="store_true")
    parser.add_argument("--variable-groups", action="store_true")
    args = parser.parse_args()
    n_atoms = 500
    records, evaluated = generate_fixture(
        args.frames, n_atoms, 8, args.distribution, 251
    )
    if args.variable_groups:
        records = _vary_ring_sizes(records, n_atoms)
    result = msm.Interactions.from_records(
        records, n_atoms=n_atoms, n_structures=args.frames,
        evaluated_structure_indices=evaluated, method=METHOD,
        measure_units=UNITS, parameters={"seed": 251},
        source_id="synthetic_contract",
    )
    labels = _labels(records)
    descriptors = _descriptor_arrays(result, labels, "global")
    common = _common_arrays(result, labels, 0, args.frames)
    atom_offsets, atom_occurrences, _ = _direct_postings(result)
    index_bytes = atom_offsets.nbytes + atom_occurrences.nbytes
    numeric_total = (sum(array.nbytes for array in descriptors.values())
                     + sum(array.nbytes for array in common.values())
                     + index_bytes)
    families = defaultdict(list)
    n_relations = len(result.relation_types)
    for relation_id in range(n_relations):
        relation = result.relation(relation_id)
        key = _family_key(relation)
        families[key].append((relation_id, relation))
    family_names = sorted(families)
    family_start = np.r_[0, np.cumsum(
        [len(families[key]) for key in family_names]
    )].astype(np.uint32)
    family_of_relation = np.empty(n_relations, dtype=np.uint8)
    local_of_relation = np.empty(n_relations, dtype=np.uint32)
    fixed_atoms = []
    for family_id, key in enumerate(family_names):
        atom_rows = []
        for local_id, (relation_id, relation) in enumerate(families[key]):
            family_of_relation[relation_id] = family_id
            local_of_relation[relation_id] = local_id
            atom_rows.append([atom for part in relation["participants"]
                              for atom in part["atom_indices"]])
        fixed_atoms.append(np.asarray(atom_rows, dtype=result.participant_atoms.dtype))
    for relation_id in range(n_relations):
        family_id = int(family_of_relation[relation_id])
        local_id = int(local_of_relation[relation_id])
        relation = result.relation(relation_id)
        actual = fixed_atoms[family_id][local_id].tolist()
        expected = [atom for part in relation["participants"]
                    for atom in part["atom_indices"]]
        if actual != expected:
            raise AssertionError("specialized relation atoms changed")
    specialized_descriptor_bytes = (
        descriptors["occurrence_relations"].nbytes
        + sum(array.nbytes for array in fixed_atoms)
        + family_start.nbytes + family_of_relation.nbytes
        + local_of_relation.nbytes
    )
    general_descriptor_bytes = sum(array.nbytes for array in descriptors.values())
    optimistic_total = numeric_total - general_descriptor_bytes + specialized_descriptor_bytes
    file_result = None
    if args.file_probe:
        family_kind_codes = np.asarray([
            labels["types"].index(key[0]) for key in family_names
        ], dtype=np.uint16)
        schema_role_codes = []
        schema_atom_lengths = []
        schema_offsets = [0]
        for _, pattern in family_names:
            for role, length in pattern:
                schema_role_codes.append(labels["roles"].index(role))
                schema_atom_lengths.append(length)
            schema_offsets.append(len(schema_role_codes))
        specialized = {
            "occurrence_relations": descriptors["occurrence_relations"],
            "relation_family": family_of_relation,
            "relation_local": local_of_relation,
            "family_starts": family_start,
            "family_kind_codes": family_kind_codes,
            "family_role_offsets": np.asarray(schema_offsets, dtype=np.uint32),
            "family_role_codes": np.asarray(schema_role_codes, dtype=np.uint16),
            "family_atom_lengths": np.asarray(schema_atom_lengths, dtype=np.uint16),
            **{f"family_atoms_{index}": array
               for index, array in enumerate(fixed_atoms)},
        }
        index_arrays = {"atom_offsets": atom_offsets,
                        "atom_occurrences": atom_occurrences}
        with tempfile.TemporaryDirectory() as directory:
            global_path = Path(directory) / "global.h5i"
            family_path = Path(directory) / "families.h5i"
            global_bytes = _write_file(
                global_path, result, evaluated, labels, common,
                index_arrays, descriptors,
            )
            family_bytes = _write_file(
                family_path, result, evaluated, labels, common,
                index_arrays, descriptors, specialized,
            )
            _check_specialized_file(
                family_path, result, evaluated, labels, common,
                index_arrays, family_names,
            )
            file_result = {
                "global_file_bytes": global_bytes,
                "specialized_file_bytes": family_bytes,
                "specialized_file_saving_pct": round(
                    100 * (global_bytes - family_bytes) / global_bytes, 2
                ),
                "global_full_load_ms": _load_time(global_path, 5),
                "specialized_full_load_ms": _load_time(family_path, 5),
                "full_load_repeats": 5,
            }
    print(json.dumps({
        "platform": platform.platform(), "frames": args.frames,
        "distribution": args.distribution,
        "variable_groups": args.variable_groups,
        "occurrences": result.n_interactions,
        "relations": n_relations,
        "families": len(family_names),
        "family_counts": {str(key): len(families[key]) for key in family_names},
        "general_descriptor_bytes": general_descriptor_bytes,
        "optimistic_specialized_descriptor_bytes": specialized_descriptor_bytes,
        "complete_numeric_bytes_before": numeric_total,
        "optimistic_complete_numeric_bytes_after": optimistic_total,
        "optimistic_complete_saving_pct": round(
            100 * (numeric_total - optimistic_total) / numeric_total, 2
        ),
        "file_probe": file_result,
    }, indent=2))


if __name__ == "__main__":
    main()
