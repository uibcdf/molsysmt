import numpy as np

from molsysmt.native import ViewerJSON
from molsysmt import convert, get


def _viewer_json():
    data = {
        "version": "0.1",
        "atoms": {
            "atom_id": ["0", "1"],
            "atom_name": ["A", "B"],
            "group_id": ["10", "10"],
            "group_name": ["GRP", "GRP"],
            "chain_id": ["1", "1"],
            "entity_id": ["100", "100"],
        },
        "bonds": {"atom_pairs": [[0, 1]], "order": ["1"]},
        "structures": [],
    }
    return ViewerJSON(data=data)


def test_viewerjson_to_topology():
    vjson = _viewer_json()
    topo = convert(vjson, to_form="molsysmt.Topology")

    assert topo.atoms.shape[0] == 2
    assert topo.bonds.shape[0] == 1
    assert list(topo.atoms["group_index"]) == [0, 0]


def test_get_uses_native_attribute_pipes():
    vjson = _viewer_json()

    atom_indices, atom_ids, group_names = get(
        vjson,
        element='atom',
        atom_index=True,
        atom_id=True,
        group_name=True,
    )

    assert atom_indices == [0, 1]
    assert atom_ids == ['0', '1']
    assert group_names == ['GRP', 'GRP']
