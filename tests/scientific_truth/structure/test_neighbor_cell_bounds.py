"""Small physical pairs remain complete after population-bounded grid coarsening."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import Structures


@pytest.mark.parametrize("periodic", [False, True])
def test_sparse_small_cutoff_retains_known_pairs_and_periodic_images(periodic):
    box = np.array([[3.0, 0, 0], [0.7, 3.0, 0], [0.4, 0.6, 3.0]])
    a = np.array([0.01, 0.01, 0.01])
    c = a + [1.0, 1.0, 1.0]
    coordinates = np.array(
        [a, a + [0.0004, 0, 0], c, c + [0, 0.0006, 0], a + box[0] - [0.0007, 0, 0]]
    )
    source = Structures(
        coordinates=msm.pyunitwizard.quantity(coordinates[None], "nm"),
        box=msm.pyunitwizard.quantity(box[None], "nm") if periodic else None,
    )
    neighbors = msm.structure.get_neighbors(
        source, threshold="0.001 nm", pbc=periodic, output_type="csr"
    )
    expected = [[(1, 0.0004)], [(0, 0.0004)], [(3, 0.0006)], [(2, 0.0006)], []]
    if periodic:
        expected[0].append((4, 0.0007))
        expected[4].append((0, 0.0007))
    matrix = np.eye(5, dtype=bool)[None]
    for atom, pairs in enumerate(expected):
        span = slice(neighbors[0][atom], neighbors[0][atom + 1])
        np.testing.assert_array_equal(neighbors[1][span], [i for i, _ in pairs])
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(neighbors[2][span], to_unit="nm"),
            [d for _, d in pairs],
            rtol=0,
            atol=2e-13,
        )
        for index, _ in pairs:
            matrix[0, atom, index] = True
    contacts = msm.structure.get_contacts(
        source, threshold="0.001 nm", pbc=periodic, cell_list=True, use_gpu=False
    )
    np.testing.assert_array_equal(contacts, matrix)
