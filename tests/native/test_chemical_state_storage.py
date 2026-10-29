"""Protect independent chemical storage and legacy trusted-pickle recovery."""

import hashlib
import json
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm

_DATA = Path(__file__).with_name("data")


def _legacy_states():
    """Load only the trusted fixture generated before the storage move."""
    payload = (_DATA / "chemical_states_before_separation.pkl").read_bytes()
    metadata = json.loads(
        (_DATA / "chemical_states_before_separation.json").read_text()
    )
    assert hashlib.sha256(payload).hexdigest() == metadata["sha256"]
    assert len(payload) == metadata["bytes"]
    assert b"molsysmt.native.topology" in payload
    return pickle.loads(payload)


def _forbid_topology_storage(monkeypatch):
    from molsysmt.native import topology

    def forbidden(*args, **kwargs):
        pytest.fail("Independent chemical storage used a Topology storage gateway")

    for name in ("Bonds_DataFrame", "Components_DataFrame", "_ChemicalStateStorage"):
        monkeypatch.setattr(topology, name, forbidden, raising=False)
    for name in ("_coerce_bond_table", "_remap_bond_atom_indices"):
        monkeypatch.setattr(
            topology.Topology, name, staticmethod(forbidden), raising=False
        )


def test_old_pickle_resolves_one_canonical_chemical_storage_owner():
    from molsysmt.native import _chemical_state, topology

    states = _legacy_states()
    assert states.n_atoms == 3
    assert states.n_chemical_states == 2
    assert states.reference_chemical_state_index == 0
    assert type(states._states[0]) is _chemical_state._ChemicalStateStorage
    assert type(states.get_bonds()) is _chemical_state.Bonds_DataFrame
    assert topology._ChemicalStateStorage is _chemical_state._ChemicalStateStorage
    assert topology.Bonds_DataFrame is _chemical_state.Bonds_DataFrame
    assert topology.Components_DataFrame is _chemical_state.Components_DataFrame
    assert states.get_bonds(chemical_state=0)[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [[0, 1], [1, 2]]
    assert states._states[1].atom_attributes.formal_charge.tolist() == [1, -1, 0]


def test_standalone_creation_growth_and_copy_do_not_use_topology_storage(monkeypatch):
    _forbid_topology_storage(monkeypatch)
    states = msm.ChemicalStates(n_atoms=3)
    assert states.n_chemical_states == 0
    assert states.append_state() == 0
    states._extend_atom_domain(5)
    clone = states.copy()
    assert clone.n_atoms == 5
    assert clone.append_state() == 1
    assert states.n_chemical_states == 1
    assert states.get_bonds().empty
    assert states._states[0].component_indices.isna().all()
    assert states._states[0].connectivity_completeness == "unavailable"


def test_typed_codec_does_not_use_topology_storage(monkeypatch):
    states = _legacy_states()
    _forbid_topology_storage(monkeypatch)
    encoded = msm.convert(states, to_form="molsysmt.ChemicalStatesDict")
    restored = msm.convert(encoded, to_form="molsysmt.ChemicalStates")
    assert restored.n_chemical_states == 2
    assert restored.get_bonds(chemical_state=1)[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [[0, 1]]
    assert restored._states[1].atom_attributes.formal_charge.tolist() == [1, -1, 0]
    assert restored._states[1].component_indices.tolist() == [0, 0, 1]
    assert restored._states[1].components.component_id.tolist() == [
        "split-0",
        "split-1",
    ]


def test_atom_restriction_does_not_use_topology_normalizers(monkeypatch):
    states = _legacy_states()
    _forbid_topology_storage(monkeypatch)
    extracted = states._extract_atoms([2, 1])
    assert extracted.n_atoms == 2
    assert extracted.n_chemical_states == 2
    assert extracted.get_bonds(chemical_state=0)[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [[0, 1]]
    assert extracted.get_bonds(chemical_state=1).empty
    assert extracted._states[1].atom_attributes.formal_charge.tolist() == [0, -1]
    assert states.n_atoms == 3
    assert states.get_bonds(chemical_state=0).shape[0] == 2


def test_empty_collection_codec_does_not_synthesize_a_state(monkeypatch):
    _forbid_topology_storage(monkeypatch)
    empty = msm.ChemicalStates(n_atoms=3)
    payload = msm.convert(empty, to_form="molsysmt.ChemicalStatesDict")
    restored = msm.convert(payload, to_form="molsysmt.ChemicalStates")
    assert restored.n_atoms == 3
    assert restored.n_chemical_states == 0
    assert restored.reference_chemical_state_index is None


def test_owned_concatenation_preserves_typed_sparse_bond_metadata(monkeypatch):
    from molsysmt.native._chemical_state import _concatenate_bond_tables

    states = _legacy_states()
    first = states.get_bonds(chemical_state=0).copy(deep=True)
    second = states.get_bonds(chemical_state=1).copy(deep=True)
    second["atom1_index"] += 3
    second["atom2_index"] += 3
    first["is_conjugated"] = pd.array([True, pd.NA], dtype="boolean")
    second["is_conjugated"] = pd.array([pd.NA], dtype="boolean")
    first["bond_id"] = pd.array(["one", None], dtype="string")
    second["bond_id"] = pd.array(["one"], dtype="string")
    original = first.copy(deep=True)
    _forbid_topology_storage(monkeypatch)
    output = _concatenate_bond_tables(first, second)
    assert output[["atom1_index", "atom2_index"]].values.tolist() == [
        [0, 1],
        [1, 2],
        [3, 4],
    ]
    assert output.is_conjugated.tolist() == [True, pd.NA, pd.NA]
    assert str(output.is_conjugated.dtype) == "boolean"
    assert str(output.bond_order.dtype) == "UInt8"
    assert output.bond_id.tolist() == ["one", pd.NA, "one"]
    pd.testing.assert_frame_equal(first, original)


def test_complete_induced_graph_splits_components_without_topology(monkeypatch):
    states = _legacy_states()
    original_components = states._states[0].components.copy(deep=True)
    original_membership = states._states[0].component_indices.copy(deep=True)
    _forbid_topology_storage(monkeypatch)
    result = states._extract_atoms([2, 0])
    state = result._states[0]
    assert state.bonds.empty
    assert state.component_indices.tolist() == [0, 1]
    assert state.components.component_id.tolist() == ["0", "1"]
    assert state.components.component_name.isna().all()
    assert state.components.component_type.isna().all()
    assert state.component_completeness == "complete"
    assert state.component_evidence == "inferred"
    pd.testing.assert_frame_equal(states._states[0].components, original_components)
    pd.testing.assert_series_equal(
        states._states[0].component_indices, original_membership
    )


def test_complete_restriction_retains_labels_only_for_full_source_atom_sets():
    states = _legacy_states()
    result = states._extract_atoms([2, 0])
    state = result._states[1]
    assert state.component_indices.tolist() == [0, 1]
    assert state.components.component_id.tolist() == ["split-1", "1"]
    assert state.components.component_name.iloc[0] == "part-1"
    assert pd.isna(state.components.component_name.iloc[1])
    assert state.atom_attributes.formal_charge.tolist() == [0, 1]
    assert (
        result.reference_chemical_state_index == states.reference_chemical_state_index
    )


@pytest.mark.parametrize("connectivity", ["partial", "unavailable"])
def test_incomplete_graph_restricts_declarations_without_inventing_a_partition(
    connectivity,
):
    states = _legacy_states()
    source = states._states[0]
    source.connectivity_completeness = connectivity
    result = states._extract_atoms([2, 0])._states[0]
    assert result.component_indices.tolist() == [0, 0]
    pd.testing.assert_frame_equal(result.components, source.components)
    assert result.connectivity_completeness == connectivity
    assert result.component_completeness == "partial"
    assert result.component_evidence == source.component_evidence
    assert source.component_completeness == "complete"


def test_removing_whole_components_preserves_complete_declarations_with_partial_graph():
    states = _legacy_states()
    source = states._states[1]
    source.connectivity_completeness = "partial"
    result = states._extract_atoms([2])._states[1]
    assert result.component_indices.tolist() == [0]
    assert result.components.component_id.tolist() == ["split-1"]
    assert result.component_completeness == "complete"


@pytest.mark.parametrize("selection", [[], [2, 1, 0]])
def test_complete_restriction_handles_empty_and_reordered_domains(selection):
    states = _legacy_states()
    result = states._extract_atoms(selection)
    assert result.n_atoms == len(selection)
    assert result.n_chemical_states == 2
    state = result._states[0]
    assert len(state.components) == (1 if selection else 0)
    assert state.component_indices.tolist() == ([0, 0, 0] if selection else [])
    if selection:
        assert (
            state.components.component_id.tolist()
            == states._states[0].components.component_id.tolist()
        )
    assert state.component_completeness == "complete"


@pytest.mark.parametrize(
    "corruption", ["unknown_length", "row_labels", "negative", "outside"]
)
def test_invalid_source_membership_rejects_without_legacy_repair(corruption):
    states = _legacy_states()
    state = states._states[0]
    if corruption == "unknown_length":
        state.component_indices = pd.Series([pd.NA], dtype="Int64")
    elif corruption == "row_labels":
        state.component_indices.index = [2, 1, 0]
    else:
        state.component_indices.iloc[0] = -1 if corruption == "negative" else 100
    original = state.component_indices.copy(deep=True)
    with pytest.raises(msm.StructuralInconsistencyError):
        states._extract_atoms([0, 2])
    pd.testing.assert_series_equal(state.component_indices, original)


def test_extraction_never_normalizes_its_source_in_place(monkeypatch):
    from molsysmt.native._chemical_state import _ChemicalStateStorage

    states = _legacy_states()
    original = _ChemicalStateStorage._ensure_compatibility

    def guard(record, n_atoms):
        if any(record is source for source in states._states):
            pytest.fail("Extraction tried to repair its source record")
        return original(record, n_atoms)

    monkeypatch.setattr(_ChemicalStateStorage, "_ensure_compatibility", guard)
    result = states._extract_atoms(np.array([2, 0], dtype=np.int64))
    assert result._states[0].component_indices.tolist() == [0, 1]


def _directional_stereo_state():
    """Declare an analytical four-atom graph with endpoint-local references."""
    from molsysmt.native._chemical_state import Components_DataFrame, _coerce_bond_table

    states = msm.ChemicalStates(n_atoms=4)
    states.append_state()
    state = states._states[0]
    state.bonds = _coerce_bond_table(
        pd.DataFrame(
            {
                "atom1_index": [0, 0, 1],
                "atom2_index": [1, 2, 3],
                "bond_order": [2, 1, 1],
                "bond_type": ["covalent"] * 3,
                "stereochemistry": ["E", None, None],
                "stereo_atom1_index": [2, None, None],
                "stereo_atom2_index": [3, None, None],
                "donor_atom_index": [0, None, None],
                "acceptor_atom_index": [1, None, None],
            }
        ),
        n_atoms=4,
    )
    state.components = Components_DataFrame(n_components=1)
    state.components["component_id"] = pd.array(["alkene"], dtype="string")
    state.component_indices = pd.Series([0, 0, 0, 0], dtype="Int64")
    state.connectivity_completeness = "complete"
    state.component_completeness = "complete"
    state.component_evidence = "explicit"
    return states


def test_reversed_endpoints_remap_stereo_neighbors_and_directional_atom_roles(tmp_path):
    states = _directional_stereo_state()
    original = states.get_bonds().copy(deep=True)
    result = states._extract_atoms([1, 0, 3, 2])
    edge = result.get_bonds().iloc[0]
    assert edge[["atom1_index", "atom2_index"]].tolist() == [0, 1]
    assert edge[["stereo_atom1_index", "stereo_atom2_index"]].tolist() == [2, 3]
    assert edge[["donor_atom_index", "acceptor_atom_index"]].tolist() == [1, 0]
    assert edge.stereochemistry == "E"
    assert result._states[0].components.component_id.tolist() == ["alkene"]
    assert result._states[0].component_evidence == "explicit"
    pd.testing.assert_frame_equal(states.get_bonds(), original)

    from molsysmt.native import MolSys

    source = MolSys._from_partial_domains(chemical_states=states)
    selected = msm.extract(source, selection=[1, 0, 3, 2])
    assert selected.topology is None
    pd.testing.assert_frame_equal(
        selected.chemical_states.get_bonds(), result.get_bonds()
    )
    filename = msm.convert(selected, to_form=str(tmp_path / "ordered_chemistry.h5msm"))
    restored = msm.convert(filename, to_form="molsysmt.MolSys")
    assert restored.topology is None
    pd.testing.assert_frame_equal(
        restored.chemical_states.get_bonds(), result.get_bonds()
    )
    assert restored.chemical_states._states[0].components.component_id.tolist() == [
        "alkene"
    ]
    pd.testing.assert_frame_equal(states.get_bonds(), original)


def test_missing_stereo_neighbor_clears_both_references_without_inventing_a_replacement():
    states = _directional_stereo_state()
    result = states._extract_atoms([0, 1, 2])
    edge = result.get_bonds().iloc[0]
    assert {"stereochemistry", "stereo_atom1_index", "stereo_atom2_index"}.isdisjoint(
        result.get_bonds().columns
    )
    assert edge[["donor_atom_index", "acceptor_atom_index"]].tolist() == [0, 1]
    assert states.get_bonds().iloc[0].stereochemistry == "E"


def test_component_participation_override_is_respected_during_restriction():
    from molsysmt.native._chemical_state import _coerce_bond_table

    states = _legacy_states()
    state = states._states[0]
    bonds = state.bonds.copy(deep=True)
    bonds["joins_components"] = pd.array([False, True], dtype="boolean")
    bonds["evidence"] = pd.array(["explicit", "explicit"], dtype="string")
    state.bonds = _coerce_bond_table(bonds, n_atoms=3)
    result = states._extract_atoms([0, 1, 2])._states[0]
    assert result.component_indices.tolist() == [0, 1, 1]
    assert result.components.component_name.isna().all()
    assert result.component_completeness == "complete"


@pytest.mark.parametrize(
    "change",
    ["reference", "state_order", "charge", "labels", "evidence", "atom_domain"],
)
def test_owned_inventory_comparison_is_strict_and_does_not_use_topology(
    change, monkeypatch
):
    states = _legacy_states()
    other = states.copy()
    _forbid_topology_storage(monkeypatch)
    assert states._inventory_equals(other)
    if change == "reference":
        other._set_reference_index(1)
    elif change == "state_order":
        other._states.reverse()
    elif change == "charge":
        other._states[1].set_atom_attribute("formal_charge", 2, atom_indices=[0])
    elif change == "labels":
        other._states[1].components.loc[0, "component_id"] = "other"
    elif change == "evidence":
        other._states[0].component_evidence = "user_defined"
    else:
        other._extend_atom_domain(4)
    assert not states._inventory_equals(other)
    assert not other._inventory_equals(states)
    assert states.reference_chemical_state_index == 0
    assert states.n_atoms == 3


def test_empty_chemical_inventory_comparison_never_selects_a_state():
    states = msm.ChemicalStates(n_atoms=3)
    assert states._inventory_equals(states.copy())
    assert not states._inventory_equals(msm.ChemicalStates(n_atoms=4))
    assert not states._inventory_equals(None)
