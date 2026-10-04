"""Round-trip contracts for typed chemical-state dictionary forms."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import MolSys, Topology


def test_empty_collection_roundtrip_preserves_absence():
    original = msm.ChemicalStates(n_atoms=4)

    encoded = msm.convert(original, to_form="molsysmt.ChemicalStatesDict")
    decoded = msm.convert(encoded, to_form="molsysmt.ChemicalStates")

    assert msm.get_form(encoded) == "molsysmt.ChemicalStatesDict"
    assert decoded.n_atoms == 4
    assert decoded.n_chemical_states == 0
    assert decoded.reference_chemical_state_index is None
    assert msm.get(encoded, n_atoms=True, n_chemical_states=True) == [4, 0]
    with pytest.raises(msm.StructuralInconsistencyError):
        decoded.get_bonds()


def test_object_backed_bond_fields_preserve_boolean_numeric_values_and_nulls():
    topology = Topology(n_atoms=3)
    topology.bonds = pd.DataFrame(dict(atom1_index=[0, 1], atom2_index=[1, 2]))
    state = topology._chemical_states[0]
    state.bonds["bond_order"] = pd.Series([1, pd.NA], dtype=object)
    state.bonds["is_aromatic"] = pd.Series([False, pd.NA], dtype=object)
    state.bonds["joins_components"] = pd.Series([True, False], dtype=object)
    original = state.bonds.copy(deep=True)
    encoded = msm.convert(topology, to_form="molsysmt.ChemicalStatesDict")
    columns = encoded.data["states"][0]["bonds"]["columns"]
    assert columns["bond_order"]["dtype"] == "UInt8"
    assert columns["bond_order"]["values"].tolist() == [1, 0]
    assert columns["bond_order"]["null_mask"].tolist() == [False, True]
    assert columns["is_aromatic"]["values"].dtype == np.dtype("bool")
    restored = msm.convert(encoded, to_form="molsysmt.ChemicalStates")
    bonds = restored.get_bonds()
    assert bonds["bond_order"].iloc[0] == 1
    assert pd.isna(bonds["bond_order"].iloc[1])
    assert not bonds["is_aromatic"].iloc[0]
    assert pd.isna(bonds["is_aromatic"].iloc[1])
    assert bonds["joins_components"].tolist() == [True, False]
    pd.testing.assert_frame_equal(state.bonds, original)


def test_multistate_roundtrip_preserves_nullable_chemistry_and_reference():
    topology = Topology(n_atoms=3)
    topology._append_chemical_state_bonds(
        [[0, 1]], bond_order=[2], bond_type=["covalent"]
    )
    topology._set_chemical_state_atom_attribute("formal_charge", [0, pd.NA, -1])
    second = topology._append_chemical_state(state_id="product")
    topology._append_chemical_state_bonds(
        [[1, 2]], bond_order=[1], bond_type=["covalent"], state_index=second
    )
    topology._set_reference_chemical_state_index(None)

    encoded = msm.convert(topology, to_form="molsysmt.ChemicalStatesDict")
    decoded = msm.convert(encoded, to_form="molsysmt.ChemicalStates")

    assert msm.get_form(decoded) == "molsysmt.ChemicalStates"
    assert decoded.n_atoms == 3
    assert decoded.n_chemical_states == 2
    assert decoded.reference_chemical_state_index is None
    assert decoded._states[1].state_id == "product"
    pd.testing.assert_frame_equal(
        decoded.get_bonds(0), topology._chemical_states[0].bonds
    )
    pd.testing.assert_frame_equal(
        decoded.get_bonds(1), topology._chemical_states[1].bonds
    )
    pd.testing.assert_frame_equal(
        decoded._states[0].atom_attributes,
        topology._chemical_states[0].atom_attributes,
    )
    assert encoded.data["states"][0]["atom_attributes"]["columns"]["formal_charge"][
        "null_mask"
    ].tolist() == [False, True, False]
    assert isinstance(
        encoded.data["states"][0]["bonds"]["columns"]["bond_order"]["values"],
        np.ndarray,
    )


def test_dictionary_copy_is_independent_and_schema_is_versioned():
    original = msm.ChemicalStates(n_atoms=2)
    original.append_state()
    encoded = msm.convert(original, to_form="molsysmt.ChemicalStatesDict")
    copied = msm.convert(encoded, to_form="molsysmt.ChemicalStatesDict")

    copied.data["states"][0]["component_indices"]["values"][0] = 1
    assert encoded.data["states"][0]["component_indices"]["values"][0] == 0
    assert encoded.data["schema"] == "molsysmt.chemical_states_dict"
    assert encoded.data["version"] == 1

    copied.data["version"] = 99
    with pytest.raises(ValueError, match="version"):
        msm.convert(copied, to_form="molsysmt.ChemicalStates")


def test_chemical_states_are_complementary_to_matching_topology():
    topology = Topology(n_atoms=2)
    states = msm.ChemicalStates(n_atoms=2)
    states.append_state()
    encoded = msm.convert(states, to_form="molsysmt.ChemicalStatesDict")

    assert msm.is_a_molecular_system([topology, states])
    assert msm.is_a_molecular_system([topology, encoded])
    assert not msm.is_a_molecular_system([Topology(n_atoms=3), encoded])


@pytest.mark.parametrize("source_kind", ["topology", "molsys"])
@pytest.mark.parametrize(
    "target_form", ["molsysmt.ChemicalStates", "molsysmt.ChemicalStatesDict"]
)
def test_direct_conversion_from_native_system_preserves_and_detaches_states(
    source_kind, target_form
):
    source = Topology(n_atoms=3) if source_kind == "topology" else MolSys(n_atoms=3)
    topology = source if source_kind == "topology" else source.topology
    topology.add_bonds([[0, 1]])
    topology._append_chemical_state(state_id="second")
    topology._append_chemical_state_bonds([[1, 2]], state_index=1)

    result = msm.convert(source, to_form=target_form)
    states = (
        result
        if target_form == "molsysmt.ChemicalStates"
        else msm.convert(result, to_form="molsysmt.ChemicalStates")
    )

    assert msm.get_form(result) == target_form
    assert states.n_atoms == 3
    assert states.n_chemical_states == 2
    assert len(states.get_bonds(0)) == 1
    assert len(states.get_bonds(1)) == 1
    assert states._states[1].state_id == "second"
    states._states[0].bonds.loc[0, "atom2_index"] = 2
    assert (
        msm.convert(topology, to_form="molsysmt.ChemicalStates")
        .get_bonds(0)
        .loc[0, "atom2_index"]
        == 1
    )


def test_direct_dictionary_conversion_rejects_a_selection_it_cannot_remap():
    source = MolSys(n_atoms=3)
    source.topology.add_bonds([[0, 1], [1, 2]])

    with pytest.raises(ValueError, match="requires all atom and structure indices"):
        msm.convert(
            source,
            selection=[0, 1],
            to_form="molsysmt.ChemicalStatesDict",
        )
