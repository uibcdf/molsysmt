#!/usr/bin/env python3
"""Compare complete synthetic interaction payloads under three sparse layouts.

This is an exploratory storage benchmark, not a detector or public API test.
All layouts carry the same relation roles, grouped atoms, evidence, distance,
periodic images, source maps, and evaluated-frame coverage. Optional indexes
are counted separately from the core payload. Run from the repository root.
"""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import tempfile
import time
from pathlib import Path

import h5py
import numpy as np

KINDS = ("hbond", "pi_pi", "disulfide_candidate", "four_body")
ROLES = ("donor", "hydrogen", "acceptor", "ring", "sulfur", "site")
EVIDENCE = ("observed_geometry", "declared_topology")
TEMPLATES = (
    (0, (0, 1, 2), (1, 1, 1)),
    (1, (3, 3), (6, 6)),
    (2, (4, 4), (1, 1)),
    (3, (5, 5, 5, 5), (1, 1, 1, 1)),
)


def iter_event_frames(n_frames, n_atoms, churn, duplicates=False, hot_atom=False):
    """Yield one evaluated frame at a time, including empty frames."""
    rng = np.random.default_rng(251)
    pool = []
    for template_index in range(400):
        kind, roles, sizes = TEMPLATES[template_index % len(TEMPLATES)]
        use_hot = hot_atom and template_index % 2 == 0
        chosen = rng.choice(
            n_atoms - 1 if use_hot else n_atoms,
            size=sum(sizes), replace=False,
        )
        if use_hot:
            chosen += 1
            chosen[0] = 0
        cursor = 0
        participants = []
        for role, size in zip(roles, sizes):
            participants.append((role, tuple(int(x) for x in chosen[cursor:cursor + size])))
            cursor += size
        pool.append((kind, tuple(participants)))
    counts = rng.integers(5, 16, size=n_frames)
    counts[::17] = 0
    for frame, count in enumerate(counts):
        events = []
        selected = rng.choice(len(pool), size=int(count), replace=False)
        for selection_index, template_index in enumerate(selected):
            key = pool[int(template_index)]
            if churn:
                kind, roles, sizes = TEMPLATES[int(template_index) % len(TEMPLATES)]
                use_hot = hot_atom and int(template_index) % 2 == 0
                chosen = rng.choice(
                    n_atoms - 1 if use_hot else n_atoms,
                    size=sum(sizes), replace=False,
                )
                if use_hot:
                    chosen += 1
                    chosen[0] = 0
                cursor = 0
                participants = []
                for role, size in zip(roles, sizes):
                    participants.append((role, tuple(int(x) for x in chosen[cursor:cursor + size])))
                    cursor += size
                key = (kind, tuple(participants))
            images = rng.integers(-1, 2, size=(len(key[1]), 3), dtype=np.int8)
            evidence = int(rng.integers(0, 2))
            distance = float(rng.uniform(0.1, 0.5))
            events.append((frame, key, evidence, distance, images))
            if duplicates and frame % 23 == 1 and selection_index == 0:
                other_images = images.copy()
                other_images[0, 0] = -1 if images[0, 0] == 1 else images[0, 0] + 1
                events.append((frame, key, evidence, distance + 0.01, other_images))
        yield events


def make_events(n_frames, n_atoms, churn, duplicates=False, hot_atom=False):
    """Generate the complete trajectory for in-memory layout comparisons."""
    return [event for frame in iter_event_frames(
        n_frames, n_atoms, churn, duplicates, hot_atom
    ) for event in frame]


def encode(events, n_frames, n_atoms, scope, block_size=100):
    """Encode an identical logical payload using global, block, or event scope."""
    canonical = {}
    relation_lookup = {}
    relation_types = []
    canonical_ids = []
    relation_participant_offsets = [0]
    participant_roles = []
    participant_atom_offsets = [0]
    participant_atoms = []
    occurrence_relations = []
    occurrence_evidence = []
    distances = []
    image_offsets = [0]
    image_vectors = []
    occurrence_counts = np.zeros(n_frames, dtype=np.int32)
    block_relation_counts = np.zeros(
        (n_frames + block_size - 1) // block_size, dtype=np.int32
    ) if scope == "block" else None
    for event_index, (frame, key, evidence, distance, images) in enumerate(events):
        global_id = canonical.setdefault(key, event_index)
        if scope == "global":
            scoped_key = key
        elif scope == "block":
            scoped_key = (frame // block_size, key)
        else:
            scoped_key = event_index
        relation = relation_lookup.get(scoped_key)
        if relation is None:
            relation = len(relation_types)
            relation_lookup[scoped_key] = relation
            if block_relation_counts is not None:
                block_relation_counts[frame // block_size] += 1
            kind, participants = key
            relation_types.append(kind)
            canonical_ids.append(global_id)
            for role, atoms in participants:
                participant_roles.append(role)
                participant_atoms.extend(atoms)
                participant_atom_offsets.append(len(participant_atoms))
            relation_participant_offsets.append(len(participant_roles))
        occurrence_relations.append(relation)
        occurrence_evidence.append(evidence)
        distances.append(distance)
        image_vectors.extend(images)
        image_offsets.append(len(image_vectors))
        occurrence_counts[frame] += 1
    frame_offsets = np.empty(n_frames + 1, dtype=np.int32)
    frame_offsets[0] = 0
    frame_offsets[1:] = np.cumsum(occurrence_counts, dtype=np.int32)
    arrays = {
        "evaluated_frames": np.arange(n_frames, dtype=np.int32),
        "source_atom_map": np.arange(n_atoms, dtype=np.int32),
        "source_frame_map": np.arange(n_frames, dtype=np.int32),
        "frame_offsets": frame_offsets,
        "event_id": np.arange(len(events), dtype=np.int32),
        "occurrence_evidence": np.asarray(occurrence_evidence, dtype=np.int8),
        "distance_nm": np.asarray(distances, dtype=np.float64),
        "image_offsets": np.asarray(image_offsets, dtype=np.int32),
        "image_vectors": np.asarray(image_vectors, dtype=np.int8).reshape(-1, 3),
        "relation_types": np.asarray(relation_types, dtype=np.int8),
        "relation_participant_offsets": np.asarray(
            relation_participant_offsets, dtype=np.int32
        ),
        "participant_roles": np.asarray(participant_roles, dtype=np.int8),
        "participant_atom_offsets": np.asarray(participant_atom_offsets, dtype=np.int32),
        "participant_atoms": np.asarray(participant_atoms, dtype=np.int32),
    }
    if scope != "event":
        arrays["occurrence_relations"] = np.asarray(occurrence_relations, dtype=np.int32)
    if scope == "block":
        arrays["canonical_relation_ids"] = np.asarray(canonical_ids, dtype=np.int32)
    elif scope == "event":
        repeated = np.flatnonzero(
            np.asarray(canonical_ids, dtype=np.int32) != arrays["event_id"]
        ).astype(np.int32)
        if 2 * len(repeated) < len(events):
            if len(repeated):
                arrays["duplicate_event_ids"] = repeated
                arrays["duplicate_canonical_ids"] = np.asarray(
                    canonical_ids, dtype=np.int32
                )[repeated]
        else:
            arrays["canonical_relation_ids"] = np.asarray(canonical_ids, dtype=np.int32)
    if block_relation_counts is not None:
        block_offsets = np.empty(len(block_relation_counts) + 1, dtype=np.int32)
        block_offsets[0] = 0
        block_offsets[1:] = np.cumsum(block_relation_counts, dtype=np.int32)
        arrays["block_relation_offsets"] = block_offsets
    return arrays


def event_relation(arrays, event):
    relations = arrays.get("occurrence_relations")
    return event if relations is None else relations[event]


def canonical_event_ids(arrays, scope):
    if scope == "global":
        relations = arrays["occurrence_relations"]
        first = np.full(len(arrays["relation_types"]), len(relations), dtype=np.int32)
        np.minimum.at(first, relations, arrays["event_id"])
        return first[relations]
    if scope == "block":
        return arrays["canonical_relation_ids"][arrays["occurrence_relations"]]
    if "canonical_relation_ids" in arrays:
        return arrays["canonical_relation_ids"]
    ids = arrays["event_id"].copy()
    if "duplicate_event_ids" in arrays:
        ids[arrays["duplicate_event_ids"]] = arrays["duplicate_canonical_ids"]
    return ids


def relation_atoms(arrays, relation):
    part_start = arrays["relation_participant_offsets"][relation]
    part_end = arrays["relation_participant_offsets"][relation + 1]
    atom_start = arrays["participant_atom_offsets"][part_start]
    atom_end = arrays["participant_atom_offsets"][part_end]
    return arrays["participant_atoms"][atom_start:atom_end]


def build_atom_index(arrays, n_atoms, scope):
    """Choose direct atom-event postings for event scope; otherwise two levels."""
    posting_atoms = []
    posting_ids = []
    if scope == "event":
        for event_id in range(len(arrays["event_id"])):
            relation = event_relation(arrays, event_id)
            atoms = np.unique(relation_atoms(arrays, relation))
            posting_atoms.extend(atoms)
            posting_ids.extend([event_id] * len(atoms))
    else:
        for relation in range(len(arrays["relation_types"])):
            atoms = np.unique(relation_atoms(arrays, relation))
            posting_atoms.extend(atoms)
            posting_ids.extend([relation] * len(atoms))
    posting_atoms = np.asarray(posting_atoms, dtype=np.int32)
    posting_ids = np.asarray(posting_ids, dtype=np.int32)
    order = np.argsort(posting_atoms, kind="stable")
    counts = np.bincount(posting_atoms, minlength=n_atoms)
    atom_offsets = np.empty(n_atoms + 1, dtype=np.int32)
    atom_offsets[0] = 0
    atom_offsets[1:] = np.cumsum(counts, dtype=np.int32)
    index = {"atom_offsets": atom_offsets, "atom_postings": posting_ids[order]}
    if scope != "event":
        relations = arrays["occurrence_relations"]
        order = np.argsort(relations, kind="stable").astype(np.int32)
        counts = np.bincount(relations, minlength=len(arrays["relation_types"]))
        relation_offsets = np.empty(len(counts) + 1, dtype=np.int32)
        relation_offsets[0] = 0
        relation_offsets[1:] = np.cumsum(counts, dtype=np.int32)
        index["relation_offsets"] = relation_offsets
        index["relation_postings"] = order
    return index


def query_frame(arrays, frame):
    offsets = arrays["frame_offsets"]
    return arrays["event_id"][offsets[frame]:offsets[frame + 1]]


def query_frames(arrays, frames):
    selected = list(dict.fromkeys(int(frame) for frame in frames))
    return np.concatenate([query_frame(arrays, frame) for frame in selected])


def query_atom(arrays, index, atom, scope):
    start = index["atom_offsets"][atom]
    end = index["atom_offsets"][atom + 1]
    postings = index["atom_postings"][start:end]
    if scope == "event":
        return postings
    offsets = index["relation_offsets"]
    events = index["relation_postings"]
    return np.sort(np.concatenate([
        events[offsets[relation]:offsets[relation + 1]]
        for relation in postings
    ])) if len(postings) else np.empty(0, dtype=np.int32)


def query_atom_frames(arrays, index, atom, frames, scope):
    events = query_atom(arrays, index, atom, scope)
    selected = list(dict.fromkeys(int(frame) for frame in frames))
    frame_offsets = arrays["frame_offsets"]
    return np.concatenate([
        events[(events >= frame_offsets[frame]) &
               (events < frame_offsets[frame + 1])]
        for frame in selected
    ])


def query_set(arrays, index, atoms, mode, scope):
    selection = np.unique(np.asarray(atoms, dtype=np.int32))
    if scope != "event":
        offsets = index["atom_offsets"]
        relation_groups = [
            index["atom_postings"][offsets[atom]:offsets[atom + 1]]
            for atom in selection
        ]
        relations = np.unique(np.concatenate(relation_groups)) if relation_groups else (
            np.empty(0, dtype=np.int32)
        )
        if mode != "incident":
            membership = set(selection.tolist())
            internal = np.asarray([
                all(int(atom) in membership for atom in relation_atoms(arrays, relation))
                for relation in relations
            ], dtype=bool)
            relations = relations[internal if mode == "internal" else ~internal]
        offsets = index["relation_offsets"]
        groups = [
            index["relation_postings"][offsets[relation]:offsets[relation + 1]]
            for relation in relations
        ]
        return np.sort(np.concatenate(groups)) if groups else np.empty(0, dtype=np.int32)
    candidates = np.unique(np.concatenate([
        query_atom(arrays, index, int(atom), scope) for atom in selection
    ])) if len(selection) else np.empty(0, dtype=np.int32)
    if mode == "incident":
        return candidates
    membership = set(selection.tolist())
    internal = np.asarray([
        all(int(atom) in membership for atom in relation_atoms(
            arrays, event_relation(arrays, event)
        )) for event in candidates
    ], dtype=bool)
    return candidates[internal if mode == "internal" else ~internal]


def relation_atom_cardinalities(arrays):
    return np.asarray([
        len(np.unique(relation_atoms(arrays, relation)))
        for relation in range(len(arrays["relation_types"]))
    ], dtype=np.int32)


def query_set_counted(arrays, index, atoms, mode, scope, cardinalities):
    selection = np.unique(np.asarray(atoms, dtype=np.int32))
    offsets = index["atom_offsets"]
    groups = [
        index["atom_postings"][offsets[atom]:offsets[atom + 1]]
        for atom in selection
    ]
    if not groups:
        return np.empty(0, dtype=np.int32)
    candidates, counts = np.unique(np.concatenate(groups), return_counts=True)
    if mode != "incident":
        if scope == "event":
            relations = arrays.get("occurrence_relations")
            required = cardinalities[
                candidates if relations is None else relations[candidates]
            ]
        else:
            required = cardinalities[candidates]
        internal = counts == required
        candidates = candidates[internal if mode == "internal" else ~internal]
    if scope == "event":
        return candidates.astype(np.int32, copy=False)
    relation_offsets = index["relation_offsets"]
    event_groups = [
        index["relation_postings"][
            relation_offsets[relation]:relation_offsets[relation + 1]
        ] for relation in candidates
    ]
    return np.sort(np.concatenate(event_groups)) if event_groups else (
        np.empty(0, dtype=np.int32)
    )


def payload_bytes(arrays):
    return sum(array.nbytes for array in arrays.values())


def time_queries(query, requests):
    if len(requests) == 0:
        return None
    query(requests[0])
    samples = []
    for request in requests:
        start = time.perf_counter_ns()
        query(request)
        samples.append((time.perf_counter_ns() - start) / 1e6)
    return {"median_ms": round(statistics.median(samples), 4),
            "p95_ms": round(sorted(samples)[int(0.95 * (len(samples) - 1))], 4)}


def benchmark_queries(arrays, index, scope, frames, atoms, frame_groups,
                      atom_groups, complete_groups, cardinalities):
    return {
        "frame_query": time_queries(
            lambda frame: query_frame(arrays, int(frame)), frames
        ),
        "four_frame_query": time_queries(
            lambda selected: query_frames(arrays, selected), frame_groups
        ),
        "atom_query": time_queries(
            lambda atom: query_atom(arrays, index, int(atom), scope), atoms
        ),
        "atom_four_frame_query": time_queries(
            lambda request: query_atom_frames(
                arrays, index, int(request[0]), request[1], scope
            ), list(zip(atoms, frame_groups))
        ),
        "five_atom_internal_query": time_queries(
            lambda group: query_set(arrays, index, group, "internal", scope),
            atom_groups,
        ),
        "complete_relation_internal_query": time_queries(
            lambda group: query_set(arrays, index, group, "internal", scope),
            complete_groups,
        ),
        "counted_five_atom_internal_query": time_queries(
            lambda group: query_set_counted(
                arrays, index, group, "internal", scope, cardinalities
            ), atom_groups,
        ),
        "counted_complete_relation_internal_query": time_queries(
            lambda group: query_set_counted(
                arrays, index, group, "internal", scope, cardinalities
            ), complete_groups,
        ),
    }


def save_arrays(path, arrays, scope, block_size):
    with h5py.File(path, "w") as file:
        file.attrs["method"] = "synthetic_layout_benchmark"
        file.attrs["measure_units"] = json.dumps({"distance_nm": "nm"})
        file.attrs["type_labels"] = json.dumps(KINDS)
        file.attrs["role_labels"] = json.dumps(ROLES)
        file.attrs["evidence_labels"] = json.dumps(EVIDENCE)
        file.attrs["scope"] = scope
        file.attrs["block_size"] = block_size
        file.attrs["canonical_encoding"] = (
            "full" if "canonical_relation_ids" in arrays else
            "exceptions" if "duplicate_event_ids" in arrays else "implicit"
        )
        file.attrs["occurrence_relations_implicit"] = (
            "occurrence_relations" not in arrays
        )
        for name, array in arrays.items():
            file.create_dataset(name, data=array,
                                compression="gzip" if array.size else None)


def check_lossless(arrays, events, n_frames):
    assert len(arrays["evaluated_frames"]) == n_frames
    assert len(arrays["event_id"]) == len(events)
    for event in (0, len(events) // 2, len(events) - 1):
        frame, key, evidence, distance, images = events[event]
        relation = event_relation(arrays, event)
        assert arrays["frame_offsets"][frame] <= event < arrays["frame_offsets"][frame + 1]
        assert arrays["relation_types"][relation] == key[0]
        part_start = arrays["relation_participant_offsets"][relation]
        part_end = arrays["relation_participant_offsets"][relation + 1]
        assert part_end - part_start == len(key[1])
        for offset, (role, atoms) in enumerate(key[1]):
            part = part_start + offset
            assert arrays["participant_roles"][part] == role
            first = arrays["participant_atom_offsets"][part]
            last = arrays["participant_atom_offsets"][part + 1]
            assert tuple(arrays["participant_atoms"][first:last]) == atoms
        assert arrays["occurrence_evidence"][event] == evidence
        assert arrays["distance_nm"][event] == distance
        first = arrays["image_offsets"][event]
        last = arrays["image_offsets"][event + 1]
        np.testing.assert_array_equal(arrays["image_vectors"][first:last], images)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=1000)
    parser.add_argument("--atoms", type=int, default=1000)
    parser.add_argument("--block-size", type=int, default=100)
    parser.add_argument("--churn", action="store_true")
    parser.add_argument("--duplicates", action="store_true")
    parser.add_argument("--hot-atom", action="store_true")
    args = parser.parse_args()
    if args.frames < 2 or args.atoms < 20 or args.block_size < 1:
        parser.error("frames >= 2, atoms >= 20, and block-size positive are required")
    events = make_events(
        args.frames, args.atoms, args.churn, args.duplicates, args.hot_atom
    )
    first_event_by_relation = {}
    expected_canonical_ids = np.asarray([
        first_event_by_relation.setdefault(event[1], event_id)
        for event_id, event in enumerate(events)
    ], dtype=np.int32)
    duplicate_events = sum(
        events[index][0] == events[index - 1][0]
        and events[index][1] == events[index - 1][1]
        for index in range(1, len(events))
    )
    if args.duplicates:
        assert duplicate_events > 0
    rng = np.random.default_rng(26)
    frames = rng.integers(0, args.frames, size=200)
    atoms = rng.integers(0, args.atoms, size=200)
    frame_groups = rng.integers(0, args.frames, size=(200, 4))
    atom_groups = rng.integers(0, args.atoms, size=(50, 5))
    complete_groups = [
        np.asarray(sorted({atom for _, member_atoms in events[event][1][1]
                           for atom in member_atoms}), dtype=np.int32)
        for event in np.linspace(0, len(events) - 1, 50, dtype=np.int32)
    ]
    result = {}
    reference = None
    for scope in ("global", "block", "event"):
        start = time.perf_counter()
        arrays = encode(events, args.frames, args.atoms, scope, args.block_size)
        build_s = time.perf_counter() - start
        np.testing.assert_array_equal(
            canonical_event_ids(arrays, scope), expected_canonical_ids
        )
        check_lossless(arrays, events, args.frames)
        start = time.perf_counter()
        index = build_atom_index(arrays, args.atoms, scope)
        index_s = time.perf_counter() - start
        start = time.perf_counter()
        cardinalities = relation_atom_cardinalities(arrays)
        cardinalities_s = time.perf_counter() - start
        for mode in ("incident", "internal", "cross"):
            for group in [*atom_groups[:3], *complete_groups[:3]]:
                np.testing.assert_array_equal(
                    query_set_counted(arrays, index, group, mode, scope,
                                      cardinalities),
                    query_set(arrays, index, group, mode, scope),
                )
        signatures = (
            tuple(query_frame(arrays, int(frame)).tolist() for frame in frames[:5]),
            tuple(query_atom(arrays, index, int(atom), scope).tolist()
                  for atom in atoms[:5]),
            tuple(query_set(arrays, index, group, mode, scope).tolist()
                  for mode in ("incident", "internal", "cross")
                  for group in [*atom_groups[:3], *complete_groups[:3]]),
        )
        if reference is None:
            reference = signatures
        else:
            assert signatures == reference, "layouts disagree on queries"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "interactions.h5i"
            start = time.perf_counter()
            save_arrays(path, arrays, scope, args.block_size)
            save_s = time.perf_counter() - start
            disk_bytes = path.stat().st_size
            with h5py.File(path, "r") as file:
                file_offsets = file["frame_offsets"][:]
                file_events = file["event_id"]
                start = time.perf_counter_ns()
                first_frame_ids = file_events[
                    file_offsets[int(frames[0])]:file_offsets[int(frames[0]) + 1]
                ]
                first_file_frame_ms = (time.perf_counter_ns() - start) / 1e6
                np.testing.assert_array_equal(
                    first_frame_ids, query_frame(arrays, int(frames[0]))
                )
                def read_file_frame(frame, dataset=file_events, offsets=file_offsets):
                    return dataset[offsets[int(frame)]:offsets[int(frame) + 1]]
                file_frame_query = time_queries(read_file_frame, frames)
            start = time.perf_counter()
            with h5py.File(path, "r") as file:
                loaded = {name: dataset[:] for name, dataset in file.items()}
            load_s = time.perf_counter() - start
            for name in arrays:
                np.testing.assert_array_equal(loaded[name], arrays[name])
        result[scope] = {
            "relations": len(arrays["relation_types"]),
            "core_bytes": payload_bytes(arrays),
            "atom_index_bytes": payload_bytes(index),
            "build_s": round(build_s, 3),
            "atom_index_build_s": round(index_s, 3),
            "hot_atom_occurrences": len(query_atom(arrays, index, 0, scope)),
            "hot_atom_query": time_queries(
                lambda _request, arrays=arrays, index=index, scope=scope: query_atom(
                    arrays, index, 0, scope
                ), frames,
            ),
            "cardinality_bytes": cardinalities.nbytes,
            "cardinality_build_s": round(cardinalities_s, 3),
            **benchmark_queries(arrays, index, scope, frames, atoms,
                                frame_groups, atom_groups, complete_groups,
                                cardinalities),
            "file_bytes": disk_bytes,
            "save_s": round(save_s, 3),
            "load_s": round(load_s, 3),
            "first_file_frame_ms": round(first_file_frame_ms, 4),
            "file_frame_query": file_frame_query,
        }
        if scope != "event":
            start = time.perf_counter()
            direct_index = build_atom_index(arrays, args.atoms, "event")
            direct_index_s = time.perf_counter() - start
            for atom in atoms[:5]:
                np.testing.assert_array_equal(
                    query_atom(arrays, direct_index, int(atom), "event"),
                    query_atom(arrays, index, int(atom), scope),
                )
            direct_timings = benchmark_queries(
                arrays, direct_index, "event", frames, atoms,
                frame_groups, atom_groups, complete_groups, cardinalities,
            )
            result[scope]["direct_atom_index_bytes"] = payload_bytes(direct_index)
            result[scope]["direct_atom_index_build_s"] = round(direct_index_s, 3)
            result[scope]["direct_hot_atom_query"] = time_queries(
                lambda _request, arrays=arrays, index=direct_index: query_atom(
                    arrays, index, 0, "event"
                ), frames,
            )
            result[scope]["direct_atom_query"] = direct_timings["atom_query"]
            result[scope]["direct_atom_four_frame_query"] = direct_timings[
                "atom_four_frame_query"
            ]
            result[scope]["direct_five_atom_internal_query"] = direct_timings[
                "five_atom_internal_query"
            ]
            result[scope]["direct_complete_relation_internal_query"] = direct_timings[
                "complete_relation_internal_query"
            ]
            result[scope]["direct_counted_complete_relation_internal_query"] = (
                direct_timings["counted_complete_relation_internal_query"]
            )
    cpu_info = Path("/proc/cpuinfo")
    cpu_model = next((line.split(":", 1)[1].strip()
                      for line in cpu_info.read_text().splitlines()
                      if line.startswith("model name")), None) if cpu_info.exists() else None
    print(json.dumps({
        "platform": platform.platform(), "python": platform.python_version(),
        "cpu_model": cpu_model, "numpy": np.__version__, "h5py": h5py.__version__,
        "frames": args.frames, "atoms": args.atoms, "events": len(events),
        "evaluated_empty_frames": int(sum(np.diff(
            result_arrays_frame_offsets(events, args.frames)
        ) == 0)),
        "block_size": args.block_size, "churn": args.churn,
        "hot_atom": args.hot_atom,
        "duplicate_events": duplicate_events,
        "comparison": result,
    }, indent=2))


def result_arrays_frame_offsets(events, n_frames):
    counts = np.bincount([event[0] for event in events], minlength=n_frames)
    return np.r_[0, np.cumsum(counts)]


if __name__ == "__main__":
    main()
