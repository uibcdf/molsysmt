"""Protecting native topology operations under warning-strict pandas execution."""

import warnings

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native._chemical_state import Bonds_DataFrame
from tests.native.test_topology_operations import build_minimal_chemical_molsys


@pytest.fixture(autouse=True)
def strict_pandas_warnings():
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        warnings.simplefilter("error", UserWarning)
        yield


@pytest.mark.parametrize("n_bonds", [0, 1, 3])
def test_sort_preserves_bond_table_identity_metadata_and_nullable_dtypes(n_bonds):
    bonds = Bonds_DataFrame(n_bonds)
    bonds["atom1_index"] = [3, 2, 1][:n_bonds]
    bonds["atom2_index"] = [1, 0, 0][:n_bonds]
    bonds["bond_id"] = ["30", "20", "10"][:n_bonds]
    bonds["bond_order"] = [3, pd.NA, 1][:n_bonds]
    bonds["evidence"] = ["explicit", "inferred", "user_defined"][:n_bonds]
    bonds.index = [8, 5, 2][:n_bonds]
    before = bonds.copy(deep=True)
    alias = bonds
    expected = pd.DataFrame(
        {
            "atom1_index": pd.array([1, 0, 0][:n_bonds], dtype="Int64"),
            "atom2_index": pd.array([3, 2, 1][:n_bonds], dtype="Int64"),
            "bond_id": pd.array(["30", "20", "10"][:n_bonds], dtype="string"),
            "bond_order": pd.array([3, pd.NA, 1][:n_bonds], dtype="UInt8"),
            "evidence": pd.array(
                ["explicit", "inferred", "user_defined"][:n_bonds], dtype="string"
            ),
        }
    ).sort_values(["atom1_index", "atom2_index"], ignore_index=True)
    bonds._sort_bonds()
    assert bonds is alias and isinstance(bonds, Bonds_DataFrame)
    pd.testing.assert_frame_equal(bonds, expected, check_frame_type=False)
    if n_bonds:
        bonds.loc[0, "bond_id"] = "changed"
        assert before.bond_id.tolist() == ["30", "20", "10"][:n_bonds]


@pytest.mark.parametrize("form", ["topology", "molsys"])
def test_public_extract_copy_and_pickle_preserve_source_domains(form):
    import pickle

    molsys = build_minimal_chemical_molsys()
    molsys.chemical_states._set_chemical_state_bonds(
        pd.DataFrame(
            {
                "atom1_index": [3, 2, 1],
                "atom2_index": [1, 0, 0],
                "bond_id": ["30", "20", "10"],
                "bond_order": [1, 2, 1],
                "bond_type": ["covalent"] * 3,
            }
        )
    )
    topology = molsys.topology
    source = topology if form == "topology" else molsys
    original = source.copy()
    states = molsys.chemical_states
    assert list(msm.select(source, selection="group_index==1")) == [2, 3]
    output = msm.extract(source, selection=[3, 1])
    selected = output if form == "topology" else output.topology
    assert selected.atoms.atom_id.tolist() == ["1", "3"]
    assert selected.groups.group_id.tolist() == ["10", "11"]
    assert selected.chains.chain_id.tolist() == ["A", "B"]
    assert not hasattr(selected, "bonds")
    assert molsys.chemical_states is states
    if form == "molsys":
        bonds = output.chemical_states.get_bonds()
        assert bonds[["atom1_index", "atom2_index"]].values.tolist() == [[0, 1]]
        assert bonds.bond_id.tolist() == ["30"]
        assert output.chemical_states is not states
    for table in ("atoms", "groups", "molecules", "entities", "chains"):
        previous = getattr(original if form == "topology" else original.topology, table)
        pd.testing.assert_frame_equal(
            getattr(topology, table), previous, check_frame_type=False
        )
        assert getattr(selected, table).index.tolist() == list(
            range(len(getattr(selected, table)))
        )
    restored = pickle.loads(pickle.dumps(output))
    if form == "molsys":
        pd.testing.assert_frame_equal(
            restored.chemical_states.get_bonds(),
            output.chemical_states.get_bonds(),
            check_frame_type=False,
        )
    selected.atoms.loc[0, "atom_name"] = "edited"
    assert topology.atoms.atom_name.tolist() == ["N", "CA", "O", "H"]


def test_chemical_state_extraction_resets_membership_and_preserves_assignments():
    molsys = build_minimal_chemical_molsys()
    molsys.chemical_states._set_chemical_state_atom_attribute(
        "formal_charge", [0, 1, -1, 0]
    )
    states = molsys.chemical_states
    before = states.copy()
    selected = states._extract_atoms([3, 1])
    record = selected._states[0]
    # Native chemical-state extraction preserves its explicit requested order.
    np.testing.assert_array_equal(record.atom_attributes.formal_charge, [0, 1])
    assert record.atom_attributes.index.tolist() == [0, 1]
    assert record.component_indices.index.tolist() == [0, 1]
    assert record.components.index.tolist() == [0, 1]
    pd.testing.assert_frame_equal(
        states._states[0].atom_attributes, before._states[0].atom_attributes
    )
    selected._states[0].atom_attributes.loc[0, "formal_charge"] = 2
    assert states._states[0].atom_attributes.formal_charge.tolist() == [0, 1, -1, 0]


def test_atom_assignment_removal_preserves_table_identity_and_copy():
    molsys = build_minimal_chemical_molsys()
    molsys.chemical_states._set_chemical_state_atom_attribute(
        "formal_charge", [0, 1, -1, 0]
    )
    record = molsys.chemical_states._states[0]
    table = record.atom_attributes
    duplicate = record.copy()
    record.remove_atom_attribute("formal_charge")
    assert record.atom_attributes is table
    assert "formal_charge" not in table
    assert duplicate.atom_attributes.formal_charge.tolist() == [0, 1, -1, 0]
