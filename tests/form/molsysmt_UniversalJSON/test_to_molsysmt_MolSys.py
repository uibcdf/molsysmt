import numpy as np

from molsysmt.native import UniversalJSON, MolSys
from molsysmt.form.molsysmt_UniversalJSON import to_molsysmt_MolSys


def _universal_json():
    data = {
        "version": "0.1",
        "topology": {
            "atoms": {
                "atom_id": [0, 1],
                "atom_name": ["A", "B"],
                "group_id": [10, 10],
                "group_name": ["GRP", "GRP"],
                "chain_id": [1, 1],
                "entity_id": [100, 100],
            }
        },
        "bonds": {"indexA": [0], "indexB": [1], "order": ["1"]},
        "coordinates": {
            "collections": [
                {"label": "default", "frames": [{"positions": [[0, 0, 0], [1, 0, 0]], "time": 0.0}]}
            ]
        },
    }
    return UniversalJSON(data=data)


def test_universaljson_to_molsys():
    ujson = _universal_json()
    molsys = to_molsysmt_MolSys(ujson)

    assert isinstance(molsys, MolSys)
    assert molsys.topology.atoms.shape[0] == 2
    assert molsys.topology.bonds.shape[0] == 1
    coords = np.asarray(molsys.structures.coordinates.magnitude)
    assert coords.shape == (1, 2, 3)
    assert np.allclose(coords[0, 1], [1.0, 0.0, 0.0])
