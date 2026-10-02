#!/usr/bin/env python3
"""Compare explicit compaction with the existing full-query packing boundary."""

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
from pathlib import Path

import numpy as np
from benchmark_interactions_frame_replacement import patch
from benchmark_interactions_invalidation_memory import make_result, process_memory

ROOT = Path(__file__).resolve().parents[2]
SOURCES = ("molsysmt/interactions/result.py", "molsysmt/interactions/_compaction.py",
           "molsysmt/interactions/_hdf5_writer.py", "molsysmt/interactions/_frame_validity.py",
           "molsysmt/interactions/_frame_replacement.py", "molsysmt/interactions/_execution_provenance.py")


def packed(source):
    from molsysmt.interactions._frame_validity import _interchange_result

    with _interchange_result(source) as result:
        return result


def fingerprint(result):
    digest = hashlib.sha256()
    for name in ("evaluated_structure_indices", "occurrence_structures", "occurrence_relations",
                 "occurrence_evidence", "occurrence_image_offsets", "image_vectors"):
        value = getattr(result, name)
        digest.update(name.encode())
        digest.update(b"None" if value is None else value.tobytes())
    for name, values in result.measurements.items():
        digest.update(name.encode())
        digest.update(values.tobytes())
    for record in result.execution_records:
        digest.update(record["structure_indices"].tobytes())
        digest.update(json.dumps(record["details"], sort_keys=True).encode())
    return digest.hexdigest()


def worker(count, images, kind, variant, samples):
    operation = packed if variant == "projection" else lambda source: source.compact()
    operation(make_result(100, images).invalidate_structures([10]))
    base = make_result(count, images)
    source = base.invalidate_structures(np.arange(0, 10_000, 2))
    if kind == "patched":
        source = source.replace_structures(patch(images))
    timings = []
    for _ in range(samples):
        gc.collect()
        start = time.perf_counter()
        result = operation(source)
        timings.append(time.perf_counter() - start)
        del result
    gc.collect()
    before = process_memory()
    tracemalloc.start()
    try:
        result = operation(source)
        live, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    after = process_memory()
    assert source._packed_result is None
    assert result.n_interactions == source.n_interactions
    assert not hasattr(result, "_segments") and not hasattr(result, "_root")
    return dict(input_occurrences=count, active_occurrences=result.n_interactions,
                atoms=source.n_atoms, structures=source.n_structures, periodic_images=images,
                representation=kind, method=variant, untraced_seconds=timings,
                median_seconds=float(np.median(timings)), additional_traced_live_bytes=live,
                additional_traced_peak_bytes=peak, numeric_before_bytes=source.numeric_nbytes,
                numeric_after_bytes=result.numeric_nbytes, process_memory_before=before,
                process_memory_after=after, active_fingerprint=fingerprint(result))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--worker", nargs=4)
    args = parser.parse_args()
    if args.samples < 1:
        parser.error("--samples must be positive")
    if args.worker:
        count, images, kind, variant = args.worker
        print(json.dumps(worker(int(count), bool(int(images)), kind, variant, args.samples)))
        return
    cases = []
    for count in (100_000, 1_000_000):
        for images in (False, True):
            for kind in ("filtered", "patched"):
                pair = [json.loads(subprocess.check_output([
                    sys.executable, str(Path(__file__).resolve()), "--samples", str(args.samples),
                    "--worker", str(count), str(int(images)), kind, variant], text=True))
                        for variant in ("projection", "compact")]
                assert pair[0]["active_fingerprint"] == pair[1]["active_fingerprint"]
                cases.extend(pair)
                print(f"{count} {kind} images={images}: {pair[0]['additional_traced_peak_bytes']} -> {pair[1]['additional_traced_peak_bytes']} bytes", flush=True)
    report = dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),
                  working_reference=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                  methodology="Fresh worker for each case/variant. Discarded warm-up. Separate repeated untraced timings and traced allocation sample. Inputs excluded; destination retained in traced live allocation. Half the frame indices invalidated, one frame restored in patched cases. Constant measures and zero images are synthetic. No coordinates or disk IO. RSS/lifetime HWM are not isolated allocation peaks. Active column/provenance fingerprints compared outside measurement.",
                  environment=dict(python=sys.version, platform=platform.platform(), numpy=np.__version__),
                  source_sha256={name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in SOURCES},
                  cases=cases)
    if args.output is not None:
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    else:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
