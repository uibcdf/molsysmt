#!/usr/bin/env python3
"""Compare exact temporal runs with frame-major full-result queries.

Runs use evaluated-structure ordinals and encode parallel-observation count
exceptions. The relation-major event-position map is test instrumentation:
a temporal file would reorder the complete occurrence payload instead.
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
    expected,
    generate_fixture,
    materialize,
)

import molsysmt as msm


def build_runs(result, block_size):
    evaluated = result.evaluated_structure_indices
    frame_to_ordinal = {int(frame): ordinal for ordinal, frame in enumerate(evaluated)}
    n_relations = len(result.relation_types)
    by_relation = [defaultdict(list) for _ in range(n_relations)]
    for position, (frame, relation) in enumerate(
        zip(result.occurrence_structures, result.occurrence_relations)
    ):
        by_relation[int(relation)][frame_to_ordinal[int(frame)]].append(position)
    relation_offsets = [0]
    starts, ends, payload_starts = [], [], []
    exception_offsets = [0]
    exception_ordinals, exception_extras = [], []
    relation_major_positions = []
    n_blocks = (len(evaluated) + block_size - 1) // block_size
    candidates = np.zeros((n_blocks, n_relations), dtype=np.bool_)
    for relation, frames in enumerate(by_relation):
        ordinals = sorted(frames)
        if ordinals:
            run_start = ordinals[0]
            current = []
            for ordinal in ordinals:
                if current and ordinal != current[-1] + 1:
                    _emit_run(
                        relation,
                        run_start,
                        current,
                        frames,
                        starts,
                        ends,
                        payload_starts,
                        exception_offsets,
                        exception_ordinals,
                        exception_extras,
                        relation_major_positions,
                        candidates,
                        block_size,
                    )
                    run_start = ordinal
                    current = []
                current.append(ordinal)
            _emit_run(
                relation,
                run_start,
                current,
                frames,
                starts,
                ends,
                payload_starts,
                exception_offsets,
                exception_ordinals,
                exception_extras,
                relation_major_positions,
                candidates,
                block_size,
            )
        relation_offsets.append(len(starts))
    arrays = {
        "relation_offsets": np.asarray(relation_offsets, dtype=np.int64),
        "run_starts": np.asarray(starts, dtype=np.int32),
        "run_ends": np.asarray(ends, dtype=np.int32),
        "run_payload_starts": np.asarray(payload_starts, dtype=np.int64),
        "exception_offsets": np.asarray(exception_offsets, dtype=np.int64),
        "exception_ordinals": np.asarray(exception_ordinals, dtype=np.int32),
        "exception_extras": np.asarray(exception_extras, dtype=np.int32),
        "candidates": np.packbits(candidates, axis=1, bitorder="little"),
        "test_position_map": np.asarray(relation_major_positions, dtype=np.int64),
    }
    if (
        len(arrays["test_position_map"]) != result.n_interactions
        or len(np.unique(arrays["test_position_map"])) != result.n_interactions
    ):
        raise AssertionError("temporal payload permutation lost an observation")
    return arrays


def _emit_run(
    relation,
    start,
    ordinals,
    frames,
    starts,
    ends,
    payload_starts,
    exception_offsets,
    exception_ordinals,
    exception_extras,
    positions,
    candidates,
    block_size,
):
    starts.append(start)
    ends.append(ordinals[-1] + 1)
    payload_starts.append(len(positions))
    for ordinal in ordinals:
        group = frames[ordinal]
        positions.extend(group)
        if len(group) > 1:
            exception_ordinals.append(ordinal)
            exception_extras.append(len(group) - 1)
    exception_offsets.append(len(exception_ordinals))
    candidates[start // block_size : ordinals[-1] // block_size + 1, relation] = True


def query_positions(arrays, ordinal, block_size, n_relations):
    if ordinal is None:
        return np.empty(0, dtype=np.int64)
    bits = np.unpackbits(
        arrays["candidates"][ordinal // block_size], bitorder="little"
    )[:n_relations]
    positions = []
    for relation in np.flatnonzero(bits):
        first = int(arrays["relation_offsets"][relation])
        last = int(arrays["relation_offsets"][relation + 1])
        if first == last:
            continue
        run = (
            first
            + int(
                np.searchsorted(arrays["run_starts"][first:last], ordinal, side="right")
            )
            - 1
        )
        if run < first or ordinal >= arrays["run_ends"][run]:
            continue
        ex_first = int(arrays["exception_offsets"][run])
        ex_last = int(arrays["exception_offsets"][run + 1])
        ex_ordinals = arrays["exception_ordinals"][ex_first:ex_last]
        before = int(np.searchsorted(ex_ordinals, ordinal, side="left"))
        extras_before = int(
            np.sum(arrays["exception_extras"][ex_first : ex_first + before])
        )
        count = 1
        if before < len(ex_ordinals) and ex_ordinals[before] == ordinal:
            count += int(arrays["exception_extras"][ex_first + before])
        row = int(
            arrays["run_payload_starts"][run]
            + ordinal
            - arrays["run_starts"][run]
            + extras_before
        )
        if "test_position_map" in arrays:
            positions.extend(arrays["test_position_map"][row : row + count])
        else:
            positions.extend(range(row, row + count))
    return np.asarray(sorted(positions), dtype=np.int64)


def _time_queries(query, frames):
    samples = []
    for frame in frames:
        start = time.perf_counter_ns()
        query(frame)
        samples.append((time.perf_counter_ns() - start) / 1e6)
    return {
        "median_ms": round(statistics.median(samples), 4),
        "p95_ms": round(float(np.percentile(samples, 95)), 4),
    }


def _write_probe_file(
    path, result, evaluated, labels, common, index, descriptors, run_index=None
):
    with h5py.File(path, "w") as file:
        file.attrs["format"] = "molsysmt.interactions.temporal_probe"
        file.attrs["schema_version"] = 1
        file.attrs["metadata"] = json.dumps(
            {
                "n_atoms": result.n_atoms,
                "n_structures": result.n_structures,
                "method": result.method,
                "parameters": result.parameters,
                "source_id": result.source_id,
                "measure_units": result.measure_units,
            }
        )
        text_dtype = h5py.string_dtype(encoding="utf-8")
        group = file.create_group("labels")
        for name, values in labels.items():
            group.create_dataset(name, data=np.asarray(values, dtype=text_dtype))
        file.create_dataset(
            "evaluated_structure_indices",
            data=np.asarray(evaluated, dtype=np.int64),
            compression="gzip",
        )
        sections = {"common": common, "index": index, "descriptors": descriptors}
        if run_index is not None:
            sections["runs"] = run_index
        for name, arrays in sections.items():
            group = file.create_group(name)
            for key, value in arrays.items():
                group.create_dataset(
                    key, data=value, compression="gzip" if value.size else None
                )
    with h5py.File(path, "r") as file:
        if json.loads(file.attrs["metadata"])["measure_units"] != result.measure_units:
            raise AssertionError("file metadata changed")
        if file["evaluated_structure_indices"][:].tolist() != evaluated:
            raise AssertionError("file coverage changed")
        for section, expected_arrays in sections.items():
            for name, expected_array in expected_arrays.items():
                if not np.array_equal(file[f"{section}/{name}"][:], expected_array):
                    raise AssertionError(f"file {section}/{name} changed")
    return path.stat().st_size


def _file_probe(result, records, evaluated, arrays, frame_offsets, query_callback=None):
    labels = _labels(records)
    common = _common_arrays(result, labels, 0, result.n_structures)
    descriptors = _descriptor_arrays(result, labels, "global")
    atom_offsets, atom_occurrences, _ = _direct_postings(result)
    normal_index = {"atom_offsets": atom_offsets, "atom_occurrences": atom_occurrences}
    order = arrays["test_position_map"]
    inverse = np.empty(len(order), dtype=np.int64)
    inverse[order] = np.arange(len(order))
    temporal_common = {
        name: value[order]
        for name, value in common.items()
        if name
        not in (
            "occurrence_structures",
            "frame_offsets",
            "occurrence_image_offsets",
            "image_vectors",
        )
    }
    old_offsets = common["occurrence_image_offsets"]
    sizes = np.diff(old_offsets)[order]
    temporal_common["occurrence_image_offsets"] = np.r_[
        0, np.cumsum(sizes, dtype=np.int64)
    ]
    temporal_common["image_vectors"] = np.concatenate(
        [
            common["image_vectors"][old_offsets[pos] : old_offsets[pos + 1]]
            for pos in order
        ]
    )
    temporal_descriptors = {
        name: value
        for name, value in descriptors.items()
        if name != "occurrence_relations"
    }
    temporal_index = {
        "atom_offsets": atom_offsets,
        "atom_occurrences": inverse[atom_occurrences],
    }
    run_index = {
        name: value for name, value in arrays.items() if name != "test_position_map"
    }
    if not np.array_equal(common["frame_offsets"], frame_offsets):
        raise AssertionError("frame offsets changed")
    for name, value in common.items():
        if name in (
            "occurrence_structures",
            "frame_offsets",
            "occurrence_image_offsets",
            "image_vectors",
        ):
            continue
        if not np.array_equal(temporal_common[name][inverse], value):
            raise AssertionError(f"temporal {name} permutation changed")
    new_offsets = temporal_common["occurrence_image_offsets"]
    for original in range(result.n_interactions):
        moved = inverse[original]
        if not np.array_equal(
            temporal_common["image_vectors"][
                new_offsets[moved] : new_offsets[moved + 1]
            ],
            common["image_vectors"][old_offsets[original] : old_offsets[original + 1]],
        ):
            raise AssertionError(f"temporal images changed at {original}")
    if not np.array_equal(order[temporal_index["atom_occurrences"]], atom_occurrences):
        raise AssertionError("temporal atom postings changed")
    with tempfile.TemporaryDirectory() as directory:
        normal = Path(directory) / "frame.h5i"
        temporal = Path(directory) / "temporal.h5i"
        normal_bytes = _write_probe_file(
            normal,
            result,
            evaluated,
            labels,
            common,
            normal_index,
            descriptors,
        )
        temporal_bytes = _write_probe_file(
            temporal,
            result,
            evaluated,
            labels,
            temporal_common,
            temporal_index,
            temporal_descriptors,
            run_index,
        )
        output = {
            "frame_major_file_bytes": normal_bytes,
            "temporal_file_bytes": temporal_bytes,
            "temporal_file_saving_pct": round(
                100 * (normal_bytes - temporal_bytes) / normal_bytes, 2
            ),
        }
        if query_callback is not None:
            output["file_queries"] = query_callback(normal, temporal)
        return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=1000)
    parser.add_argument(
        "--distribution",
        choices=("stable", "churn", "mixed", "persistent"),
        default="persistent",
    )
    parser.add_argument("--block-size", type=int, default=100)
    parser.add_argument("--file-probe", action="store_true")
    args = parser.parse_args()
    n_atoms = 500
    records, evaluated = generate_fixture(
        args.frames, n_atoms, 8, args.distribution, 251
    )
    result = msm.Interactions.from_records(
        records,
        n_atoms=n_atoms,
        n_structures=args.frames,
        evaluated_structure_indices=evaluated,
        method=METHOD,
        measure_units=UNITS,
        parameters={"seed": 251},
        source_id="synthetic_contract",
    )
    arrays = build_runs(result, args.block_size)
    ordinal_by_frame = {frame: ordinal for ordinal, frame in enumerate(evaluated)}
    frame_offsets = np.searchsorted(
        result.occurrence_structures, np.arange(args.frames + 1), side="left"
    ).astype(np.int64)
    rng = np.random.default_rng(252)
    sample_frames = rng.choice(
        args.frames, size=min(200, args.frames), replace=False
    ).tolist()
    sample_frames.extend([0, 1, 2, args.frames - 1])

    def direct_positions(frame):
        if frame not in ordinal_by_frame:
            return np.empty(0, dtype=np.int64)
        return np.arange(frame_offsets[frame], frame_offsets[frame + 1])

    def temporal_positions(frame):
        return query_positions(
            arrays,
            ordinal_by_frame.get(frame),
            args.block_size,
            len(result.relation_types),
        )

    def complete(frame, locator):
        coverage = [frame] if frame in ordinal_by_frame else []
        return materialize(result._view(locator(frame), coverage))

    for frame in sample_frames:
        direct = direct_positions(frame)
        temporal = temporal_positions(frame)
        if not np.array_equal(direct, temporal):
            raise AssertionError(f"temporal event positions differ at {frame}")
        oracle = expected(records, evaluated, frames=[frame])
        if complete(frame, temporal_positions) != oracle:
            raise AssertionError(f"temporal full result differs at {frame}")
    index_only = {
        "frame_major": _time_queries(direct_positions, sample_frames),
        "temporal": _time_queries(temporal_positions, sample_frames),
    }
    complete_queries = {
        "frame_major": _time_queries(
            lambda frame: complete(frame, direct_positions), sample_frames
        ),
        "temporal": _time_queries(
            lambda frame: complete(frame, temporal_positions), sample_frames
        ),
    }
    index_arrays = {
        name: array for name, array in arrays.items() if name != "test_position_map"
    }
    temporal_bytes = sum(array.nbytes for array in index_arrays.values())
    frame_major_bytes = (
        frame_offsets.nbytes
        + result.occurrence_structures.nbytes
        + result.occurrence_relations.nbytes
    )
    file_result = (
        _file_probe(result, records, evaluated, arrays, frame_offsets)
        if args.file_probe
        else None
    )
    print(
        json.dumps(
            {
                "platform": platform.platform(),
                "distribution": args.distribution,
                "frames": args.frames,
                "atoms": n_atoms,
                "evaluated_frames": len(evaluated),
                "occurrences": result.n_interactions,
                "relations": len(result.relation_types),
                "runs": len(arrays["run_starts"]),
                "duplicate_count_exceptions": len(arrays["exception_ordinals"]),
                "frame_major_index_bytes": frame_major_bytes,
                "temporal_index_bytes": temporal_bytes,
                "temporal_test_position_map_bytes_excluded": arrays[
                    "test_position_map"
                ].nbytes,
                "sampled_checked_frames": len(sample_frames),
                "index_only_query": index_only,
                "complete_query": complete_queries,
                "file_probe": file_result,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
