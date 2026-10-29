"""Protect independent chemical storage and legacy trusted-pickle recovery."""

import hashlib
import json
import pickle
from pathlib import Path

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
