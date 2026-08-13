import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.argdigest.argument.box import digest_box
from molsysmt._private.argdigest.argument.box_lengths import digest_box_lengths
from molsysmt._private.argdigest.argument.coordinates import digest_coordinates


def test_digest_box_lengths_returns_nm_float64_array_for_pbc_callers():
    value = [[20.0, 20.0, 20.0]] * msm.pyunitwizard.unit("angstrom")

    output = digest_box_lengths(
        value,
        caller="molsysmt.pbc.get_box_from_lengths_and_angles.get_box_from_lengths_and_angles",
    )

    assert isinstance(output, np.ndarray)
    assert output.dtype == np.float64
    assert output.shape == (1, 3)
    assert np.allclose(output, [[2.0, 2.0, 2.0]])


def test_digest_box_returns_nm_float64_array_for_pbc_callers():
    value = [[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]] * msm.pyunitwizard.unit("angstrom")

    output = digest_box(
        value,
        caller="molsysmt.pbc.get_volume_from_box.get_volume_from_box",
    )

    assert isinstance(output, np.ndarray)
    assert output.dtype == np.float64
    assert output.shape == (1, 3, 3)
    assert np.allclose(output, [[[0.2, 0.0, 0.0], [0.0, 0.2, 0.0], [0.0, 0.0, 0.2]]])


def test_canonical_scientific_arrays_skip_general_dimensionality_check(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("general dimensionality checking is forbidden")

    monkeypatch.setattr(msm.pyunitwizard, "check", fail_if_called)

    lengths = digest_box_lengths(
        msm.pyunitwizard.quantity([2.0, 2.0, 2.0], "nm"),
        caller="molsysmt.pbc.get_box_from_lengths_and_angles.get_box_from_lengths_and_angles",
    )
    box = digest_box(
        msm.pyunitwizard.quantity(np.eye(3), "nm"),
        caller="molsysmt.pbc.get_volume_from_box.get_volume_from_box",
    )
    coordinates = digest_coordinates(
        msm.pyunitwizard.quantity(np.ones((4, 3)), "nm")
    )

    assert lengths.shape == (1, 3)
    assert box.shape == (1, 3, 3)
    assert msm.pyunitwizard.has_unit(coordinates, "nm") is True
    assert msm.pyunitwizard.get_value(coordinates).shape == (1, 4, 3)


def test_scientific_array_fast_paths_keep_wrong_unit_validation():
    wrong_lengths = msm.pyunitwizard.quantity([1.0, 2.0, 3.0], "ps")
    wrong_box = msm.pyunitwizard.quantity(np.eye(3), "ps")
    wrong_coordinates = msm.pyunitwizard.quantity(np.ones((4, 3)), "ps")

    with pytest.raises(ArgumentError):
        digest_box_lengths(
            wrong_lengths,
            caller="molsysmt.pbc.get_box_from_lengths_and_angles.get_box_from_lengths_and_angles",
        )
    with pytest.raises(ArgumentError):
        digest_box(
            wrong_box,
            caller="molsysmt.pbc.get_volume_from_box.get_volume_from_box",
        )
    with pytest.raises(ArgumentError):
        digest_coordinates(wrong_coordinates)
