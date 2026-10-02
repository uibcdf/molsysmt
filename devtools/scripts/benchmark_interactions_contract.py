#!/usr/bin/env python3
"""Check and benchmark complete interaction queries against a record oracle.

This benchmark covers the experimental class's supported single-method,
source-index contract. Unsupported requirements are reported explicitly.
Run from the repository root; no detector or H5MSM behavior is measured.
"""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import tempfile
import time
from collections import Counter
from importlib.metadata import version
from pathlib import Path

import numpy as np

import molsysmt as msm

METHOD = "synthetic_full_contract"
UNITS = {"distance": "nm", "angle": "radians"}
TEMPLATES = (
    ("hbond", (("donor", 1), ("hydrogen", 1), ("acceptor", 1))),
    ("pi_pi", (("ring", 6), ("ring", 6))),
    ("disulfide_candidate", (("sulfur", 1), ("sulfur", 1))),
    ("four_body", (("site", 1),) * 4),
)


def _relation(rng, n_atoms, template_index, hot_atom=False):
    kind, template = TEMPLATES[template_index % len(TEMPLATES)]
    count = sum(size for _, size in template)
    chosen = rng.choice(n_atoms, size=count, replace=False)
    if hot_atom:
        chosen[0] = 0
        if 0 in chosen[1:]:
            replacement = next(atom for atom in range(1, n_atoms) if atom not in chosen)
            chosen[np.flatnonzero(chosen[1:] == 0)[0] + 1] = replacement
    participants = []
    start = 0
    for role, size in template:
        participants.append(
            {
                "role": role,
                "atom_indices": [int(atom) for atom in chosen[start : start + size]],
            }
        )
        start += size
    return kind, participants


def iter_fixture(n_frames, n_atoms, per_frame, distribution, seed):
    """Yield full-field records in structure-index order without retaining them."""
    rng = np.random.default_rng(seed)
    pool_size = max(120, 2 * per_frame)
    pool = [_relation(rng, n_atoms, i, hot_atom=i % 3 == 0) for i in range(pool_size)]
    persistent = []
    for frame in range(n_frames):
        if frame % 29 == 0:
            continue
        if frame % 17 == 1:
            continue
        count = per_frame + frame % 3 - 1
        stable = distribution == "stable" or (
            distribution == "mixed" and frame < n_frames // 2
        )
        if distribution == "persistent":
            retained = [index for index in persistent if rng.random() < 0.95][:count]
            remaining = count - len(retained)
            choices = [index for index in range(len(pool)) if index not in retained]
            selected = (
                retained + rng.choice(choices, size=remaining, replace=False).tolist()
            )
            persistent = selected
        else:
            selected = rng.choice(len(pool), size=count, replace=False).tolist()
        for ordinal, pool_index in enumerate(selected):
            if stable or distribution == "persistent":
                kind, participants = pool[pool_index]
            else:
                kind, participants = _relation(
                    rng, n_atoms, pool_index, hot_atom=ordinal % 3 == 0
                )
            images = rng.integers(-1, 2, size=(len(participants), 3)).tolist()
            record = {
                "structure_index": frame,
                "interaction_type": kind,
                "participants": participants,
                "evidence": "source_annotation"
                if kind == "disulfide_candidate" and ordinal % 7 == 0
                else "observed_geometry",
                "measurements": {
                    "distance": round(float(rng.uniform(0.15, 0.5)), 6),
                    "angle": round(float(rng.uniform(0.0, 0.6)), 6)
                    if kind == "hbond"
                    else -1.0,
                },
                "images": images,
            }
            yield record
            if frame % 31 == 2 and ordinal == 0:
                duplicate = {
                    **record,
                    "measurements": {
                        **record["measurements"],
                        "distance": record["measurements"]["distance"] + 0.01,
                    },
                    "images": [list(vector) for vector in images],
                }
                duplicate["images"][0][0] += 1
                yield duplicate


def generate_fixture(n_frames, n_atoms, per_frame, distribution, seed):
    """Generate evaluated coverage and full-field records in source indices."""
    evaluated = [frame for frame in range(n_frames) if frame % 29 != 0]
    return list(
        iter_fixture(n_frames, n_atoms, per_frame, distribution, seed)
    ), evaluated


def _signature(record):
    participants = tuple(
        (part["role"], tuple(part["atom_indices"])) for part in record["participants"]
    )
    measures = tuple(
        (name, float(record["measurements"][name])) for name in sorted(UNITS)
    )
    images = tuple(tuple(int(value) for value in image) for image in record["images"])
    return (
        int(record["structure_index"]),
        record["interaction_type"],
        participants,
        record["evidence"],
        measures,
        images,
    )


def _selected_frames(evaluated, request):
    if request is None:
        return evaluated
    known = set(evaluated)
    return [frame for frame in dict.fromkeys(request) if frame in known]


def _record_atoms(record):
    return {atom for part in record["participants"] for atom in part["atom_indices"]}


def expected(
    records,
    evaluated,
    *,
    frames=None,
    atoms=None,
    mode="incident",
    between=None,
    exclusive=False,
):
    """Select from plain records without using result indexes or arrays."""
    coverage = _selected_frames(evaluated, frames)
    frame_set = set(coverage)
    selected_atoms = None if atoms is None else set(atoms)
    a, b = (None, None) if between is None else (set(between[0]), set(between[1]))
    selected = []
    for record in records:
        if record["structure_index"] not in frame_set:
            continue
        involved = _record_atoms(record)
        if selected_atoms is not None:
            hits = bool(involved & selected_atoms)
            internal = involved <= selected_atoms
            if not (
                hits
                if mode == "incident"
                else internal
                if mode == "internal"
                else hits and not internal
            ):
                continue
        if between is not None and not (
            involved & a and involved & b and (not exclusive or involved <= a | b)
        ):
            continue
        selected.append(_signature(record))
    return coverage, Counter(selected)


def materialize(result):
    """Decode complete selected observations, including grouped participants."""
    columns = result.to_dict()
    output = []
    for row, relation_index in enumerate(columns["relation_indices"]):
        relation = result.relation(relation_index)
        first = columns["image_offsets"][row]
        last = columns["image_offsets"][row + 1]
        output.append(
            _signature(
                {
                    "structure_index": columns["structure_indices"][row],
                    "interaction_type": relation["interaction_type"],
                    "participants": relation["participants"],
                    "evidence": columns["evidence"][row],
                    "measurements": {
                        name: values[row]
                        for name, values in columns["measurements"].items()
                    },
                    "images": columns["image_vectors"][first:last],
                }
            )
        )
    return columns["evaluated_structure_indices"].tolist(), Counter(output)


def _run_query(result, spec):
    if "between" in spec:
        a, b = spec["between"]
        return result.between(
            a,
            b,
            structure_indices=spec.get("frames"),
            exclusive=spec.get("exclusive", False),
        )
    return result.query(
        structure_indices=spec.get("frames"),
        atom_indices=spec.get("atoms"),
        mode=spec.get("mode", "incident"),
    )


def _requests(rng, records, n_frames, n_atoms, n_samples):
    requests = {
        name: []
        for name in (
            "frame",
            "nonconsecutive",
            "atom",
            "incident",
            "internal",
            "cross",
            "between",
            "between_exclusive",
            "combined",
        )
    }
    for sample_index in range(n_samples):
        chosen = records[int(rng.integers(0, len(records)))]
        frame = int(rng.integers(0, n_frames))
        if sample_index % 2 == 0:
            group = sorted(_record_atoms(chosen))
            atom = group[0]
        else:
            atom = int(rng.integers(0, n_atoms))
            group = rng.choice(n_atoms, size=min(16, n_atoms), replace=False).tolist()
        frames = rng.choice(n_frames, size=4, replace=False).tolist()
        if sample_index % 2 == 0:
            frames[0] = chosen["structure_index"]
        frames.append(frames[0])
        requests["frame"].append({"frames": [frame]})
        requests["nonconsecutive"].append({"frames": frames})
        requests["atom"].append({"atoms": [atom]})
        for mode in ("incident", "internal", "cross"):
            requests[mode].append({"atoms": group, "mode": mode})
        split = len(group) // 2
        a, b = group[:split], group[split:]
        requests["between"].append({"between": (a, b)})
        requests["between_exclusive"].append({"between": (a, b), "exclusive": True})
        requests["combined"].append({"frames": frames, "atoms": group})
    return requests


def _summary(samples):
    ordered = sorted(samples)
    return {
        "median_ms": statistics.median(ordered),
        "p95_ms": ordered[int(0.95 * (len(ordered) - 1))],
    }


def _rss():
    status = Path("/proc/self/status")
    if not status.exists():
        return {}
    values = {}
    for line in status.read_text().splitlines():
        name, _, raw = line.partition(":")
        if name in {"VmRSS", "VmHWM"}:
            values[name] = int(raw.split()[0]) * 1024
    return values


def _direct_postings(result):
    """Build experimental atom-to-occurrence postings and distinct cardinalities."""
    atoms = []
    occurrences = []
    cardinality = np.empty(result.n_interactions, dtype=np.int64)
    for position, relation in enumerate(result.occurrence_relations):
        involved = np.unique(result._relation_atoms(relation))
        cardinality[position] = len(involved)
        atoms.extend(involved)
        occurrences.extend([position] * len(involved))
    atoms = np.asarray(atoms, dtype=np.int64)
    occurrences = np.asarray(occurrences, dtype=np.int64)
    order = np.argsort(atoms, kind="stable")
    counts = np.bincount(atoms, minlength=result.n_atoms)
    offsets = np.r_[0, np.cumsum(counts)]
    return offsets, occurrences[order], cardinality


def _direct_query(result, index, spec):
    """Select atom-set observations with direct postings for this probe only."""
    offsets, postings, cardinality = index
    coverage = _selected_frames(
        result.evaluated_structure_indices.tolist(), spec.get("frames")
    )
    atoms = sorted(set(spec["atoms"]))
    batches = [postings[offsets[atom] : offsets[atom + 1]] for atom in atoms]
    if batches:
        positions, counts = np.unique(np.concatenate(batches), return_counts=True)
    else:
        positions = np.empty(0, dtype=np.int64)
        counts = np.empty(0, dtype=np.int64)
    mode = spec.get("mode", "incident")
    if mode == "internal":
        positions = positions[counts == cardinality[positions]]
    elif mode == "cross":
        positions = positions[counts < cardinality[positions]]
    elif mode != "incident":
        raise ValueError(f"unsupported mode: {mode}")
    if spec.get("frames") is not None:
        priorities = {frame: rank for rank, frame in enumerate(coverage)}
        positions = positions[
            np.isin(result.occurrence_structures[positions], coverage)
        ]
        rank = np.fromiter(
            (priorities[int(result.occurrence_structures[pos])] for pos in positions),
            dtype=np.int64,
        )
        positions = positions[np.lexsort((positions, rank))]
    return result._view(positions, coverage)


def _probe_direct_index(result, records, evaluated, requests):
    start = time.perf_counter()
    index = _direct_postings(result)
    build_s = time.perf_counter() - start
    checked = 0
    query_only = {}
    complete = {}
    for name in ("atom", "incident", "internal", "cross", "combined"):
        query_samples = []
        complete_samples = []
        for spec in requests[name]:
            actual = materialize(_direct_query(result, index, spec))
            if actual != expected(records, evaluated, **spec):
                raise AssertionError(f"direct index oracle mismatch in {name}: {spec}")
            start = time.perf_counter_ns()
            selected_count = _direct_query(result, index, spec).n_interactions
            query_samples.append((time.perf_counter_ns() - start) / 1_000_000)
            if selected_count != sum(actual[1].values()):
                raise AssertionError(f"direct index count mismatch in {name}: {spec}")
            start = time.perf_counter_ns()
            materialize(_direct_query(result, index, spec))
            complete_samples.append((time.perf_counter_ns() - start) / 1_000_000)
            checked += 1
        query_only[name] = _summary(query_samples)
        complete[name] = _summary(complete_samples)
    return {
        "build_s": build_s,
        "numeric_bytes": sum(array.nbytes for array in index),
        "queries_checked": checked,
        "query_only_ms": query_only,
        "complete_query_ms": complete,
    }


def _cpu_model():
    cpu_info = Path("/proc/cpuinfo")
    if not cpu_info.exists():
        return None
    return next(
        (
            line.partition(":")[2].strip()
            for line in cpu_info.read_text().splitlines()
            if line.startswith("model name")
        ),
        None,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=300)
    parser.add_argument("--atoms", type=int, default=200)
    parser.add_argument("--per-frame", type=int, default=8)
    parser.add_argument(
        "--distribution",
        choices=("stable", "churn", "mixed", "persistent"),
        default="mixed",
    )
    parser.add_argument("--samples", type=int, default=40)
    parser.add_argument("--seed", type=int, default=251)
    parser.add_argument(
        "--direct-index-probe",
        action="store_true",
        help="Compare an experimental direct atom posting index",
    )
    args = parser.parse_args()
    if (
        args.frames < 30
        or args.atoms < 30
        or not 1 <= args.per_frame <= 119
        or args.samples < 1
    ):
        parser.error("frames and atoms must be >=30; per-frame 1..119; samples >=1")

    rss_before = _rss()
    records, evaluated = generate_fixture(
        args.frames, args.atoms, args.per_frame, args.distribution, args.seed
    )
    start = time.perf_counter()
    result = msm.Interactions.from_records(
        records,
        n_atoms=args.atoms,
        n_structures=args.frames,
        evaluated_structure_indices=evaluated,
        method=METHOD,
        measure_units=UNITS,
        parameters={"seed": args.seed},
        source_id="synthetic_contract",
    )
    build_s = time.perf_counter() - start
    rss_after_build = _rss()
    assert result.method == METHOD and result.measure_units == UNITS

    requests = _requests(
        np.random.default_rng(args.seed + 1),
        records,
        args.frames,
        args.atoms,
        args.samples,
    )
    # Add deterministic edge cases that random queries may miss.
    requests["nonconsecutive"].append({"frames": [2, 1, 0, 2]})
    requests["frame"].append({"frames": [1]})
    numeric_before_index = result.numeric_nbytes
    first_index_start = time.perf_counter()
    materialize(result.query(atom_indices=[0]))
    first_atom_s = time.perf_counter() - first_index_start
    memory_after_index = _rss()
    timings = {}
    query_only_timings = {}
    result_counts = {}
    checked = 0
    for name, specs in requests.items():
        samples = []
        query_samples = []
        counts = []
        for spec in specs:
            selected = _run_query(result, spec)
            actual = materialize(selected)
            reference = expected(records, evaluated, **spec)
            if actual != reference:
                raise AssertionError(f"oracle mismatch in {name}: {spec}")
            counts.append(sum(actual[1].values()))
            start = time.perf_counter_ns()
            selected_count = _run_query(result, spec).n_interactions
            query_samples.append((time.perf_counter_ns() - start) / 1_000_000)
            if selected_count != counts[-1]:
                raise AssertionError(f"selection count changed in {name}: {spec}")
            start = time.perf_counter_ns()
            materialize(_run_query(result, spec))
            samples.append((time.perf_counter_ns() - start) / 1_000_000)
            checked += 1
        timings[name] = _summary(samples)
        query_only_timings[name] = _summary(query_samples)
        result_counts[name] = {
            "median": statistics.median(counts),
            "max": max(counts),
        }

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "interactions.h5i"
        start = time.perf_counter()
        result.save(path)
        save_s = time.perf_counter() - start
        file_bytes = path.stat().st_size
        start = time.perf_counter()
        loaded = msm.Interactions.load(path)
        load_s = time.perf_counter() - start
        if (
            loaded.method != METHOD
            or loaded.measure_units != UNITS
            or loaded.parameters != {"seed": args.seed}
            or loaded.source_id != "synthetic_contract"
        ):
            raise AssertionError("standalone round trip changed analysis metadata")
        if materialize(loaded) != expected(records, evaluated):
            raise AssertionError("standalone round trip changed the full result")

    baseline_peak = _rss().get("VmHWM")
    direct = (
        _probe_direct_index(result, records, evaluated, requests)
        if args.direct_index_probe
        else None
    )
    print(
        json.dumps(
            {
                "platform": platform.platform(),
                "python": platform.python_version(),
                "cpu_model": _cpu_model(),
                "numpy": np.__version__,
                "h5py": version("h5py"),
                "distribution": args.distribution,
                "frames": args.frames,
                "atoms": args.atoms,
                "evaluated_frames": len(evaluated),
                "occurrences": result.n_interactions,
                "relations": len(result.relation_types),
                "queries_checked": checked,
                "build_s": build_s,
                "first_atom_query_s": first_atom_s,
                "numeric_bytes_before_index": numeric_before_index,
                "numeric_bytes_after_index": result.numeric_nbytes,
                "rss_before_bytes": rss_before.get("VmRSS"),
                "rss_after_build_bytes": rss_after_build.get("VmRSS"),
                "rss_after_index_bytes": memory_after_index.get("VmRSS"),
                "peak_rss_bytes": baseline_peak,
                "query_only_ms": query_only_timings,
                "complete_query_ms": timings,
                "result_rows": result_counts,
                "file_bytes": file_bytes,
                "save_s": save_s,
                "load_s": load_s,
                "direct_postings_probe": direct,
                "unsupported_gates": [
                    "source_index_maps",
                    "multi_analysis",
                    "incremental_edits",
                    "remapping",
                    "streaming_write",
                    "lazy_file_query",
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
