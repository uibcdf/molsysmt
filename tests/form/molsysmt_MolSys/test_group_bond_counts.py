"""Protect native MolSys group counts over one selected chemical-state owner."""

from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolSys, Structures


@pytest.fixture
def grouped_system():
    builder = msm.MolSysBuilder()
    atoms = [builder.add_atom(atom_name="C", atom_type="C") for _ in range(5)]
    builder.add_group(atoms[:2], group_name="A", group_type="unknown")
    builder.add_group(atoms[2:4], group_name="B", group_type="unknown")
    builder.add_group(atoms[4:], group_name="C", group_type="unknown")
    for pair in [[0, 1], [2, 3], [1, 2]]:
        builder.add_bond(*pair)
    source = builder.build()
    source.chemical_states.append_state()
    with source.topology._using_chemical_state(1):
        source.topology.add_bonds([[0, 4]])
    return source


def test_empty_topomt_pdb_group_counts_have_a_public_delivery_route():
    fixture = (
        Path(__file__).parents[1]
        / "molsysmt_Topology/data/topomt_geometric_tetrahedron.pdb"
    )
    source = msm.convert(str(fixture), to_form="molsysmt.MolSys")
    assert msm.get(source, element="group", n_bonds=True) == [0, 0, 0, 0]
    assert msm.get(source, element="group", selection=[1, 3], n_bonds=True) == [0, 0]
    assert msm.get(source, element="group", selection=[], n_bonds=True) == []


@pytest.mark.parametrize(
    "state,expected", [("reference", [2, 2, 0]), (0, [2, 2, 0]), (1, [1, 0, 1])]
)
@pytest.mark.parametrize("selection", ["all", [2, 0], []])
def test_bonded_group_counts_state_and_topology_parity(
    grouped_system, state, expected, selection
):
    source = grouped_system
    wanted = expected if selection == "all" else [expected[i] for i in selection]
    before = source.chemical_states.reference_chemical_state_index
    result = msm.get(
        source, element="group", selection=selection, chemical_state=state, n_bonds=True
    )
    assert result == wanted
    assert result == msm.get(
        source.topology,
        element="group",
        selection=selection,
        chemical_state=state,
        n_bonds=True,
    )
    assert source.chemical_states.reference_chemical_state_index == before
    assert source.chemical_states is source.topology._chemical_states_domain
    assert len(source.chemical_states.get_bonds(chemical_state=0)) == 3
    assert len(source.chemical_states.get_bonds(chemical_state=1)) == 1


def test_mixed_group_attributes_and_selection_mask(grouped_system):
    result = msm.get(
        grouped_system,
        element="group",
        selection='group_name in ["A","C"]',
        chemical_state=1,
        output_type="dictionary",
        group_name=True,
        n_atoms=True,
        n_bonds=True,
    )
    assert result == {"group_name": ["A", "C"], "n_atoms": [2, 1], "n_bonds": [1, 1]}
    assert msm.get(
        grouped_system, element="group", selection="all", mask=[1], n_bonds=True
    ) == [2]


def test_structure_associations_select_counts_and_reject_mixed_states(grouped_system):
    source = grouped_system
    source.structures.append(
        coordinates=msm.pyunitwizard.quantity(np.zeros((3, 5, 3)), "nm")
    )
    msm.set(source, structure_chemical_state_index=[0, 1, 0])
    assert msm.get(
        source,
        element="group",
        chemical_state="structure",
        structure_indices=[1],
        n_bonds=True,
    ) == [1, 0, 1]
    assert msm.get(
        source,
        element="group",
        chemical_state="structure",
        structure_indices=[2, 0],
        n_bonds=True,
    ) == [2, 2, 0]
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.get(
            source,
            element="group",
            chemical_state="structure",
            structure_indices=[0, 1],
            n_bonds=True,
        )
    assert source.chemical_states.reference_chemical_state_index == 0


def test_ambiguous_reference_and_absent_topology_are_not_silently_zero(grouped_system):
    source = grouped_system
    source.topology._set_reference_chemical_state_index(None)
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.get(source, element="group", n_bonds=True)
    assert msm.get(source, element="group", chemical_state=1, n_bonds=True) == [1, 0, 1]
    structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((1, 5, 3)), "nm")
    )
    partial = MolSys._from_partial_domains(structures=structures)
    assert msm.get(partial, element="group", n_bonds=True) is None


def test_invalid_state_does_not_mutate_reference(grouped_system):
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.get(grouped_system, element="group", chemical_state=2, n_bonds=True)
    assert grouped_system.chemical_states.reference_chemical_state_index == 0
