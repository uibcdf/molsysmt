#!/usr/bin/env python3
"""Measure pi-pi calculation, queries and H5MSM in isolated sequential workers."""

import argparse
import gc
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def fixture(atoms, structures, rings):
    import molsysmt as msm
    from molsysmt.native import MolSys, Topology

    molsys = MolSys()
    molsys.topology = Topology(n_atoms=atoms)
    molsys.topology.atoms["atom_type"] = "C"
    pairs = np.column_stack(
        (
            np.arange(6 * rings),
            np.arange(6 * rings).reshape(-1, 6)[:, [1, 2, 3, 4, 5, 0]].ravel(),
        )
    )
    molsys.topology.bonds = pd.DataFrame(
        {
            "atom1_index": pairs[:, 0],
            "atom2_index": pairs[:, 1],
            "bond_type": "covalent",
            "is_aromatic": True,
        }
    )
    molsys.topology._set_chemical_state_atom_attribute(
        "is_aromatic", [True] * (6 * rings) + [False] * (atoms - 6 * rings)
    )
    molsys.chemical_states._states[0].connectivity_completeness = "complete"
    phase = np.arange(6) * np.pi / 3
    ring = 0.14 * np.column_stack((np.cos(phase), np.sin(phase), np.zeros(6)))
    centers = np.column_stack(
        (
            np.repeat(np.arange(rings // 2) * 3.0, 2),
            np.zeros(rings),
            np.tile([0.0, 0.35], rings // 2),
        )
    )
    xyz = np.zeros((structures, atoms, 3))
    xyz[:, : 6 * rings] = (centers[:, None] + ring).reshape(-1, 3)
    for frame in range(structures):
        if frame % 5 == 1:
            xyz[frame, np.arange(6 * rings).reshape(-1, 6)[1::2].ravel(), 2] += 2
        elif frame % 5 == 2:
            xyz[frame, np.arange(6 * rings).reshape(-1, 6)[1::6].ravel(), 2] += 2
    molsys.structures.append(coordinates=msm.pyunitwizard.quantity(xyz, "nm"))
    return molsys


def worker(args):
    import molsysmt as msm
    from devtools.scripts.benchmark_ionic_interactions import _rss_bytes

    def calculate(source):
        return msm.interactions.pi_pi.get_pi_pi_interactions(
            source,
            ".6 nm",
            "30 degrees",
            ".2 nm",
            ".02 nm",
            pbc=False,
            heavy_mode=args.mode,
        )

    calculate(fixture(12, 1, 2))
    source = (
        msm.convert(args.input, to_form="molsysmt.MolSys")
        if args.source == "native"
        else args.input
    )
    times, rss = [], []
    with msm.configure.context(
        chunk_size=args.chunk,
        chunk_memory_fraction=0,
        max_ram_usage=args.budget,
        emit_heavy_telemetry=False,
    ):
        for _ in range(args.repetitions):
            result = None
            gc.collect()
            rss.append(_rss_bytes())
            start = time.perf_counter()
            result = calculate(source)
            times.append(time.perf_counter() - start)
    expected = sum(
        0
        if frame % 5 == 1
        else args.rings // 2 - (args.rings // 2 + 2) // 3
        if frame % 5 == 2
        else args.rings // 2
        for frame in range(args.structures)
    )
    assert result.n_interactions == expected
    np.testing.assert_allclose(
        result.measurements["distance"], 0.35, atol=1e-10, rtol=0
    )
    numeric_before = result.numeric_nbytes

    def query_time(function, repetitions=50):
        samples = []
        for _ in range(repetitions):
            start = time.perf_counter()
            function()
            samples.append(time.perf_counter() - start)
        return float(np.median(samples))

    first_query = query_time(lambda: result.query(atom_indices=[0]), 1)
    frame_query = query_time(lambda: result.query(structure_indices=[0]))
    atom_query = query_time(lambda: result.query(atom_indices=[0]))
    with tempfile.TemporaryDirectory() as directory:
        path = str(Path(directory) / "analysis.h5msm")
        start = time.perf_counter()
        msm.h5msm.write_layers(path, interactions={"pi": result})
        write = time.perf_counter() - start
        disk_bytes = Path(path).stat().st_size
        start = time.perf_counter()
        restored = msm.h5msm.read_layers(path, layers="interactions")["interactions"][
            "pi"
        ]
        read = time.perf_counter() - start
        np.testing.assert_array_equal(
            restored.occurrence_structures, result.occurrence_structures
        )
        for name in result.measurements:
            np.testing.assert_array_equal(
                restored.measurements[name], result.measurements[name]
            )
    return dict(
        source=args.source,
        heavy_mode=args.mode,
        samples_seconds=times,
        median_seconds=float(np.median(times)),
        occurrences=result.n_interactions,
        relations=len(result.relation_types),
        chunks=result.execution_records[0]["details"]["execution_chunks"],
        numeric_bytes_before_index=numeric_before,
        numeric_bytes_after_index=result.numeric_nbytes,
        rss_before_calculation_bytes=rss,
        process_peak_rss_bytes=_rss_bytes("VmHWM"),
        first_atom_query_s=first_query,
        atom_query_median_s=atom_query,
        frame_query_median_s=frame_query,
        h5msm_write_s=write,
        h5msm_read_s=read,
        h5msm_bytes=disk_bytes,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atoms", type=int, default=100_000)
    parser.add_argument("--structures", type=int, default=100)
    parser.add_argument("--rings", type=int, default=1000)
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--chunk", type=int, default=16)
    parser.add_argument("--budget", type=int, default=1024**3)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--input")
    parser.add_argument("--source", choices=["native", "file"])
    parser.add_argument("--mode", choices=["off", "force"])
    args = parser.parse_args()
    if (
        min(args.structures, args.rings, args.repetitions, args.chunk, args.budget) < 1
        or args.rings % 2
        or args.atoms < args.rings * 6
    ):
        parser.error(
            "Require positive counts, even ring count and at least six atoms per ring."
        )
    if args.input:
        print(json.dumps(worker(args)))
        return
    import molsysmt._rust as rust

    import molsysmt as msm

    if args.output is None:
        parser.error("An output artifact path is required.")
    molsys = fixture(args.atoms, args.structures, args.rings)
    results = []
    with tempfile.TemporaryDirectory() as directory:
        path = str(Path(directory) / "source.h5msm")
        msm.convert(molsys, to_form=path)
        del molsys
        gc.collect()
        for source in ("native", "file"):
            for mode in ("off", "force"):
                command = [
                    sys.executable,
                    str(Path(__file__).resolve()),
                    "--input",
                    path,
                    "--source",
                    source,
                    "--mode",
                    mode,
                    "--atoms",
                    str(args.atoms),
                    "--structures",
                    str(args.structures),
                    "--rings",
                    str(args.rings),
                    "--repetitions",
                    str(args.repetitions),
                    "--chunk",
                    str(args.chunk),
                    "--budget",
                    str(args.budget),
                ]
                completed = subprocess.run(
                    command, check=True, capture_output=True, text=True
                )
                results.append(json.loads(completed.stdout))
                print(f"Completed {source}/{mode}", file=sys.stderr, flush=True)
    paths = [
        Path(__file__).resolve(),
        ROOT / "molsysmt/interactions/pi_pi/get_pi_pi_interactions.py",
        ROOT / "molsysmt/interactions/pi_pi/_reducer.py",
        ROOT / "molsysmt/structure/_plane.py",
        ROOT / "molsysmt/structure/_group_minimum_contacts.py",
        ROOT / "molsysmt/_private/sparse_membership.py",
    ]
    record = dict(
        record_version="pi_pi_benchmark@1",
        date=time.strftime("%Y-%m-%d"),
        git_head=subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        dirty_worktree=bool(
            subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=ROOT, text=True
            )
        ),
        source_hashes={
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths
        },
        extension_sha256=hashlib.sha256(Path(rust.__file__).read_bytes()).hexdigest(),
        platform=platform.platform(),
        python=platform.python_version(),
        numpy=np.__version__,
        molsysmt=msm.__version__,
        cpu=next(
            (
                line.split(":", 1)[1].strip()
                for line in Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")
            ),
            "unknown",
        ),
        thread_environment={
            key: os.environ.get(key)
            for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")
        },
        parallel_configuration={
            key: getattr(msm.configure, key)
            for key in (
                "num_threads",
                "parallel_mode",
                "parallel_threshold",
                "min_payload_per_thread",
            )
        },
        atoms=args.atoms,
        structures=args.structures,
        rings=args.rings,
        coordinate_bytes=24 * args.atoms * args.structures,
        chunk_size_limit=args.chunk,
        ram_budget_bytes=args.budget,
        repetitions=args.repetitions,
        fixture="Separated regular hexagon pairs, variable counts and every fifth frame empty; no PBC; declared synthetic aromaticity.",
        timing="Full public detector, including chemistry preparation, projection, geometry and sparse packing; source creation/loading excluded.",
        warmup="One tiny calculation per isolated worker; OS page cache uncontrolled.",
        rss="Linux VmHWM since worker exec, including imports, source loading, calculations, indexing, serialization and reload; not allocation delta.",
        disk="Standalone interactions layer in H5MSM 0.5; coordinate source write is not timed.",
        results=results,
    )
    args.output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "results": results}, indent=2))


if __name__ == "__main__":
    main()
