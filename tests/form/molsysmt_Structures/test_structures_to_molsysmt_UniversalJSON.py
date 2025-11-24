import numpy as np

from molsysmt.native import MolSys, UniversalJSON
from molsysmt import pyunitwizard as puw
from molsysmt.form.molsysmt_Structures import to_molsysmt_UniversalJSON


def _minimal_structures():
    molsys = MolSys(n_atoms=2, n_bonds=0)
    coords = puw.quantity(np.array([[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]]), "nanometer")
    times = puw.quantity(np.array([0.5]), "picosecond")
    box = puw.quantity(np.array([np.eye(3)]), "nanometer")

    molsys.structures.coordinates = coords
    molsys.structures.time = times
    molsys.structures.box = box
    return molsys.structures

def test_structures_to_UniversalJSON():
    structures = _minimal_structures()
    ujson = to_molsysmt_UniversalJSON(structures)

    assert isinstance(ujson, UniversalJSON)
    frames = ujson.data["coordinates"]["collections"][0]["frames"]
    assert len(frames) == 1
    assert np.allclose(np.array(frames[0]["positions"]), [[0, 0, 0], [1, 0, 0]])
