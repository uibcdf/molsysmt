import json

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.form.molsysmt_MolSys.to_molsysmt_ViewerJSON import (
    to_molsysmt_ViewerJSON,
)
from molsysmt.native import MolSys, ViewerJSON


def _minimal_topology():
    molsys = MolSys(
        n_atoms=2,
        n_groups=1,
        n_components=1,
        n_molecules=1,
        n_entities=1,
        n_chains=1,
        n_bonds=1,
    )
    topo = molsys.topology
    topo.atoms.loc[:, "atom_id"] = ["0", "1"]
    topo.atoms.loc[:, "atom_name"] = ["A", "B"]
    topo.atoms.loc[:, "group_index"] = [0, 0]
    molsys.chemical_states._set_component_indices([0, 0])
    topo.atoms.loc[:, "chain_index"] = [0, 0]

    topo.groups.loc[:, "group_id"] = ["10"]
    topo.groups.loc[:, "group_name"] = ["GRP"]
    topo.groups.loc[:, "group_type"] = ["type"]
    topo.groups.loc[:, "molecule_index"] = [0]

    topo.chains.loc[:, "chain_id"] = ["1"]
    topo.chains.loc[:, "chain_name"] = ["A"]
    topo.chains.loc[:, "chain_type"] = ["polymer"]

    topo.molecules.loc[:, "molecule_id"] = ["100"]
    topo.molecules.loc[:, "molecule_name"] = ["Mol"]
    topo.molecules.loc[:, "molecule_type"] = ["protein"]
    topo.molecules.loc[:, "entity_index"] = [0]

    topo.entities.loc[:, "entity_id"] = ["1000"]
    topo.entities.loc[:, "entity_name"] = ["Ent"]
    topo.entities.loc[:, "entity_type"] = ["polymer"]

    molsys.chemical_states.get_bonds().loc[0, "atom1_index"] = 0
    molsys.chemical_states.get_bonds().loc[0, "atom2_index"] = 1
    molsys.chemical_states.get_bonds().loc[0, "bond_order"] = 1

    return molsys


def test_topology_to_ViewerJSON():
    topo = _minimal_topology()
    viewer = to_molsysmt_ViewerJSON(topo)

    assert isinstance(viewer, ViewerJSON)
    data = viewer.data
    assert data["atoms"]["group_id"] == ["10", "10"]
    assert data["atoms"]["chain_id"] == ["1", "1"]
    assert data["bonds"]["indexA"] == [0]
    assert data["bonds"]["indexB"] == [1]
    assert data["structures"] == []


@pytest.mark.parametrize("with_bonds", [False, True])
def test_topology_export_has_json_scalars(with_bonds, tmp_path):
    """The producer supplies ordinary JSON data before any encoder runs."""
    topo = MolSys(n_atoms=3)
    if with_bonds:
        topo.chemical_states.add_bonds([[0, 1], [1, 2]])
        topo.chemical_states.get_bonds()["bond_order"] = pd.Series(
            [1, None], dtype="Int8"
        )
        topo.chemical_states.get_bonds()["bond_type"] = pd.Series(
            ["single", None], dtype="string"
        )
    viewer = msm.convert(topo, to_form="molsysmt.ViewerJSON")
    data = viewer.to_dict(copy=False)

    def check_json_types(value):
        assert type(value) in (dict, list, str, int, float, bool, type(None))
        if isinstance(value, dict):
            for key, child in value.items():
                assert type(key) is str
                check_json_types(child)
        elif isinstance(value, list):
            for child in value:
                check_json_types(child)

    check_json_types(data)
    expected = {
        "atom_pairs": [[0, 1], [1, 2]] if with_bonds else [],
        "order": [1, None] if with_bonds else [],
        "type": ["single", None] if with_bonds else [],
        "indexA": [0, 1] if with_bonds else [],
        "indexB": [1, 2] if with_bonds else [],
    }
    assert json.loads(json.dumps(data))["bonds"] == expected
    assert json.loads(viewer.dumps())["bonds"] == expected
    path = tmp_path / "viewer.json"
    viewer.dump(str(path))
    assert json.loads(path.read_text())["bonds"] == expected


def test_topology_export_normalizes_nullable_numpy_atom_fields():
    topo = _minimal_topology()
    topo.chemical_states._set_chemical_state_atom_attribute(
        "formal_charge", [np.int64(1), None]
    )
    viewer = msm.convert(topo, to_form="molsysmt.ViewerJSON")
    assert json.loads(viewer.dumps())["atoms"]["formal_charge"] == [1, None]


def test_stable_topology_projection_omits_chemical_edges():
    complete = _minimal_topology()
    projected = msm.convert(complete.topology, to_form="molsysmt.ViewerJSON")
    assert projected.data["bonds"]["indexA"] == []
    assert projected.data["bonds"]["indexB"] == []
    assert projected.data["atoms"]["group_id"] == ["10", "10"]
