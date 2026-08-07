import numpy as np

import molsysmt as msm
from molsysmt._private.argdigest.argument.box import digest_box
from molsysmt._private.argdigest.argument.box_lengths import digest_box_lengths


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
