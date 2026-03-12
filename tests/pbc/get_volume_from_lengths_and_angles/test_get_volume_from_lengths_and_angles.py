import numpy as np

import molsysmt as msm


def test_get_volume_from_lengths_and_angles_returns_expected_nm3_volume():
    lengths = [[2.0, 2.0, 2.0]] * msm.pyunitwizard.unit("nm")
    angles = [[90.0, 90.0, 90.0]] * msm.pyunitwizard.unit("degrees")

    volume = msm.pbc.get_volume_from_lengths_and_angles(lengths, angles)

    assert np.allclose(msm.pyunitwizard.get_value(volume, to_unit="nm**3"), [8.0])


def test_get_volume_from_lengths_and_angles_avoids_repeated_length_normalization(monkeypatch):
    call_count = {"n": 0}
    original = msm.pyunitwizard.to_nanometers

    def counted(value, parser=None):
        call_count["n"] += 1
        return original(value, parser=parser)

    monkeypatch.setattr(msm.pyunitwizard, "to_nanometers", counted)

    lengths = [[20.0, 20.0, 20.0]] * msm.pyunitwizard.unit("angstrom")
    angles = [[90.0, 90.0, 90.0]] * msm.pyunitwizard.unit("degrees")

    volume = msm.pbc.get_volume_from_lengths_and_angles(lengths, angles)

    assert np.allclose(msm.pyunitwizard.get_value(volume, to_unit="nm**3"), [8.0])
    assert call_count["n"] == 2
