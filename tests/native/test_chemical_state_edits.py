"""Exercise controlled selected-state edits without Topology chemical gateways."""

import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import Topology
from tests.native import test_chemical_domain_separation as contract_fixtures

states = contract_fixtures.states
system = contract_fixtures.system


def _analysis(system):
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=3,
        n_structures=4,
        evaluated_structure_indices=[0, 2],
        method="controlled_selected_state_edit",
    )
    system.interactions = {"control": analysis}
    return analysis


@pytest.mark.parametrize(
    "method,arguments",
    [
        ("add_bonds", ([[0, 1]],)),
        ("remove_bonds", ()),
        ("rebuild_components", ()),
    ],
)
def test_empty_collection_edits_never_create_an_implicit_state(method, arguments):
    collection = msm.ChemicalStates(n_atoms=3)
    with pytest.raises(StructuralInconsistencyError, match="unavailable"):
        getattr(collection, method)(*arguments)
    assert collection.n_chemical_states == 0


@pytest.mark.parametrize(
    "method,arguments",
    [
        ("add_bonds", ([],)),
        ("remove_bonds", ([],)),
        ("rebuild_components", ()),
    ],
)
def test_ambiguous_reference_and_invalid_state_reject_before_editing(
    states, method, arguments
):
    states._set_reference_index(None)
    before = states.get_bonds(chemical_state=1)
    with pytest.raises(StructuralInconsistencyError):
        getattr(states, method)(*arguments)
    with pytest.raises(StructuralInconsistencyError):
        getattr(states, method)(*arguments, chemical_state=9)
    assert states.reference_chemical_state_index is None
    assert states.get_bonds(chemical_state=1) is before


@pytest.mark.parametrize("selector", [True, -1, 1.0, "structure", "split"])
def test_native_edits_reject_nonpositional_or_structure_scoped_state_selectors(
    states, selector
):
    before = states.get_bonds(chemical_state=1)
    with pytest.raises(ArgumentError):
        states.remove_bonds(0, chemical_state=selector)
    assert states.get_bonds(chemical_state=1) is before


@pytest.mark.parametrize(
    "pairs",
    [
        True,
        [0, 1],
        [[0, 1.0]],
        [[False, 1]],
        [[0, 1, 2]],
        [[-1, 1]],
        [[0, 3]],
        [[0, 0]],
        [[0, 1]],
        [[1, 2], [2, 1]],
    ],
)
def test_invalid_addition_preserves_graph_components_and_analyses(system, pairs):
    analysis = _analysis(system)
    state = system.chemical_states._states[1]
    before = (state.bonds, state.components, state.component_indices)
    with pytest.raises((ArgumentError, StructuralInconsistencyError)):
        system.chemical_states.add_bonds(pairs, chemical_state=1)
    assert all(
        current is original
        for current, original in zip(
            (state.bonds, state.components, state.component_indices), before
        )
    )
    assert system.interactions["control"] is analysis


@pytest.mark.parametrize("indices", [True, [False], [0.0], [[0]], -1, 1, "bond-label"])
def test_removal_indices_use_only_the_selected_states_bond_domain(system, indices):
    analysis = _analysis(system)
    before = system.chemical_states.get_bonds(chemical_state=1)
    with pytest.raises((ArgumentError, StructuralInconsistencyError)):
        system.chemical_states.remove_bonds(indices, chemical_state=1)
    assert system.chemical_states.get_bonds(chemical_state=1) is before
    assert system.interactions["control"] is analysis


@pytest.mark.parametrize("method,argument", [("add_bonds", []), ("remove_bonds", [])])
def test_empty_edits_preserve_table_and_analysis_identity(system, method, argument):
    analysis = _analysis(system)
    state = system.chemical_states._states[1]
    before = (state.bonds, state.components, state.component_indices)
    assert getattr(system.chemical_states, method)(argument, chemical_state=1) is None
    assert all(
        current is original
        for current, original in zip(
            (state.bonds, state.components, state.component_indices), before
        )
    )
    assert system.interactions["control"] is analysis


def test_removing_duplicate_positions_is_idempotent_and_complete_empty_graph_stays_known(
    states,
):
    assert states.remove_bonds([0, 0], chemical_state=1) is None
    state = states._states[1]
    assert state.bonds.empty
    assert state.component_indices.tolist() == [0, 1, 2]
    assert state.component_completeness == "complete"
    assert state.connectivity_completeness == "complete"
    assert states.get_bonds(chemical_state=0).shape[0] == 2


def test_no_stored_bonds_do_not_imply_complete_connectivity_or_components(monkeypatch):
    from molsysmt.native import _chemical_edits

    def unnecessary(*args, **kwargs):
        pytest.fail("Rebuilding all labels tried to match discarded metadata")

    monkeypatch.setattr(_chemical_edits, "unchanged_rows", unnecessary)
    states = msm.ChemicalStates(n_atoms=3)
    states.append_state()
    states.remove_bonds()
    assert states._states[0].component_completeness == "unavailable"
    states.rebuild_components()
    assert states._states[0].component_indices.tolist() == [0, 1, 2]
    assert states._states[0].component_completeness == "partial"
    assert states._states[0].connectivity_completeness == "unavailable"
    assert states._states[0].components.component_type.isna().all()
    assert states._states[0].components.component_name.isna().all()


@pytest.mark.parametrize("stage", ["partition", "invalidation"])
def test_failure_before_publication_preserves_all_selected_state_fields(
    system, monkeypatch, stage
):
    from molsysmt._private import rust_backend

    analysis = _analysis(system)
    state = system.chemical_states._states[1]
    before = (state.bonds, state.components, state.component_indices)
    geometry = system.structures._coordinates

    def failed(*args, **kwargs):
        raise MemoryError("Cannot stage chemical edit")

    if stage == "partition":
        monkeypatch.setattr(
            rust_backend, "get_component_index_from_bonded_atom_pairs", failed
        )
    else:
        monkeypatch.setattr(msm.Interactions, "invalidate_structures", failed)
    with pytest.raises(MemoryError, match="stage chemical"):
        system.chemical_states.add_bonds([[1, 2]], chemical_state=1)
    assert all(
        current is original
        for current, original in zip(
            (state.bonds, state.components, state.component_indices), before
        )
    )
    assert system.interactions["control"] is analysis
    assert system.structures._coordinates is geometry


def test_successful_edit_retains_assignments_history_reference_and_structure_map(
    system,
):
    original = system.chemical_states._states[0]
    selected = system.chemical_states._states[1]
    attributes, history = selected.atom_attributes, selected._preparation_history
    mapping = system._structure_chemical_state_indices.copy()
    geometry = system.structures._coordinates
    analysis = _analysis(system)
    old_table = selected.bonds
    system.chemical_states.add_bonds([[1, 2]], chemical_state=1)
    assert system.chemical_states._states[0] is original
    assert selected.atom_attributes is attributes
    assert selected._preparation_history is history
    assert selected.component_indices.tolist() == [0, 0, 0]
    assert selected.bonds.shape[0] == 2
    assert len(old_table) == 1
    assert system.chemical_states.reference_chemical_state_index == 0
    pd.testing.assert_extension_array_equal(
        system._structure_chemical_state_indices, mapping
    )
    assert system.structures._coordinates is geometry
    assert system.interactions["control"].evaluated_structure_indices.size == 0
    assert analysis.evaluated_structure_indices.tolist() == [0, 2]


def test_reconstruction_preserves_only_exact_full_component_labels(states):
    states._states[1].components["component_name"] = pd.Series(
        ["first", "second"], dtype=object
    )
    before = states._states[1].components.copy(deep=True)
    states.rebuild_components(False, False, False, False, force=True, chemical_state=1)
    pd.testing.assert_frame_equal(states._states[1].components, before)
    states._states[1].bonds = states._states[1].bonds.iloc[:0].copy()
    states.rebuild_components(True, False, False, False, chemical_state=1)
    result = states._states[1].components
    assert result.iloc[:2].isna().all(axis=None)
    assert result.iloc[2].tolist() == before.iloc[1].tolist()


def test_label_only_reconstruction_retains_occurrences_and_evidence(system):
    analysis = _analysis(system)
    state = system.chemical_states._states[1]
    state.components["component_id"] = ["first", "second"]
    system.chemical_states.rebuild_components(
        False, True, False, False, chemical_state=1
    )
    assert state.components.component_id.tolist() == ["0", "1"]
    assert state.component_evidence == "explicit"
    assert system.interactions["control"] is analysis


def test_explicit_stable_context_does_not_read_or_modify_topology_chemistry(
    states, monkeypatch
):
    topology = Topology(n_atoms=3, n_groups=2)
    topology.atoms["group_index"] = pd.array([0, 0, 1], dtype="Int64")
    topology.groups["group_name"] = ["ALA", "HOH"]
    topology.groups["group_type"] = pd.array([None, None], dtype="string")
    before = topology.groups.copy(deep=True)

    def forbidden(*args, **kwargs):
        pytest.fail("Component labeling traversed Topology chemistry")

    for name in (
        "_get_component_indices",
        "_resolve_chemical_state",
        "_get_chemical_state_bonds",
    ):
        monkeypatch.setattr(topology, name, forbidden)
    states.rebuild_components(chemical_state=1, topology=topology)
    assert states._states[1].components.component_type.tolist() == ["peptide", "water"]
    assert states._states[1].components.component_name.tolist() == [
        "peptide 0",
        "water",
    ]
    pd.testing.assert_frame_equal(topology.groups, before)


@pytest.mark.parametrize(
    "option,value",
    [
        ("force", 1),
        ("force", "yes"),
        ("redefine_ids", 1),
        ("redefine_types", None),
        ("redefine_names", "yes"),
        ("topology", "unknown"),
    ],
)
def test_reconstruction_validates_native_flags_and_context(states, option, value):
    with pytest.raises(ArgumentError):
        states.rebuild_components(**{option: value})


def test_mismatched_context_rejects_without_changing_state(states):
    before = states._states[0].components
    with pytest.raises(StructuralInconsistencyError, match="same atom domain"):
        states.rebuild_components(topology=Topology(n_atoms=4))
    assert states._states[0].components is before


@pytest.mark.parametrize(
    "method,value", [("add_bonds", [[1, 2]]), ("remove_bonds", [0])]
)
def test_index_inputs_never_accept_physical_units(states, method, value):
    quantity = msm.pyunitwizard.quantity(value, "nm")
    with pytest.raises(ArgumentError):
        getattr(states, method)(quantity, chemical_state=1)


def test_native_edits_never_instantiate_topology(states, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Standalone chemical edit instantiated Topology")

    monkeypatch.setattr(Topology, "__init__", forbidden)
    states.add_bonds([[1, 2]], chemical_state=1)
    states.remove_bonds([0], chemical_state=1)
    states.rebuild_components(chemical_state=1)
    assert states.get_bonds(chemical_state=1).shape[0] == 1


@pytest.mark.parametrize("group_name", [None, "UNKNOWN_NUCLEOTIDE"])
def test_incomplete_nucleotide_context_does_not_invent_type_or_name(states, group_name):
    topology = Topology(n_atoms=3, n_groups=1)
    topology.atoms["group_index"] = pd.array([0, 0, 0], dtype="Int64")
    topology.groups["group_type"] = ["nucleotide"]
    topology.groups["group_name"] = pd.array([group_name], dtype="string")
    states.rebuild_components(chemical_state=1, topology=topology)
    assert states._states[1].component_indices.tolist() == [0, 0, 1]
    assert states._states[1].components.component_type.isna().all()
    assert states._states[1].components.component_name.isna().all()
