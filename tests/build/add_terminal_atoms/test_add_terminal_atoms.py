"""Checking transactional native attachment independently of hydrogen engines."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentError,
    StructuralAttributeDropWarning,
    StructuralInconsistencyError,
)


def system():
    builder = msm.MolSysBuilder()
    builder.add_atom(atom_type="C", atom_name="C", atom_id="10")
    builder.add_atom(atom_type="O", atom_name="O", atom_id="11")
    builder.add_group([0, 1], group_name="LIG", group_type="small molecule")
    builder.add_bond(0, 1)
    builder.set_coordinates(
        msm.pyunitwizard.quantity(
            [[[0, 0, 0], [0.14, 0, 0]], [[0, 0, 1], [0.14, 0, 1]]], "nm"
        )
    )
    return builder.build()


def test_all_frames_identity_membership_and_h5_roundtrip(tmp_path):
    source = system()
    atoms = source.topology.atoms.copy(deep=True)
    coordinates = msm.pyunitwizard.get_value(source.structures.coordinates).copy()
    source.interactions = {
        "example": msm.Interactions.from_records(
            [],
            n_atoms=2,
            n_structures=2,
            evaluated_structure_indices=[0, 1],
            method="test",
        )
    }
    added = msm.build.add_terminal_atoms(
        source,
        [{"parent_atom_index": 1, "atom_type": "H", "atom_id": 40, "isotope": 2}],
        msm.pyunitwizard.quantity([[[1.4, 0, 1]], [[1.4, 0, 11]]], "angstrom"),
    )
    output = added["molecular_system"]
    assert output.get_n_atoms() == 3
    assert output.topology.atoms.at[2, "atom_id"] == "40"
    assert (
        output.topology.atoms.at[2, "group_index"]
        == source.topology.atoms.at[1, "group_index"]
    )
    assert output.topology.atoms.at[2, "isotope"] == 2
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(output.structures.coordinates)[:, :2], coordinates
    )
    pd.testing.assert_frame_equal(source.topology.atoms, atoms)
    assert output.interactions["example"].n_atoms == 3
    assert output.interactions["example"].evaluated_structure_indices.tolist() == []
    assert output.interactions["example"].atom_source_indices.tolist() == [0, 1, -1]
    assert source.interactions["example"].evaluated_structure_indices.tolist() == [0, 1]
    path = tmp_path / "attached.h5msm"
    msm.convert(output, to_form="file:h5msm", output_filename=str(path))
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    assert loaded.topology.atoms.at[2, "atom_id"] == "40"
    assert loaded.topology.atoms.at[2, "isotope"] == 2
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(loaded.structures.coordinates),
        msm.pyunitwizard.get_value(output.structures.coordinates),
    )


def test_attribute_policy_reports_drops_and_strict_rejects_transactionally():
    source = system()
    source.structures.occupancy = np.ones((2, 2))
    records = [{"parent_atom_index": 0, "atom_type": "H"}]
    positions = msm.pyunitwizard.quantity(np.ones((2, 1, 3)), "nm")
    with pytest.raises(StructuralInconsistencyError):
        msm.build.add_terminal_atoms(
            source, records, positions, attribute_policy="strict"
        )
    with pytest.warns(StructuralAttributeDropWarning):
        result = msm.build.add_terminal_atoms(source, records, positions)
    assert result["report"]["dropped_attributes"] == ["occupancy"]
    assert result["molecular_system"].structures.occupancy is None
    assert source.structures.occupancy.shape == (2, 2)
    assert source.get_n_atoms() == 2


@pytest.mark.parametrize(
    "record",
    [
        {"parent_atom_index": 2, "atom_type": "H"},
        {"parent_atom_index": 0, "atom_type": "Du"},
        {"parent_atom_index": 0, "atom_type": "H", "atom_id": "10"},
    ],
)
def test_invalid_declarations_leave_source_unchanged(record):
    source = system()
    with pytest.raises(StructuralInconsistencyError):
        msm.build.add_terminal_atoms(
            source, [record], msm.pyunitwizard.quantity(np.ones((2, 1, 3)), "nm")
        )
    assert source.get_n_atoms() == 2


@pytest.mark.parametrize(
    "record",
    [
        {"parent_atom_index": True, "atom_type": "H"},
        {"parent_atom_index": 0, "atom_type": "H", "isotope": -1},
        {"parent_atom_index": 0, "atom_type": "H", "bond_order": 1.0},
    ],
)
def test_invalid_record_types(record):
    with pytest.raises(ArgumentError):
        msm.build.add_terminal_atoms(
            system(), [record], msm.pyunitwizard.quantity(np.ones((2, 1, 3)), "nm")
        )


def test_appending_to_an_earlier_group_does_not_sort_old_atoms_or_reset_state_metadata():
    b = msm.MolSysBuilder()
    b.add_atom(atom_type="C", atom_name="C", atom_id="a")
    b.add_atom(atom_type="O", atom_name="O", atom_id="b")
    b.add_group([0], group_id="first", group_name="A")
    b.add_group([1], group_id="second", group_name="B")
    b.add_bond(0, 1, bond_order=1, bond_type="covalent")
    b.set_coordinates(msm.pyunitwizard.quantity([[[0, 0, 0], [0.14, 0, 0]]], "nm"))
    source = b.build()
    state = source.chemical_states._states[0]
    state.state_id = "selected-state"
    state.provenance_index = 3
    state.connectivity_completeness = "complete"
    source.topology._set_chemical_state_atom_attribute("formal_charge", [0, -1])
    result = msm.build.add_terminal_atoms(
        source,
        [
            {
                "parent_atom_index": 0,
                "atom_type": "H",
                "chemical_attributes": {"formal_charge": 0},
            }
        ],
        msm.pyunitwizard.quantity([[[0, 0, 0.109]]], "nm"),
    )
    output = result["molecular_system"]
    assert output.topology.atoms["atom_id"].iloc[:2].tolist() == ["a", "b"]
    assert output.topology.atoms["group_index"].tolist() == [0, 1, 0]
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(output.structures.coordinates)[:, :2],
        msm.pyunitwizard.get_value(source.structures.coordinates),
    )
    returned = output.chemical_states._states[0]
    assert returned.state_id == "selected-state"
    assert returned.provenance_index == 3
    assert returned.atom_attributes["formal_charge"].tolist() == [0, -1, 0]


def test_empty_attachment_preserves_attributes_and_has_typed_complete_report():
    source = system()
    source.structures.occupancy = np.ones((2, 2))
    source.interactions = {
        "empty": msm.Interactions.from_records(
            [],
            n_atoms=2,
            n_structures=2,
            evaluated_structure_indices=[0, 1],
            method="example",
        )
    }
    result = msm.build.add_terminal_atoms(
        source,
        [],
        msm.pyunitwizard.quantity(np.empty((2, 0, 3)), "nm"),
        attribute_policy="strict",
    )
    assert result["molecular_system"] is not source
    assert result["report"]["status"] == "unchanged"
    assert result["report"]["generated_atom_ids"] == []
    assert result["report"]["coordinate_unit"] == "nm"
    assert result["report"]["parent_atom_pairs"].shape == (0, 2)
    assert result["report"]["parent_atom_pairs"].dtype == np.int64
    np.testing.assert_array_equal(
        result["molecular_system"].structures.occupancy, source.structures.occupancy
    )
    assert result["molecular_system"].interactions[
        "empty"
    ].evaluated_structure_indices.tolist() == [0, 1]
