#!/usr/bin/env python3
"""Probe sparse result layouts with bundled pentalanine trajectory geometry.

This reproduces the Buch H-to-acceptor distance criterion using the same donor,
acceptor, and neighbor helpers. It handles frames with zero accepted bonds in
the benchmark adapter; it is not a substitute for the public detector output.
"""

from __future__ import annotations

import argparse
import json
import platform
import resource
import statistics
import time
from collections import Counter
from pathlib import Path

import numpy as np
from benchmark_interactions_temporal_complete import (
    _file_probe,
    build_runs,
    query_positions,
)
from benchmark_interactions_temporal_file_queries import compare_files

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def _records(path, n_frames, block_size):
    donors = msm.interactions.hbonds.get_donor_atoms(path)
    acceptors = msm.interactions.hbonds.get_acceptor_atoms(path)
    records = []
    n_donors = len(donors)
    for start in range(0, n_frames, block_size):
        frames = list(range(start, min(start + block_size, n_frames)))
        offsets, indices, distances = msm.structure.get_neighbors(
            path,
            selection=donors[:, 1],
            selection_2=acceptors,
            structure_indices=frames,
            threshold="2.3 angstroms",
            pbc=False,
            output_type="csr",
        )
        nanometers = puw.get_value(distances, to_unit="nanometers")
        for local, frame in enumerate(frames):
            for donor_position, (donor, hydrogen) in enumerate(donors):
                row = local * n_donors + donor_position
                for position in range(offsets[row], offsets[row + 1]):
                    acceptor = int(acceptors[indices[position]])
                    if donor == acceptor:
                        continue
                    records.append(
                        {
                            "structure_index": frame,
                            "interaction_type": "hbond",
                            "participants": [
                                {"role": "donor", "atom_indices": [int(donor)]},
                                {"role": "hydrogen", "atom_indices": [int(hydrogen)]},
                                {"role": "acceptor", "atom_indices": [acceptor]},
                            ],
                            "evidence": "observed_geometry",
                            "measurements": {"distance": float(nanometers[position])},
                            "images": [[0, 0, 0]] * 3,
                        }
                    )
    return records


def _signature(record):
    return (
        record["structure_index"],
        tuple(part["atom_indices"][0] for part in record["participants"]),
        round(record["measurements"]["distance"], 8),
    )


def _view_signatures(view):
    columns = view.to_dict()
    found = []
    for row, relation in enumerate(columns["relation_indices"]):
        participants = view.relation(relation)["participants"]
        found.append(
            (
                int(columns["structure_indices"][row]),
                tuple(int(part["atom_indices"][0]) for part in participants),
                round(float(columns["measurements"]["distance"][row]), 8),
            )
        )
    return columns["evaluated_structure_indices"].tolist(), Counter(found)


def _time_requests(requests):
    samples = []
    for call in requests:
        start = time.perf_counter_ns()
        call().to_dict()
        samples.append((time.perf_counter_ns() - start) / 1e6)
    return round(statistics.median(samples), 4)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=5000)
    parser.add_argument("--block-size", type=int, default=100)
    args = parser.parse_args()
    path = "molsysmt/data/h5msm/traj_pentalanine.h5msm"
    n_atoms, available = (
        int(value) for value in msm.get(path, n_atoms=True, n_structures=True)
    )
    if not 0 < args.frames <= available or args.block_size < 1:
        parser.error("frames must fit the trajectory and block size be positive")
    initial_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    start = time.perf_counter()
    records = _records(path, args.frames, args.block_size)
    detector_seconds = time.perf_counter() - start
    evaluated = list(range(args.frames))
    result = msm.Interactions.from_records(
        records,
        n_atoms=n_atoms,
        n_structures=args.frames,
        evaluated_structure_indices=evaluated,
        method="buch_h_acceptor_0.23_nm",
        measure_units={"distance": "nm"},
        parameters={"distance_threshold_nm": 0.23, "pbc": False},
        source_id=Path(path).name,
    )
    arrays = build_runs(result, 100)
    offsets = np.searchsorted(
        result.occurrence_structures, np.arange(args.frames + 1), side="left"
    )
    original_by_frame = {}
    for record in records:
        original_by_frame.setdefault(record["structure_index"], []).append(
            _signature(record)
        )
    checked = list(range(min(args.frames, 100)))
    checked.extend(range(100, args.frames, max(1, args.frames // 100)))
    for frame in dict.fromkeys(checked):
        selected = query_positions(arrays, frame, 100, len(result.relation_types))
        direct = np.arange(offsets[frame], offsets[frame + 1])
        if not np.array_equal(selected, direct):
            raise AssertionError(f"temporal lookup differs at frame {frame}")
        coverage, found = _view_signatures(result.query(structure_indices=[frame]))
        if coverage != [frame] or found != Counter(original_by_frame.get(frame, [])):
            raise AssertionError(f"full-result oracle differs at frame {frame}")
    frame_request = list(
        dict.fromkeys(
            [
                args.frames - 1,
                10,
                10,
                0,
                min(125, args.frames - 1),
                99,
            ]
        )
    )
    frame_request = [frame for frame in frame_request if frame < args.frames]
    coverage, found = _view_signatures(result.query(structure_indices=frame_request))
    frame_set = set(frame_request)
    if coverage != frame_request or found != Counter(
        _signature(row) for row in records if row["structure_index"] in frame_set
    ):
        raise AssertionError("nonconsecutive frame request differs")
    frequency = Counter(
        atom
        for row in records
        for part in row["participants"]
        for atom in part["atom_indices"]
    )
    hot_atom = frequency.most_common(1)[0][0]
    group = {
        hot_atom,
        *(atom for part in records[0]["participants"] for atom in part["atom_indices"]),
    }
    query_counts = {}
    for mode in ("incident", "internal", "cross"):
        _, found = _view_signatures(result.query(atom_indices=sorted(group), mode=mode))
        oracle = Counter()
        for row in records:
            atoms = {
                atom for part in row["participants"] for atom in part["atom_indices"]
            }
            incident = bool(atoms & group)
            internal = atoms <= group
            if (
                (mode == "incident" and incident)
                or (mode == "internal" and internal)
                or (mode == "cross" and incident and not internal)
            ):
                oracle[_signature(row)] += 1
        if found != oracle:
            raise AssertionError(f"real-data {mode} query differs")
        query_counts[mode] = sum(found.values())
    rng = np.random.default_rng(253)
    frame_calls = [
        lambda frame=int(frame): result.query(structure_indices=[frame])
        for frame in rng.integers(0, args.frames, size=100)
    ]
    atom_calls = [
        lambda atom=int(atom): result.query(atom_indices=[atom])
        for atom in rng.integers(0, n_atoms, size=100)
    ]
    # Build the lazy atom index before timing its warm query path.
    result.query(atom_indices=[hot_atom]).to_dict()
    query_ms = {
        "frame": _time_requests(frame_calls),
        "atom": _time_requests(atom_calls),
    }
    files = _file_probe(
        result,
        records,
        evaluated,
        arrays,
        offsets,
        query_callback=lambda normal, temporal: compare_files(
            normal,
            temporal,
            records,
            evaluated,
            n_atoms,
            args.frames,
        ),
    )
    frame_counts = np.bincount(result.occurrence_structures, minlength=args.frames)
    index_bytes = sum(
        value.nbytes for name, value in arrays.items() if name != "test_position_map"
    )
    frame_index_bytes = (
        offsets.nbytes
        + result.occurrence_structures.nbytes
        + result.occurrence_relations.nbytes
    )
    print(
        json.dumps(
            {
                "platform": platform.platform(),
                "source": path,
                "frames": args.frames,
                "atoms": n_atoms,
                "detector_seconds": round(detector_seconds, 3),
                "occurrences": len(records),
                "relations": len(result.relation_types),
                "runs": len(arrays["run_starts"]),
                "empty_evaluated_frames": int(np.count_nonzero(frame_counts == 0)),
                "max_per_frame": int(np.max(frame_counts)),
                "median_per_frame": float(statistics.median(frame_counts)),
                "raw_frame_index_bytes": frame_index_bytes,
                "raw_temporal_index_bytes": index_bytes,
                "sampled_oracle_checked_frames": len(set(checked)),
                "nonconsecutive_frame_request": frame_request,
                "hot_atom": hot_atom,
                "group_query_counts": query_counts,
                "warm_complete_query_median_ms": query_ms,
                "peak_rss_growth_after_import_kib": resource.getrusage(
                    resource.RUSAGE_SELF
                ).ru_maxrss
                - initial_rss,
                "file_probe": files,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
