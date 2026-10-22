"""Protect collection publication and distinguish chemistry from historical evidence."""

import copy
import pickle

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import MolSys
from tests.native.test_molsys_interactions import _analysis, _system


@pytest.fixture
def system():
    result = _system()
    result.interactions = {
        "pairs": _analysis(),
        "second": _analysis().invalidate_structures([0]),
    }
    return result


@pytest.mark.parametrize("initial", [0, 1, 2])
def test_append_invalidates_all_coverage_and_retains_old_snapshots(initial):
    system = _system()
    if initial == 0:
        system.topology._clear_chemical_states()
    elif initial == 2:
        system.chemical_states.append_state()
    previous = _analysis()
    system.interactions = {"pairs": previous, "second": previous.remap()}
    old_view = previous.query(structure_indices=[2, 0])
    states = system.chemical_states
    old_records = tuple(states._states)
    old_reference = states.reference_chemical_state_index

    assert states.append_state() == initial
    assert states.n_chemical_states == initial + 1
    assert states.reference_chemical_state_index == (
        0 if initial == 0 else old_reference
    )
    assert all(current is old for current, old in zip(states._states, old_records))
    assert system.topology._chemical_states_domain is states
    for result in system.interactions.values():
        assert result.evaluated_structure_indices.size == 0
        assert result.n_interactions == 0
        np.testing.assert_array_equal(
            result.atom_source_indices, previous.atom_source_indices
        )
        assert result.source_id == previous.source_id
    np.testing.assert_array_equal(previous.evaluated_structure_indices, [0, 1, 2])
    assert old_view.n_interactions == 1


def test_second_state_preserves_explicit_associations_but_does_not_infer_new_ones(
    system,
):
    system._set_structure_chemical_state_indices([0, None, 0])
    system.interactions = {"pairs": _analysis()}
    system.chemical_states.append_state()
    assert list(system._get_structure_chemical_state_indices()) == [0, pd.NA, 0]

    implicit = _system()
    assert list(implicit._get_structure_chemical_state_indices()) == [0, 0, 0]
    implicit.chemical_states.append_state()
    assert pd.isna(implicit._get_structure_chemical_state_indices()).all()


@pytest.mark.parametrize("failure", ["creation", "invalidation"])
def test_prepublication_allocation_failure_keeps_collection_and_analyses(
    system, failure, monkeypatch
):
    from molsysmt.native.topology import _ChemicalStateStorage

    records = system.chemical_states._states
    reference = system.chemical_states.reference_chemical_state_index
    analyses = dict(system.interactions)

    def failed(*args, **kwargs):
        raise MemoryError("Cannot prepare state publication")

    if failure == "creation":
        monkeypatch.setattr(_ChemicalStateStorage, "__init__", failed)
    else:
        monkeypatch.setattr(msm.Interactions, "invalidate_structures", failed)
    with pytest.raises(MemoryError, match="state publication"):
        system.chemical_states.append_state()
    assert system.chemical_states._states is records
    assert system.chemical_states.reference_chemical_state_index == reference
    assert all(system.interactions[name] is value for name, value in analyses.items())


def test_state_append_does_not_copy_existing_states_or_geometry(system, monkeypatch):
    from molsysmt.native._structure_array import _StructureArray
    from molsysmt.native.topology import _ChemicalStateStorage

    geometry = system.structures._coordinates
    original_state = system.chemical_states._states[0]

    def forbidden(*args, **kwargs):
        pytest.fail("Appending a state copied existing chemical or coordinate payloads")

    monkeypatch.setattr(_StructureArray, "_dense", forbidden)
    monkeypatch.setattr(_StructureArray, "_fork", forbidden)
    monkeypatch.setattr(_ChemicalStateStorage, "__deepcopy__", forbidden, raising=False)
    assert system.chemical_states.append_state() == 1
    assert system.chemical_states._states[0] is original_state
    assert system.structures._coordinates is geometry
    assert system.interactions["pairs"].evaluated_structure_indices.size == 0


@pytest.mark.parametrize("route", ["copy", "deepcopy", "pickle", "h5msm"])
def test_copied_or_restored_collection_notifies_only_its_own_system(
    system, route, tmp_path
):
    if route == "copy":
        duplicate = copy.copy(system)
    elif route == "deepcopy":
        duplicate = copy.deepcopy(system)
    elif route == "pickle":
        duplicate = pickle.loads(pickle.dumps(system))
    else:
        path = str(tmp_path / "collection.h5msm")
        msm.convert(system, to_form=path)
        duplicate = msm.convert(path, to_form="molsysmt.MolSys")
    duplicate.chemical_states.append_state()
    assert duplicate.interactions["pairs"].evaluated_structure_indices.size == 0
    assert duplicate.chemical_states.n_chemical_states == 2
    assert system.chemical_states.n_chemical_states == 1
    np.testing.assert_array_equal(
        system.interactions["pairs"].evaluated_structure_indices, [0, 1, 2]
    )


def test_standalone_collection_copy_is_detached(system):
    standalone = system.chemical_states.copy()
    standalone.append_state()
    assert standalone.n_chemical_states == 2
    assert system.chemical_states.n_chemical_states == 1
    np.testing.assert_array_equal(
        system.interactions["pairs"].evaluated_structure_indices, [0, 1, 2]
    )


def test_append_works_for_chemistry_and_interactions_without_structures():
    partial = MolSys._from_partial_domains(
        chemical_states=msm.ChemicalStates(n_atoms=3),
        interactions={"pairs": _analysis()},
    )
    assert partial.chemical_states.append_state() == 0
    assert partial.structures is None
    assert partial.chemical_states.n_chemical_states == 1
    assert partial.interactions["pairs"].evaluated_structure_indices.size == 0


@pytest.mark.parametrize("empty", [False, True])
def test_historical_evidence_does_not_change_chemistry_or_analysis_validity(
    system, empty
):
    previous = dict(system.interactions)
    record = {
        "schema": "molsysmt.preparation_record@1",
        "index_scope": "operation",
        "output": {"n_atoms": 3, "n_bonds": 0, "chemical_state_index": 0},
        "report": {"schema": "example.historical_operation@1", "values": [1]},
    }
    history = [] if empty else [record]
    indices = system.chemical_states.append_preparation_history(history)
    assert indices == (() if empty else (0,))
    assert all(system.interactions[name] is value for name, value in previous.items())
    assert system.chemical_states.n_chemical_states == 1
    if not empty:
        record["report"]["values"].append(2)
        assert system.chemical_states.get_preparation_history()[0]["report"][
            "values"
        ] == [1]


def test_repeated_appends_reuse_already_invalidated_analysis(system, monkeypatch):
    original = msm.Interactions.invalidate_structures
    calls = []

    def counted(self, structure_indices, **kwargs):
        calls.append(self)
        return original(self, structure_indices, **kwargs)

    monkeypatch.setattr(msm.Interactions, "invalidate_structures", counted)
    system.chemical_states.append_state()
    invalidated = dict(system.interactions)
    system.chemical_states.append_state()
    assert len(calls) == len(invalidated)
    assert all(
        system.interactions[name] is value for name, value in invalidated.items()
    )
