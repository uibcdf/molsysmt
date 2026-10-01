#!/usr/bin/env python3
"""Measure packed-result invalidation without allocating trajectory coordinates.

Each case runs in a fresh process. Array payload, traced additional allocation
and process RSS are different measurements; none includes a disk write.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import platform
import subprocess
import sys
import time
import tracemalloc
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]


def make_result(count, images):
    from molsysmt import Interactions

    occupied = np.arange(10_000, dtype=np.int64)
    occupied = occupied[occupied % 10 != 9]
    frames = occupied[np.arange(count, dtype=np.int64) * len(occupied) // count]
    return Interactions(
        n_atoms=100_000, n_structures=10_000,
        evaluated_structure_indices=np.arange(10_000, dtype=np.int64),
        relation_types=("hbond",) * 1000,
        relation_participant_offsets=np.arange(1001, dtype=np.int64) * 3,
        participant_roles=("donor", "hydrogen", "acceptor") * 1000,
        participant_atom_offsets=np.arange(3001, dtype=np.int64),
        participant_atoms=np.arange(3000, dtype=np.int64),
        occurrence_structures=frames,
        occurrence_relations=np.arange(count, dtype=np.int64) % 1000,
        occurrence_evidence=np.zeros(count, dtype=np.int32),
        evidence_labels=("synthetic_geometry",),
        measurements={"distance": np.full(count, 0.3),
                      "angle": np.full(count, 2.9)},
        measure_units={"distance": "nm", "angle": "radian"},
        method="synthetic_memory_probe", software={"molsysmt": version("molsysmt")},
        occurrence_image_offsets=(np.arange(count + 1, dtype=np.int64) * 3
                                  if images else None),
        image_vectors=(np.zeros((3 * count, 3), dtype=np.int32) if images else None),
    )


def array_bytes(result):
    """Count distinct numeric arrays, including row handles and source maps."""
    arrays = [value for value in vars(result).values() if isinstance(value, np.ndarray)]
    arrays.extend(result.measurements.values())
    return sum(value.nbytes for value in {id(array): array for array in arrays}.values())


def process_memory():
    values = {}
    path = Path("/proc/self/status")
    if path.exists():
        for line in path.read_text().splitlines():
            name, _, value = line.partition(":")
            if name in {"VmRSS", "VmHWM"}:
                values[name] = int(value.split()[0]) * 1024
    return values


def worker(count, images, scope):
    # Warm the import and invalidation paths; discard the small result.
    warm = make_result(100, images).invalidate_structures([10])
    del warm
    result = make_result(count, images)
    view = result.query(structure_indices=[10])
    old_rows = view.to_dict()["occurrence_indices"].copy()
    frames = [10] if scope == "one_frame" else np.arange(result.n_structures)
    removed = int(np.isin(result.occurrence_structures, frames).sum())
    gc.collect()
    before = process_memory()
    tracemalloc.start()
    start = time.perf_counter()
    edited = result.invalidate_structures(frames)
    elapsed = time.perf_counter() - start
    live, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    after = process_memory()

    # Verify semantics outside the timed/allocated region, including old views.
    assert len(edited.occurrence_relations) == count - removed
    assert not np.isin(edited.evaluated_structure_indices, frames).any()
    assert not np.isin(edited.occurrence_structures, frames).any()
    assert np.array_equal(result.evaluated_structure_indices, np.arange(10_000))
    assert np.array_equal(view.to_dict()["occurrence_indices"], old_rows)
    keep = ~np.isin(result.occurrence_structures, frames)
    for name in ("occurrence_structures", "occurrence_relations", "occurrence_evidence"):
        assert np.array_equal(getattr(edited, name), getattr(result, name)[keep])
    for name, values in result.measurements.items():
        assert np.array_equal(edited.measurements[name], values[keep])
    if images:
        assert edited.image_vectors.shape == (3 * (count - removed), 3)
        assert np.all(edited.image_vectors == 0)
    return {
        "occurrences": count, "periodic_images": images, "scope": scope,
        "removed_occurrences": removed, "remaining_occurrences": count - removed,
        "input_array_bytes": array_bytes(result),
        "output_array_bytes": array_bytes(edited),
        "additional_traced_live_bytes": live, "additional_traced_peak_bytes": peak,
        "elapsed_seconds": elapsed, "process_before_bytes": before,
        "process_after_bytes": after, "checks_passed": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--count", type=int, default=100_000)
    parser.add_argument("--images", action="store_true")
    parser.add_argument("--scope", choices=("one_frame", "all_frames"), default="one_frame")
    args = parser.parse_args()
    if args.count <= 0:
        parser.error("count must be positive")
    if args.worker:
        print(json.dumps(worker(args.count, args.images, args.scope)))
        return
    results = []
    for count in (100_000, 1_000_000):
        for images in (False, True):
            for scope in ("one_frame", "all_frames"):
                command = [sys.executable, str(Path(__file__).resolve()), "--worker",
                           "--count", str(count), "--scope", scope]
                if images:
                    command.append("--images")
                completed = subprocess.run(command, cwd=ROOT, text=True,
                                           capture_output=True, check=True)
                result = json.loads(completed.stdout)
                results.append(result)
                print(json.dumps(result), flush=True)
    cpu_info = Path("/proc/cpuinfo")
    report = {
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "source_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "result_source_sha256": hashlib.sha256(
            (ROOT / "molsysmt/interactions/result.py").read_bytes()).hexdigest(),
        "platform": platform.platform(), "processor": platform.processor(),
        "python": platform.python_version(), "numpy": np.__version__,
        "installed_molsysmt": version("molsysmt"),
        "cpu_model": next((line.split(":", 1)[1].strip()
                           for line in (cpu_info.read_text().splitlines()
                                        if cpu_info.exists() else [])
                           if line.startswith("model name")), None),
        "methodology": {
            "statistic": "one measured call per isolated case; not a timing comparison",
            "warmup": "one discarded 100-occurrence invalidation before constructing the fixture",
            "fixture": "100,000 atoms, 10,000 structures, 1,000 reusable three-role relations; "
                       "every tenth frame evaluated-empty; distance and angle columns",
            "coordinates": "not allocated or copied; interaction-only measurement",
            "array_bytes": "unique ndarray objects, including row handles/maps; excludes Python overhead",
            "traced_bytes": "tracemalloc starts after fixture construction; live original is excluded; "
                            "peak includes output and temporaries, not whole-process peak RSS",
            "rss": "Linux process RSS and lifetime high-water mark before/after operation; "
                   "includes imports and allocator retention",
            "disk": "not measured; invalidation performs no disk write",
        },
        "cases": results,
    }
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
