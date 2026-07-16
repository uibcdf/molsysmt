"""Regression tests for MDTraj XTC box-vector delivery."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import systems


md = pytest.importorskip("mdtraj")


def test_box_uses_xtc_box_vectors_instead_of_step_values():
    path = systems["nglview"]["md_1u19.xtc"]
    structure_indices = [0, 25, 50]
    with md.formats.XTCTrajectoryFile(str(path), mode="r") as handle:
        expected = handle.read()[3][structure_indices]

    observed = msm.get(
        path,
        element="system",
        structure_indices=structure_indices,
        box=True,
    )

    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(observed, to_unit="nm"),
        expected,
        rtol=0.0,
        atol=1.0e-7,
    )
