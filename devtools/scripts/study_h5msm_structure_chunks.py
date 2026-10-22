"""Compare HDF5 geometry chunk layouts against native transfer blocks (#121).

Run with python -m devtools.scripts.study_h5msm_structure_chunks. Only isolated
study workers override dataset creation; the default runtime is not patched.
"""

import argparse
import gc
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
import tempfile
import tracemalloc
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from statistics import median
from time import perf_counter
from unittest.mock import patch

import h5py
import numpy as np

import molsysmt as msm
from devtools.scripts.benchmark_native_copy import (
    _THREADS,
    _check_system,
    _expected,
    _fixture,
    _rss,
)
from molsysmt import pyunitwizard as puw
from molsysmt.form._h5msm05_structures import read_independent_structures

_LAYOUTS = {
    "auto": None,
    "aligned_64k": 65536,
    "aligned_256k": 262144,
    "aligned_1m": 1048576,
}


def _aligned_chunks(shape, storage_rows, transfer_rows, budget):
    """Propose complete-xyz chunks aligned with every native write boundary."""
    if not shape[0] or not shape[1]:
        return None
    common = math.gcd(storage_rows, transfer_rows)
    limit = min(common, max(1, budget // (shape[1] * 24)))
    rows = next(value for value in range(limit, 0, -1) if common % value == 0)
    atoms = min(shape[1], max(1, budget // (rows * 24)))
    return rows, atoms, 3


def _measure(prepare, operation, validate, repeats):
    subject = prepare()
    output = operation(subject)
    validate(output)
    del subject, output
    samples = []
    for _ in range(repeats):
        subject = prepare()
        gc.collect()
        start = perf_counter()
        output = operation(subject)
        samples.append(perf_counter() - start)
        validate(output)
        del subject, output
    subject = prepare()
    gc.collect()
    tracemalloc.start()
    try:
        output = operation(subject)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    validate(output)
    return {
        "median_seconds": median(samples),
        "samples_seconds": samples,
        "traced_operation_peak_bytes": peak,
    }


def _worker(atoms, structures, layout, repeats):
    source = _fixture(atoms, structures)
    budget = _LAYOUTS[layout]
    chunks = (
        None
        if budget is None
        else _aligned_chunks(
            source.structures._coordinates.shape,
            source.structures._coordinates._block_size,
            256,
            budget,
        )
    )
    original = h5py.Group.create_dataset

    def create(group, name, *args, **kwargs):
        if group.name == "/structures" and name == "coordinates":
            # auto is an explicit reference even if production later improves.
            kwargs.pop("chunks", None)
            if chunks is not None:
                kwargs["chunks"] = chunks
        return original(group, name, *args, **kwargs)

    with tempfile.TemporaryDirectory(prefix="molsysmt121-chunks-") as directory:
        filename = Path(directory) / "geometry.h5msm"

        def prepare_write():
            filename.unlink(missing_ok=True)
            return source

        def write(system):
            with patch.object(h5py.Group, "create_dataset", create):
                msm.convert(system, to_form="file:h5msm", output_filename=filename)
            return filename

        def check_file(path):
            with h5py.File(path, "r") as file:
                assert file.attrs["version"] == "0.5"
                dataset = file["structures/coordinates"]
                assert dataset.shape == (structures, atoms, 3)
                assert dataset.attrs["unit"] == "nm"
                np.testing.assert_allclose(
                    dataset[structures // 2, [0, atoms - 1]],
                    _expected(atoms, [structures // 2], [0, atoms - 1])[0],
                    rtol=1e-6,
                    atol=1e-6,
                )

        measurements = {
            "public_write": _measure(prepare_write, write, check_file, repeats)
        }
        measurements["public_load"] = _measure(
            lambda: filename,
            lambda path: msm.convert(path, to_form="molsysmt.MolSys"),
            lambda system: _check_system(system, atoms, structures, persisted=True),
            repeats,
        )
        for label, selected_structures, selected_atoms in (
            ("private_one_structure", [structures // 2], None),
            (
                "private_nonconsecutive_two_atoms",
                [structures - 1, 0, structures // 2, 0],
                [atoms - 1, 0],
            ),
        ):

            def read(
                path,
                selected_structures=selected_structures,
                selected_atoms=selected_atoms,
            ):
                with h5py.File(path, "r") as file:
                    return read_independent_structures(
                        file,
                        structure_indices=selected_structures,
                        atom_indices=selected_atoms,
                    )

            def check(
                system,
                selected_structures=selected_structures,
                selected_atoms=selected_atoms,
            ):
                chosen_atoms = (
                    np.arange(atoms) if selected_atoms is None else selected_atoms
                )
                np.testing.assert_allclose(
                    puw.get_value(system.get_coordinates(), to_unit="nm"),
                    _expected(atoms, selected_structures, chosen_atoms),
                    rtol=1e-6,
                    atol=1e-6,
                )

            measurements[label] = _measure(lambda: filename, read, check, repeats)
        with h5py.File(filename, "r") as file:
            actual_chunks = file["structures/coordinates"].chunks
        return {
            "layout": layout,
            "coordinate_chunks": actual_chunks,
            "storage_rows": source.structures._coordinates._block_size,
            "file_bytes": filename.stat().st_size,
            "worker_peak_rss_bytes": _rss("VmHWM"),
            "operations": measurements,
        }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", action="append")
    parser.add_argument("--layout", action="append", choices=_LAYOUTS)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        cases = [
            tuple(map(int, value.split("x")))
            for value in (args.case or ["62x512", "10000x128", "100000x16"])
        ]
        if args.repeats < 1 or any(len(case) != 2 or min(case) < 3 for case in cases):
            raise ValueError
    except ValueError:
        parser.error(
            "Use positive repeats and at least three atoms/structures per case."
        )
    if args.worker:
        if len(cases) != 1 or not args.layout or len(args.layout) != 1:
            parser.error("One case and one layout are required per worker.")
        print(json.dumps(_worker(*cases[0], args.layout[0], args.repeats)))
        return
    if args.output is None:
        parser.error("--output is required.")
    root = Path(__file__).resolve().parents[2]
    result = {
        "scope": "experimental coordinate chunk layouts, not default runtime or installed-client qualification",
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "base_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip(),
        "worktree_dirty": bool(
            subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=root, text=True
            ).strip()
        ),
        "implementation_sha256": {
            str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (
                Path(__file__),
                root / "devtools/scripts/benchmark_native_copy.py",
                root / "molsysmt/basic/convert.py",
                root / "molsysmt/form/_h5msm05_structures.py",
            )
        },
        "platform": platform.platform(),
        "python": platform.python_version(),
        "packages": {
            name: version(name) for name in ("numpy", "pandas", "h5py", "pyunitwizard")
        },
        "cpu": next(
            (
                line.split(":", 1)[1].strip()
                for line in Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")
            ),
            "unknown",
        )
        if Path("/proc/cpuinfo").exists()
        else platform.machine(),
        "thread_environment": dict.fromkeys(_THREADS, "1"),
        "repeats": args.repeats,
        "measurement": "fresh worker per case/layout; one warm-up; three operations use new file handles per call; untraced timing and separate tracemalloc pass; warm/uncontrolled OS cache; temporary files cleaned",
        "query_scope": "selected queries use the private structures codec, including open/close; not public selective-file APIs",
        "units": {"coordinates": "nm", "time": "ps"},
        "cases": [],
    }
    for atoms, structures in cases:
        case = {"n_atoms": atoms, "n_structures": structures, "layouts": []}
        for layout in args.layout or _LAYOUTS:
            command = [
                sys.executable,
                "-m",
                "devtools.scripts.study_h5msm_structure_chunks",
                "--worker",
                "--case",
                f"{atoms}x{structures}",
                "--layout",
                layout,
                "--repeats",
                str(args.repeats),
            ]
            process = subprocess.run(
                command,
                cwd=root,
                text=True,
                capture_output=True,
                env={**os.environ, **result["thread_environment"]},
            )
            if process.stderr:
                print(process.stderr, file=sys.stderr, end="")
            process.check_returncode()
            case["layouts"].append(json.loads(process.stdout))
            print(f"Measured {atoms}x{structures}: {layout}", flush=True)
        result["cases"].append(case)
    args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
