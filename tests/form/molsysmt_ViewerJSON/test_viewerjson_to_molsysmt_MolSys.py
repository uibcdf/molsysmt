import numpy as np

from molsysmt.native import ViewerJSON, MolSys
from molsysmt.form.molsysmt_ViewerJSON import to_molsysmt_MolSys


def _viewer_json():
    data = {
        "version": "0.1",
        "atoms": {
            "atom_id": [0, 1],
            "atom_name": ["A", "B"],
            "group_id": [10, 10],
            "group_name": ["GRP", "GRP"],
            "chain_id": [1, 1],
            "entity_id": [100, 100],
            "element_symbol": ["C", "O"],
            "formal_charge": [0, 0],
        },
        "bonds": {
            "indexA": [0],
            "indexB": [1],
            "order": ["1"],
        },
        "estructures": [
            {"positions": [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]], "time": 0.0},
        ],
    }
    return ViewerJSON(data=data)


def test_viewerjson_to_molsys():
    vjson = _viewer_json()
    molsys = to_molsysmt_MolSys(vjson)

    assert isinstance(molsys, MolSys)
    assert molsys.topology.atoms.shape[0] == 2
    assert molsys.topology.bonds.shape[0] == 1
    coords = molsys.structures.coordinates
    assert coords is not None
    arr = np.asarray(coords.magnitude)
    assert arr.shape == (1, 2, 3)
    assert np.allclose(arr[0, 1], [1.0, 0.0, 0.0])
