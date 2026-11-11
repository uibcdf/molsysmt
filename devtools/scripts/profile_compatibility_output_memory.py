"""Measure bounded neighbor/contact representation examples without a search.

Run inside an OS memory limit on shared machines. Defaults stay below 100 MiB
of projection payload; tracemalloc and imported runtimes have separate costs.
Legacy formulas are frozen comparison controls, not runtime alternatives.
"""

import argparse
import gc
import json
import platform
import sys
import tracemalloc
from functools import partial
from hashlib import sha256
from importlib.metadata import version
from pathlib import Path
from statistics import median
from time import perf_counter

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt.structure._compatibility_output import (
    contact_pairs,
    neighbor_object_arrays,
)


def measure(operation):
    for _ in range(2):
        warmed = operation()
        del warmed
    elapsed = []
    for _ in range(5):
        gc.collect()
        start = perf_counter()
        timed = operation()
        elapsed.append(perf_counter() - start)
        del timed
    gc.collect()
    tracemalloc.start()
    try:
        output = operation()
        current, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return output, dict(
        additional_traced_current=current,
        additional_traced_peak=peak,
        untraced_projection_median_seconds=median(elapsed),
        untraced_projection_samples_seconds=elapsed,
    )


def profile():
    unit = puw.unit("nm")
    puw.quantity(np.empty(0), unit)
    samples = []
    for n_rows in (1000, 10000, 50000):
        offsets = np.arange(n_rows + 1, dtype=np.int64) * 3
        indices = np.tile(np.array([1, 2, 3], dtype=np.int64), n_rows)
        distances = np.full(3 * n_rows, 0.2)

        def legacy_neighbors(
            n_rows=n_rows, offsets=offsets, indices=indices, distances=distances
        ):
            neighbors = np.empty((1, n_rows), dtype=object)
            values = np.empty((1, n_rows), dtype=object)
            for row in range(n_rows):
                section = slice(offsets[row], offsets[row + 1])
                neighbors[0, row], values[0, row] = indices[section], distances[section]
            return neighbors, values * unit

        for mode in ("legacy", "current"):
            output, observation = measure(
                legacy_neighbors
                if mode == "legacy"
                else partial(
                    neighbor_object_arrays,
                    offsets,
                    indices,
                    distances,
                    unit,
                    (1, n_rows),
                    512 * 1024**2,
                    "compatibility memory profile",
                )
            )
            values = puw.get_value(output[1])
            assert output[0].shape == values.shape == (1, n_rows)
            np.testing.assert_array_equal(output[0][0, -1], [1, 2, 3])
            np.testing.assert_array_equal(values[0, -1], [0.2, 0.2, 0.2])
            samples.append(
                dict(
                    kind="neighbor_object_projection",
                    mode=mode,
                    rows=n_rows,
                    occurrences=3 * n_rows,
                    csr_payload_bytes=offsets.nbytes
                    + indices.nbytes
                    + distances.nbytes,
                    distance_rows_share_csr=bool(
                        np.shares_memory(values[0, 0], distances)
                    ),
                    **observation,
                )
            )
            del output, values

    for n_atoms in (16, 128, 512):
        matrix = np.ones((1, n_atoms, n_atoms), dtype=bool)
        for mapped in (False, True):
            labels = np.arange(n_atoms - 1, -1, -1) + 1000

            def legacy_pairs(matrix=matrix, mapped=mapped, labels=labels):
                pairs = np.nonzero(np.triu(matrix[0], k=1))
                pairs = np.column_stack(pairs).tolist()
                if mapped:
                    pairs = labels[pairs].tolist()
                return [pairs]

            for mode in ("legacy", "current"):
                output, observation = measure(
                    legacy_pairs
                    if mode == "legacy"
                    else partial(
                        contact_pairs,
                        matrix,
                        paired=False,
                        strict_upper=True,
                        atom_indices=labels,
                        atom_indices_2=None,
                        output_indices="atom" if mapped else "selection",
                        sorted_pairs=False,
                        budget=512 * 1024**2,
                        caller="compatibility memory profile",
                    )
                )
                assert len(output[0]) == n_atoms * (n_atoms - 1) // 2
                assert output[0][0] == (labels[[0, 1]].tolist() if mapped else [0, 1])
                samples.append(
                    dict(
                        kind="dense_self_contact_pairs",
                        mode=mode,
                        mapped=mapped,
                        atoms=n_atoms,
                        pairs=len(output[0]),
                        map_bytes=matrix.nbytes,
                        **observation,
                    )
                )
                del output
    paths = [
        "molsysmt/structure/" + name
        for name in ("_compatibility_output.py", "get_neighbors.py", "get_contacts.py")
    ]
    return dict(
        python=sys.version.split()[0],
        numpy=np.__version__,
        pyunitwizard=version("pyunitwizard"),
        pint=version("pint"),
        quantity_form=puw.get_form(unit),
        platform=platform.platform(),
        scope="tracemalloc of isolated Python projection; inputs allocated before tracing; not RSS or a search benchmark",
        timing_policy="two warmups; median of five untraced projection-only samples; GC collected before timing; result retirement excluded",
        source_sha256={
            name: sha256(Path(name).read_bytes()).hexdigest() for name in paths
        },
        samples=samples,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    result = profile()
    arguments.output.write_text(json.dumps(result, indent=2) + "\n")
    print(
        f"Recorded {len(result['samples'])} bounded projection samples in {arguments.output}"
    )
