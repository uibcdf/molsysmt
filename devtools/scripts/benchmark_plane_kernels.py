"""Comparing plane kernels in sequential, isolated processes with fixed workloads."""

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

import molsysmt._rust as rust
import numpy as np
from _plane_candidates import _numpy_batched, _numpy_grouped

import molsysmt as msm

CASES = {
    "one_plane": (1, [6]),
    "many_groups": (1, [6] * 1000),
    "many_frames": (5000, [6]),
    "groups_and_frames": (50, [6] * 1000),
    "ragged": (20, [3, 6, 12, 128] * 60),
    "large_cloud": (8, [10000]),
}
CANDIDATES = ("numpy_grouped", "numpy_batched", "rust_1", "rust_4")


def _fixture(case):
    ns, lengths = CASES[case]
    offsets = np.concatenate(([0], np.cumsum(lengths))).astype(np.int64)
    coordinates = np.empty((ns, offsets[-1], 3))
    rng = np.random.default_rng(824)
    for group, length in enumerate(lengths):
        axes, _ = np.linalg.qr(rng.normal(size=(3, 3)))
        phase = np.arange(length) * (2 * np.pi / length)
        ring = .14 * (np.cos(phase)[:, None] * axes[:, 0] + np.sin(phase)[:, None] * axes[:, 1])
        xyz = np.broadcast_to(ring, (ns, length, 3)).copy()
        xyz[:, 0] += (.01 + .005 * np.sin(np.arange(ns)))[:, None] * axes[:, 2]
        xyz += [group * .3, .4, -.2]
        coordinates[:, offsets[group]:offsets[group + 1]] = xyz
    return coordinates, offsets, np.arange(offsets[-1], dtype=np.int64)


def _peak_rss():
    return next((int(line.split()[1]) * 1024 for line in
                 Path("/proc/self/status").read_text().splitlines() if line.startswith("VmHWM:")), None)


def _call(candidate, coordinates, offsets, positions):
    if candidate == "numpy_grouped":
        return _numpy_grouped(coordinates, offsets, positions, caller="benchmark")
    if candidate == "numpy_batched":
        return _numpy_batched(coordinates, offsets, positions)
    return rust.get_least_squares_planes(coordinates, offsets, positions, int(candidate[-1]))


def _child(args):
    coordinates, offsets, positions = _fixture(args.case)
    source_peak = _peak_rss()
    warm = _call(args.candidate, coordinates, offsets, positions)
    del warm
    samples = []
    for _ in range(args.repetitions):
        start = time.perf_counter()
        result = _call(args.candidate, coordinates, offsets, positions)
        samples.append(time.perf_counter() - start)
        if len(samples) < args.repetitions:
            del result
    peak = _peak_rss()
    # Validation occurs after the memory/timing snapshot so its reference
    # allocations cannot contaminate a candidate's isolated high-water mark.
    reference = _numpy_grouped(coordinates, offsets, positions, caller="benchmark_reference")
    for column in (0, 2, 3):
        np.testing.assert_allclose(result[column], reference[column], rtol=1e-10, atol=1e-12)
    np.testing.assert_allclose(np.abs(np.sum(result[1] * reference[1], axis=-1)), 1, rtol=0, atol=1e-12)
    record = {
        "case": args.case, "candidate": args.candidate,
        "n_structures": len(coordinates), "n_groups": len(offsets) - 1, "n_atoms": coordinates.shape[1],
        "seconds": samples, "median_seconds": float(np.median(samples)),
        "input_numeric_bytes": sum(a.nbytes for a in (coordinates, offsets, positions)),
        "returned_numeric_bytes": sum(a.nbytes for a in result),
        "source_process_peak_rss_bytes": source_peak, "candidate_process_peak_rss_bytes": peak,
        "numpy_workspace_budget_bytes": 8 * 1024**2 if args.candidate == "numpy_batched" else None,
        "validation": "all outputs compared with grouped NumPy control; normal comparisons are unoriented",
    }
    print(json.dumps(record))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--repetitions", type=int, default=5)
    parser.add_argument("--case", choices=CASES)
    parser.add_argument("--candidate", choices=CANDIDATES)
    args = parser.parse_args()
    if args.repetitions < 1:
        parser.error("Require a positive repetition count.")
    if args.case or args.candidate:
        if not args.case or not args.candidate:
            parser.error("Child measurement requires both case and candidate.")
        _child(args)
        return
    if args.output is None:
        parser.error("Require an output path for the complete comparison.")
    records = []
    child_env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
    for case in CASES:
        for candidate in CANDIDATES:
            result = subprocess.run([
                sys.executable, __file__, "--case", case, "--candidate", candidate,
                "--repetitions", str(args.repetitions),
            ], env=child_env, capture_output=True, text=True)
            if result.returncode:
                sys.stderr.write(result.stderr)
                raise SystemExit(result.returncode)
            row = json.loads(result.stdout)
            records.append(row)
            print(f"{case}: {candidate}, median {row['median_seconds']:.6f}s", flush=True)
    source_files = ("rust/src/planes.rs", "molsysmt/structure/_plane.py", "devtools/scripts/_plane_candidates.py", "rust/Cargo.lock")
    record = {
        "record_version": "plane_kernel_comparison@1", "date": time.strftime("%Y-%m-%d"),
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(subprocess.check_output(["git", "status", "--porcelain"], text=True)),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_hashes": {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in source_files},
        "extension_sha256": hashlib.sha256(Path(rust.__file__).read_bytes()).hexdigest(),
        "versions": {"python": platform.python_version(), "numpy": np.__version__, "molsysmt": msm.__version__,
                     "rustc": subprocess.check_output(["rustc", "--version"], text=True).strip()},
        "host": platform.node(), "platform": platform.platform(),
        "cpu": next((line.split(":", 1)[1].strip() for line in Path("/proc/cpuinfo").read_text().splitlines() if line.startswith("model name")), "unknown"),
        "available_cpu_count": len(os.sched_getaffinity(0)),
        "numpy_configuration": np.show_config(mode="dicts"),
        "methodology": {
            "processes": "one new subprocess per case/candidate, executed sequentially",
            "warmup": "one complete candidate call, discarded", "repetitions": args.repetitions,
            "timing": "numeric kernel only, no public digestion/units/PBC/I/O; fixture and reference validation excluded",
            "units": "all inputs and length outputs are canonical nm numeric values",
            "rss": "Linux process high-water including imports/source/warmup; captured before reference validation; not allocation attribution",
            "numpy_threads": "OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1",
            "rust_threads": "one or four Rayon threads; frame-axis parallelism",
            "truth": "synthetic rotated/warped fixtures and NumPy parity; analytical geometry tests are separate",
        }, "records": records,
    }
    args.output.write_text(json.dumps(record, indent=2) + "\n")


if __name__ == "__main__":
    main()
