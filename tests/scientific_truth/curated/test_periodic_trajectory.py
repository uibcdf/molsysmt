"""Scientific agreement tests on a curated periodic trajectory."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import systems


md = pytest.importorskip("mdtraj")
pytest.importorskip("MDAnalysis")
import MDAnalysis as mda
from MDAnalysis.lib.distances import calc_bonds


def test_multiframe_mic_distances_agree_with_both_oracles(external_float32_atol):
    """Compare boundary-spanning CA pairs in three trajectory frames."""

    gro = systems["nglview"]["md_1u19.gro"]
    xtc = systems["nglview"]["md_1u19.xtc"]
    structure_indices = [0, 25, 50]
    pairs = np.array([[226, 5538], [248, 5538], [226, 5514]], dtype=np.int64)

    trajectory = md.load(str(xtc), top=str(gro))
    expected_mdtraj = md.compute_distances(
        trajectory[structure_indices],
        pairs,
        periodic=True,
        opt=False,
    )

    universe = mda.Universe(str(gro), str(xtc))
    expected_mda = np.stack(
        [
            calc_bonds(
                universe.trajectory[index].positions[pairs[:, 0]],
                universe.trajectory[index].positions[pairs[:, 1]],
                box=universe.trajectory[index].dimensions,
            )
            / 10.0
            for index in structure_indices
        ]
    )

    observed = msm.structure.get_distances(
        [gro, xtc],
        selection=pairs,
        structure_indices=structure_indices,
        pairs=True,
        pbc=True,
        heavy_mode="off",
        use_gpu=False,
    )
    observed = msm.pyunitwizard.get_value(observed, to_unit="nm")

    for expected in (expected_mdtraj, expected_mda):
        np.testing.assert_allclose(
            observed,
            expected,
            rtol=0.0,
            atol=external_float32_atol,
        )
