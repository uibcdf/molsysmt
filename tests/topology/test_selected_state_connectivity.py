"""Check induced source-index connectivity before and after state resolution."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys, Structures


def source():
    topology = MolSys(n_atoms=6)
    topology.topology.atoms["atom_type"] = "C"
    topology.chemical_states._set_chemical_state_bonds(
        pd.DataFrame(
            {
                "atom1_index": [0, 1, 2, 3, 4],
                "atom2_index": [1, 2, 3, 4, 5],
                "bond_type": ["covalent"] * 5,
            }
        )
    )
    molsys = msm.convert(topology, to_form="molsysmt.MolSys")
    state = molsys.chemical_states._states[0]
    state.connectivity_completeness = "complete"
    second = state.copy()
    second.state_id = "assigned-split"
    second.bonds = second.bonds.drop(index=2).reset_index(drop=True)
    molsys.chemical_states._states.append(second)
    molsys.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((3, 6, 3)), "nm")
    )
    molsys._set_structure_chemical_state_indices([1, 0, 1])
    return molsys


def blocks(molecular_system, **kwargs):
    return msm.chemical_states.get_covalent_blocks(molecular_system, **kwargs).tolist()


def test_assigned_state_differs_from_reference_without_changing_either():
    molsys = source()
    before = molsys.copy()
    assert blocks(molsys) == [set(range(6))]
    assert blocks(molsys, chemical_state="structure", structure_indices=[2, 0, 2]) == [
        {0, 1, 2},
        {3, 4, 5},
    ]
    graph = msm.chemical_states.get_bondgraph(
        molsys, chemical_state="structure", structure_indices=0
    )
    assert set(graph.edges) == {(0, 1), (1, 2), (3, 4), (4, 5)}
    assert blocks(molsys, chemical_state=1) == [{0, 1, 2}, {3, 4, 5}]
    assert blocks(molsys) == [set(range(6))]
    assert molsys.chemical_states.reference_chemical_state_index == 0
    for actual, expected in zip(
        molsys.chemical_states._states, before.chemical_states._states
    ):
        pd.testing.assert_frame_equal(actual.bonds, expected.bonds)
    np.testing.assert_array_equal(
        molsys._get_structure_chemical_state_indices(),
        before._get_structure_chemical_state_indices(),
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(molsys.structures.coordinates),
        msm.pyunitwizard.get_value(before.structures.coordinates),
    )


def test_selected_graph_is_induced_not_full_graph_projection():
    molsys = source()
    selection = [5, 1, 0, 3, 1]
    assert blocks(molsys, selection=selection) == [{0, 1}, {3}, {5}]
    np.testing.assert_array_equal(
        msm.chemical_states.get_covalent_blocks(
            molsys, selection=selection, output_type="numpy.ndarray"
        ),
        [0, 0, -1, 1, -1, 2],
    )
    assert blocks(
        molsys, selection=[5, 4, 3, 1, 0], chemical_state=1, remove_bonds=[[4, 5]]
    ) == [{0, 1}, {3, 4}, {5}]
    graph = msm.chemical_states.get_bondgraph(
        molsys, selection=selection, chemical_state=1
    )
    assert list(graph.nodes) == [0, 1, 3, 5]
    assert list(graph.edges) == [(0, 1)]
    assert blocks(molsys, selection=[]) == []
    np.testing.assert_array_equal(
        msm.chemical_states.get_covalent_blocks(
            molsys, selection=[], output_type="numpy.ndarray"
        ),
        [-1] * 6,
    )


@pytest.mark.parametrize("function", ["get_bondgraph", "get_covalent_blocks"])
def test_ambiguous_missing_invalid_or_unavailable_state_never_falls_back(function):
    molsys = source()
    operation = getattr(msm.chemical_states, function)
    for options in (
        {"chemical_state": "structure", "structure_indices": [0, 1]},
        {"chemical_state": "structure", "structure_indices": []},
        {"chemical_state": "structure", "structure_indices": [3]},
        {"chemical_state": 7},
    ):
        with pytest.raises((ArgumentError, StructuralInconsistencyError)):
            operation(molsys, **options)
    molsys._set_structure_chemical_state_indices([None, 0, 1])
    with pytest.raises(StructuralInconsistencyError):
        operation(molsys, chemical_state="structure", structure_indices=0)


@pytest.mark.parametrize(
    "form", ["molsysmt.MolSys", "molsysmt.ChemicalStates", "file:h5msm"]
)
def test_forms_and_partial_reference_do_not_override_explicit_state(form, tmp_path):
    molsys = source()
    molsys.chemical_states._states[0].connectivity_completeness = "partial"
    if form == "file:h5msm":
        path = tmp_path / "states.h5msm"
        msm.convert(molsys, to_form=path)
        system = path
    else:
        system = msm.convert(
            molsys.topology if form == "molsysmt.TopologyDict" else molsys, to_form=form
        )
    assert blocks(system, selection=[5, 4, 3, 2, 1, 0], chemical_state=1) == [
        {0, 1, 2},
        {3, 4, 5},
    ]
    assert blocks(system) == [set(range(6))]


def test_spatial_selection_uses_requested_structure():
    molsys = source()
    positions = np.zeros((3, 6, 3))
    positions[:, :, 0] = np.arange(6)
    positions[2, 3, 0] = 0.2
    msm.set(molsys, coordinates=msm.pyunitwizard.quantity(positions, "nm"))
    assert blocks(
        molsys,
        selection="atom_index != 0 within 0.5 nm of atom_index == 0",
        chemical_state="structure",
        structure_indices=2,
    ) == [{3}]


@pytest.mark.parametrize("form", ["molsysmt.MolSysDict", "molsysmt.TopologyDict"])
def test_dictionary_reference_graph_can_be_requested_explicitly(form):
    molsys = source()
    system = msm.convert(
        molsys.topology if form == "molsysmt.TopologyDict" else molsys, to_form=form
    )
    if form == "molsysmt.TopologyDict":
        with pytest.raises(ArgumentError):
            blocks(system, chemical_state=0)
        with pytest.raises(StructuralInconsistencyError):
            blocks(system)
        return
    assert blocks(system, selection=[5, 1, 0, 3], chemical_state=0) == [
        {0, 1},
        {3},
        {5},
    ]
    # MolSysDict 0.2 preserves the independent collection, not only its reference.
    assert blocks(system, chemical_state=1) == [{0, 1, 2}, {3, 4, 5}]
