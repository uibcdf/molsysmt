#!/usr/bin/env python3
"""Measure immutable frame replacement separately from packing and index creation.

Coordinates and disk writes are excluded. Workers use fresh processes and the
same sparse trajectory fixture as the frame-invalidation memory qualification.
"""

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
from importlib.metadata import version
from pathlib import Path

from benchmark_interactions_invalidation_memory import make_result

ROOT = Path(__file__).resolve().parents[2]


def patch(images, value=.31, relation_start=0):
    from molsysmt import Interactions

    return Interactions.from_records([
        dict(structure_index=10, interaction_type='hbond', participants=[
            dict(role=role, atom_indices=[3 * relation + item])
            for item, role in enumerate(('donor', 'hydrogen', 'acceptor'))],
            evidence='synthetic_geometry', measurements={'distance': value, 'angle': 2.9},
            **({'images': [[0, 0, 0]] * 3} if images else {}))
        for relation in range(relation_start, relation_start + 10)], n_atoms=100_000, n_structures=10_000,
        evaluated_structure_indices=[10], measure_units={'distance': 'nm', 'angle': 'radian'},
        method='synthetic_memory_probe', software={'molsysmt': version('molsysmt')})


def measured(operation):
    gc.collect()
    tracemalloc.start()
    start = time.perf_counter()
    result = operation()
    elapsed = time.perf_counter() - start
    live, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, dict(seconds=elapsed, additional_live_bytes=live, additional_peak_bytes=peak)


def worker(count, images, edits):
    make_result(100, images).replace_structures(patch(images))  # Discard warm-up.
    source = make_result(count, images)
    source.query(atom_indices=[0])  # Build the unchanged base's inverse index.
    incoming = [patch(images, .31 + item * .001) for item in range(edits)]
    old_count = source.query(structure_indices=[10]).n_interactions

    def replace():
        current = source
        snapshots = []
        for fresh in incoming:
            current = current.replace_structures(fresh)
            snapshots.append(current)
        return snapshots

    snapshots, allocation = measured(replace)
    current = snapshots[-1]
    visible, frame_query = measured(lambda: current.query(structure_indices=[10]).to_dict())
    atom, first_atom_query = measured(lambda: current.query(atom_indices=[0]).to_dict())
    _, warm_atom_query = measured(lambda: current.query(atom_indices=[0]).to_dict())
    assert current._packed_result is None
    assert current.n_interactions == count - old_count + 10
    assert visible['occurrence_indices'].size == 10
    assert atom['occurrence_indices'].size > 0
    assert len(current._segments) == 2
    _, packing = measured(lambda: current.occurrence_structures)
    assert current.occurrence_structures.size == current.n_interactions
    return dict(occurrences=count, periodic_images=images, retained_snapshots=edits,
                replacement_rows=10, original_frame_rows=old_count,
                replacement=allocation, visible_frame_query=frame_query,
                first_atom_query=first_atom_query, warm_atom_query=warm_atom_query,
                complete_column_materialization=packing, checks_passed=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--worker', action='store_true')
    parser.add_argument('--count', type=int, default=100_000)
    parser.add_argument('--images', action='store_true')
    parser.add_argument('--edits', type=int, default=1)
    args = parser.parse_args()
    if args.worker:
        print(json.dumps(worker(args.count, args.images, args.edits)))
        return
    cases = []
    for count, images, edits in [(count, images, 1) for count in (100_000, 1_000_000)
                                 for images in (False, True)] + [(1_000_000, True, 20)]:
        command = [sys.executable, str(Path(__file__).resolve()), '--worker', '--count', str(count),
                   '--edits', str(edits)] + (['--images'] if images else [])
        completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=True)
        cases.append(json.loads(completed.stdout))
    files = ['molsysmt/interactions/result.py', 'molsysmt/interactions/_frame_validity.py',
             'molsysmt/interactions/_frame_replacement.py',
             'devtools/scripts/benchmark_interactions_frame_replacement.py',
             'devtools/scripts/benchmark_interactions_invalidation_memory.py']
    report = dict(schema='molsysmt.interactions_frame_replacement_benchmark@1',
                  recorded_at=datetime.now(timezone.utc).isoformat(),
                  source_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                  source_sha256={path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in files},
                  python=sys.version, platform=platform.platform(),
                  versions={name: version(name) for name in ('molsysmt', 'numpy')},
                  description='Fresh workers; 100k atoms, 10k frames, 1000 relations; '
                              'warm-up discarded; prebuilt base atom index; patch inputs built before tracing; '
                              'no coordinates/disk IO; first patch index and full packing measured separately.',
                  cases=cases)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    else:
        print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
