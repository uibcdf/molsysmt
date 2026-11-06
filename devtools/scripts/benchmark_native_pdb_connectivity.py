"""Measuring repeated isolated PDB conversion and analytic graph-size workloads."""

from __future__ import annotations

import argparse
import json
import os
import platform
import statistics
import subprocess
import sys
import tempfile
from hashlib import sha256
from pathlib import Path
from time import perf_counter


def _alanine_source(n_groups, groups_per_chain=32):
    """Construct a synthetic heavy-atom input and independently specified edges.

    These coordinates exercise template lookup and polymer distance criteria;
    they are not a force-field geometry or an experimental peptide structure.
    TER separates bounded chains, including when their displayed IDs repeat.
    """
    if not 1 <= n_groups <= 19999:
        raise ValueError("Synthetic input requires 1 to 19999 alanine groups.")
    if not 1 <= groups_per_chain <= 100:
        raise ValueError("Synthetic chains require 1 to 100 groups.")
    if ((n_groups - 1) // groups_per_chain) * 4.0 + 1.6 > 9999.999:
        raise ValueError("Synthetic chain positions exceed the PDB coordinate field.")
    lines = ["HEADER    SYNTHETIC CONNECTIVITY SCALING; NOT EXPERIMENTAL\n"]
    pairs = []
    for group in range(n_groups):
        chain, position = divmod(group, groups_per_chain)
        x, y = position * 3.8, chain * 4.0
        atoms = [
            ("N", "N", (x, y, 0)),
            ("CA", "C", (x + 1.45, y + 0.8, 0)),
            ("C", "C", (x + 2.5, y + 0.4, 0)),
            ("O", "O", (x + 2.6, y + 1.6, 0)),
            ("CB", "C", (x + 1.4, y + 0.8, 1.52)),
        ]
        start = group * 5
        for offset, (name, element, coordinates) in enumerate(atoms):
            cx, cy, cz = coordinates
            lines.append(
                f"ATOM  {start + offset + 1:5d} {name:<4} ALA A{position + 1:4d}    "
                f"{cx:8.3f}{cy:8.3f}{cz:8.3f}{1.0:6.2f}{0.0:6.2f}          {element:>2}  \n"
            )
        pairs.extend(
            (start + a, start + b) for a, b in [(0, 1), (1, 2), (1, 4), (2, 3)]
        )
        if position:
            pairs.append((start - 3, start))
        if position == groups_per_chain - 1 or group == n_groups - 1:
            lines.append("TER\n")
    lines.append("END\n")
    return "".join(lines), sorted(pairs)


def _distribution(values):
    """Keep all observations alongside a limited descriptive summary."""
    ordered = sorted(values)
    quartiles = statistics.quantiles(ordered, n=4, method="inclusive")
    return dict(
        n=len(values),
        values=values,
        minimum=ordered[0],
        median=statistics.median(ordered),
        maximum=ordered[-1],
        interquartile_range=quartiles[2] - quartiles[0],
    )


def _receive(path, engines, repetitions, expected_pairs=None):
    """Measure serial fresh interpreters, refusing changed axes or edge sets."""
    import numpy as np

    probe = Path(__file__).with_name("probe_native_pdb_connectivity.py")
    source_hash = sha256(path.read_bytes()).hexdigest()
    routes = []
    edge_sets = {}
    if expected_pairs is not None:
        expected_pairs = [list(pair) for pair in expected_pairs]
    for engine in engines:
        observations = []
        for repeat in range(repetitions):
            start = perf_counter()
            completed = subprocess.run(
                [sys.executable, str(probe), str(path), "--child-engine", engine],
                capture_output=True,
                text=True,
                check=True,
                env=os.environ.copy(),
            )
            elapsed = perf_counter() - start
            row = json.loads(completed.stdout)
            pairs = row.pop("pairs")
            row["fresh_process_wall_seconds"] = elapsed
            row["replicate_index"] = repeat
            row["stderr"] = dict(
                n_lines=len(completed.stderr.splitlines()),
                sha256=sha256(completed.stderr.encode()).hexdigest(),
                preview=completed.stderr[:2000],
            )
            if expected_pairs is not None:
                assert pairs == ([] if engine == "disabled" else expected_pairs), (
                    path.name,
                    engine,
                    "independent analytic inventory",
                )
            if engine in edge_sets:
                assert edge_sets[engine] == pairs, (
                    path.name,
                    engine,
                    "nondeterministic graph",
                )
            edge_sets[engine] = pairs
            observations.append(row)
            print(
                f"{path.name}: {engine} replicate {repeat + 1}/{repetitions}",
                flush=True,
            )
        metrics = [
            "first_conversion_seconds",
            "repeated_conversion_seconds",
            "fresh_process_wall_seconds",
            "post_import_peak_rss_bytes",
            "conversion_peak_rss_bytes",
            "process_peak_rss_bytes",
        ]
        if engine == "MolSysMT":
            metrics.extend(["h5msm_write_seconds", "h5msm_read_seconds", "h5msm_bytes"])
        routes.append(
            dict(
                engine=engine,
                observations=observations,
                statistics={
                    metric: _distribution([row[metric] for row in observations])
                    for metric in metrics
                },
            )
        )
    all_observations = [row for route in routes for row in route["observations"]]
    for key in ["atom_axis_sha256", "coordinate_sha256"]:
        assert len({row[key] for row in all_observations}) == 1, (path.name, key)
    assert set(map(tuple, edge_sets["disabled"])) <= set(
        map(tuple, edge_sets["MolSysMT"])
    )
    assert sha256(path.read_bytes()).hexdigest() == source_hash
    result = dict(
        source=path.name,
        sha256=source_hash,
        synthetic=expected_pairs is not None,
        routes=routes,
    )
    if expected_pairs is not None:
        result["independent_expected_pairs_sha256"] = sha256(
            np.asarray(expected_pairs, dtype="<i8").tobytes()
        ).hexdigest()
    if "OpenMM" in edge_sets:
        native, comparison = (
            set(map(tuple, edge_sets[name])) for name in ["MolSysMT", "OpenMM"]
        )
        result["native_only_pairs"] = sorted(native - comparison)
        result["openmm_only_pairs"] = sorted(comparison - native)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdb", nargs="*", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--alanine-groups", nargs="*", type=int, default=[])
    parser.add_argument("--compare-openmm", action="store_true")
    arguments = parser.parse_args()
    if sys.platform != "linux":
        parser.error("This RSS benchmark is qualified for Linux only.")
    if arguments.repetitions < 3:
        parser.error("Use at least three independent processes per source/engine.")
    if not arguments.pdb and not arguments.alanine_groups:
        parser.error("Supply original PDB sources or --alanine-groups workloads.")
    engines = [
        "disabled",
        "MolSysMT",
        *(["OpenMM"] if arguments.compare_openmm else []),
    ]
    sources = [
        _receive(path.resolve(), engines, arguments.repetitions)
        for path in arguments.pdb
    ]
    with tempfile.TemporaryDirectory(prefix="molsysmt-304-scaling-") as directory:
        for n_groups in arguments.alanine_groups:
            text, expected = _alanine_source(n_groups)
            path = Path(directory) / f"synthetic_ala_{n_groups}.pdb"
            path.write_text(text)
            row = _receive(path, engines, arguments.repetitions, expected)
            row["generator"] = dict(
                n_groups=n_groups,
                groups_per_chain=32,
                observed_hydrogens=0,
                units="angstrom",
                experimental=False,
            )
            sources.append(row)
    root = Path(__file__).resolve().parents[2]
    names = [
        "devtools/scripts/benchmark_native_pdb_connectivity.py",
        "devtools/scripts/probe_native_pdb_connectivity.py",
        "molsysmt/_private/pdb_declarations.py",
        "molsysmt/_private/covalent_inference.py",
        "molsysmt/_private/hydrogen_covalent_candidates.py",
        "molsysmt/form/molsysmt_PDBFileHandler/to_molsysmt_MolSys.py",
        "molsysmt/_rust.abi3.so",
    ]
    payload = dict(
        schema="molsysmt.native_pdb_connectivity_benchmark@1",
        platform=platform.platform(),
        python=platform.python_version(),
        base_commit=subprocess.check_output(
            ["git", "-c", "core.fsmonitor=false", "rev-parse", "HEAD"],
            cwd=root,
            text=True,
        ).strip(),
        source_files={
            name: sha256((root / name).read_bytes()).hexdigest() for name in names
        },
        environment={
            name: os.environ.get(name)
            for name in [
                "OMP_NUM_THREADS",
                "OPENMM_CPU_THREADS",
                "OPENBLAS_NUM_THREADS",
                "MKL_NUM_THREADS",
            ]
        },
        measurement_scope="Serial fresh-process replicates, two conversions per process. First conversion excludes interpreter/package startup but includes lazy initialization; repeated conversion reuses process caches after releasing the prior result. Collection is untimed. Conversion RSS is process high-water before queries/H5MSM; final RSS includes native H5MSM write/read verification. Neither is allocation attribution or an isolated single-structure buffer size. Fresh-process wall includes startup and verification. Synthetic heavy-alanine chains test scaling and literal expected graphs, not experimental or force-field geometry. Raw observations, warnings and graph disagreements are retained. Small sample summaries do not establish universal speed or memory superiority.",
        sources=sources,
    )
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Retained {len(sources)} workloads in {arguments.output}", flush=True)


if __name__ == "__main__":
    main()
