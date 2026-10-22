import json

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import FormatError
from molsysmt.native import MolSys, ViewerJSON


def _labeled_system():
    molsys = MolSys(
        n_atoms=6, n_groups=3, n_components=3, n_molecules=3, n_entities=2, n_chains=2
    )
    topo = molsys.topology
    topo.atoms["atom_id"] = ["007", "C", "2", "99", "-1", "B"]
    topo.atoms["atom_name"] = ["C1", "O1", "O2", "H2", "N1", "H1"]
    topo.atoms["atom_type"] = ["C", "O", "O", "H", "N", "H"]
    topo.atoms["group_index"] = [0, 0, 1, 1, 2, 2]
    topo.atoms["chain_index"] = [0, 0, 1, 1, 1, 1]
    topo._set_component_indices([0, 0, 1, 1, 2, 2])
    topo.groups["group_id"] = ["010", "010", "X"]
    topo.groups["group_name"] = ["LIG", "WAT", "ION"]
    topo.groups["molecule_index"] = [0, 1, 2]
    topo.molecules["entity_index"] = [0, 0, 1]
    topo.entities["entity_id"] = ["protein-A", "009"]
    topo.chains["chain_id"] = ["A", "B"]
    molsys.structures.coordinates = msm.pyunitwizard.quantity(
        np.arange(18, dtype=float).reshape(1, 6, 3), "nm"
    )
    return molsys


def test_generated_payload_preserves_string_ids_and_positional_membership():
    source = _labeled_system()
    payload = msm.convert(source, to_form="molsysmt.ViewerJSON")
    restored = msm.convert(
        ViewerJSON(data=json.loads(payload.dumps())), to_form="molsysmt.MolSys"
    )
    topo = restored.topology
    assert topo.atoms["atom_id"].tolist() == ["007", "C", "2", "99", "-1", "B"]
    assert topo.atoms["atom_type"].tolist() == ["C", "O", "O", "H", "N", "H"]
    assert topo.atoms["group_index"].tolist() == [0, 0, 1, 1, 2, 2]
    assert topo.atoms["chain_index"].tolist() == [0, 0, 1, 1, 1, 1]
    assert topo.groups["group_id"].tolist() == ["010", "010", "X"]
    assert topo.groups["group_name"].tolist() == ["LIG", "WAT", "ION"]
    assert topo.groups["molecule_index"].tolist() == [0, 1, 2]
    assert topo.molecules["entity_index"].tolist() == [0, 0, 1]
    assert topo.entities["entity_id"].tolist() == ["protein-A", "009"]
    assert topo.chains["chain_id"].tolist() == ["A", "B"]
    for table, column in [
        (topo.atoms, "atom_id"),
        (topo.groups, "group_id"),
        (topo.components, "component_id"),
        (topo.molecules, "molecule_id"),
        (topo.entities, "entity_id"),
        (topo.chains, "chain_id"),
    ]:
        assert str(table[column].dtype) == "string"
        assert all(isinstance(value, str) for value in table[column])
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(restored.structures.coordinates, to_unit="nm"),
        np.arange(18).reshape(1, 6, 3),
    )


def test_generated_indices_distinguish_duplicate_labels_within_one_chain():
    source = _labeled_system()
    source.topology.chains["chain_id"] = ["A", "A"]
    source.topology.atoms["chain_index"] = [0, 0, 0, 0, 1, 1]
    source.topology.entities["entity_id"] = ["E", "E"]
    payload = msm.convert(source, to_form="molsysmt.ViewerJSON")
    assert payload.data["atoms"]["group_index"] == [0, 0, 1, 1, 2, 2]
    assert payload.data["atoms"]["chain_index"] == [0, 0, 0, 0, 1, 1]
    assert payload.data["atoms"]["entity_index"] == [0, 0, 0, 0, 1, 1]
    restored = msm.convert(payload, to_form="molsysmt.MolSys").topology
    assert restored.groups["group_id"].tolist() == ["010", "010", "X"]
    assert restored.chains["chain_id"].tolist() == ["A", "A"]
    assert restored.entities["entity_id"].tolist() == ["E", "E"]


def test_legacy_labels_are_strings_and_group_ids_are_scoped_by_chain():
    payload = msm.convert(_labeled_system(), to_form="molsysmt.ViewerJSON")
    for field in ["group_index", "chain_index", "entity_index"]:
        payload.data["atoms"].pop(field, None)
    topo = msm.convert(payload, to_form="molsysmt.Topology")
    assert topo.atoms["group_index"].tolist() == [0, 0, 1, 1, 2, 2]
    assert topo.groups["group_name"].tolist() == ["LIG", "WAT", "ION"]
    assert topo.groups["group_id"].tolist() == ["010", "010", "X"]
    assert topo.chains["chain_id"].tolist() == ["A", "B"]


@pytest.mark.parametrize("field", ["group_index", "chain_index", "entity_index"])
@pytest.mark.parametrize("indices", [[0], [-1] * 6, [False] * 6, [0.5] * 6])
def test_invalid_axis_indices_are_rejected(field, indices):
    payload = msm.convert(_labeled_system(), to_form="molsysmt.ViewerJSON")
    payload.data["atoms"][field] = indices
    with pytest.raises(FormatError, match=field):
        msm.convert(payload, to_form="molsysmt.MolSys")


def test_conflicting_labels_for_one_explicit_index_are_rejected():
    payload = msm.convert(_labeled_system(), to_form="molsysmt.ViewerJSON")
    payload.data["atoms"]["group_id"][1] = "OTHER"
    with pytest.raises(FormatError, match="group_id"):
        msm.convert(payload, to_form="molsysmt.MolSys")


def test_reported_builder_with_alphabetic_chain_round_trips():
    builder = msm.MolSysBuilder()
    builder.add_atom(atom_name="C", atom_type="C")
    builder.add_group([0], group_name="LIG", group_id="10")
    builder.add_chain(group_indices=[0], chain_id="A")
    builder.set_coordinates(msm.pyunitwizard.quantity([[[0.0, 0.0, 0.0]]], "nm"))
    payload = msm.convert(builder.build(), to_form="molsysmt.ViewerJSON")
    restored = msm.convert(payload, to_form="molsysmt.MolSys")
    assert restored.topology.chains["chain_id"].tolist() == ["A"]
    assert restored.topology.groups["group_id"].tolist() == ["10"]
    assert restored.topology.atoms["chain_index"].tolist() == [0]


def test_sparse_axes_keep_source_order_when_atoms_are_reordered():
    payload = msm.convert(_labeled_system(), to_form="molsysmt.ViewerJSON")
    # This payload has only three atoms and two nonconsecutive group positions.
    selected = [5, 1, 0]
    payload.data["atoms"] = {
        key: [values[i] for i in selected] if values else []
        for key, values in payload.data["atoms"].items()
    }
    payload.data["structures"] = []
    topo = msm.convert(payload, to_form="molsysmt.Topology")
    assert topo.groups["group_id"].tolist() == ["010", "X"]
    assert topo.atoms["group_index"].tolist() == [1, 0, 0]
    assert topo.atoms["chain_index"].tolist() == [1, 0, 0]
    assert topo.molecules["entity_index"].tolist() == [0, 1]


def test_legacy_conflicting_group_names_require_positional_identity():
    payload = msm.convert(_labeled_system(), to_form="molsysmt.ViewerJSON")
    payload.data["atoms"].pop("group_index")
    payload.data["atoms"]["chain_index"] = [0] * 6
    payload.data["atoms"]["chain_id"] = ["A"] * 6
    with pytest.raises(FormatError, match="group_name"):
        msm.convert(payload, to_form="molsysmt.MolSys")


def test_empty_payload_has_no_invented_hierarchy():
    topo = msm.convert(ViewerJSON(), to_form="molsysmt.Topology")
    assert (topo.n_atoms, topo.n_groups, topo.n_chains, topo.n_entities) == (0, 0, 0, 0)


def test_components_follow_stored_connectivity_across_group_boundaries():
    payload = msm.convert(_labeled_system(), to_form="molsysmt.ViewerJSON")
    payload.data["bonds"] = {"atom_pairs": [[0, 1], [1, 2]], "order": [1, 1]}
    topo = msm.convert(payload, to_form="molsysmt.Topology")
    assert topo._get_component_indices().tolist() == [0, 0, 0, 1, 2, 3]
    assert topo.components["component_id"].tolist() == ["0", "1", "2", "3"]


def test_legacy_numeric_labels_normalize_to_strings_and_null_stays_unknown():
    payload = ViewerJSON(
        data={
            "atoms": {
                "atom_id": [101, 203],
                "atom_name": ["C", "O"],
                "group_id": [10, 10],
                "chain_id": [9, 9],
                "entity_id": [None, None],
            }
        }
    )
    topo = msm.convert(payload, to_form="molsysmt.Topology")
    assert topo.atoms["atom_id"].tolist() == ["101", "203"]
    assert topo.groups["group_id"].tolist() == ["10"]
    assert topo.chains["chain_id"].tolist() == ["9"]
    assert topo.n_entities == 0
    assert topo.molecules["entity_index"].isna().all()
