import molsysmt as msm

from molsysmt.native import ViewerJSON
from molsysmt.form.molsysmt_ViewerJSON import to_molsysmt_MolSys


def test_viewerjson_to_molsys_preserves_bond_type_and_charges():
    viewer_json = ViewerJSON(data={
        "version": "0.1",
        "atoms": {
            "atom_id": ["0", "1"],
            "atom_name": ["N", "O"],
            "group_id": ["1", "1"],
            "group_name": ["LIG", "LIG"],
            "chain_id": ["1", "1"],
            "entity_id": ["1", "1"],
            "element_symbol": ["N", "O"],
            "formal_charge": [1, -1],
            "partial_charge": [0.25, -0.25],
        },
        "bonds": {
            "atom_pairs": [[0, 1]],
            "order": ["2"],
            "type": ["double"],
        },
        "structures": [],
    })

    molsys = to_molsysmt_MolSys(viewer_json)

    assert molsys.topology.bonds["bond_order"].tolist() == [2]
    assert "bond_type" not in molsys.topology.bonds
    assert molsys.molecular_mechanics.formal_charge.tolist() == [1, -1]
    assert molsys.molecular_mechanics.partial_charge.tolist() == [0.25, -0.25]
    assert msm.get(viewer_json, element="bond", bond_order=True) == ["2"]
    assert msm.get(viewer_json, element="bond", bond_type=True) == ["double"]
    assert msm.get(viewer_json, element="atom", partial_charge=True) == [0.25, -0.25]
