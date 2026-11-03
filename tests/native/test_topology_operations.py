import pickle

import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native import MolSys, Topology
from molsysmt.native._chemical_state import (
    Bonds_DataFrame,
    Components_DataFrame,
    _ChemicalStateStorage,
)


def build_minimal_topology():
    topology = Topology(n_atoms=4, n_groups=2, n_molecules=2, n_entities=2, n_chains=2)

    topology.atoms["atom_id"] = ["0", "1", "2", "3"]
    topology.atoms["atom_name"] = ["N", "CA", "O", "H"]
    topology.atoms["atom_type"] = ["N", "C", "O", "H"]
    topology.atoms["group_index"] = pd.Series([0, 0, 1, 1], dtype="Int64")
    topology.atoms["chain_index"] = pd.Series([0, 0, 1, 1], dtype="Int64")

    topology.groups["group_id"] = ["10", "11"]
    topology.groups["group_name"] = ["ALA", "HOH"]
    topology.groups["group_type"] = ["amino acid", "water"]
    topology.groups["molecule_index"] = pd.Series([0, 1], dtype="Int64")

    topology.molecules["molecule_id"] = ["30", "31"]
    topology.molecules["molecule_name"] = ["peptide 0", "water"]
    topology.molecules["molecule_type"] = ["peptide", "water"]
    topology.molecules["entity_index"] = pd.Series([0, 1], dtype="Int64")

    topology.entities["entity_id"] = ["40", "41"]
    topology.entities["entity_name"] = ["peptide 0", "water"]
    topology.entities["entity_type"] = ["peptide", "water"]

    topology.chains["chain_id"] = ["A", "B"]
    topology.chains["chain_name"] = ["A", "B"]
    topology.chains["chain_type"] = ["protein", "water"]

    return topology


def build_minimal_chemical_molsys():
    from molsysmt.native import MolSys

    system = MolSys._from_partial_domains(
        topology=build_minimal_topology(), chemical_states=msm.ChemicalStates(n_atoms=4)
    )
    system.chemical_states.append_state()
    state = system.chemical_states._states[0]
    state.components = Components_DataFrame(n_components=2)
    state.components["component_id"] = ["20", "21"]
    state.components["component_name"] = ["peptide 0", "water"]
    state.components["component_type"] = ["peptide", "water"]
    system.chemical_states._set_component_indices([0, 0, 1, 1])
    system.chemical_states._append_chemical_state_bonds(
        [[0, 1]], bond_order=1, bond_type="covalent"
    )
    return system


def test_reset_dataframe_sizes_and_id_dtypes():
    topology = MolSys(
        n_atoms=3,
        n_groups=2,
        n_components=1,
        n_molecules=1,
        n_entities=1,
        n_chains=1,
        n_bonds=2,
    )

    assert topology.topology.n_atoms == 3
    assert topology.topology.n_groups == 2
    assert topology.chemical_states.get(n_components=True) == 1
    assert topology.topology.n_molecules == 1
    assert topology.topology.n_entities == 1
    assert topology.topology.n_chains == 1
    assert topology.chemical_states.get(n_bonds=True) == 2

    assert str(topology.topology.atoms["atom_id"].dtype) == "string"
    assert str(topology.topology.groups["group_id"].dtype) == "string"
    assert (
        str(
            topology.chemical_states._resolve_chemical_state()
            .components["component_id"]
            .dtype
        )
        == "string"
    )
    assert str(topology.topology.molecules["molecule_id"].dtype) == "string"
    assert str(topology.topology.entities["entity_id"].dtype) == "string"
    assert str(topology.topology.chains["chain_id"].dtype) == "string"


def test_copy_returns_independent_topology():
    topology = build_minimal_topology()
    cloned = topology.copy()

    cloned.atoms.at[0, "atom_name"] = "X"
    cloned.groups.at[0, "group_name"] = "GLY"

    assert topology.atoms.at[0, "atom_name"] == "N"
    assert topology.groups.at[0, "group_name"] == "ALA"


def test_bonds_and_components_use_reference_chemical_state_storage():
    topology = build_minimal_chemical_molsys()

    assert (
        topology.chemical_states.get_bonds()
        is topology.chemical_states._states[0].bonds
    )
    assert topology.chemical_states._molsys_owner_ref() is topology

    topology = MolSys(n_atoms=4, n_bonds=2, n_components=1)

    assert (
        topology.chemical_states.get_bonds()
        is topology.chemical_states._states[0].bonds
    )
    assert topology.chemical_states._molsys_owner_ref() is topology
    assert topology.chemical_states.get(n_bonds=True) == 2
    assert topology.chemical_states.get(n_components=True) == 1


def test_component_membership_has_no_duplicate_storage_in_stable_atoms():
    topology = build_minimal_chemical_molsys()

    assert "component_index" not in topology.topology.atoms.columns
    assert topology.chemical_states._get_component_indices().tolist() == [0, 0, 1, 1]


def test_default_topology_has_one_private_implicit_reference_state():
    topology = MolSys(n_atoms=2)

    assert len(topology.chemical_states._states) == 1
    assert topology.chemical_states.reference_chemical_state_index == 0
    assert (
        topology.chemical_states._resolve_chemical_state()
        is topology.chemical_states._states[0]
    )
    assert topology.chemical_states._resolve_chemical_state().atom_attributes.shape == (
        2,
        0,
    )


def test_private_chemical_state_metadata_is_validated():
    state = MolSys().chemical_states._resolve_chemical_state()

    state.connectivity_completeness = "partial"
    state.component_completeness = "complete"
    state.component_evidence = "inferred"
    state.provenance_index = 3

    assert state.connectivity_completeness == "partial"
    assert state.component_completeness == "complete"
    assert state.component_evidence == "inferred"
    assert state.provenance_index == 3

    with pytest.raises(StructuralInconsistencyError, match="connectivity completeness"):
        state.connectivity_completeness = "guessed"
    with pytest.raises(StructuralInconsistencyError, match="component evidence"):
        state.component_evidence = "automatic"
    with pytest.raises(StructuralInconsistencyError, match="provenance_index"):
        state.provenance_index = -1


def test_optional_atom_state_columns_preserve_nullable_dtypes_and_values():
    topology = MolSys(n_atoms=3)

    topology.chemical_states._set_chemical_state_atom_attribute(
        "formal_charge", [-1, 0, 1]
    )
    topology.chemical_states._set_chemical_state_atom_attribute(
        "is_aromatic", [True, False, pd.NA]
    )
    topology.chemical_states._set_chemical_state_atom_attribute(
        "n_unpaired_electrons", [0, 1, pd.NA]
    )
    topology.chemical_states._set_chemical_state_atom_attribute(
        "n_implicit_hydrogens", [3, 0, pd.NA]
    )
    topology.chemical_states._set_chemical_state_atom_attribute(
        "allows_implicit_hydrogens", [True, False, pd.NA]
    )
    topology.chemical_states._set_chemical_state_atom_attribute(
        "stereochemistry", ["R", "unspecified", pd.NA]
    )

    topology.chemical_states._set_chemical_state_atom_attribute(
        "n_explicit_hydrogens", [0, 2, pd.NA]
    )
    atom_attributes = topology.chemical_states._resolve_chemical_state().atom_attributes
    assert atom_attributes.columns.tolist() == [
        "formal_charge",
        "is_aromatic",
        "n_unpaired_electrons",
        "n_implicit_hydrogens",
        "n_explicit_hydrogens",
        "allows_implicit_hydrogens",
        "stereochemistry",
    ]
    assert str(atom_attributes["formal_charge"].dtype) == "Int16"
    assert str(atom_attributes["is_aromatic"].dtype) == "boolean"
    assert str(atom_attributes["n_unpaired_electrons"].dtype) == "UInt8"
    assert str(atom_attributes["n_implicit_hydrogens"].dtype) == "UInt8"
    assert str(atom_attributes["n_explicit_hydrogens"].dtype) == "UInt8"
    assert atom_attributes["n_explicit_hydrogens"].tolist() == [0, 2, pd.NA]
    assert str(atom_attributes["allows_implicit_hydrogens"].dtype) == "boolean"
    assert str(atom_attributes["stereochemistry"].dtype) == "string"
    assert atom_attributes["formal_charge"].tolist() == [-1, 0, 1]
    assert atom_attributes["stereochemistry"].tolist() == ["R", "unspecified", pd.NA]


def test_partial_atom_state_assignment_materializes_missing_values():
    topology = MolSys(n_atoms=3)

    topology.chemical_states._set_chemical_state_atom_attribute(
        "stereochemistry", "S", atom_indices=[1]
    )

    values = topology.chemical_states._get_chemical_state_atom_attribute(
        "stereochemistry"
    )
    assert values.tolist() == [pd.NA, "S", pd.NA]
    assert topology.chemical_states._has_chemical_state_atom_attribute(
        "stereochemistry"
    )

    topology.chemical_states._set_chemical_state_atom_attribute("formal_charge", pd.NA)
    assert not topology.chemical_states._has_chemical_state_atom_attribute(
        "formal_charge"
    )
    assert topology.chemical_states._has_chemical_state_atom_attribute(
        "formal_charge", include_none=True
    )


def test_atom_state_assignment_rejects_invalid_names_values_lengths_and_indices():
    topology = MolSys(n_atoms=3)

    with pytest.raises(
        StructuralInconsistencyError, match="Unknown chemical-state atom attribute"
    ):
        topology.chemical_states._set_chemical_state_atom_attribute(
            "partial_charge", [0, 0, 0]
        )
    with pytest.raises(
        StructuralInconsistencyError, match="Invalid atom stereochemistry"
    ):
        topology.chemical_states._set_chemical_state_atom_attribute(
            "stereochemistry", ["CW", "S", "R"]
        )
    with pytest.raises(StructuralInconsistencyError, match="accepts only boolean"):
        topology.chemical_states._set_chemical_state_atom_attribute(
            "is_aromatic", [1, 0, 1]
        )
    with pytest.raises(
        StructuralInconsistencyError, match="cannot be represented as UInt8"
    ):
        topology.chemical_states._set_chemical_state_atom_attribute(
            "n_implicit_hydrogens", [0, -1, 2]
        )
    with pytest.raises(
        StructuralInconsistencyError, match="received 2 values; expected 3"
    ):
        topology.chemical_states._set_chemical_state_atom_attribute(
            "formal_charge", [0, 1]
        )
    with pytest.raises(
        StructuralInconsistencyError, match="must not contain duplicates"
    ):
        topology.chemical_states._set_chemical_state_atom_attribute(
            "formal_charge", [0, 1], atom_indices=[1, 1]
        )
    with pytest.raises(StructuralInconsistencyError, match="outside the valid range"):
        topology.chemical_states._set_chemical_state_atom_attribute(
            "formal_charge", 0, atom_indices=[3]
        )


def test_optional_atom_state_column_can_be_removed():
    topology = MolSys(n_atoms=2)
    topology.chemical_states._set_chemical_state_atom_attribute("formal_charge", [0, 1])

    topology.chemical_states._remove_chemical_state_atom_attribute("formal_charge")

    assert (
        topology.chemical_states._get_chemical_state_atom_attribute("formal_charge")
        is None
    )
    assert not topology.chemical_states._has_chemical_state_atom_attribute(
        "formal_charge", include_none=True
    )


def test_zero_state_requires_explicit_state_creation_before_assignment():
    topology = MolSys(n_atoms=2)
    topology.chemical_states._replace_states([], None)

    with pytest.raises(StructuralInconsistencyError, match="no chemical state"):
        _ = topology.chemical_states._resolve_chemical_state().bonds

    replacement = Bonds_DataFrame(n_bonds=0)
    with pytest.raises(StructuralInconsistencyError, match="no chemical state"):
        topology.chemical_states._set_chemical_state_bonds(replacement)
    topology.chemical_states.append_state()
    topology.chemical_states._set_chemical_state_bonds(replacement)

    assert len(topology.chemical_states._states) == 1
    assert topology.chemical_states.reference_chemical_state_index == 0
    assert (
        topology.chemical_states.get_bonds()
        is topology.chemical_states._states[0].bonds
    )
    assert topology.chemical_states._resolve_chemical_state().bonds is not replacement


def test_multiple_states_require_an_unambiguous_reference():
    topology = MolSys(n_atoms=2)
    second_index = topology.chemical_states._append_state(
        _ChemicalStateStorage(n_atoms=topology.get_n_atoms(), state_id="product"),
        set_as_reference=False,
    )
    topology.chemical_states._set_reference_index(None)

    with pytest.raises(StructuralInconsistencyError, match="ambiguous"):
        _ = topology.chemical_states._resolve_chemical_state().components

    topology.chemical_states._set_reference_index(second_index)

    assert topology.chemical_states._resolve_chemical_state().state_id == "product"


def test_duplicate_state_labels_do_not_replace_internal_row_identity():
    topology = MolSys(n_atoms=1)
    topology.chemical_states._states[0].state_id = "state"
    second_index = topology.chemical_states._append_state(
        _ChemicalStateStorage(n_atoms=topology.get_n_atoms(), state_id="state"),
        set_as_reference=False,
    )

    assert len(topology.chemical_states._states) == 2
    assert (
        topology.chemical_states._states[0].state_id
        == topology.chemical_states._states[second_index].state_id
    )
    assert (
        topology.chemical_states._states[0]
        is not topology.chemical_states._states[second_index]
    )


def test_explicit_state_index_allows_atom_attribute_access_without_reference():
    topology = MolSys(n_atoms=2)
    second_index = topology.chemical_states._append_state(
        _ChemicalStateStorage(n_atoms=topology.get_n_atoms(), state_id="product"),
        set_as_reference=False,
    )
    topology.chemical_states._set_reference_index(None)

    topology.chemical_states._set_chemical_state_atom_attribute(
        "formal_charge", [0, -1], state_index=second_index
    )

    assert topology.chemical_states._get_chemical_state_atom_attribute(
        "formal_charge", state_index=second_index
    ).tolist() == [0, -1]


def test_private_bond_seam_resolves_explicit_state_without_reference():
    topology = MolSys(n_atoms=3)
    second_index = topology.chemical_states._append_state(
        _ChemicalStateStorage(n_atoms=topology.get_n_atoms(), state_id="product"),
        set_as_reference=False,
    )
    topology.chemical_states._set_reference_index(None)

    topology.chemical_states._append_chemical_state_bonds(
        [[2, 1]], orders="aromatic", types="dative", state_index=second_index
    )

    bonds = topology.chemical_states._get_chemical_state_bonds(state_index=second_index)
    assert bonds[["atom1_index", "atom2_index"]].values.tolist() == [[1, 2]]
    assert bonds["is_aromatic"].tolist() == [True]
    assert bonds["bond_type"].tolist() == ["dative"]
    assert bonds["joins_components"].tolist() == [False]
    with pytest.raises(StructuralInconsistencyError, match="ambiguous"):
        topology.chemical_states._get_chemical_state_bonds()


def test_private_bond_mutation_requires_explicit_state_creation():
    topology = MolSys(n_atoms=2)
    topology.chemical_states._replace_states([], None)

    with pytest.raises(StructuralInconsistencyError, match="no chemical state"):
        topology.chemical_states._get_chemical_state_bonds()

    with pytest.raises(StructuralInconsistencyError, match="no chemical state"):
        topology.chemical_states._append_chemical_state_bonds([[0, 1]], orders="1")
    topology.chemical_states.append_state()
    topology.chemical_states._append_chemical_state_bonds([[0, 1]], orders="1")

    assert len(topology.chemical_states._states) == 1
    assert topology.chemical_states.reference_chemical_state_index == 0
    assert topology.chemical_states._get_chemical_state_bonds()[
        "bond_order"
    ].tolist() == [1]


def test_private_bond_seam_normalizes_unambiguous_legacy_columns():
    topology = MolSys(n_atoms=2)
    plain_table = pd.DataFrame(
        {
            "atom1_index": [0],
            "atom2_index": [1],
            "order": ["1.5"],
            "type": ["dative"],
        }
    )

    topology.chemical_states._set_chemical_state_bonds(plain_table)

    bonds = topology.chemical_states._get_chemical_state_bonds()
    assert isinstance(bonds, Bonds_DataFrame)
    assert str(bonds["atom1_index"].dtype) == "Int64"
    assert str(bonds["atom2_index"].dtype) == "Int64"
    assert bonds["fractional_bond_order"].tolist() == [1.5]
    assert bonds["bond_type"].tolist() == ["dative"]
    assert bonds["joins_components"].tolist() == [False]


def test_private_bond_seam_rejects_opaque_legacy_metadata():
    topology = MolSys(n_atoms=2)
    plain_table = pd.DataFrame(
        {
            "atom1_index": [0],
            "atom2_index": [1],
            "type": ["amide"],
        }
    )

    with pytest.raises(StructuralInconsistencyError, match="no unambiguous mapping"):
        topology.chemical_states._set_chemical_state_bonds(plain_table)


def test_normalized_bond_table_uses_nullable_canonical_dtypes():
    topology = MolSys(n_atoms=4)
    topology.chemical_states._append_chemical_state_bonds(
        [[1, 0]],
        bond_id="external-7",
        bond_order=2,
        fractional_bond_order=1.75,
        bond_type="dative",
        is_aromatic=False,
        is_conjugated=True,
        stereochemistry="E",
        stereo_atom1_index=2,
        stereo_atom2_index=3,
        donor_atom_index=0,
        acceptor_atom_index=1,
        evidence="explicit",
        provenance_index=4,
    )

    bonds = topology.chemical_states._get_chemical_state_bonds()
    assert bonds[["atom1_index", "atom2_index"]].values.tolist() == [[0, 1]]
    assert str(bonds["bond_id"].dtype) == "string"
    assert str(bonds["bond_order"].dtype) == "UInt8"
    assert str(bonds["fractional_bond_order"].dtype) == "Float64"
    assert str(bonds["bond_type"].dtype) == "string"
    assert str(bonds["is_aromatic"].dtype) == "boolean"
    assert str(bonds["is_conjugated"].dtype) == "boolean"
    assert str(bonds["stereo_atom1_index"].dtype) == "Int64"
    assert str(bonds["donor_atom_index"].dtype) == "Int64"
    assert bonds["joins_components"].tolist() == [False]


def test_normalized_bond_table_rejects_malformed_graph_edges():
    topology = MolSys(n_atoms=3)

    with pytest.raises(StructuralInconsistencyError, match="Self-bonds"):
        topology.chemical_states._append_chemical_state_bonds([[1, 1]])

    topology.chemical_states._append_chemical_state_bonds([[0, 1]])
    with pytest.raises(StructuralInconsistencyError, match="Only one bond"):
        topology.chemical_states._append_chemical_state_bonds([[1, 0]])

    with pytest.raises(StructuralInconsistencyError, match="one of the bond endpoints"):
        MolSys(n_atoms=3).chemical_states._append_chemical_state_bonds(
            [[0, 1]], donor_atom_index=2
        )


def test_non_default_component_participation_requires_evidence():
    topology = MolSys(n_atoms=2)

    with pytest.raises(
        StructuralInconsistencyError, match="requires explicit bond evidence"
    ):
        topology.chemical_states._append_chemical_state_bonds(
            [[0, 1]], bond_type="dative", joins_components=True
        )

    topology.chemical_states._append_chemical_state_bonds(
        [[0, 1]], bond_type="dative", joins_components=True, evidence="explicit"
    )
    assert topology.chemical_states._resolve_chemical_state().bonds[
        "joins_components"
    ].tolist() == [True]


def test_component_inference_excludes_explicit_non_participating_bonds():
    topology = MolSys(n_atoms=3)
    topology.chemical_states._append_chemical_state_bonds(
        [[0, 1]], bond_type="covalent"
    )
    topology.chemical_states._append_chemical_state_bonds([[1, 2]], bond_type="dative")

    topology.rebuild_components(
        redefine_indices=True,
        redefine_ids=True,
        redefine_types=False,
        redefine_names=False,
    )

    assert topology.chemical_states._get_component_indices().tolist() == [0, 0, 1]
    assert (
        topology.chemical_states._resolve_chemical_state().component_evidence
        == "inferred"
    )
    assert (
        topology.chemical_states._resolve_chemical_state().component_completeness
        == "partial"
    )


def test_extract_remaps_all_bond_atom_references_together():
    topology = build_minimal_chemical_molsys()
    topology.chemical_states.remove_bonds("all")
    topology.chemical_states._append_chemical_state_bonds(
        [[1, 3]],
        bond_type="dative",
        donor_atom_index=3,
        acceptor_atom_index=1,
        stereochemistry="E",
        stereo_atom1_index=0,
        stereo_atom2_index=2,
    )

    extracted = topology.extract(atom_indices=[3, 1, 2], skip_digestion=True)
    bonds = extracted.chemical_states._get_chemical_state_bonds()

    assert bonds[["atom1_index", "atom2_index"]].values.tolist() == [[0, 2]]
    assert bonds["donor_atom_index"].tolist() == [2]
    assert bonds["acceptor_atom_index"].tolist() == [0]
    assert "stereochemistry" not in bonds
    assert "stereo_atom1_index" not in bonds
    assert "stereo_atom2_index" not in bonds


def test_native_add_offsets_all_bond_atom_references():
    left = build_minimal_chemical_molsys()
    right = build_minimal_chemical_molsys()
    right.chemical_states.remove_bonds("all")
    right.chemical_states._append_chemical_state_bonds(
        [[1, 3]],
        bond_type="dative",
        donor_atom_index=3,
        acceptor_atom_index=1,
        stereochemistry="E",
        stereo_atom1_index=0,
        stereo_atom2_index=2,
    )

    left.add(right, skip_digestion=True)
    added_bond = (
        left.chemical_states._resolve_chemical_state()
        .bonds.loc[
            left.chemical_states._resolve_chemical_state()
            .bonds["donor_atom_index"]
            .notna()
        ]
        .iloc[0]
    )

    assert [added_bond["atom1_index"], added_bond["atom2_index"]] == [5, 7]
    assert added_bond["donor_atom_index"] == 7
    assert added_bond["acceptor_atom_index"] == 5
    assert added_bond["stereo_atom1_index"] == 4
    assert added_bond["stereo_atom2_index"] == 6


def test_private_bond_append_validates_shape_bounds_and_metadata_lengths():
    topology = MolSys(n_atoms=3)

    with pytest.raises(StructuralInconsistencyError, match=r"shape \(n_bonds, 2\)"):
        topology.chemical_states._append_chemical_state_bonds([0, 1])
    with pytest.raises(StructuralInconsistencyError, match="between 0 and 2"):
        topology.chemical_states._append_chemical_state_bonds([[0, 3]])
    with pytest.raises(
        StructuralInconsistencyError, match="received 1 values; expected 2"
    ):
        topology.chemical_states._append_chemical_state_bonds(
            [[0, 1], [1, 2]], orders=["1"]
        )


def test_private_bond_removal_isolated_to_explicit_state():
    topology = MolSys(n_atoms=3)
    topology.chemical_states._append_chemical_state_bonds([[0, 1]], orders="1")
    second_index = topology.chemical_states._append_state(
        _ChemicalStateStorage(n_atoms=topology.get_n_atoms(), state_id="product"),
        set_as_reference=False,
    )
    topology.chemical_states._append_chemical_state_bonds(
        [[0, 2], [1, 2]], orders=["1", "2"], state_index=second_index
    )

    topology.chemical_states.remove_bonds([0], chemical_state=second_index)

    assert topology.chemical_states._get_chemical_state_bonds()[
        "bond_order"
    ].tolist() == [1]
    assert topology.chemical_states._get_chemical_state_bonds(state_index=second_index)[
        "bond_order"
    ].tolist() == [2]


def test_multistate_extract_preserves_and_remaps_each_state_independently():
    topology = build_minimal_chemical_molsys()
    topology.chemical_states._set_chemical_state_atom_attribute(
        "formal_charge", [0, 0, -1, 1]
    )
    second_index = topology.chemical_states._append_state(
        _ChemicalStateStorage(n_atoms=topology.get_n_atoms(), state_id="product"),
        set_as_reference=False,
    )
    topology.chemical_states._set_component_indices(
        [0, 1, 1, 1], state_index=second_index
    )
    topology.chemical_states._states[
        second_index
    ].components = topology.chemical_states._resolve_chemical_state().components.copy()
    topology.chemical_states._states[second_index].components.loc[
        0, "component_name"
    ] = "reactant fragment"
    topology.chemical_states._append_chemical_state_bonds(
        [[0, 2], [2, 3]], orders=[1, 2], state_index=second_index
    )
    topology.chemical_states._set_reference_index(None)

    extracted = topology.extract(atom_indices=[0, 2, 3], skip_digestion=True)

    assert len(extracted.chemical_states._states) == 2
    assert extracted.chemical_states.reference_chemical_state_index is None
    assert extracted.chemical_states._get_component_indices(state_index=0).tolist() == [
        0,
        1,
        1,
    ]
    assert extracted.chemical_states._get_component_indices(
        state_index=second_index
    ).tolist() == [
        0,
        1,
        1,
    ]
    assert extracted.chemical_states._states[0].components[
        "component_name"
    ].tolist() == [
        "peptide 0",
        "water",
    ]
    assert extracted.chemical_states._states[second_index].components[
        "component_name"
    ].tolist() == ["reactant fragment", "water"]
    assert (
        extracted.chemical_states._get_chemical_state_bonds(state_index=0).shape[0] == 0
    )
    assert extracted.chemical_states._get_chemical_state_bonds(
        state_index=second_index
    )[["atom1_index", "atom2_index"]].values.tolist() == [[0, 1], [1, 2]]
    assert extracted.chemical_states._states[0].atom_attributes[
        "formal_charge"
    ].tolist() == [
        0,
        -1,
        1,
    ]


def test_component_membership_seam_supports_full_and_partial_updates():
    topology = MolSys(n_atoms=3)

    assert topology.chemical_states._get_component_indices().isna().any()

    topology.chemical_states._set_component_indices([0, 0, 1])

    assert topology.chemical_states._get_component_indices().tolist() == [0, 0, 1]
    assert not topology.chemical_states._get_component_indices().isna().any()

    topology.chemical_states._set_component_indices(pd.NA, atom_indices=1)

    assert topology.chemical_states._get_component_indices().tolist() == [0, pd.NA, 1]
    assert topology.chemical_states._get_component_indices().isna().any()

    with pytest.raises(StructuralInconsistencyError, match="must be non-negative"):
        topology.chemical_states._set_component_indices([0, -1, 1])


def test_copy_keeps_reference_chemical_state_storage_independent():
    topology = build_minimal_chemical_molsys()
    cloned = topology.copy()

    cloned.chemical_states._resolve_chemical_state().bonds.at[0, "bond_order"] = 2
    cloned.chemical_states._resolve_chemical_state().components.at[
        0, "component_name"
    ] = "changed"

    assert (
        topology.chemical_states._resolve_chemical_state().bonds.at[0, "bond_order"]
        == 1
    )
    assert (
        topology.chemical_states._resolve_chemical_state().components.at[
            0, "component_name"
        ]
        == "peptide 0"
    )


def test_copy_preserves_all_private_states_and_reference_independently():
    topology = build_minimal_chemical_molsys()
    topology.chemical_states._set_chemical_state_atom_attribute(
        "formal_charge", [0, 0, -1, 1]
    )
    topology.chemical_states._resolve_chemical_state().connectivity_completeness = (
        "complete"
    )
    second_index = topology.chemical_states._append_state(
        _ChemicalStateStorage(n_atoms=topology.get_n_atoms(), state_id="product"),
        set_as_reference=True,
    )
    topology.chemical_states._states[second_index].connectivity_completeness = "partial"

    cloned = topology.copy()
    cloned.chemical_states._states[0].bonds.at[0, "bond_order"] = 2
    cloned.chemical_states._states[0].atom_attributes.at[0, "formal_charge"] = 1
    cloned.chemical_states._states[second_index].state_id = "changed"

    assert cloned.chemical_states.reference_chemical_state_index == second_index
    assert topology.chemical_states._states[0].bonds.at[0, "bond_order"] == 1
    assert (
        topology.chemical_states._states[0].atom_attributes.at[0, "formal_charge"] == 0
    )
    assert topology.chemical_states._states[second_index].state_id == "product"


def test_pickle_roundtrip_preserves_reference_chemical_state_storage():
    topology = build_minimal_chemical_molsys()

    restored = pickle.loads(pickle.dumps(topology))

    assert (
        restored.chemical_states.get_bonds()
        is restored.chemical_states._states[0].bonds
    )
    assert restored.chemical_states._molsys_owner_ref() is restored
    assert restored.chemical_states._resolve_chemical_state().bonds[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [[0, 1]]
    assert restored.chemical_states._resolve_chemical_state().components[
        "component_name"
    ].tolist() == ["peptide 0", "water"]


def test_pickle_roundtrip_preserves_private_state_collection_and_metadata():
    topology = build_minimal_chemical_molsys()
    topology.chemical_states._set_chemical_state_atom_attribute(
        "formal_charge", [0, 0, -1, 1]
    )
    topology.chemical_states._resolve_chemical_state().connectivity_completeness = (
        "complete"
    )
    second_index = topology.chemical_states._append_state(
        _ChemicalStateStorage(n_atoms=topology.get_n_atoms(), state_id="product"),
        set_as_reference=True,
    )
    topology.chemical_states._states[second_index].component_evidence = "user_defined"

    restored = pickle.loads(pickle.dumps(topology))

    assert len(restored.chemical_states._states) == 2
    assert restored.chemical_states.reference_chemical_state_index == second_index
    assert restored.chemical_states._states[0].connectivity_completeness == "complete"
    assert restored.chemical_states._states[0].atom_attributes[
        "formal_charge"
    ].tolist() == [
        0,
        0,
        -1,
        1,
    ]
    assert (
        restored.chemical_states._resolve_chemical_state().component_evidence
        == "user_defined"
    )


def test_legacy_direct_table_state_migrates_on_restore():
    source = build_minimal_chemical_molsys()
    legacy = source.topology.__getstate__()
    legacy["bonds"] = source.chemical_states.get_bonds()
    legacy["components"] = source.chemical_states._states[0].components
    restored = Topology.__new__(Topology)
    with pytest.raises(ValueError, match="Legacy Topology pickle carries chemistry"):
        restored.__setstate__(legacy)
    assert vars(restored) == {}
    assert source.chemical_states.get(n_bonds=True, n_components=True) == [1, 2]


def test_legacy_atom_component_column_migrates_to_reference_state_on_restore():
    source = build_minimal_chemical_molsys()
    legacy = source.topology.__getstate__()
    legacy["atoms"] = pd.DataFrame(source.topology.atoms.copy())
    legacy["atoms"]["component_index"] = [0, 0, 1, 1]
    legacy["bonds"] = source.chemical_states.get_bonds()
    legacy["components"] = source.chemical_states._states[0].components
    restored = Topology.__new__(Topology)
    with pytest.raises(ValueError, match="Legacy Topology pickle carries chemistry"):
        restored.__setstate__(legacy)
    assert vars(restored) == {}
    assert source.chemical_states.get(n_bonds=True, n_components=True) == [1, 2]


def test_intermediate_reference_state_storage_migrates_on_restore():
    source = build_minimal_chemical_molsys()
    legacy = source.topology.__getstate__()
    legacy["_reference_chemical_state"] = source.chemical_states._states[0]
    restored = Topology.__new__(Topology)
    with pytest.raises(ValueError, match="Legacy Topology pickle carries chemistry"):
        restored.__setstate__(legacy)
    assert vars(restored) == {}
    assert source.chemical_states.get(n_bonds=True, n_components=True) == [1, 2]


def test_extract_reindexes_hierarchy_and_bonds():
    topology = build_minimal_chemical_molsys()
    topology.chemical_states._set_chemical_state_atom_attribute(
        "formal_charge", [0, 1, -1, 0]
    )
    extracted = topology.extract(atom_indices=[0, 1], skip_digestion=True)

    assert extracted.topology.n_atoms == 2
    assert extracted.topology.n_groups == 1
    assert extracted.chemical_states.get(n_components=True) == 1
    assert extracted.topology.n_molecules == 1
    assert extracted.topology.n_entities == 1
    assert extracted.topology.n_chains == 1
    assert extracted.chemical_states._resolve_chemical_state().bonds[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [[0, 1]]
    assert extracted.topology.atoms["group_index"].tolist() == [0, 0]
    assert extracted.chemical_states._get_component_indices().tolist() == [0, 0]
    assert extracted.topology.atoms["chain_index"].tolist() == [0, 0]
    assert extracted.chemical_states._get_chemical_state_atom_attribute(
        "formal_charge"
    ).tolist() == [
        0,
        1,
    ]


def test_remove_returns_topology_without_removed_atoms():
    topology = build_minimal_topology()
    trimmed = topology.remove(atom_indices=[2, 3], skip_digestion=True)

    assert trimmed.n_atoms == 2
    assert trimmed.atoms["atom_id"].tolist() == ["0", "1"]
    assert trimmed.n_groups == 1


def test_add_offsets_indices_and_can_rebuild_ids():
    left = build_minimal_chemical_molsys()
    right = build_minimal_chemical_molsys()
    left.chemical_states._set_chemical_state_atom_attribute(
        "formal_charge", [0, 1, 0, -1]
    )
    right.chemical_states._set_chemical_state_atom_attribute(
        "formal_charge", [-1, 0, 1, 0]
    )

    left.add(right, keep_ids=False, skip_digestion=True)

    assert left.topology.n_atoms == 8
    assert left.topology.n_groups == 4
    assert left.chemical_states.get(n_components=True) == 6
    assert left.topology.n_molecules == 4
    assert left.topology.n_entities == 4
    assert left.topology.n_chains == 4
    assert left.chemical_states.get(n_bonds=True) == 2
    assert left.topology.atoms["group_index"].tolist() == [0, 0, 1, 1, 2, 2, 3, 3]
    assert left.chemical_states._get_component_indices().tolist() == [
        0,
        0,
        1,
        2,
        3,
        3,
        4,
        5,
    ]
    assert left.chemical_states._resolve_chemical_state().bonds[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [
        [0, 1],
        [4, 5],
    ]
    assert left.topology.atoms["atom_id"].map(type).eq(str).all()
    assert left.topology.groups["group_id"].map(type).eq(str).all()
    assert left.topology.molecules["entity_index"].tolist() == [0, 1, 2, 3]
    assert left.chemical_states._get_chemical_state_atom_attribute(
        "formal_charge"
    ).tolist() == [
        0,
        1,
        0,
        -1,
        -1,
        0,
        1,
        0,
    ]


def test_add_bonds_sorts_pairs_and_rebuilds_components():
    topology = build_minimal_chemical_molsys()
    topology.chemical_states.add_bonds([[3, 2], [2, 1]], skip_digestion=True)

    assert topology.chemical_states.get(n_bonds=True) == 3
    assert topology.chemical_states._resolve_chemical_state().bonds[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [
        [0, 1],
        [1, 2],
        [2, 3],
    ]
    assert topology.chemical_states._get_component_indices().tolist() == [0, 0, 0, 0]


def test_remove_bonds_all_resets_connectivity():
    topology = build_minimal_chemical_molsys()
    topology.chemical_states.add_bonds([[2, 3]], skip_digestion=True)

    topology.chemical_states.remove_bonds("all", skip_digestion=True)

    assert topology.chemical_states.get(n_bonds=True) == 0
    assert topology.chemical_states._resolve_chemical_state().components.shape[0] == 4
    assert topology.chemical_states._get_component_indices().tolist() == [0, 1, 2, 3]


def test_remove_specific_bond_keeps_remaining_bonds():
    topology = build_minimal_chemical_molsys()
    topology.chemical_states.add_bonds([[2, 3]], skip_digestion=True)

    topology.chemical_states.remove_bonds([0], skip_digestion=True)

    assert topology.chemical_states._resolve_chemical_state().bonds[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [[2, 3]]


def test_fix_null_values_normalizes_id_columns_to_string_dtype():
    topology = build_minimal_chemical_molsys()
    topology.topology.atoms.at[0, "atom_id"] = None
    topology.topology.groups.at[0, "group_id"] = None
    topology.chemical_states._resolve_chemical_state().components.at[
        0, "component_id"
    ] = None
    topology.topology.molecules.at[0, "molecule_id"] = None
    topology.topology.entities.at[0, "entity_id"] = None
    topology.topology.chains.at[0, "chain_id"] = None

    topology.topology._fix_null_values()
    topology.chemical_states._states[0].components._fix_null_values()

    assert str(topology.topology.atoms["atom_id"].dtype) == "string"
    assert str(topology.topology.groups["group_id"].dtype) == "string"
    assert (
        str(
            topology.chemical_states._resolve_chemical_state()
            .components["component_id"]
            .dtype
        )
        == "string"
    )
    assert str(topology.topology.molecules["molecule_id"].dtype) == "string"
    assert str(topology.topology.entities["entity_id"].dtype) == "string"
    assert str(topology.topology.chains["chain_id"].dtype) == "string"


def test_sort_bonds_orders_atom_pairs_in_place():
    topology = build_minimal_chemical_molsys()
    topology.chemical_states._states[0].bonds = Bonds_DataFrame(n_bonds=2)
    topology.chemical_states._resolve_chemical_state().bonds["atom1_index"] = pd.Series(
        [3, 1], dtype="Int64"
    )
    topology.chemical_states._resolve_chemical_state().bonds["atom2_index"] = pd.Series(
        [2, 0], dtype="Int64"
    )
    topology.chemical_states._resolve_chemical_state().bonds["bond_order"] = pd.array(
        [1, 1], dtype="UInt8"
    )
    topology.chemical_states._resolve_chemical_state().bonds["bond_type"] = pd.array(
        ["covalent", "covalent"], dtype="string"
    )

    topology.chemical_states.get_bonds()._sort_bonds()

    assert topology.chemical_states._resolve_chemical_state().bonds[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [
        [0, 1],
        [2, 3],
    ]


def test_compare_supports_boolean_and_dictionary_outputs():
    left = build_minimal_topology()
    right = build_minimal_topology()

    result = msm.compare(
        left,
        right,
        rule="equal",
        output_type="dictionary",
        n_atoms=True,
        atom_id=True,
        atom_name=True,
        atom_type=True,
        n_groups=True,
        group_index=True,
        group_id=True,
        group_name=True,
        group_type=True,
        component_index=True,
        component_id=True,
        component_name=True,
        component_type=True,
        molecule_index=True,
        molecule_id=True,
        molecule_name=True,
        molecule_type=True,
        entity_index=True,
        entity_id=True,
        entity_name=True,
        entity_type=True,
        chain_index=True,
        chain_id=True,
        chain_name=True,
        chain_type=True,
        n_bonds=True,
        bonded_atom_pairs=True,
        skip_digestion=True,
    )

    assert all(result.values())
    assert (
        msm.compare(
            left,
            right,
            rule="equal",
            output_type="boolean",
            atom_name=True,
            group_name=True,
            skip_digestion=True,
        )
        is True
    )

    right.atoms.at[0, "atom_name"] = "X"
    mismatch = msm.compare(
        left,
        right,
        rule="equal",
        output_type="dictionary",
        atom_name=True,
        skip_digestion=True,
    )
    assert mismatch == {"atom_name": False}


def test_get_atom_indices_filters_across_hierarchy_levels():
    topology = build_minimal_topology()

    assert topology.get_atom_indices(atom_name="N") == [0]
    assert topology.get_atom_indices(group_name="HOH") == [2, 3]
    assert msm.select(build_minimal_chemical_molsys(), "component_type=='peptide'") == [
        0,
        1,
    ]
    assert topology.get_atom_indices(molecule_name="water") == [2, 3]
    assert topology.get_atom_indices(entity_name="peptide 0") == [0, 1]
    assert topology.get_atom_indices(chain_name="B") == [2, 3]
    assert topology.get_atom_indices(atom_id=["0", "1"], entity_id="40") == [0, 1]
