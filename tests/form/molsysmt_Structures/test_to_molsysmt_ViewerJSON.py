import numpy as np

from molsysmt.native import MolSys, ViewerJSON
from molsysmt import pyunitwizard as puw
from molsysmt.form.molsysmt_Structures.to_molsysmt_ViewerJSON import to_molsysmt_ViewerJSON


def _minimal_structures():
    molsys = MolSys(n_atoms=2, n_bonds=0)
    coords = puw.quantity(np.array([[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]]), "nanometer")
    times = puw.quantity(np.array([0.5]), "picosecond")
    box = puw.quantity(np.array([np.eye(3)]), "nanometer")

    molsys.structures.coordinates = coords
    molsys.structures.time = times
    molsys.structures.box = box
    return molsys.structures


def test_structures_to_ViewerJSON():
    structures = _minimal_structures()
    viewer = to_molsysmt_ViewerJSON(structures)

    assert isinstance(viewer, ViewerJSON)
    frame = viewer.data["structures"][0]
    assert np.allclose(np.array(frame["coordinates"]), [[0, 0, 0], [1, 0, 0]])
    assert frame["time"] == 0.5
    assert frame["box"]["v0"] == [1.0, 0.0, 0.0]
    assert frame["box"]["v1"] == [0.0, 1.0, 0.0]
    assert frame["box"]["v2"] == [0.0, 0.0, 1.0]
