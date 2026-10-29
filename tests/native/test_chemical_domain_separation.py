"""Exercise #255's target contract, not yet implemented on the migration branch.

These tests intentionally fail against the pre-migration provider. They have no
xfail/skip gate and must not be merged to main before the coherent cutover.
Hand-authored public ChemicalStatesDict inputs avoid depending on the Topology
chemical implementation that the migration removes.
"""

import importlib

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys, Structures, Topology


def _column(dtype, values):
    storage_dtype = np.str_ if dtype == "string" else np.dtype(dtype.lower())
    return {
        "dtype": dtype,
        "values": np.asarray(values, dtype=storage_dtype),
        "null_mask": np.zeros(len(values), dtype=np.bool_),
    }


def _record(state_id, pairs, membership, charges):
    """Declare analytical graphs through the existing version-1 wire contract."""
    count = max(membership) + 1
    return {
        "state_id": state_id,
        "connectivity_completeness": "complete",
        "component_completeness": "complete",
        "component_evidence": "explicit",
        "provenance_index": None,
        "component_indices": _column("Int64", membership),
        "components": {
            "n_rows": count,
            "columns": {
                "component_id": _column(
                    "string", [f"{state_id}-{i}" for i in range(count)]
                ),
                "component_name": _column(
                    "string", [f"part-{i}" for i in range(count)]
                ),
                "component_type": _column("string", ["small molecule"] * count),
            },
        },
        "atom_attributes": {
            "n_rows": 3,
            "columns": {"formal_charge": _column("Int16", charges)},
        },
        "bonds": {
            "n_rows": len(pairs),
            "columns": {
                "atom1_index": _column("Int64", [a for a, _ in pairs]),
                "atom2_index": _column("Int64", [b for _, b in pairs]),
                "bond_order": _column("UInt8", [1] * len(pairs)),
                "bond_type": _column("string", ["covalent"] * len(pairs)),
            },
        },
    }


@pytest.fixture
def states():
    payload = msm.ChemicalStatesDict(
        {
            "schema": "molsysmt.chemical_states_dict",
            "version": 1,
            "n_atoms": 3,
            "reference_chemical_state_index": 0,
            "states": [
                _record("path", [(0, 1), (1, 2)], [0, 0, 0], [0, 0, 0]),
                _record("split", [(0, 1)], [0, 0, 1], [1, -1, 0]),
            ],
        }
    )
    return msm.convert(payload, to_form="molsysmt.ChemicalStates")


@pytest.fixture
def system(states):
    topology = Topology(n_atoms=3)
    topology.atoms["atom_id"] = ["a", "b", "c"]
    topology.atoms["atom_name"] = ["C0", "C1", "C2"]
    topology.atoms["atom_type"] = ["C", "C", "C"]
    structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.arange(36).reshape(4, 3, 3), "nm")
    )
    result = msm.convert([topology, states, structures], to_form="molsysmt.MolSys")
    msm.set(result, structure_chemical_state_index=[0, 1, 0, 1])
    return result


def test_analytical_fixture_is_valid_without_a_topology_owner(states):
    assert states.n_atoms == 3
    assert states.n_chemical_states == 2
    assert states.reference_chemical_state_index == 0
    assert states.get_bonds(chemical_state=0)[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [
        [0, 1],
        [1, 2],
    ]
    assert states.get_bonds(chemical_state=1)[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [[0, 1]]


@pytest.mark.parametrize("attached", [False, True])
def test_topology_never_delivers_chemical_capabilities(system, attached):
    topology = system.topology if attached else Topology(n_atoms=3)
    for attribute in ("n_bonds", "component_index", "formal_charge"):
        assert not msm.has_attribute(topology, attribute, include_none=True)
    for name in ("bonds", "components", "n_bonds", "n_components"):
        assert not hasattr(topology, name)


@pytest.mark.parametrize("attached", [False, True])
def test_topology_copy_does_not_traverse_a_hidden_chemical_collection(
    system, attached, monkeypatch
):
    topology = system.topology if attached else Topology(n_atoms=3)

    def forbidden(*args, **kwargs):
        pytest.fail("A pure Topology copy traversed chemical storage")

    monkeypatch.setattr(msm.ChemicalStates, "__deepcopy__", forbidden)
    clone = topology.copy()
    assert clone is not topology
    pd.testing.assert_frame_equal(clone.atoms, topology.atoms)


def test_topology_projection_cannot_create_a_chemical_state():
    projected = msm.convert(Topology(n_atoms=3), to_form="molsysmt.MolSys")
    assert projected.chemical_states is None
    assert projected.topology.n_atoms == 3


@pytest.mark.parametrize("state_index,bonds,components", [(0, 2, 1), (1, 1, 2)])
def test_standalone_state_queries_deliver_selected_counts(
    states, state_index, bonds, components
):
    assert states.get(chemical_state=state_index, n_bonds=True, n_components=True) == [
        bonds,
        components,
    ]
    assert states.reference_chemical_state_index == 0


def test_state_local_indices_are_validated_after_resolving_the_state(states):
    assert states.get(
        element="bond", selection=[1], chemical_state=0, bond_index=True
    ) == [1]
    with pytest.raises(ArgumentError):
        states.get(element="bond", selection=[1], chemical_state=1, bond_index=True)
    assert states.reference_chemical_state_index == 0


def test_failed_state_resolution_does_not_change_the_reference(states):
    with pytest.raises(StructuralInconsistencyError):
        states.get(chemical_state=7, n_bonds=True)
    assert states.reference_chemical_state_index == 0
    assert states.get(chemical_state=0, n_bonds=True) == 2


def test_an_ambiguous_reference_requires_an_explicit_state(states):
    payload = msm.convert(states, to_form="molsysmt.ChemicalStatesDict")
    payload.data["reference_chemical_state_index"] = None
    ambiguous = msm.convert(payload, to_form="molsysmt.ChemicalStates")
    with pytest.raises(StructuralInconsistencyError):
        ambiguous.get(n_bonds=True)
    assert ambiguous.get(chemical_state=1, n_bonds=True) == 1
    assert ambiguous.reference_chemical_state_index is None


def test_absent_domain_and_present_zero_state_collection_are_distinct():
    empty = msm.ChemicalStates(n_atoms=3)
    assert empty.n_chemical_states == 0
    assert empty.reference_chemical_state_index is None
    coordinates_only = MolSys._from_partial_domains(
        structures=Structures(
            coordinates=msm.pyunitwizard.quantity(np.zeros((1, 3, 3)), "nm")
        )
    )
    states_only = MolSys._from_partial_domains(chemical_states=empty)
    assert coordinates_only.chemical_states is None
    assert states_only.chemical_states is empty
    assert states_only.topology is None
    with pytest.raises(StructuralInconsistencyError):
        empty.get(n_bonds=True)


def test_complete_edge_free_graph_and_unknown_empty_bonds_keep_their_evidence():
    unknown = msm.ChemicalStates(n_atoms=3)
    unknown.append_state()
    payload = msm.ChemicalStatesDict(
        {
            "schema": "molsysmt.chemical_states_dict",
            "version": 1,
            "n_atoms": 3,
            "reference_chemical_state_index": 0,
            "states": [_record("edge-free", [], [0, 1, 2], [0, 0, 0])],
        }
    )
    complete = msm.convert(payload, to_form="molsysmt.ChemicalStates")
    assert complete.get(n_bonds=True, connectivity_completeness=True) == [0, "complete"]
    assert unknown.get(n_bonds=True, connectivity_completeness=True) == [
        0,
        "unavailable",
    ]
    assert complete.get(n_components=True) == 3
    assert unknown.get(component_completeness=True) == "unavailable"


def test_nonconsecutive_structures_and_atoms_keep_the_selected_state(system):
    assert system.get(
        element="atom",
        selection=[2, 0, 2],
        structure_indices=[3, 1, 3],
        chemical_state="structure",
        formal_charge=True,
    ) == [0, 1, 0]
    assert system.chemical_states.reference_chemical_state_index == 0
    with pytest.raises(StructuralInconsistencyError):
        system.get(structure_indices=[0, 3], chemical_state="structure", n_bonds=True)
    assert system.chemical_states.reference_chemical_state_index == 0


def test_existing_controlled_assignment_does_not_edit_an_independent_copy(system):
    clone = msm.copy(system)
    msm.set(system, element="atom", selection=[0], chemical_state=1, formal_charge=2)
    assert msm.get(system, element="atom", chemical_state=1, formal_charge=True) == [
        2,
        -1,
        0,
    ]
    assert msm.get(clone, element="atom", chemical_state=1, formal_charge=True) == [
        1,
        -1,
        0,
    ]
    assert msm.get(system, element="atom", chemical_state=0, formal_charge=True) == [
        0,
        0,
        0,
    ]


def test_current_full_h5msm_roundtrip_keeps_two_states_and_explicit_associations(
    system, tmp_path
):
    filename = msm.convert(system, to_form=str(tmp_path / "two_states.h5msm"))
    restored = msm.convert(filename, to_form="molsysmt.MolSys")
    assert restored.get(structure_chemical_state_index=True) == [0, 1, 0, 1]
    assert restored.get(chemical_state=0, n_bonds=True, n_components=True) == [2, 1]
    assert restored.get(chemical_state=1, n_bonds=True, n_components=True) == [1, 2]
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(restored.structures.coordinates, to_unit="nm"),
        np.arange(36).reshape(4, 3, 3),
    )


def test_replacing_topology_preserves_chemical_authority_and_associations(system):
    original = system.chemical_states
    replacement = Topology(n_atoms=3)
    replacement.atoms["atom_id"] = ["x", "y", "z"]
    system.topology = replacement
    assert system.chemical_states is original
    assert msm.get(system, structure_chemical_state_index=True) == [0, 1, 0, 1]


def test_builder_keeps_source_chemical_states_and_structure_associations(system):
    rebuilt = msm.MolSysBuilder(system).build()
    assert rebuilt.chemical_states is not system.chemical_states
    assert rebuilt.chemical_states.n_chemical_states == 2
    pd.testing.assert_extension_array_equal(
        pd.array(msm.get(rebuilt, structure_chemical_state_index=True), dtype="Int64"),
        pd.array([0, 1, 0, 1], dtype="Int64"),
    )
    assert rebuilt.chemical_states.get_bonds(chemical_state=1).shape[0] == 1


def test_complete_path_restriction_splits_components_but_keeps_its_molecule(system):
    system.topology.reset_molecules(n_molecules=1)
    system.topology.set_atom_molecules([0, 0, 0])
    selected = msm.extract(system, selection=[0, 2])
    assert selected.get(chemical_state=0, n_components=True) == 2
    assert selected.get(element="atom", molecule_index=True) == [0, 0]
    assert selected.get(n_groups=True) == 0
    assert selected.get(n_molecules=True) == 1
    assert system.get(chemical_state=0, n_components=True) == 1


def test_pure_topology_keeps_mixed_group_and_ungrouped_molecule_memberships():
    topology = Topology(n_atoms=3, n_groups=1, n_molecules=2)
    topology.atoms["group_index"] = pd.array([0, None, None], dtype="Int64")
    topology.groups["molecule_index"] = pd.array([1], dtype="Int64")
    topology.set_atom_molecules([1, 0, 0])
    assert topology.get(element="atom", molecule_index=True) == [1, 0, 0]
    with pytest.raises(StructuralInconsistencyError):
        topology.set_atom_molecules([0], atom_indices=[0])
    assert topology.get(element="atom", molecule_index=True) == [1, 0, 0]


def test_selected_state_edit_preserves_other_state_and_stable_molecules(system):
    system.topology.reset_molecules(n_molecules=1)
    system.topology.set_atom_molecules([0, 0, 0])
    original = system.chemical_states.get_bonds(chemical_state=0).copy(deep=True)
    system.chemical_states.remove_bonds([0], chemical_state=1)
    assert system.get(chemical_state=1, n_bonds=True, n_components=True) == [0, 3]
    assert system.get(element="atom", molecule_index=True) == [0, 0, 0]
    pd.testing.assert_frame_equal(
        original, system.chemical_states.get_bonds(chemical_state=0)
    )


def test_component_failure_does_not_publish_bonds_or_invalidate_analyses(
    system, monkeypatch
):
    from molsysmt._private import rust_backend

    analysis = msm.Interactions.from_records(
        [],
        n_atoms=3,
        n_structures=4,
        evaluated_structure_indices=[0, 2],
        method="atomic_chemical_edit_control",
    )
    system.interactions = {"control": analysis}
    before = system.chemical_states.get_bonds(chemical_state=1).copy(deep=True)
    geometry = system.structures._coordinates

    def failed(*args, **kwargs):
        raise MemoryError("Cannot prepare component partition")

    monkeypatch.setattr(
        rust_backend, "get_component_index_from_bonded_atom_pairs", failed
    )
    with pytest.raises(MemoryError, match="component partition"):
        system.chemical_states.add_bonds([[1, 2]], chemical_state=1)
    pd.testing.assert_frame_equal(
        before, system.chemical_states.get_bonds(chemical_state=1)
    )
    assert system.interactions["control"] is analysis
    assert system.interactions["control"].evaluated_structure_indices.tolist() == [0, 2]
    assert system.structures._coordinates is geometry


def test_successful_chemical_edit_invalidates_evaluated_empty_coverage(system):
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=3,
        n_structures=4,
        evaluated_structure_indices=[0, 2],
        method="empty_coverage_control",
    )
    system.interactions = {"control": analysis}
    geometry = system.structures._coordinates
    system.chemical_states.add_bonds([[1, 2]], chemical_state=1)
    assert system.interactions["control"].evaluated_structure_indices.size == 0
    assert analysis.evaluated_structure_indices.tolist() == [0, 2]
    assert system.structures._coordinates is geometry


@pytest.mark.parametrize(
    "to_form", ["molsysmt.MolSysDict", "h5msm"], ids=["dictionary", "h5msm"]
)
def test_persistence_keeps_explicit_group_free_membership_and_state_maps(
    system, to_form, tmp_path
):
    system.topology.reset_molecules(n_molecules=1)
    system.topology.set_atom_molecules([0, 0, 0])
    target = str(tmp_path / "domains.h5msm") if to_form == "h5msm" else to_form
    encoded = msm.convert(system, to_form=target)
    restored = msm.convert(encoded, to_form="molsysmt.MolSys")
    assert restored.get(n_groups=True, n_molecules=True) == [0, 1]
    assert restored.get(element="atom", molecule_index=True) == [0, 0, 0]
    assert restored.get(structure_chemical_state_index=True) == [0, 1, 0, 1]
    assert restored.get(chemical_state=0, n_components=True) == 1
    assert restored.get(chemical_state=1, n_components=True) == 2


@pytest.mark.parametrize(
    "name",
    [
        "get_bondgraph",
        "get_covalent_blocks",
        "get_covalent_paths",
        "get_rings",
        "get_rotatable_bonds",
        "get_rigid_fragments",
        "get_substructure_matches",
        "get_atom_correspondences",
        "get_dihedral_quartets",
    ],
)
def test_existing_graph_tools_have_the_canonical_chemical_owner(name):
    module = importlib.import_module("molsysmt.chemical_states")
    function = getattr(module, name)
    assert callable(function)
    assert function.__module__.startswith("molsysmt.chemical_states.")


def test_bondgraph_on_state_only_input_preserves_source_indices(states):
    module = importlib.import_module("molsysmt.chemical_states")
    graph = module.get_bondgraph(states, selection=[2, 0], chemical_state=0)
    assert list(graph.nodes) == [0, 2]
    assert list(graph.edges) == []


def test_covalent_paths_accept_explicit_state_without_reference_mutation(system):
    module = importlib.import_module("molsysmt.chemical_states")
    assert module.get_covalent_paths(
        system, path=[[0], [1], [2]], chemical_state=0
    ).tolist() == [[0, 1, 2]]
    empty = module.get_covalent_paths(system, path=[[0], [1], [2]], chemical_state=1)
    assert empty.shape == (0, 3)
    assert empty.dtype == np.int64
    assert system.chemical_states.reference_chemical_state_index == 0
