#!/usr/bin/env python3
"""Measure atom-scope and source-map costs for a large sparse analysis."""

from __future__ import annotations

import argparse
import json
import tempfile
import time
from pathlib import Path

import numpy as np

import molsysmt as msm
from molsysmt.native.molsys import _extend_interaction_atoms


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atoms", type=int, default=300_000)
    parser.add_argument("--structures", type=int, default=30_000)
    parser.add_argument("--added-atoms", type=int, default=100)
    args = parser.parse_args()
    if args.atoms < 2 or args.structures < 1 or args.added_atoms < 1:
        parser.error("atoms >= 2, structures >= 1, and added-atoms >= 1 are required")

    record = {
        "structure_index": args.structures - 1,
        "interaction_type": "pair",
        "participants": [
            {"role": "first", "atom_indices": [0]},
            {"role": "second", "atom_indices": [args.atoms - 1]},
        ],
    }
    start = time.perf_counter()
    result = msm.Interactions.from_records(
        [record],
        n_atoms=args.atoms,
        n_structures=args.structures,
        evaluated_structure_indices=[0, args.structures - 1],
        method="scope_probe",
    )
    build_s = time.perf_counter() - start
    base_bytes = result.numeric_nbytes
    start = time.perf_counter()
    extended = _extend_interaction_atoms(result, args.atoms + args.added_atoms)
    extend_s = time.perf_counter() - start
    expected_scope = np.arange(args.atoms, dtype=np.int64)
    if not np.array_equal(extended.evaluation_universe_indices, expected_scope):
        raise AssertionError("old atom universe was not preserved")
    if extended.query(atom_indices=[args.atoms]).n_interactions:
        raise AssertionError("new atom was incorrectly reported as evaluated")

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "scoped.h5i"
        start = time.perf_counter()
        extended.save(path)
        save_s = time.perf_counter() - start
        disk_bytes = path.stat().st_size
        start = time.perf_counter()
        loaded = msm.Interactions.load(path)
        load_s = time.perf_counter() - start
        if not np.array_equal(loaded.evaluation_universe_indices, expected_scope):
            raise AssertionError("atom search scope changed after HDF5 round trip")

    print(
        json.dumps(
            {
                "atoms": args.atoms,
                "structures": args.structures,
                "added_atoms": args.added_atoms,
                "observations": result.n_interactions,
                "base_numeric_bytes": base_bytes,
                "extended_numeric_bytes": extended.numeric_nbytes,
                "additional_numeric_bytes": extended.numeric_nbytes - base_bytes,
                "scope_array_bytes": extended.evaluation_universe_indices.nbytes,
                "standalone_disk_bytes": disk_bytes,
                "build_s": build_s,
                "extend_s": extend_s,
                "save_s": save_s,
                "load_s": load_s,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
