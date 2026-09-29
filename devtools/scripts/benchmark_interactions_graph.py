#!/usr/bin/env python3
"""Compare multilayer graph and columnar encodings of semantic interactions.

Run each mode in a fresh process. The source event list remains alive in every
run, so RSS differences estimate representation costs over a common baseline.
This is an exploratory comparison, not a proposed public graph API.
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import time

import networkx as nx
import numpy as np
from benchmark_interactions_file_backed import event_signature, source_signature
from benchmark_interactions_layouts import (
    build_atom_index,
    encode,
    make_events,
    payload_bytes,
)
from benchmark_interactions_layouts import (
    query_atom as query_atom_columnar,
)


def resident_bytes():
    with open("/proc/self/statm", encoding="utf-8") as stream:
        return int(stream.read().split()[1]) * os.sysconf("SC_PAGE_SIZE")


def high_water_bytes():
    with open("/proc/self/status", encoding="utf-8") as stream:
        for line in stream:
            if line.startswith("VmHWM:"):
                return int(line.split()[1]) * 1024
    raise RuntimeError("VmHWM is unavailable on this platform")


def image_key(image):
    return tuple(tuple(int(x) for x in vector) for vector in image)


def add_participants(graph, relation_node, participants, prefix):
    for part_index, (role, atoms) in enumerate(participants):
        part_node = (prefix, relation_node[1], part_index)
        graph.add_node(part_node, role=role)
        graph.add_edge(relation_node, part_node)
        for atom_position, atom in enumerate(atoms):
            graph.add_edge(part_node, int(atom), ordinal=atom_position)


def build_layers(events, n_frames, n_atoms):
    graphs = [nx.MultiGraph(frame_index=frame, n_atoms=n_atoms, n_occurrences=0)
              for frame in range(n_frames)]
    atom_postings = [[] for _ in range(n_atoms)]
    local_counts = np.zeros(n_frames, dtype=np.int32)
    for frame, (kind, participants), evidence, distance, image in events:
        local = int(local_counts[frame])
        local_counts[frame] += 1
        occurrence = ("occ", local)
        graph = graphs[frame]
        graph.graph["n_occurrences"] += 1
        graph.add_node(occurrence, kind=kind, evidence=evidence,
                       distance_nm=distance, image=image_key(image))
        add_participants(graph, occurrence, participants, "part")
        for atom in {int(atom) for _, atoms in participants for atom in atoms}:
            atom_postings[atom].append((frame, local))
    return graphs, atom_postings


def build_shared(events, n_frames, n_atoms):
    graph = nx.MultiGraph(n_frames=n_frames, n_atoms=n_atoms)
    graph.add_nodes_from(("frame", frame) for frame in range(n_frames))
    relation_lookup = {}
    for event, (frame, key, evidence, distance, image) in enumerate(events):
        relation = relation_lookup.get(key)
        if relation is None:
            relation = len(relation_lookup)
            relation_lookup[key] = relation
            relation_node = ("relation", relation)
            kind, participants = key
            graph.add_node(relation_node, kind=kind)
            add_participants(graph, relation_node, participants, "part")
        else:
            relation_node = ("relation", relation)
        occurrence = ("occ", event)
        graph.add_node(occurrence, frame_index=frame, evidence=evidence,
                       distance_nm=distance, image=image_key(image))
        graph.add_edge(("frame", frame), occurrence)
        graph.add_edge(occurrence, relation_node)
    return graph


def participant_signature(graph, relation_node, prefix):
    participant_nodes = sorted(
        neighbor for neighbor in graph.neighbors(relation_node)
        if isinstance(neighbor, tuple) and neighbor[0] == prefix
    )
    participants = []
    for part_node in participant_nodes:
        ordered_atoms = sorted(
            (int(data["ordinal"]), int(atom))
            for atom in graph.neighbors(part_node) if isinstance(atom, int)
            for data in graph[part_node][atom].values()
        )
        participants.append((
            int(graph.nodes[part_node]["role"]),
            tuple(atom for _, atom in ordered_atoms),
        ))
    return tuple(participants)


def layer_signature(graph, frame, local):
    occurrence = ("occ", local)
    attributes = graph.nodes[occurrence]
    return (
        frame, int(attributes["kind"]),
        participant_signature(graph, occurrence, "part"),
        int(attributes["evidence"]), float(attributes["distance_nm"]),
        attributes["image"],
    )


def shared_signature(graph, event):
    occurrence = ("occ", event)
    attributes = graph.nodes[occurrence]
    relation = next(
        neighbor for neighbor in graph.neighbors(occurrence)
        if neighbor[0] == "relation"
    )
    return (
        int(attributes["frame_index"]), int(graph.nodes[relation]["kind"]),
        participant_signature(graph, relation, "part"),
        int(attributes["evidence"]), float(attributes["distance_nm"]),
        attributes["image"],
    )


def graph_queries(mode, result, n_frames):
    if mode == "layers":
        graphs, atom_postings = result

        def frame_query(frame):
            graph = graphs[frame]
            return [layer_signature(graph, frame, local)
                    for local in range(graph.graph["n_occurrences"])]

        def atom_query(atom):
            return [layer_signature(graphs[frame], frame, local)
                    for frame, local in atom_postings[atom]]

        return frame_query, atom_query

    graph = result

    def frame_query(frame):
        events = sorted(node[1] for node in graph.neighbors(("frame", frame)))
        return [shared_signature(graph, event) for event in events]

    def atom_query(atom):
        if atom not in graph:
            return []
        events = set()
        for part in graph.neighbors(atom):
            for relation in graph.neighbors(part):
                if isinstance(relation, tuple) and relation[0] == "relation":
                    events.update(node[1] for node in graph.neighbors(relation)
                                  if isinstance(node, tuple) and node[0] == "occ")
        return [shared_signature(graph, event) for event in sorted(events)]

    return frame_query, atom_query


def columnar_queries(events, n_frames, n_atoms, scope):
    arrays = encode(events, n_frames, n_atoms, scope)
    index = build_atom_index(arrays, n_atoms, "event")

    def frame_query(frame):
        first = int(arrays["frame_offsets"][frame])
        last = int(arrays["frame_offsets"][frame + 1])
        return [event_signature(arrays, event, frame) for event in range(first, last)]

    def atom_query(atom):
        events = query_atom_columnar(arrays, index, atom, "event")
        return [event_signature(
            arrays, int(event),
            int(np.searchsorted(arrays["frame_offsets"], event, side="right") - 1),
        ) for event in events]

    return (arrays, index), frame_query, atom_query


def timed(query, requests):
    samples = []
    for request in requests:
        start = time.perf_counter_ns()
        query(int(request))
        samples.append((time.perf_counter_ns() - start) / 1e6)
    return {
        "median_ms": round(statistics.median(samples), 4),
        "p95_ms": round(sorted(samples)[int(0.95 * (len(samples) - 1))], 4),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("layers", "shared", "columnar_global",
                                            "columnar_event"), required=True)
    parser.add_argument("--frames", type=int, default=1000)
    parser.add_argument("--atoms", type=int, default=1000)
    parser.add_argument("--churn", action="store_true")
    parser.add_argument("--duplicates", action="store_true")
    args = parser.parse_args()
    if args.frames < 2 or args.atoms < 20:
        parser.error("frames >= 2 and atoms >= 20 are required")
    events = make_events(args.frames, args.atoms, args.churn, args.duplicates)
    baseline_rss = resident_bytes()
    start = time.perf_counter()
    if args.mode.startswith("columnar"):
        scope = args.mode.removeprefix("columnar_")
        result, frame_query, atom_query = columnar_queries(
            events, args.frames, args.atoms, scope
        )
        numeric_bytes = payload_bytes(result[0]) + payload_bytes(result[1])
    else:
        result = (build_layers(events, args.frames, args.atoms) if args.mode == "layers"
                  else build_shared(events, args.frames, args.atoms))
        frame_query, atom_query = graph_queries(args.mode, result, args.frames)
        numeric_bytes = None
    build_s = time.perf_counter() - start
    after_rss = resident_bytes()
    rng = np.random.default_rng(29)
    frames = [0, 1, min(17, args.frames - 1), args.frames - 1]
    frames.extend(int(x) for x in rng.integers(0, args.frames, size=30))
    atoms = [0, 1, args.atoms // 2]
    atoms.extend(int(x) for x in rng.integers(0, args.atoms, size=10))
    expected_frames = {frame: [] for frame in frames}
    expected_atoms = {atom: [] for atom in atoms}
    for event in events:
        frame, key = event[:2]
        signature = source_signature(event)
        if frame in expected_frames:
            expected_frames[frame].append(signature)
        involved = {atom for _, members in key[1] for atom in members}
        for atom in involved & expected_atoms.keys():
            expected_atoms[atom].append(signature)
    for frame, expected in expected_frames.items():
        assert frame_query(frame) == expected
    for atom, expected in expected_atoms.items():
        assert atom_query(atom) == expected
    output = {
        "config": vars(args),
        "events": len(events),
        "evaluated_empty_frames": int(np.count_nonzero(
            np.bincount([event[0] for event in events], minlength=args.frames) == 0
        )),
        "build_s": round(build_s, 3),
        "baseline_rss_bytes": baseline_rss,
        "after_build_rss_bytes": after_rss,
        "incremental_rss_bytes": after_rss - baseline_rss,
        "peak_rss_bytes": high_water_bytes(),
        "numeric_payload_and_index_bytes": numeric_bytes,
        "complete_frame_query": timed(frame_query, frames),
        "complete_atom_query": timed(atom_query, atoms),
    }
    if args.mode == "layers":
        output["graph_count"] = len(result[0])
        output["graph_nodes"] = sum(graph.number_of_nodes() for graph in result[0])
        output["graph_edges"] = sum(graph.number_of_edges() for graph in result[0])
    elif args.mode == "shared":
        output["graph_nodes"] = result.number_of_nodes()
        output["graph_edges"] = result.number_of_edges()
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
