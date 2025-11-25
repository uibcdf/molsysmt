import numpy as np

from molsysmt.native import ViewerJSON
from molsysmt import convert


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
        },
        "bonds": {"indexA": [0], "indexB": [1], "order": ["1"]},
        "estructures": [
            {"positions": [[0.5, 0.0, 0.0], [1.5, 0.0, 0.0]], "time": 1.0},
        ],
    }
    return ViewerJSON(data=data)


def test_viewerjson_to_structures():
    vjson = _viewer_json()
    structures = convert(vjson, to_form="molsysmt.Structures")

    coords = np.asarray(structures.coordinates.magnitude)
    assert coords.shape == (1, 2, 3)
    assert np.allclose(coords[0, 0], [0.5, 0.0, 0.0])
