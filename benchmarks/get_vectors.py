"""Measure directed-vector kernels and public delivery in isolated processes.

Run ``python benchmarks/get_vectors.py --output /tmp/get_vectors.json``.
RSS includes imports, inputs, control arrays and retained outputs; it is not a
measurement of output bytes alone. Each case uses a fresh process. Public warm
samples follow one explicitly reported cold call and include argument/unit work.
"""

import argparse
import hashlib
import json
import os
import platform
import statistics
import subprocess
import sys
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def source_hashes():
    return {
        path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        for path in (
            "molsysmt/structure/get_vectors.py",
            "molsysmt/structure/_vectors.py",
            "molsysmt/_private/rust_backend.py",
            "rust/src/vectors.rs",
        )
    }


def sample(operation, repeats=5):
    times = []
    for _ in range(repeats):
        start = perf_counter()
        result = operation()
        times.append(perf_counter() - start)
        del result
    return {"seconds": times, "median_seconds": statistics.median(times)}


def worker(case):
    import resource

    import numpy as np

    import molsysmt as msm
    from molsysmt import _rust
    from molsysmt import pyunitwizard as puw
    from molsysmt.native import Structures

    ns, na, pairs, periodic, details = {
        "pairs": (10, 100000, True, False, False),
        "cartesian": (4, 500, False, False, False),
        "periodic": (10, 10000, True, True, True),
        "structures": (5000, 62, True, False, False),
    }[case]
    rng = np.random.default_rng(375)
    a = rng.random((ns, na, 3))
    b = rng.random((ns, na, 3)) * 2
    boxes = np.repeat((np.eye(3) * 2)[None], ns, axis=0) if periodic else None
    expected = b - a if pairs else b[:, None] - a[:, :, None]
    if periodic:
        expected -= 2 * np.floor(expected / 2 + 0.5)
    native = {}
    for threads in (1, 12):

        def operation(threads=threads):
            return _rust.get_vectors(a, b, boxes, pairs, details, threads)

        result = operation()
        observed = result[0].reshape(expected.shape)
        np.testing.assert_allclose(observed, expected, atol=1e-14)
        if details:
            np.testing.assert_allclose(result[1], np.linalg.norm(expected, axis=-1))
            np.testing.assert_allclose(
                result[2], expected / np.linalg.norm(expected, axis=-1)[..., None]
            )
        native[str(threads)] = sample(operation)
        native[str(threads)]["returned_array_bytes"] = sum(
            item.nbytes for item in result
        )
        del result, observed
    control = (
        sample(lambda: b - a if pairs else b[:, None] - a[:, :, None])
        if not periodic
        else None
    )
    first = Structures(
        coordinates=puw.quantity(a, "nm"),
        box=None if boxes is None else puw.quantity(boxes, "nm"),
    )
    second = Structures(coordinates=puw.quantity(b, "nm"))
    public = {}
    for mode in ("off", "force"):

        def operation(mode=mode):
            return msm.structure.get_vectors(
                first,
                molecular_system_2=second,
                pairs=pairs,
                pbc=periodic,
                output_type="dictionary" if details else "numpy.ndarray",
                heavy_mode=mode,
                num_threads=12,
                parallel=True,
            )

        start = perf_counter()
        result = operation()
        cold = perf_counter() - start
        vectors = result["vectors"] if details else result
        np.testing.assert_allclose(
            puw.get_value(vectors, to_unit="nm"), expected, atol=1e-14
        )
        del result, vectors
        public[mode] = {"first_call_seconds": cold, **sample(operation, repeats=3)}
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return dict(
        case=case,
        n_atoms=na,
        n_structures=ns,
        pairs=pairs,
        periodic=periodic,
        dictionary=details,
        vector_output_bytes=expected.nbytes,
        native=native,
        numpy_nonperiodic_control=control,
        public=public,
        peak_process_rss_bytes=int(rss if sys.platform == "darwin" else rss * 1024),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--worker", choices=("pairs", "cartesian", "periodic", "structures")
    )
    args = parser.parse_args()
    if args.worker:
        print(json.dumps(worker(args.worker)))
        return
    before = source_hashes()
    cases = []
    for case in ("pairs", "cartesian", "periodic", "structures"):
        run = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--worker", case],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if run.returncode:
            sys.stderr.write(run.stdout + run.stderr)
            raise subprocess.CalledProcessError(run.returncode, run.args)
        cases.append(json.loads(run.stdout))
    if source_hashes() != before:
        raise RuntimeError(
            "Vector sources changed during measurement; discard the samples."
        )
    import molsysmt
    from molsysmt import _rust

    native = Path(_rust.__file__)
    report = dict(
        schema="molsysmt.get-vectors-benchmark@1",
        python=sys.version,
        platform=platform.platform(),
        logical_cpus=os.cpu_count(),
        source_commit=subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        source_dirty=bool(
            subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=ROOT, text=True
            )
        ),
        software_version=molsysmt.__version__,
        native_sha256=hashlib.sha256(native.read_bytes()).hexdigest(),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        source_sha256=before,
        cases=cases,
        limitations="Warm source-tree measurements, uncontrolled host load. RSS includes inputs and NumPy controls. No installed-candidate or speed-superiority claim.",
    )
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
