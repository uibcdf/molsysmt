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


def test_anchors_prune_compiled_enumeration_before_the_candidate_limit():
    with pytest.raises(UnsupportedHeavyOperationError):
        msm.topology.get_atom_correspondences("smiles:c1ccccc1", max_matches=2)
    result = msm.topology.get_atom_correspondences(
        "smiles:c1ccccc1", fixed_atom_correspondence=[[0, 0]], max_matches=2
    )
    assert result["n_candidate_matches"] == 2
    assert result["atom_correspondences"].shape == (2, 6, 2)
    assert np.all(result["atom_correspondences"][:, 0] == [0, 0])
    assert result["search_scope"] == "anchored_chemical_correspondences"
    only = msm.topology.get_atom_correspondences(
        "smiles:c1ccccc1", fixed_atom_correspondence=[[1, 1], [0, 0]], max_matches=1
    )
    np.testing.assert_array_equal(only["atom_correspondences"][0, :, 1], np.arange(6))
    assert only["fixed_atom_correspondence"].tolist() == [[0, 0], [1, 1]]


def test_context_anchors_can_fix_omitted_hydrogens_and_canonical_witnesses():
    source = Chem.AddHs(Chem.MolFromSmiles("CC"))
    result = msm.topology.get_atom_correspondences(
        source,
        selection=[0, 1],
        fixed_atom_correspondence=[[2, 2]],
        candidate_atom_correspondences=[[1, 1], [0, 0]],
        max_matches=1,
    )
    assert result["n_candidate_matches"] == 1
    assert result["context_atom_correspondences"][0].tolist() == [
        [index, index] for index in range(8)
    ]
    # A subset map still has to extend through the unselected context.
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_atom_correspondences(
            source,
            selection=[0, 1],
            fixed_atom_correspondence=[[2, 2]],
            candidate_atom_correspondences=[[0, 1], [1, 0]],
        )


def test_candidates_are_deduplicated_sorted_detached_and_use_source_indices():
    source = Chem.MolFromSmiles("[Na+].c1ccccc1")
    reference = Chem.RenumberAtoms(source, [6, 5, 4, 3, 2, 1, 0])
    first = np.column_stack((np.arange(1, 7), np.arange(5, -1, -1)))
    second = np.column_stack((np.arange(1, 7), np.arange(6) % 6))
    candidates = np.stack([first[::-1], second, first])
    result = msm.topology.get_atom_correspondences(
        source,
        selection=[6, 1, 2, 5, 4, 3, 1],
        reference_molecular_system=reference,
        reference_selection=[5, 2, 3, 0, 1, 4],
        candidate_atom_correspondences=candidates,
    )
    assert result["search_scope"] == "supplied_atom_correspondences"
    assert result["search_complete"] and result["n_candidate_matches"] == 2
    np.testing.assert_array_equal(result["atom_correspondences"], [second, first])
    candidates[:] = 0
    np.testing.assert_array_equal(
        result["candidate_atom_correspondences"], [second, first]
    )


@pytest.mark.parametrize(
    "pairs",
    [
        [[0, 0], [0, 1]],
        [[0, 0], [1, 0]],
        [[0.0, 0]],
        [[True, 0]],
        [[-1, 0]],
        [[6, 0]],
        [[0, 6]],
        [[0]],
        [[2**64 - 1, 0]],
    ],
)
def test_invalid_anchor_indices_raise_argument_error(pairs):
    with pytest.raises(ArgumentError):
        msm.topology.get_atom_correspondences(
            "smiles:c1ccccc1", fixed_atom_correspondence=pairs
        )


@pytest.mark.parametrize(
    "candidates",
    [
        [],
        [[0, 0]],
        [[0, 0], [1, 0]],
        [[0.0, 0], [1, 1]],
        [[True, 0], [1, 1]],
        [[[0, 0]], [[0, 0], [1, 1]]],
    ],
)
def test_invalid_or_incomplete_candidates_raise_argument_error(candidates):
    with pytest.raises(ArgumentError):
        msm.topology.get_atom_correspondences(
            "smiles:CC", candidate_atom_correspondences=candidates
        )


def test_candidates_cannot_override_bonds_labels_stereo_or_anchors():
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_atom_correspondences(
            "smiles:c1ccccc1",
            selection=[0, 1, 2],
            candidate_atom_correspondences=[[0, 0], [1, 2], [2, 1]],
        )
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_atom_correspondences(
            "smiles:CCO",
            candidate_atom_correspondences=[[0, 2], [1, 1], [2, 0]],
        )
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_atom_correspondences(
            "smiles:C[C@H](O)F",
            reference_molecular_system="smiles:C[C@@H](O)F",
            candidate_atom_correspondences=np.column_stack(
                (np.arange(4), np.arange(4))
            ),
        )
    with pytest.raises(ArgumentError):
        msm.topology.get_atom_correspondences(
            "smiles:CC",
            fixed_atom_correspondence=[[0, 1]],
            candidate_atom_correspondences=[[0, 0], [1, 1]],
        )
    empty = msm.topology.get_atom_correspondences(
        "smiles:CCO",
        fixed_atom_correspondence=[[0, 2]],
    )
    assert empty["atom_correspondences"].shape == (0, 3, 2)
    assert empty["search_complete"]


def test_candidates_have_a_bound_and_empty_anchors_are_unrestricted():
    maps = msm.topology.get_atom_correspondences("smiles:c1ccccc1")[
        "atom_correspondences"
    ]
    with pytest.raises(UnsupportedHeavyOperationError):
        msm.topology.get_atom_correspondences(
            "smiles:c1ccccc1",
            candidate_atom_correspondences=maps,
            max_matches=2,
        )
    result = msm.topology.get_atom_correspondences(
        "smiles:c1ccccc1", fixed_atom_correspondence=[]
    )
    assert result["search_scope"] == "all_chemical_correspondences"
    assert result["fixed_atom_correspondence"].shape == (0, 2)


def test_one_bad_candidate_fails_the_whole_proposal_and_outside_component_anchors_fail():
    valid = np.column_stack((np.arange(3), np.arange(3)))
    invalid = np.column_stack((np.arange(3), [2, 1, 0]))
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_atom_correspondences(
            "smiles:CCO", candidate_atom_correspondences=[valid, invalid]
        )
    with pytest.raises(ArgumentError):
        msm.topology.get_atom_correspondences(
            "smiles:CC.[Na+]", selection=[0, 1], fixed_atom_correspondence=[[2, 2]]
        )


def test_proposed_context_witness_is_independent_of_bond_insertion_order():
    source = Chem.AddHs(Chem.MolFromSmiles("CC"))
    rebuilt = Chem.RWMol()
    for atom in source.GetAtoms():
        rebuilt.AddAtom(Chem.Atom(atom))
    for bond in reversed(list(source.GetBonds())):
        rebuilt.AddBond(
            bond.GetBeginAtomIdx(), bond.GetEndAtomIdx(), bond.GetBondType()
        )
    rebuilt = rebuilt.GetMol()
    Chem.SanitizeMol(rebuilt)
    options = dict(selection=[0, 1], candidate_atom_correspondences=[[0, 1], [1, 0]])
    original = msm.topology.get_atom_correspondences(source, **options)
    reordered = msm.topology.get_atom_correspondences(rebuilt, **options)
    np.testing.assert_array_equal(
        original["context_atom_correspondences"],
        reordered["context_atom_correspondences"],
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
