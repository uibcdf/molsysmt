"""Measure PDBQT storage in fresh processes; timings are evidence, not CI gates."""

import argparse
import gc
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path
from statistics import median
from time import perf_counter

TEMPLATE = (
    "ATOM     17   C1 LIG B   7       1.000   2.000   3.000  1.00 20.00     0.125 C"
)


def write_fixture(path, structures, atoms):
    """Generate fixed-column ensembles one model at a time, without a full string."""
    with Path(path).open("w", encoding="utf-8", newline="\n") as output:
        output.write(
            "REMARK deterministic storage benchmark, not chemical ground truth\n"
        )
        for structure in range(structures):
            output.write(f"MODEL {structure + 1}\n")
            for atom in range(atoms):
                output.write(
                    TEMPLATE[:6]
                    + f"{atom + 1:5d}"
                    + TEMPLATE[11:12]
                    + f"C{atom + 1:<3}"
                    + TEMPLATE[16:30]
                    + f"{1.0 + (structure % 1000) / 1000.0:8.3f}{atom / 100.0:8.3f}{3.0:8.3f}"
                    + TEMPLATE[54:]
                    + "\n"
                )
            output.write("END\nENDMDL\n")


def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for data in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(data)
    return digest.hexdigest()


def rss_bytes():
    """Read Linux resident memory separately from process high-water marks."""
    status = Path("/proc/self/status")
    if not status.exists():
        return None
    for line in status.read_text().splitlines():
        if line.startswith("VmRSS:"):
            return int(line.split()[1]) * 1024
    return None


def peak_bytes():
    import resource

    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value if sys.platform == "darwin" else value * 1024)


def worker(args):
    import numpy as np

    import molsysmt as msm
    from molsysmt.form.molsysmt_PDBQTFileHandler.iterators import StructuresIterator
    from molsysmt.native import PDBQTFileHandler

    with tempfile.TemporaryDirectory(prefix="molsysmt-pdbqt-benchmark-") as temporary:
        root = Path(temporary)
        warm = root / "warm.pdbqt"
        write_fixture(warm, 4, args.atoms)
        # Warm imports, native metadata, unit paths and byte-copy machinery only.
        with PDBQTFileHandler(warm, storage_mode=args.mode) as handle:
            handle.get_coordinates()
            msm.convert(handle, to_form=root / "warm-copy.pdbqt")
        gc.collect()
        baseline_rss, baseline_peak = rss_bytes(), peak_bytes()
        start = perf_counter()
        handle = PDBQTFileHandler(args.input, storage_mode=args.mode)
        opened = perf_counter()
        open_rss = rss_bytes()
        try:
            count = handle.n_structures
            first = handle.get_coordinates(
                structure_indices=list(range(min(count, args.chunk)))
            )
            queried = perf_counter()
            assert first.shape == (min(count, args.chunk), args.atoms, 3)
            first_rss = rss_bytes()
            wanted = [count - 1, 1, count // 2, count - 1]
            random_times = []
            for _ in range(10):
                tick = perf_counter()
                values = msm.pyunitwizard.get_value(
                    handle.get_coordinates(structure_indices=wanted), to_unit="nm"
                )
                random_times.append(perf_counter() - tick)
                np.testing.assert_allclose(
                    values[:, 0, 0], [0.1 + (i % 1000) / 10000.0 for i in wanted]
                )
            tick = perf_counter()
            visited = 0
            with StructuresIterator(
                handle, chunk=args.chunk, coordinates=True
            ) as iterator:
                for coordinates in iterator:
                    assert coordinates.shape[0] <= args.chunk
                    visited += coordinates.shape[0]
            sequential = perf_counter() - tick
            assert visited == count
            target = root / "copy.pdbqt"
            tick = perf_counter()
            msm.convert(handle, to_form=target)
            copy_seconds = perf_counter() - tick
            assert file_hash(target) == file_hash(args.input)
            result = dict(
                mode=args.mode,
                structures=count,
                atoms=args.atoms,
                source_bytes=Path(args.input).stat().st_size,
                chunk=args.chunk,
                open_validation_seconds=opened - start,
                first_query_seconds=queried - opened,
                open_and_first_block_seconds=queried - start,
                random_four_structure_query_median_seconds=median(random_times),
                sequential_seconds=sequential,
                file_copy_seconds=copy_seconds,
                baseline_rss_bytes=baseline_rss,
                rss_after_open_bytes=open_rss,
                rss_after_first_block_bytes=first_rss,
                rss_after_all_operations_bytes=rss_bytes(),
                baseline_peak_bytes=baseline_peak,
                peak_bytes=peak_bytes(),
                index_bytes=int(handle._document.offsets.nbytes),
                model_ids=len(handle._document.labels),
            )
        finally:
            handle.close()
        return result


def source_hashes():
    paths = [Path(__file__), Path("molsysmt/native/pdbqt_file_handler.py")]
    paths.extend(Path("molsysmt/_private").glob("pdbqt*.py"))
    for form in ["file_pdbqt", "string_pdbqt_text", "molsysmt_PDBQTFileHandler"]:
        paths.extend((Path("molsysmt/form") / form).glob("*.py"))
    return {
        str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--structures", type=int, nargs="+", default=[256, 2048, 8192])
    parser.add_argument("--atoms", type=int, default=64)
    parser.add_argument("--chunk", type=int, default=16)
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--mode", choices=["resident", "indexed"])
    args = parser.parse_args()
    if args.input is not None:
        print(json.dumps(worker(args)))
        return
    if (
        args.output is None
        or min(args.structures) < 4
        or not 1 <= args.atoms <= 999
        or args.chunk < 1
        or args.repeats < 1
    ):
        parser.error(
            "Require --output, at least four structures, 1..999 atoms and positive chunk/repeats."
        )
    before = source_hashes()
    trials, fixtures = [], []
    with tempfile.TemporaryDirectory(prefix="molsysmt-pdbqt-inputs-") as temporary:
        for structures in args.structures:
            path = Path(temporary) / f"{structures}.pdbqt"
            write_fixture(path, structures, args.atoms)
            fixtures.append(
                dict(
                    structures=structures,
                    atoms=args.atoms,
                    bytes=path.stat().st_size,
                    sha256=file_hash(path),
                )
            )
            for mode in ["resident", "indexed"]:
                for repeat in range(args.repeats):
                    command = [
                        sys.executable,
                        str(Path(__file__).resolve()),
                        "--input",
                        str(path),
                        "--mode",
                        mode,
                        "--atoms",
                        str(args.atoms),
                        "--chunk",
                        str(args.chunk),
                    ]
                    completed = subprocess.run(
                        command, capture_output=True, text=True, check=True
                    )
                    row = json.loads(completed.stdout)
                    row.update(repeat=repeat, stderr=completed.stderr)
                    trials.append(row)
                    print(
                        f"{structures} structures, {mode}, repeat {repeat + 1}: open {row['open_validation_seconds']:.3f}s, peak {row['peak_bytes'] / 1024**2:.1f} MiB",
                        flush=True,
                    )
    result = dict(
        schema="molsysmt.pdbqt_storage_benchmark@1",
        environment=dict(
            python=platform.python_version(),
            platform=platform.platform(),
            processor=platform.processor(),
            packages={
                name: importlib.metadata.version(name)
                for name in ["numpy", "pandas", "pyunitwizard", "argdigest", "smonitor"]
            },
            logical_cpus=os.cpu_count(),
            thread_environment={
                name: os.environ.get(name)
                for name in [
                    "OMP_NUM_THREADS",
                    "OPENBLAS_NUM_THREADS",
                    "MKL_NUM_THREADS",
                    "RAYON_NUM_THREADS",
                ]
            },
        ),
        command=" ".join(sys.argv),
        methodology="Each trial uses a fresh interpreter; imports, native metadata, units and copying are warmed with a separate four-model fixture. Handler construction fully validates its actual input. OS page cache is uncontrolled. Linux VmRSS and process high-water memory are reported separately. Input generation is outside each trial process. No cold-disk claim or performance threshold.",
        inputs=fixtures,
        trials=trials,
        source_sha256=before,
    )
    if source_hashes() != before:
        raise RuntimeError(
            "Benchmark source changed during measurement; discard mixed-source trials and rerun."
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
