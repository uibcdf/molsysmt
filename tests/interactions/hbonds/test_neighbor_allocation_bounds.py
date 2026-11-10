"""Legacy detector consumers retain empty coverage with tiny valid cutoffs."""

import numpy as np
import pytest

import molsysmt as msm
from tests.interactions.hbonds.test_buch_results import _varying_system


@pytest.mark.parametrize("name", ["get_buch_hbonds", "get_luzard_chandler_hbonds"])
def test_tiny_cutoff_preserves_empty_detector_shapes_and_evaluated_structures(name):
    source = _varying_system()
    detector = getattr(msm.interactions.hbonds, name)
    result = detector(
        source, structure_indices=[2, 0, 2, 1], distance_threshold="0.001 nm", pbc=False
    )
    assert result[0].shape == (4, 0, 3)
    for values in result[1:]:
        assert values.shape == (4, 0)
    analysis = detector(
        source,
        structure_indices=[2, 0, 2, 1],
        distance_threshold="0.001 nm",
        pbc=False,
        output_type="molsysmt.Interactions",
    )
    assert analysis.n_interactions == 0
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [2, 0, 1])
    assert analysis.query(structure_indices=[1]).n_interactions == 0
