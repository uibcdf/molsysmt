"""Execute the membrane lesson against registered local structural data."""

import json
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw

NOTEBOOK = (
    Path(__file__).parents[2]
    / "docs/content/course/Path_Biophysics/40_PBC_Geometry.ipynb"
)


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_membrane_course_executes_with_real_registered_boxes(unit):
    formats = pytest.importorskip("mdtraj.formats")
    notebook = json.loads(NOTEBOOK.read_text())
    scope = {}
    with puw.context(standard_units=[unit, "ps", "radians"]):
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                exec(compile("".join(cell["source"]), str(NOTEBOOK), "exec"), scope)
        box = puw.get_value(scope["box"], to_unit="nm")
        lengths = puw.get_value(scope["lengths"], to_unit="nm")
        angles = puw.get_value(scope["angles"], to_unit="degrees")
        volume = puw.get_value(scope["volume"], to_unit="nm**3")
    assert scope["molsys"] == [
        msm.systems["POPC membrane"]["popc_membrane.psf"],
        msm.systems["POPC membrane"]["popc_membrane.dcd"],
    ]
    indices = scope["structure_indices"]
    expected_lengths, expected_angles = [], []
    with formats.DCDTrajectoryFile(
        str(msm.systems["POPC membrane"]["popc_membrane.dcd"])
    ) as reader:
        for index in indices:
            reader.seek(index)
            _, cell_lengths, cell_angles = reader.read(n_frames=1)
            expected_lengths.append(cell_lengths[0] / 10)
            expected_angles.append(cell_angles[0])
    assert box.shape == (len(indices), 3, 3)
    assert np.isfinite(box).all() and np.all(volume > 0)
    np.testing.assert_allclose(lengths, expected_lengths, atol=5e-7)
    np.testing.assert_allclose(angles, expected_angles, atol=5e-5)
    np.testing.assert_allclose(volume, np.abs(np.linalg.det(box)), rtol=1e-6)
    np.testing.assert_allclose(volume, np.prod(lengths, axis=1), rtol=1e-6)
