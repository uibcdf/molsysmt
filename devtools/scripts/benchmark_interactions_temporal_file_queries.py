#!/usr/bin/env python3
"""Compare warm complete HDF5 frame and atom reads in two sparse layouts."""

from __future__ import annotations

import argparse
import json
import statistics
import time
from collections import Counter

import h5py
import numpy as np
from benchmark_interactions_contract import METHOD, UNITS, generate_fixture
from benchmark_interactions_temporal_complete import (
    _file_probe,
    build_runs,
    query_positions,
)

import molsysmt as msm


def _signature(record):
    return (
        int(record["structure_index"]), record["interaction_type"],
        tuple((part["role"], tuple(int(atom) for atom in part["atom_indices"]))
              for part in record["participants"]),
        record["evidence"],
        tuple((name, round(float(value), 8))
              for name, value in sorted(record["measurements"].items())),
        tuple(tuple(int(value) for value in image) for image in record["images"]),
    )


class FileReader:
    def __init__(self, path, temporal):
        self.file = h5py.File(path, "r")
        self.temporal = temporal
        self.evaluated = self.file["evaluated_structure_indices"][:]
        self.ordinal = {int(frame): pos
                        for pos, frame in enumerate(self.evaluated)}
        self.labels = {name: self.file[f"labels/{name}"].asstr()[:]
                       for name in ("types", "roles", "evidence")}
        descriptors = {name: dataset[:] for name, dataset
                       in self.file["descriptors"].items()}
        self.relation_descriptor_raw_bytes = sum(
            value.nbytes for name, value in descriptors.items()
            if name != "occurrence_relations"
        )
        self.relations = []
        for relation, type_code in enumerate(descriptors["relation_type_codes"]):
            parts = []
            first = descriptors["relation_participant_offsets"][relation]
            last = descriptors["relation_participant_offsets"][relation + 1]
            for part in range(first, last):
                atom_first = descriptors["participant_atom_offsets"][part]
                atom_last = descriptors["participant_atom_offsets"][part + 1]
                parts.append((
                    self.labels["roles"][descriptors["participant_role_codes"][part]],
                    tuple(int(atom) for atom in descriptors["participant_atoms"][
                        atom_first:atom_last
                    ]),
                ))
            self.relations.append((self.labels["types"][type_code], tuple(parts)))
        if temporal:
            self.runs = {name: dataset[:] for name, dataset
                         in self.file["runs"].items()}
            self.n_relations = len(self.relations)
        else:
            self.frame_offsets = self.file["common/frame_offsets"][:]
        self.atom_offsets = self.file["index/atom_offsets"][:]
        self.index_bytes = sum(value.nbytes for value in (
            self.atom_offsets, self.evaluated,
            *(self.runs.values() if temporal else (self.frame_offsets,)),
        ))
        self.read_calls = 0
        self.logical_rows = 0

    def close(self):
        self.file.close()

    def _take(self, path, indices):
        indices = np.unique(np.asarray(indices, dtype=np.int64))
        if not len(indices):
            return {}
        dataset = self.file[path]
        first, last = int(indices[0]), int(indices[-1])
        if last - first + 1 <= 4 * len(indices):
            block = dataset[first:last + 1]
            values = (block[index - first] for index in indices)
            self.logical_rows += last - first + 1
        else:
            block = dataset[indices]
            values = iter(block)
            self.logical_rows += len(indices)
        self.read_calls += 1
        return dict(zip(indices, values))

    def _temporal_frame(self, position):
        starts = self.runs["run_payload_starts"]
        run = int(np.searchsorted(starts, position, side="right") - 1)
        delta = position - int(starts[run])
        start_ordinal = int(self.runs["run_starts"][run])
        first = int(self.runs["exception_offsets"][run])
        last = int(self.runs["exception_offsets"][run + 1])
        extras = 0
        for ex in range(first, last):
            ordinal = int(self.runs["exception_ordinals"][ex])
            first_position = ordinal - start_ordinal + extras
            count = int(self.runs["exception_extras"][ex]) + 1
            if delta < first_position:
                break
            if delta < first_position + count:
                return int(self.evaluated[ordinal]), run
            extras += count - 1
        return int(self.evaluated[start_ordinal + delta - extras]), run

    def _rows(self, positions, known_frame=None):
        positions = sorted(set(int(position) for position in positions))
        if not positions:
            return Counter()
        evidence = self._take("common/occurrence_evidence", positions)
        measure_names = tuple(self.file["common"].keys())
        measures = {
            name.removeprefix("measure_"): self._take(f"common/{name}", positions)
            for name in measure_names if name.startswith("measure_")
        }
        bounds = self._take("common/occurrence_image_offsets",
                            [item for position in positions
                             for item in (position, position + 1)])
        image_indices = sorted({image for position in positions
                                for image in range(int(bounds[position]),
                                                   int(bounds[position + 1]))})
        images = self._take("common/image_vectors", image_indices)
        if self.temporal:
            relation_ids = {}
            structures = {}
            for position in positions:
                frame, run = self._temporal_frame(position)
                relation_ids[position] = int(np.searchsorted(
                    self.runs["relation_offsets"], run, side="right") - 1)
                structures[position] = frame
        else:
            relation_ids = self._take("descriptors/occurrence_relations", positions)
            structures = (dict.fromkeys(positions, known_frame)
                          if known_frame is not None else
                          self._take("common/occurrence_structures", positions))
        output = Counter()
        for position in positions:
            kind, parts = self.relations[int(relation_ids[position])]
            output[(
                int(structures[position]), kind, parts,
                self.labels["evidence"][int(evidence[position])],
                tuple((name, round(float(values[position]), 8))
                      for name, values in sorted(measures.items())),
                tuple(tuple(int(value) for value in images[image])
                      for image in range(int(bounds[position]),
                                         int(bounds[position + 1]))),
            )] += 1
        return output

    def frame(self, frame):
        if frame not in self.ordinal:
            return [], Counter()
        if self.temporal:
            positions = query_positions(self.runs, self.ordinal[frame], 100,
                                        self.n_relations)
        else:
            positions = range(int(self.frame_offsets[frame]),
                              int(self.frame_offsets[frame + 1]))
        return [frame], self._rows(positions, frame)

    def atom(self, atom):
        first, last = self.atom_offsets[atom:atom + 2]
        positions = self.file["index/atom_occurrences"][first:last]
        return self.evaluated.tolist(), self._rows(positions)


def compare_files(normal_path, temporal_path, records, evaluated, n_atoms,
                  n_frames):
    rng = np.random.default_rng(254)
    frames = rng.choice(n_frames, size=min(40, n_frames), replace=False).tolist()
    frames.extend([0, 1, 2, n_frames - 1])
    atom_counts = Counter(
        atom for record in records for part in record["participants"]
        for atom in set(part["atom_indices"])
    )
    atoms = [atom for atom, _ in atom_counts.most_common(2)]
    atoms.extend(rng.choice(n_atoms, size=min(8, n_atoms), replace=False).tolist())
    readers = {"frame_major": FileReader(normal_path, False),
               "temporal": FileReader(temporal_path, True)}
    expected_frames = {frame: Counter(
        _signature(record) for record in records
        if record["structure_index"] == frame
    ) for frame in set(frames)}
    expected_atoms = {atom: Counter(
        _signature(record) for record in records
        if any(atom in part["atom_indices"] for part in record["participants"])
    ) for atom in set(atoms)}
    output = {}
    covered = set(evaluated)
    try:
        for name, reader in readers.items():
            frame_samples = []
            atom_samples = []
            for frame in frames:
                start = time.perf_counter_ns()
                found = reader.frame(frame)
                frame_samples.append((time.perf_counter_ns() - start) / 1e6)
                if found != ([frame] if frame in covered else [],
                             expected_frames[frame]):
                    raise AssertionError(
                        f"{name} frame {frame} differs: "
                        f"extra={list((found[1] - expected_frames[frame]).items())[:1]} "
                        f"missing={list((expected_frames[frame] - found[1]).items())[:1]}"
                    )
            for atom in atoms:
                start = time.perf_counter_ns()
                found = reader.atom(atom)
                atom_samples.append((time.perf_counter_ns() - start) / 1e6)
                if found != (evaluated, expected_atoms[atom]):
                    raise AssertionError(f"{name} atom {atom} differs")
            output[name] = {
                "frame_median_ms": round(statistics.median(frame_samples), 3),
                "atom_median_ms": round(statistics.median(atom_samples), 3),
                "index_and_coverage_cache_bytes": reader.index_bytes,
                "shared_relation_descriptor_raw_bytes":
                    reader.relation_descriptor_raw_bytes,
                "dataset_read_calls": reader.read_calls,
                "logical_rows_read": reader.logical_rows,
            }
    finally:
        for reader in readers.values():
            reader.close()
    return {"frames_checked": len(frames), "atoms_checked": len(atoms),
            "readers": output}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=1000)
    parser.add_argument("--distribution", choices=("stable", "mixed", "churn",
                                                 "persistent"), default="mixed")
    args = parser.parse_args()
    n_atoms = 500
    records, evaluated = generate_fixture(args.frames, n_atoms, 8,
                                          args.distribution, 251)
    result = msm.Interactions.from_records(
        records, n_atoms=n_atoms, n_structures=args.frames,
        evaluated_structure_indices=evaluated, method=METHOD,
        measure_units=UNITS, parameters={"seed": 251},
        source_id="synthetic_contract",
    )
    arrays = build_runs(result, 100)
    offsets = np.searchsorted(result.occurrence_structures,
                              np.arange(args.frames + 1), side="left")
    files = _file_probe(
        result, records, evaluated, arrays, offsets,
        query_callback=lambda normal, temporal: compare_files(
            normal, temporal, records, evaluated, n_atoms, args.frames,
        ),
    )
    print(json.dumps({"distribution": args.distribution,
                      "frames": args.frames, "file_probe": files}, indent=2))


if __name__ == "__main__":
    main()
