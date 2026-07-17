"""Providing shared deterministic fixtures for form-adapter contracts."""

import numpy as np
import pytest


@pytest.fixture
def rich_universe():
    """Building a deterministic triclinic three-frame MDAnalysis Universe."""

    mda = pytest.importorskip("MDAnalysis")
    universe = mda.Universe.empty(
        4,
        n_residues=2,
        n_segments=1,
        atom_resindex=[0, 0, 1, 1],
        residue_segindex=[0, 0],
    )
    for attribute, values in (
        ("names", ["A0", "A1", "A2", "A3"]),
        ("types", ["C", "N", "O", "S"]),
        ("ids", [10, 11, 12, 13]),
        ("resnames", ["L1", "L2"]),
        ("resids", [7, 7]),
        ("segids", ["A"]),
    ):
        universe.add_TopologyAttr(attribute, values)
    universe.add_bonds([(0, 1), (1, 2), (2, 3)])

    coordinates = np.arange(3 * 4 * 3, dtype=np.float32).reshape(3, 4, 3)
    universe.load_new(
        coordinates,
        format=mda.coordinates.memory.MemoryReader,
        velocities=coordinates / 10.0,
        dimensions=np.asarray(
            [
                [20.0, 30.0, 40.0, 80.0, 90.0, 100.0],
                [21.0, 31.0, 41.0, 81.0, 91.0, 101.0],
                [22.0, 32.0, 42.0, 82.0, 92.0, 102.0],
            ],
            dtype=np.float32,
        ),
        dt=2.0,
        time_offset=5.0,
    )
    return universe
