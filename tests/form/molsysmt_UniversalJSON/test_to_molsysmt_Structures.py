import numpy as np

from molsysmt.native import UniversalJSON
from molsysmt import convert


def _universal_json():
    data = {
        "version": "0.1",
        "topology": {
            "atoms": {
                "atom_id": ["0", "1"],
                "atom_name": ["A", "B"],
                "group_id": ["10", "10"],
                "group_name": ["GRP", "GRP"],
                "chain_id": ["1", "1"],
                "entity_id": ["100", "100"],
            }
        },
        "bonds": {"atom_pairs": [[0, 1]], "order": ["1"]},
        "coordinates": {
            "collections": [
                {
                    "label": "default",
                    "structures": [
                        {
                            "coordinates": [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
                            "time": 2.0,
                            "box": {"v0": [1.0, 0.0, 0.0], "v1": [0.0, 1.0, 0.0], "v2": [0.0, 0.0, 1.0]},
                        }
                    ],
                }
            ]
        },
    }
    return UniversalJSON(data=data)


def test_universaljson_to_structures():
    ujson = _universal_json()
    structures = convert(ujson, to_form="molsysmt.Structures")

    coords = np.asarray(structures.coordinates.magnitude)
    assert coords.shape == (1, 2, 3)
    assert np.isclose(coords[0, 1, 0], 1.0)
    assert np.allclose(np.asarray(structures.box.magnitude)[0], np.eye(3))
