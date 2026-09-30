"""Measuring projected plane fitting on a resident synthetic coordinate ensemble."""

import argparse
import hashlib
import json
import os
import platform
import subprocess
import time
from pathlib import Path

import molsysmt._rust as rust
import numpy as np

import molsysmt as msm
from molsysmt import configure
from molsysmt import pyunitwizard as puw
from molsysmt.native import Structures


def _peak_rss():
    return next((int(line.split()[1]) * 1024 for line in
                 Path("/proc/self/status").read_text().splitlines() if line.startswith("VmHWM:")), None)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atoms", type=int, default=100_000)
    parser.add_argument("--planes", type=int, default=1000)
    parser.add_argument("--structures", type=int, default=100)
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if min(args.planes, args.structures, args.repetitions) < 1 or args.atoms < 6 * args.planes:
        parser.error("Require positive plane/frame/repetition counts and six atoms per plane.")
    xyz = np.zeros((args.structures, args.atoms, 3))
    phase = np.arange(6) * np.pi / 3
    ring = .14 * np.column_stack((np.cos(phase), np.sin(phase), np.zeros(6)))
    centers = np.column_stack((np.arange(args.planes) * .5, np.zeros(args.planes), np.zeros(args.planes)))
    xyz[:, :6 * args.planes] = (centers[:, None] + ring).reshape(-1, 3)
    molsys = Structures(coordinates=puw.quantity(xyz, "nm"))
    del xyz
    groups = np.arange(6 * args.planes).reshape(-1, 6).tolist()
    frames = np.arange(args.structures - 1, -1, -2, dtype=np.int64)
    configure.chunk_size = 8
    configure.chunk_memory_fraction = 0
    source_peak = _peak_rss()
    records = []
    for mode in ("off", "force"):
        msm.structure.get_least_squares_plane(molsys, selection=groups, structure_indices=frames, heavy_mode=mode)
        timings = []
        for _ in range(args.repetitions):
            start = time.perf_counter()
            result = msm.structure.get_least_squares_plane(molsys, selection=groups, structure_indices=frames, heavy_mode=mode)
            timings.append(time.perf_counter() - start)
            np.testing.assert_allclose(result["normals"], np.broadcast_to([0., 0., 1.], (len(frames), args.planes, 3)), atol=1e-12)
            np.testing.assert_allclose(puw.get_value(result["centers"], to_unit="nm"), np.broadcast_to(centers, (len(frames), args.planes, 3)), atol=1e-12)
            np.testing.assert_allclose(puw.get_value(result["rms_deviation"], to_unit="nm"), 0, atol=1e-12)
        records.append({
            "heavy_mode": mode, "seconds": timings, "median_seconds": float(np.median(timings)),
            "returned_numeric_bytes": sum(
                (puw.get_value(value).nbytes if puw.is_quantity(value) else value.nbytes)
                for value in result.values() if puw.is_quantity(value) or isinstance(value, np.ndarray)
            ), "process_peak_rss_bytes": _peak_rss(),
        })
        del result
    record = {
        "record_version": "plane_fitting_benchmark@1", "date": time.strftime("%Y-%m-%d"),
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(subprocess.check_output(["git", "status", "--porcelain"], text=True)),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_hashes": {name: hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in (
            "molsysmt/structure/get_least_squares_plane.py", "molsysmt/structure/_plane.py",
            "molsysmt/_private/execution/chunked_executor.py",
            "rust/src/planes.rs", "rust/Cargo.lock", "molsysmt/_private/rust_backend.py",
        )},
        "extension_sha256": hashlib.sha256(Path(rust.__file__).read_bytes()).hexdigest(),
        "host": platform.node(), "platform": platform.platform(),
        "cpu": next((line.split(":", 1)[1].strip() for line in Path("/proc/cpuinfo").read_text().splitlines() if line.startswith("model name")), "unknown"),
        "available_cpu_count": len(os.sched_getaffinity(0)),
        "thread_environment": {name: os.environ.get(name) for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")},
        "versions": {"python": platform.python_version(), "molsysmt": msm.__version__, "numpy": np.__version__},
        "configuration": {"chunk_size": configure.chunk_size, "chunk_memory_fraction": configure.chunk_memory_fraction,
                          "max_ram_usage": configure.max_ram_usage, "num_threads": configure.num_threads,
                          "parallel_mode": configure.parallel_mode, "parallel_threshold": configure.parallel_threshold, "min_payload_per_thread": configure.min_payload_per_thread},
        "dataset": {"n_atoms": args.atoms, "n_structures": args.structures, "n_planes": args.planes,
                    "selected_atoms": 6 * args.planes, "selected_structures": len(frames),
                    "source_coordinate_bytes": 24 * args.atoms * args.structures},
        "methodology": {
            "warmup": "one complete call per mode", "repetitions": args.repetitions, "statistic": "median",
            "timing": "public selection, coordinate projection, packed Rust/Faer SVD and output quantities; fixture construction excluded",
            "oracle": "known planar regular hexagons with prescribed centers and z normals; no chemistry claims",
            "rss": "Linux process VmHWM including imports, resident source, warmup and earlier modes; not allocation delta or isolated-mode comparison",
            "numeric_memory": "returned NumPy/quantity buffers only; Python containers, work arrays and source excluded",
            "io": "no file I/O timed; source is resident native Structures",
        },
        "source_process_peak_rss_bytes": source_peak, "records": records,
    }
    args.output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "records": records}, indent=2))


if __name__ == "__main__":
    main()
