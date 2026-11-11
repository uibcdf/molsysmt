"""Check independent geometry and custody in the advisory native profile."""

import numpy as np
import pytest

from benchmarks.neighbor_kernel_profile import (
    _bounded_dims,
    _check,
    _grid_diagnostics,
    _load_baseline,
    _oracle,
)


def test_all_pairs_oracle_excludes_self_includes_cutoff_and_orders_ties():
    xyz = np.array(
        [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0], [3.0, 0.0, 0.0]]]
    )
    expected = (np.array([0, 2, 3, 4, 4]), np.array([1, 2, 0, 0]), np.ones(4))
    _check(_oracle(xyz, None, 1.0), expected)
    with pytest.raises(AssertionError):
        _check((expected[0], expected[1][::-1], expected[2]), expected)


@pytest.mark.parametrize("skew", [False, True])
def test_oracle_periodic_images_have_known_physical_distances(skew):
    box = (
        np.array([[2.0, 0.0, 0.0], [0.4, 1.8, 0.0], [0.2, 0.3, 1.5]])
        if skew
        else np.eye(3)
    )
    fractions = np.array([[[0.0, 0.0, 0.0], [0.9, 0.9 if skew else 0.0, 0.0]]])
    distance = 0.3 if skew else 0.1
    actual = _oracle(fractions @ box, box[None], distance + 0.01)
    _check(actual, (np.array([0, 1, 2]), np.array([1, 0]), np.full(2, distance)))


def test_coarsening_model_retains_last_maximum_tie_and_population_bound():
    np.testing.assert_array_equal(_bounded_dims([33, 33, 33], 1000), [16, 16, 8])
    for population in (1, 2, 10, 1000):
        dims = _bounded_dims([33, 50, 71], population)
        assert all(dims >= 1)
        assert np.prod(dims) <= 4 * population


def test_grid_model_distinguishes_extra_candidate_visits_from_occurrences():
    xyz = np.array([[[0.1, 0.0, 0.0], [0.9, 0.0, 0.0]]])
    model = _grid_diagnostics(xyz, np.eye(3)[None], 0.1)
    assert model["state"] == "source_model_not_native_instrumentation"
    row = model["structures"][0]
    assert row["baseline"]["heads"] == 1000
    assert row["current"]["heads"] == 8
    assert row["baseline"]["predicted_candidate_visits"] == 0
    assert row["current"]["predicted_candidate_visits"] == 2
    assert len(_oracle(xyz, np.eye(3)[None], 0.1)[1]) == 0


def test_unreviewed_extension_is_refused_before_native_loading(tmp_path):
    path = tmp_path / "_rust.abi3.so"
    path.write_bytes(b"not a reviewed executable")
    with pytest.raises(ValueError, match="reviewed digest"):
        _load_baseline(path)
