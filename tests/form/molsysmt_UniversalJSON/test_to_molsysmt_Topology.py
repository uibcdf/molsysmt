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
        "bonds": {"indexA": [0], "indexB": [1], "order": ["1"]},
        "coordinates": {"collections": [{"label": "default", "estructures": []}]},
    }
    return UniversalJSON(data=data)


def test_universaljson_to_topology():
    ujson = _universal_json()
    topo = convert(ujson, to_form="molsysmt.Topology")

    assert topo.atoms.shape[0] == 2
    assert topo.bonds.shape[0] == 1
    assert list(topo.bonds["atom1_index"]) == [0]
