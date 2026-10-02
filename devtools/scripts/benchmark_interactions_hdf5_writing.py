#!/usr/bin/env python3
"""Compare active-column HDF5 writing with the historical packing boundary.

Fresh workers exclude resident source construction from traced allocation.
Untraced timing samples and a separate allocation sample write different files;
logical dataset fingerprints verify equivalent codec content outside measurement.
"""

import argparse
import ast
import gc
import hashlib
import json
import platform
import subprocess
import sys
import tempfile
import time
import tracemalloc
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import h5py
import numpy as np
from benchmark_interactions_frame_replacement import patch
from benchmark_interactions_invalidation_memory import make_result, process_memory

ROOT = Path(__file__).resolve().parents[2]
SOURCES = (
    "molsysmt/interactions/result.py",
    "molsysmt/interactions/_hdf5_writer.py",
    "molsysmt/interactions/_frame_validity.py",
    "molsysmt/interactions/_execution_provenance.py",
)


def historical_writer(reference):
    content = subprocess.check_output(
        ["git", "show", f"{reference}:molsysmt/interactions/result.py"],
        cwd=ROOT,
        text=True,
    )
    tree = ast.parse(content)
    cls = next(
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "Interactions"
    )
    function = next(
        node
        for node in cls.body
        if isinstance(node, ast.FunctionDef) and node.name == "_write_group"
    )
    namespace = {"np": np, "json": json, "__package__": "molsysmt.interactions"}
    exec(
        compile(
            ast.Module(body=[function], type_ignores=[]),
            f"{reference}:result.py",
            "exec",
        ),
        namespace,
    )
    return namespace["_write_group"], hashlib.sha256(content.encode()).hexdigest()


def fingerprint(path):
    digest = hashlib.sha256()
    with h5py.File(path, "r") as file:

        def visit(name, item):
            digest.update(name.encode())
            digest.update(
                json.dumps(
                    dict(item.attrs), sort_keys=True, default=lambda value: value.item()
                ).encode()
            )
            if isinstance(item, h5py.Dataset):
                digest.update(str(item.shape).encode())
                digest.update(str(item.dtype).encode())
                for first in range(0, len(item), 8192):
                    values = item[first : first + 8192]
                    if values.dtype.kind == "O":
                        for value in values:
                            digest.update(
                                value if isinstance(value, bytes) else value.encode()
                            )
                            digest.update(b"\0")
                    else:
                        digest.update(values.tobytes())

        visit("", file)
        file.visititems(visit)
    return digest.hexdigest()


def worker(count, images, kind, variant, reference, samples):
    from molsysmt.interactions._frame_validity import _interchange_result

    old, old_hash = historical_writer(reference)

    def write(result, path):
        with h5py.File(path, "w") as file:
            if variant == "historical":
                with _interchange_result(result) as packed:
                    old(packed, file)
            else:
                result._write_group(file)

    with tempfile.TemporaryDirectory() as directory:
        warm = make_result(100, images).invalidate_structures([10])
        write(warm, Path(directory) / "warm.h5i")
        del warm
        source = make_result(count, images)
        result = source if kind == "packed" else source.invalidate_structures([10])
        if kind == "patched":
            result = result.replace_structures(patch(images))
        times = []
        for index in range(samples):
            gc.collect()
            start = time.perf_counter()
            write(result, Path(directory) / f"time-{index}.h5i")
            times.append(time.perf_counter() - start)
        gc.collect()
        before = process_memory()
        tracemalloc.start()
        path = Path(directory) / "allocation.h5i"
        try:
            write(result, path)
            live, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        after = process_memory()
        assert getattr(result, "_packed_result", None) is None
        return dict(
            input_occurrences=count,
            active_occurrences=result.n_interactions,
            atoms=result.n_atoms,
            structures=result.n_structures,
            periodic_images=images,
            representation=kind,
            writer=variant,
            untraced_seconds=times,
            median_seconds=float(np.median(times)),
            additional_traced_live_bytes=live,
            additional_traced_peak_bytes=peak,
            process_memory_before=before,
            process_memory_after=after,
            file_bytes=path.stat().st_size,
            logical_fingerprint=fingerprint(path),
            historical_source_sha256=old_hash,
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", default="59ec05b9a")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument(
        "--worker", nargs=4, metavar=("COUNT", "IMAGES", "KIND", "WRITER")
    )
    args = parser.parse_args()
    if args.samples < 1:
        parser.error("--samples must be positive")
    if args.worker:
        count, images, kind, variant = args.worker
        print(
            json.dumps(
                worker(
                    int(count),
                    bool(int(images)),
                    kind,
                    variant,
                    args.baseline,
                    args.samples,
                )
            )
        )
        return
    cases = []
    for count in (100_000, 1_000_000):
        for images in (False, True):
            for kind in ("packed", "filtered", "patched"):
                pair = []
                for variant in ("historical", "bounded"):
                    output = subprocess.check_output(
                        [
                            sys.executable,
                            str(Path(__file__).resolve()),
                            "--baseline",
                            args.baseline,
                            "--samples",
                            str(args.samples),
                            "--worker",
                            str(count),
                            str(int(images)),
                            kind,
                            variant,
                        ],
                        text=True,
                    )
                    pair.append(json.loads(output))
                assert pair[0]["logical_fingerprint"] == pair[1]["logical_fingerprint"]
                cases.extend(pair)
                print(
                    f"{count} {kind} images={images}: {pair[0]['additional_traced_peak_bytes']} -> {pair[1]['additional_traced_peak_bytes']} bytes",
                    flush=True,
                )
    report = dict(
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        baseline=args.baseline,
        working_reference=subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        methodology="Fresh workers; discarded small warm-up; separate untraced repeated writes and traced allocation write. Resident source and caches excluded from traced increment. Native HDF5 buffers and RSS are not fully measured by tracemalloc. Filesystem cache uncontrolled. Logical fingerprints verified outside timing.",
        environment=dict(
            python=sys.version,
            platform=platform.platform(),
            processor=platform.processor(),
            numpy=np.__version__,
            h5py=h5py.__version__,
            hdf5=h5py.version.hdf5_version,
            molsysmt=version("molsysmt"),
        ),
        source_sha256={
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in SOURCES
        },
        cases=cases,
    )
    if args.output is not None:
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    else:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
