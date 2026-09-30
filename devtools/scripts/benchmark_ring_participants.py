"""Measuring ring preparation on isolated cycles and a long acyclic chain."""

import argparse
import hashlib
import json
import os
import platform
import subprocess
import time
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

import molsysmt as msm
from molsysmt.native import Topology


def _system(n_atoms, n_rings):
    molsys = Topology(n_atoms=n_atoms)
    aromatic_atoms = 6 * n_rings
    first = np.arange(aromatic_atoms, dtype=np.int64)
    second = 6 * (first // 6) + (first + 1) % 6
    tail = np.arange(aromatic_atoms, n_atoms - 1, dtype=np.int64)
    molsys.bonds = pd.DataFrame({
        "atom1_index": np.concatenate((first, tail)),
        "atom2_index": np.concatenate((second, tail + 1)),
        "bond_type": ["covalent"] * (len(first) + len(tail)),
        "is_aromatic": np.concatenate((np.ones(len(first), dtype=bool), np.zeros(len(tail), dtype=bool))),
    })
    msm.set(molsys, element="atom", atom_is_aromatic=np.arange(n_atoms) < aromatic_atoms)
    molsys._reference_chemical_state.connectivity_completeness = "complete"
    return molsys


def _peak_rss():
    for line in Path("/proc/self/status").read_text().splitlines():
        if line.startswith("VmHWM:"):
            return int(line.split()[1]) * 1024
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atoms", type=int, default=100_000)
    parser.add_argument("--rings", type=int, default=1000)
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.atoms < 6 * args.rings or args.rings < 1 or args.repetitions < 1:
        parser.error("Require positive rings/repetitions and at least six atoms per ring.")
    molsys = _system(args.atoms, args.rings)
    source_peak = _peak_rss()
    records = []
    for tool in (msm.topology.get_rings, msm.physchem.get_aromatic_rings):
        tool(molsys)
        elapsed = []
        for _ in range(args.repetitions):
            start = time.perf_counter()
            result = tool(molsys)
            elapsed.append(time.perf_counter() - start)
            assert result["atom_offsets"].tolist() == list(range(0, 6 * args.rings + 1, 6))
            np.testing.assert_array_equal(result["atom_indices"], np.arange(6 * args.rings))
        records.append({
            "tool": tool.__module__, "seconds": elapsed,
            "median_seconds": float(np.median(elapsed)),
            "membership_bytes": result["atom_indices"].nbytes + result["atom_offsets"].nbytes,
            "all_returned_array_bytes": sum(v.nbytes for v in result.values() if isinstance(v, np.ndarray)),
            "process_peak_rss_bytes": _peak_rss(),
        })
    document = {
        "record_version": "ring_participants_benchmark@1", "date": time.strftime("%Y-%m-%d"),
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(subprocess.check_output(["git", "status", "--porcelain"], text=True)),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_hashes": {name: hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in (
            "molsysmt/topology/_rings.py", "molsysmt/topology/get_rings.py",
            "molsysmt/physchem/get_aromatic_rings.py",
        )},
        "host": platform.node(), "platform": platform.platform(), "machine": platform.machine(),
        "available_cpu_count": len(os.sched_getaffinity(0)),
        "memory_total_kib": next((int(s.split()[1]) for s in Path("/proc/meminfo").read_text().splitlines() if s.startswith("MemTotal:")), None),
        "thread_environment": {name: os.environ.get(name) for name in (
            "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMBA_NUM_THREADS",
        )},
        "storage_scope": "No file I/O is timed; the native fixture is resident before measurement.",
        "cpu": next((s.split(":", 1)[1].strip() for s in Path("/proc/cpuinfo").read_text().splitlines() if s.startswith("model name")), "unknown"),
        "versions": {"python": platform.python_version(), "molsysmt": msm.__version__,
                     "numpy": np.__version__, "pandas": pd.__version__, "networkx": nx.__version__},
        "dataset": {"n_atoms": args.atoms, "n_isolated_six_cycles": args.rings,
                    "tail_atoms": args.atoms - 6 * args.rings},
        "methodology": {
            "warmup": "one complete call per tool", "statistic": "median", "repetitions": args.repetitions,
            "timing": "public chemistry preparation, graph perception, selection and packing; fixture construction excluded",
            "rss": "Linux VmHWM for the process, includes imports/source/warmup and preceding tool; not an isolated tool delta",
            "numeric_memory": "returned NumPy buffers only, excludes Python dictionaries, graph workspace and source tables",
            "oracle": "analytically known isolated six-cycles plus one acyclic tail; no molecular aromaticity inference",
        },
        "source_process_peak_rss_bytes": source_peak, "records": records,
    }
    args.output.write_text(json.dumps(document, indent=2) + "\n")
    print(f"Recorded {args.atoms} atoms, {args.rings} cycles in {args.output}")


if __name__ == "__main__":
    main()
