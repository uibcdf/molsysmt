"""Checking explicit provider aromaticity independently of geometric ring rules."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError

Chem = pytest.importorskip("rdkit.Chem")


@pytest.mark.parametrize(
    "smiles,aromatic_atoms,aromatic_bonds",
    [
        ("CCO", 0, 0),
        ("C1CCCCC1", 0, 0),
        ("c1ccccc1", 6, 6),
        ("c1ccncc1", 6, 6),
        ("c1cc[nH]c1", 5, 5),
        ("c1ccc2ccccc2c1", 10, 11),
        ("C1=CC2=C(C=C1)C1=CC=CC=C21", 12, 12),
    ],
)
def test_named_model_independent_ring_and_fusion_controls(
    smiles, aromatic_atoms, aromatic_bonds
):
    source = Chem.MolFromSmiles(smiles)
    before = Chem.MolToMolBlock(source)
    result = msm.physchem.get_aromaticity(source)
    assert result["atom_is_aromatic"].dtype == np.bool_
    assert result["atom_is_aromatic"].sum() == aromatic_atoms
    assert result["bond_is_aromatic"].sum() == aromatic_bonds
    assert result["software"]["rdkit"]
    assert result["implementation"] == "rdkit.AROMATICITY_RDKIT"
    assert Chem.MolToMolBlock(source) == before
    assert not any(atom.HasProp("_GasteigerCharge") for atom in source.GetAtoms())
    if "C1=CC2" in smiles:
        assert result["atom_is_aromatic"][[3, 6]].all()
        index = np.flatnonzero(np.all(result["bonded_atom_pairs"] == [3, 6], axis=1))[0]
        assert not result["bond_is_aromatic"][index]


def test_native_sdf_missing_flags_are_perceived_on_a_copy(tmp_path):
    source = msm.convert(
        msm.systems["caffeine"]["caffeine.sdf"], to_form="molsysmt.MolSys"
    )
    before = source.chemical_states._states[0].atom_attributes.copy()
    expected = msm.physchem.get_aromaticity(source)
    assert expected["atom_is_aromatic"].sum() == 9
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes, before
    )
    path = tmp_path / "chemical.h5msm"
    msm.convert(source, to_form=path)
    for item in [source.topology, str(path), msm.systems["caffeine"]["caffeine.sdf"]]:
        actual = msm.physchem.get_aromaticity(item, selection=[5, 0, 5])
        assert actual["atom_indices"].tolist() == [0, 5]
        np.testing.assert_array_equal(
            actual["atom_is_aromatic"], expected["atom_is_aromatic"][[0, 5]]
        )
    empty = msm.physchem.get_aromaticity(source, selection=[])
    assert empty["atom_is_aromatic"].shape == (0,)
    assert empty["bonded_atom_pairs"].shape == (0, 2)
    assert empty["bond_is_aromatic"].shape == (0,)


@pytest.mark.parametrize(
    "missing", ["formal_charge", "n_unpaired_electrons", "bond_order", "connectivity"]
)
def test_missing_prerequisite_fails_without_synthesizing_chemistry(missing):
    source = msm.convert(Chem.MolFromSmiles("CCO"), to_form="molsysmt.MolSys")
    state = source.chemical_states._states[0]
    if missing == "connectivity":
        state.connectivity_completeness = "partial"
    elif missing == "bond_order":
        state.bonds[missing] = pd.NA
    else:
        state.atom_attributes[missing] = pd.NA
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.get_aromaticity(source)


def test_known_aromatic_contradiction_is_not_overwritten():
    source = msm.convert(Chem.MolFromSmiles("c1ccccc1"), to_form="molsysmt.MolSys")
    source.chemical_states._states[0].atom_attributes["is_aromatic"] = False
    with pytest.raises(StructuralInconsistencyError, match="conflicts"):
        msm.physchem.get_aromaticity(source)
    assert not source.chemical_states._states[0].atom_attributes["is_aromatic"].any()


@pytest.mark.parametrize("smiles", ["[Na+]", "[CH3]", "*"])
def test_unsupported_provider_scope_fails_explicitly(smiles):
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.get_aromaticity(Chem.MolFromSmiles(smiles))


def test_explicit_frame_validation_and_original_state_resolution():
    source = Chem.MolFromSmiles("CCO")
    source.AddConformer(Chem.Conformer(source.GetNumAtoms()))
    assert msm.physchem.get_aromaticity(source, structure_indices=[0])[
        "atom_indices"
    ].tolist() == [0, 1, 2]
    with pytest.raises(ArgumentError):
        msm.physchem.get_aromaticity(source, structure_indices=[1])
    with pytest.raises(ArgumentError):
        msm.physchem.get_aromaticity(source, method="guess")


def test_query_graph_is_rejected_before_native_conversion():
    with pytest.raises(StructuralInconsistencyError, match="query"):
        msm.physchem.get_aromaticity(Chem.MolFromSmarts("[C]"))


def test_empty_graph_has_typed_empty_outputs():
    result = msm.physchem.get_aromaticity(Chem.Mol())
    assert result["atom_indices"].dtype == np.int64
    assert result["atom_is_aromatic"].shape == (0,)
    assert result["bond_is_aromatic"].dtype == np.bool_
    assert result["bonded_atom_pairs"].shape == (0, 2)


def test_nonreference_state_does_not_change_source_reference():
    source = msm.convert(Chem.MolFromSmiles("c1ccccc1"), to_form="molsysmt.MolSys")
    second = source.chemical_states._states[0].copy()
    second.state_id = "selected"
    source.chemical_states._states.append(second)
    result = msm.physchem.get_aromaticity(source, chemical_state=1)
    assert result["chemical_state_index"] == 1
    assert result["chemical_state_id"] == "selected"
    assert source.chemical_states._reference_index == 0


def test_rich_selection_does_not_mutate_a_provider_input():
    source = Chem.MolFromSmiles("c1ccccc1O")
    result = msm.physchem.get_aromaticity(source, selection="atom_type=='O'")
    assert result["atom_indices"].tolist() == [6]
    assert not any(atom.HasProp("_GasteigerCharge") for atom in source.GetAtoms())
