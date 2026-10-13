"""Protect chemically admitted permutations, source axes and bounded search."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
    StructuralInconsistencyError,
    UnsupportedHeavyOperationError,
)


@pytest.mark.parametrize("source", ["smiles:c1ccccc1", Chem.MolFromSmiles("c1ccccc1")])
def test_benzene_has_twelve_chemically_admitted_permutations(source):
    result = msm.topology.get_atom_correspondences(source)
    maps = result["atom_correspondences"]
    assert maps.shape == (12, 6, 2) and maps.dtype == np.int64
    assert np.all(maps[:, :, 0] == np.arange(6))
    assert result["search_complete"] and result["n_candidate_matches"] == 12
    assert maps[:, :, 1].tolist() == sorted(maps[:, :, 1].tolist())
    assert len({tuple(row) for row in maps[:, :, 1]}) == 12
    # Analytic dihedral group: six rotations and six reversals of the ring.
    admitted = {tuple((np.arange(6) + shift) % 6) for shift in range(6)}
    admitted |= {tuple((-np.arange(6) + shift) % 6) for shift in range(6)}
    assert {tuple(row) for row in maps[:, :, 1]} == admitted


def test_benzamidinium_permits_phenyl_symmetry_but_never_swaps_nitrogens():
    result = msm.topology.get_atom_correspondences("smiles:NC(=[NH2+])c1ccccc1")
    maps = result["atom_correspondences"]
    assert maps.shape == (2, 9, 2)
    assert np.all(maps[:, 0, 1] == 0) and np.all(maps[:, 2, 1] == 2)


@pytest.mark.parametrize(
    "query,reference",
    [
        ("C[C@H](O)F", "C[C@@H](O)F"),
        ("F/C=C/F", "F/C=C\\F"),
        ("CCO", "CC[O-]"),
        ("[13CH3]CO", "CCO"),
        ("CCO", "COC"),
        ("CC", "C=C"),
        ("[CH3]", "C"),
    ],
)
def test_nonequivalent_states_have_typed_empty_matches(query, reference):
    result = msm.topology.get_atom_correspondences(
        "smiles:" + query, reference_molecular_system="smiles:" + reference
    )
    assert result["atom_correspondences"].shape == (
        0,
        Chem.MolFromSmiles(query).GetNumAtoms(),
        2,
    )
    assert result["atom_correspondences"].dtype == np.int64


@pytest.mark.parametrize("smiles", ["CC(O)F", "FC=CF"])
def test_unassigned_potential_stereochemistry_is_not_certified(smiles):
    with pytest.raises(StructuralInconsistencyError, match="stereochemistry"):
        msm.topology.get_atom_correspondences("smiles:" + smiles)


def test_selection_preserves_full_component_context_and_source_positions():
    molsys = msm.convert(Chem.MolFromSmiles("O.CCO"), to_form="molsysmt.MolSys")
    result = msm.topology.get_atom_correspondences(molsys, selection=[3, 1])
    assert result["selection_atom_indices"].tolist() == [1, 3]
    assert result["atom_correspondences"].tolist() == [[[1, 1], [3, 3]]]
    assert result["context_atom_correspondences"].tolist() == [[[1, 1], [2, 2], [3, 3]]]
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_atom_correspondences(molsys, selection="all")


def test_explicit_hydrogens_remain_context_when_metric_excludes_them():
    molsys = Chem.AddHs(Chem.MolFromSmiles("CC"))
    result = msm.topology.get_atom_correspondences(molsys, selection=[0, 1])
    assert result["atom_correspondences"].shape == (2, 2, 2)
    assert result["context_atom_correspondences"].shape == (2, 8, 2)
    assert result["n_candidate_matches"] == 72


def test_reordered_reference_preserves_original_reference_indices():
    query = Chem.MolFromSmiles("CCO")
    reference = Chem.RenumberAtoms(query, [2, 0, 1])
    result = msm.topology.get_atom_correspondences(
        query, reference_molecular_system=reference
    )
    assert result["atom_correspondences"].tolist() == [[[0, 1], [1, 2], [2, 0]]]


@pytest.mark.parametrize(
    "attribute",
    ["formal_charge", "is_aromatic", "n_implicit_hydrogens", "stereochemistry"],
)
def test_missing_chemical_evidence_is_not_inferred(attribute):
    molsys = msm.convert(Chem.MolFromSmiles("CCO"), to_form="molsysmt.MolSys")
    molsys.chemical_states._states[0].atom_attributes.loc[0, attribute] = pd.NA
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_atom_correspondences(molsys)


def test_missing_and_malformed_connectivity_are_refused():
    molsys = msm.convert(Chem.MolFromSmiles("CCO"), to_form="molsysmt.MolSys")
    state = molsys.chemical_states._states[0]
    state.connectivity_completeness = "partial"
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_atom_correspondences(molsys)
    state.connectivity_completeness = "complete"
    state.bonds.loc[0, "atom2_index"] = 0
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_atom_correspondences(molsys)


def test_search_bound_precedes_projection_and_never_truncates():
    with pytest.raises(UnsupportedHeavyOperationError):
        msm.topology.get_atom_correspondences(
            "smiles:c1ccccc1", selection=[0], max_matches=5
        )
    with pytest.raises(UnsupportedHeavyOperationError):
        msm.topology.get_atom_correspondences(
            Chem.AddHs(Chem.MolFromSmiles("CC")), selection=[0, 1], max_matches=10
        )


def test_candidate_budget_fails_without_returning_partial_results(monkeypatch):
    monkeypatch.setattr(msm.configure, "max_ram_usage", 512)
    with pytest.raises(MemoryBudgetExceededError):
        msm.topology.get_atom_correspondences("smiles:c1ccccc1")


def test_native_chemistry_is_read_only_and_topology_form_has_parity():
    molsys = msm.convert(Chem.MolFromSmiles("c1ccccc1"), to_form="molsysmt.MolSys")
    # A chemically valid generic table must remain generic during read-only work.
    molsys.chemical_states._states[0].bonds = pd.DataFrame(
        molsys.chemical_states._states[0].bonds
    ).copy(deep=True)
    original_bonds = molsys.chemical_states._states[0].bonds
    atoms = molsys.chemical_states._states[0].atom_attributes.copy(deep=True)
    bonds = molsys.chemical_states._states[0].bonds.copy(deep=True)
    native = msm.topology.get_atom_correspondences(molsys)
    other = msm.topology.get_atom_correspondences(molsys.topology)
    np.testing.assert_array_equal(
        native["atom_correspondences"], other["atom_correspondences"]
    )
    pd.testing.assert_frame_equal(
        atoms, molsys.chemical_states._states[0].atom_attributes
    )
    pd.testing.assert_frame_equal(bonds, molsys.chemical_states._states[0].bonds)
    assert molsys.chemical_states._states[0].bonds is original_bonds
    saved = deepcopy(native)
    native["references"][0]["authors"].append("changed")
    assert saved["references"][0]["authors"] == ["Bell, Eric W.", "Zhang, Yang"]


def test_legacy_dictionary_missing_fixed_chemistry_cannot_certify_equivalence():
    molsys = msm.convert(Chem.MolFromSmiles("CCO"), to_form="molsysmt.MolSys")
    columns = msm.convert(molsys, to_form="molsysmt.MolSysDict")
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_atom_correspondences(columns)


@pytest.mark.parametrize(
    "options",
    [
        {"method": "rdkit"},
        {"max_matches": True},
        {"reference_chemical_state": -1},
        {"selection": []},
        {"selection": True},
        {"selection": [True, 2]},
        {"selection": [1.5]},
        {"reference_structure_indices": [True]},
        {"structure_indices": [[0]]},
    ],
)
def test_invalid_public_arguments_fail(options):
    with pytest.raises(ArgumentError):
        msm.topology.get_atom_correspondences("smiles:CCO", **options)


def test_different_h_encodings_are_explicitly_outside_exact_declared_profile():
    reference = Chem.MolFromSmiles("CC")
    explicit = Chem.AddHs(reference)
    result = msm.topology.get_atom_correspondences(
        explicit,
        selection=[0, 1],
        reference_molecular_system=reference,
        reference_selection=[0, 1],
    )
    assert result["atom_correspondences"].shape == (0, 2, 2)


def test_projected_h_witnesses_are_lexical_independent_of_bond_insertion():
    molsys = msm.convert(
        Chem.AddHs(Chem.MolFromSmiles("CC")), to_form="molsysmt.MolSys"
    )
    first = msm.topology.get_atom_correspondences(molsys, selection=[0, 1])
    state = molsys.chemical_states._states[0]
    state.bonds = state.bonds.iloc[::-1].reset_index(drop=True)
    second = msm.topology.get_atom_correspondences(molsys, selection=[0, 1])
    np.testing.assert_array_equal(
        first["context_atom_correspondences"], second["context_atom_correspondences"]
    )


@pytest.mark.parametrize(
    "attribute,value",
    [("formal_charge", 0.5), ("n_implicit_hydrogens", -1.0), ("is_aromatic", "False")],
)
def test_malformed_declared_chemistry_is_not_coerced_to_an_equivalence(
    attribute, value
):
    molsys = msm.convert(Chem.MolFromSmiles("CCO"), to_form="molsysmt.MolSys")
    attributes = molsys.chemical_states._states[0].atom_attributes
    attributes[attribute] = attributes[attribute].astype(object)
    attributes.loc[0, attribute] = value
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_atom_correspondences(molsys)
