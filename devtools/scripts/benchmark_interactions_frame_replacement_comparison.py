#!/usr/bin/env python3
"""Compare two frame-replacement implementations on identical sparse fixtures.

The reference implementation is loaded from a local git commit. Both paths call
private replacement kernels with already constructed valid operands. Each case
runs in a fresh worker; instrumented allocations and untraced timing samples are
reported separately. Coordinates, detection and disk IO are excluded.
"""

import argparse
import gc
import hashlib
import json
import platform
import statistics
import subprocess
import sys
import time
import types
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

from benchmark_interactions_frame_replacement import measured, patch
from benchmark_interactions_invalidation_memory import make_result

ROOT = Path(__file__).resolve().parents[2]
IMPLEMENTATION = "molsysmt/interactions/_frame_replacement.py"


def baseline(ref):
    source = subprocess.check_output(
        ["git", "show", f"{ref}:{IMPLEMENTATION}"], cwd=ROOT, text=True
    )
    module = types.ModuleType("molsysmt.interactions._benchmark_reference")
    module.__package__ = "molsysmt.interactions"
    exec(compile(source, f"{ref}:{IMPLEMENTATION}", "exec"), module.__dict__)
    return module._replace, hashlib.sha256(source.encode()).hexdigest()


def worker(ref, count, images, edits, novel, repeats):
    from molsysmt.interactions._frame_replacement import _replace

    reference, reference_hash = baseline(ref)
    # Warm imports and code paths; discard both warm-up analyses.
    for kernel in (reference, _replace):
        kernel(make_result(100, images), patch(images))
    source = make_result(count, images)
    source.query(atom_indices=[0])
    incoming = [
        patch(images, 0.31 + item * 0.001, relation_start=1000 if novel else 0)
        for item in range(edits)
    ]
    previous = source.query(structure_indices=[10])
    removed = previous.n_interactions

    def operation(kernel):
        current = source
        snapshots = []
        for fresh in incoming:
            current = kernel(current, fresh)
            snapshots.append(current)
        return snapshots

    allocations = {}
    for label, kernel in [("before", reference), ("after", _replace)]:
        snapshots, allocations[label] = measured(
            lambda kernel=kernel: operation(kernel)
        )
        current = snapshots[-1]
        observed = current.query(structure_indices=[10]).to_dict()
        assert current.n_interactions == count - removed + 10
        assert len(current._segments) == 2
        assert observed["structure_indices"].tolist() == [10] * 10
        assert all(
            value == 0.31 + (edits - 1) * 0.001
            for value in observed["measurements"]["distance"]
        )
        assert (
            current.parameters == source.parameters
            and current.software == source.software
        )
        assert previous.n_interactions == removed
        assert current._packed_result is None
        del current, snapshots
    # Alternate execution order to reduce systematic warm-up/order bias.
    samples = {"before": [], "after": []}
    kernels = [("before", reference), ("after", _replace)]
    for repeat in range(repeats):
        for label, kernel in kernels if repeat % 2 == 0 else kernels[::-1]:
            gc.collect()
            start = time.perf_counter()
            snapshots = operation(kernel)
            samples[label].append(time.perf_counter() - start)
            del snapshots
    return dict(
        occurrences=count,
        periodic_images=images,
        retained_snapshots=edits,
        novel_relations=novel,
        replacement_rows=10,
        allocation=allocations,
        untraced_seconds=samples,
        untraced_median_seconds={
            key: statistics.median(values) for key, values in samples.items()
        },
        reference_implementation_sha256=reference_hash,
        checks_passed=True,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--count", type=int, default=100_000)
    parser.add_argument("--images", action="store_true")
    parser.add_argument("--edits", type=int, default=1)
    parser.add_argument("--novel", action="store_true")
    parser.add_argument("--repeats", type=int, default=7)
    args = parser.parse_args()
    if args.worker:
        print(
            json.dumps(
                worker(
                    args.baseline,
                    args.count,
                    args.images,
                    args.edits,
                    args.novel,
                    args.repeats,
                )
            )
        )
        return
    cases = [
        (count, images, 1, False)
        for count in (100_000, 1_000_000)
        for images in (False, True)
    ]
    cases += [
        (1_000_000, True, 20, False),
        (1_000_000, True, 1, True),
        (1_000_000, True, 20, True),
    ]
    results = []
    for count, images, edits, novel in cases:
        command = [
            sys.executable,
            str(Path(__file__).resolve()),
            "--worker",
            "--baseline",
            args.baseline,
            "--count",
            str(count),
            "--edits",
            str(edits),
            "--repeats",
            str(args.repeats),
        ]
        if images:
            command.append("--images")
        if novel:
            command.append("--novel")
        output = subprocess.check_output(command, cwd=ROOT, text=True)
        results.append(json.loads(output))
    files = [
        IMPLEMENTATION,
        "molsysmt/interactions/_frame_validity.py",
        "molsysmt/interactions/result.py",
        "devtools/scripts/benchmark_interactions_frame_replacement.py",
        "devtools/scripts/benchmark_interactions_frame_replacement_comparison.py",
        "devtools/scripts/benchmark_interactions_invalidation_memory.py",
    ]
    report = dict(
        schema="molsysmt.interactions_frame_replacement_comparison@1",
        recorded_at=datetime.now(timezone.utc).isoformat(),
        baseline_ref=args.baseline,
        source_commit=subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        source_sha256={
            file: hashlib.sha256((ROOT / file).read_bytes()).hexdigest()
            for file in files
        },
        python=sys.version,
        platform=platform.platform(),
        versions={name: version(name) for name in ("molsysmt", "numpy")},
        description="Same operands; private kernels; base inverse index prebuilt; fresh workers; "
        "first registry index included in allocation; no coordinates/detector/disk IO; "
        "seven alternating untraced timing samples per version; snapshots retained during each run.",
        cases=results,
    )
    serialized = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(serialized)
    else:
        print(serialized)


if __name__ == "__main__":
    main()
