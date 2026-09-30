"""Testing formal-charge center chemistry independently of interaction geometry."""

from importlib.util import find_spec

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys, Structures, Topology


def _topology(elements, charges, bonds=(), orders=()):
    topology = Topology(n_atoms=len(elements))
    topology.atoms["atom_id"] = [
        f"atom-{index + 100}" for index in range(len(elements))
    ]
    topology.atoms["atom_type"] = elements
    topology._set_chemical_state_atom_attribute("formal_charge", charges)
    if bonds:
        topology._append_chemical_state_bonds(bonds, orders=orders, types="covalent")
    topology._reference_chemical_state.connectivity_completeness = "complete"
    return topology


def _values(result):
    return puw.get_value(result["charges"], to_unit="e")


@pytest.mark.parametrize("charges", [[0, -1, 0, 0], [0, 0, -1, 0]])
def test_carboxylate_membership_is_independent_of_resonance_localization(charges):
    orders = [1, 2, 1] if charges[1] == -1 else [2, 1, 1]
    molsys = _topology(["C", "O", "O", "C"], charges, [(0, 1), (0, 2), (0, 3)], orders)
    result = msm.physchem.get_charge_centers(molsys)
    assert result["atom_indices"].tolist() == [0, 1, 2]
    assert result["geometry_atom_indices"].tolist() == [1, 2]
    assert result["atom_offsets"].tolist() == [0, 3]
    assert result["geometry_atom_offsets"].tolist() == [0, 2]
    assert result["center_types"].tolist() == ["carboxylate"]
    np.testing.assert_array_equal(_values(result), [-1])


@pytest.mark.parametrize("charged_nitrogen", [1, 2, 3])
def test_guanidinium_is_one_center_with_three_nitrogen_references(charged_nitrogen):
    charges = [0, 0, 0, 0]
    charges[charged_nitrogen] = 1
    orders = [2 if index == charged_nitrogen else 1 for index in [1, 2, 3]]
    molsys = _topology(["C", "N", "N", "N"], charges, [(0, 1), (0, 2), (0, 3)], orders)
    result = msm.physchem.get_charge_centers(molsys)
    assert result["atom_indices"].tolist() == [0, 1, 2, 3]
    assert result["geometry_atom_indices"].tolist() == [1, 2, 3]
    assert result["center_types"].tolist() == ["guanidinium"]
    np.testing.assert_array_equal(_values(result), [1])


def test_charge_location_does_not_overclaim_a_named_ionic_group():
    molsys = _topology(["C", "O", "O"], [-1, 0, 0], [(0, 1), (0, 2)], [1, 2])
    result = msm.physchem.get_charge_centers(molsys)
    assert result["center_types"].tolist() == ["formal_charge_cluster"]
    np.testing.assert_array_equal(_values(result), [-1])


def test_chemical_protonation_changes_center_count_without_residue_name_rules():
    molsys = _topology(
        ["C", "O", "O", "C"], [0, -1, 0, 0], [(0, 1), (0, 2), (0, 3)], [1, 2, 1]
    )
    second = molsys._append_chemical_state(state_id="neutral-acid")
    molsys._set_chemical_state_atom_attribute(
        "formal_charge", [0, 0, 0, 0], state_index=second
    )
    molsys._append_chemical_state_bonds(
        [(0, 1), (0, 2), (0, 3)], orders=[1, 2, 1], types="covalent", state_index=second
    )
    molsys._chemical_states[second].connectivity_completeness = "complete"
    before = msm.physchem.get_charge_centers(molsys, chemical_state=0)
    after = msm.physchem.get_charge_centers(molsys, chemical_state=second)
    assert len(before["charges"]) == 1
    assert len(after["charges"]) == 0
    assert after["chemical_state_index"] == second
    assert molsys._reference_chemical_state_index == 0


@pytest.mark.parametrize(
    ("elements", "charges", "bonds", "orders"),
    [
        (["N", "O", "O", "C"], [1, -1, 0, 0], [(0, 1), (0, 2), (0, 3)], [1, 2, 1]),
        (["N", "O", "C"], [1, -1, 0], [(0, 1), (0, 2)], [1, 1]),
        (["C", "O"], [0, 0], [(0, 1)], [2]),
    ],
)
def test_neutral_charge_separation_and_polar_bonds_do_not_create_centers(
    elements, charges, bonds, orders
):
    result = msm.physchem.get_charge_centers(
        _topology(elements, charges, bonds, orders)
    )
    assert result["atom_indices"].shape == (0,)
    assert result["atom_indices"].dtype == np.int64
    assert result["atom_offsets"].tolist() == [0]
    assert result["geometry_atom_offsets"].tolist() == [0]
    assert _values(result).shape == (0,)
    assert result["center_types"].dtype.kind == "U"


def test_zwitterion_has_two_local_centers_despite_zero_total_charge():
    molsys = _topology(
        ["N", "C", "C", "O", "O"],
        [1, 0, 0, -1, 0],
        [(0, 1), (1, 2), (2, 3), (2, 4)],
        [1, 1, 1, 2],
    )
    result = msm.physchem.get_charge_centers(molsys)
    assert result["atom_indices"].tolist() == [0, 2, 3, 4]
    assert result["atom_offsets"].tolist() == [0, 1, 4]
    np.testing.assert_array_equal(_values(result), [1, -1])


def test_selection_preserves_original_indices_and_deduplicates_atoms():
    molsys = _topology(["Na", "Cl", "K"], [1, -1, 1])
    result = msm.physchem.get_charge_centers(molsys, selection=[2, 0, 2])
    assert result["atom_indices"].tolist() == [0, 2]
    assert result["selection_atom_indices"].tolist() == [0, 2]
    assert result["source_atom_indices"].tolist() == [0, 1, 2]
    assert result["examined_atom_indices"].tolist() == [0, 1, 2]
    assert result["software"]["molsysmt"] == msm.__version__
    assert result["charge_source"] == "chemical_states.formal_charge"


def test_cutting_a_compound_center_fails_and_whole_selection_succeeds():
    molsys = _topology(["C", "O", "O", "Na"], [0, -1, 0, 1], [(0, 1), (0, 2)], [1, 2])
    with pytest.raises(ArgumentError, match="cuts a compound charge center"):
        msm.physchem.get_charge_centers(molsys, selection=[1, 2])
    result = msm.physchem.get_charge_centers(molsys, selection=[2, 1, 0])
    assert result["atom_indices"].tolist() == [0, 1, 2]
    np.testing.assert_array_equal(_values(result), [-1])


def test_dative_bond_does_not_cancel_distinct_ionic_centers():
    molsys = _topology(["Zn", "O"], [2, -1])
    molsys._append_chemical_state_bonds([(0, 1)], types="dative")
    molsys._reference_chemical_state.connectivity_completeness = "complete"
    result = msm.physchem.get_charge_centers(molsys)
    assert result["atom_offsets"].tolist() == [0, 1, 2]
    np.testing.assert_array_equal(_values(result), [2, -1])


@pytest.mark.parametrize(
    "missing", ["formal_charge", "element", "bond_order", "bond_type", "connectivity"]
)
def test_missing_chemistry_fails_instead_of_falling_back(missing, monkeypatch):
    molsys = _topology(["C", "O"], [0, -1], [(0, 1)], [1])
    if missing == "formal_charge":
        molsys._set_chemical_state_atom_attribute("formal_charge", [0, pd.NA])
    elif missing == "element":
        molsys.atoms.loc[0, "atom_type"] = pd.NA
    elif missing in {"bond_order", "bond_type"}:
        molsys.bonds.loc[0, missing] = pd.NA
    else:
        molsys._reference_chemical_state.connectivity_completeness = "partial"

    def forbidden(*args, **kwargs):
        raise AssertionError(
            "Recognition must not obtain substitute charges or parameterize."
        )

    monkeypatch.setattr(msm.physchem, "get_charge", forbidden)
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.get_charge_centers(molsys)


def test_nonconsecutive_structure_indices_resolve_one_state_and_reject_mixed_states():
    molsys = MolSys()
    molsys.topology = _topology(["Na", "Cl"], [1, -1])
    second = molsys.topology._append_chemical_state(state_id="neutral")
    molsys.topology._set_chemical_state_atom_attribute(
        "formal_charge", [0, 0], state_index=second
    )
    molsys.topology._chemical_states[second].connectivity_completeness = "complete"
    molsys.structures = Structures()
    molsys.structures.append(coordinates=puw.quantity(np.zeros((3, 2, 3)), "nm"))
    molsys._set_structure_chemical_state_indices([0, second, 0])
    result = msm.physchem.get_charge_centers(
        molsys, chemical_state="structure", structure_indices=[2, 0, 2]
    )
    assert result["chemical_state_index"] == 0
    np.testing.assert_array_equal(_values(result), [1, -1])
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.get_charge_centers(
            molsys, chemical_state="structure", structure_indices=[0, 1]
        )


def test_ambiguous_reference_and_unsupported_definition_fail():
    molsys = _topology(["Na"], [1])
    molsys._append_chemical_state(state_id="alternative")
    molsys._set_reference_chemical_state_index(None)
    with pytest.raises(StructuralInconsistencyError, match="no reference state"):
        msm.physchem.get_charge_centers(molsys)
    with pytest.raises(ArgumentError):
        msm.physchem.get_charge_centers(molsys, definition="OpenMM")


def test_empty_topology_and_empty_selection_keep_typed_empty_results():
    for molsys, selection in [(Topology(), "all"), (_topology(["Na"], [1]), [])]:
        result = msm.physchem.get_charge_centers(molsys, selection=selection)
        assert result["atom_indices"].dtype == np.int64
        assert result["atom_indices"].shape == (0,)
        assert result["geometry_atom_indices"].shape == (0,)
        assert result["atom_offsets"].tolist() == [0]
        assert _values(result).shape == (0,)


def test_input_formal_charges_and_bonds_are_not_modified():
    molsys = _topology(["C", "O", "O"], [0, -1, 0], [(0, 1), (0, 2)], [1, 2])
    bonds = molsys.bonds.copy(deep=True)
    charges = molsys._get_chemical_state_atom_attribute("formal_charge").copy()
    msm.physchem.get_charge_centers(molsys)
    pd.testing.assert_frame_equal(molsys.bonds, bonds)
    pd.testing.assert_series_equal(
        molsys._get_chemical_state_atom_attribute("formal_charge"), charges
    )


def test_connectivity_declaration_is_explicit_and_preserves_stored_metadata():
    molsys = _topology(["Na", "Cl"], [1, -1])
    molsys._reference_chemical_state.connectivity_completeness = "unavailable"
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.get_charge_centers(molsys)
    result = msm.physchem.get_charge_centers(molsys, assume_complete_connectivity=True)
    assert result["evidence"]["assume_complete_connectivity"] is True
    assert result["evidence"]["connectivity_completeness"] == "unavailable"
    assert molsys._reference_chemical_state.connectivity_completeness == "unavailable"
    with pytest.raises(ArgumentError):
        msm.physchem.get_charge_centers(molsys, assume_complete_connectivity="yes")


def test_h5msm_round_trip_preserves_chemistry_and_atom_axes(tmp_path):
    molsys = MolSys()
    molsys.topology = _topology(["Na", "Cl"], [1, -1])
    molsys.structures.append(coordinates=puw.quantity(np.zeros((1, 2, 3)), "nm"))
    path = str(tmp_path / "ions.h5msm")
    msm.convert(molsys, to_form=path)
    result = msm.physchem.get_charge_centers(path)
    assert result["atom_indices"].tolist() == [0, 1]
    np.testing.assert_array_equal(_values(result), [1, -1])


def test_inventory_dictionary_without_chemical_state_is_not_sufficient():
    molsys = _topology(["Na", "Cl"], [1, -1])
    dictionary = msm.convert(molsys, to_form="molsysmt.TopologyDict")
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.get_charge_centers(dictionary, assume_complete_connectivity=True)


@pytest.mark.skipif(
    find_spec("rdkit") is None, reason="RDKit is an optional chemistry backend"
)
@pytest.mark.parametrize(
    ("smiles", "expected"),
    [
        ("CC(=O)[O-]", [-1]),
        ("NC(=[NH2+])N", [1]),
        ("C[N+](C)(C)C", [1]),
        ("C[N+](=O)[O-]", []),
        ("[O-][n+]1ccccc1", []),
        ("[NH3+]CC(=O)[O-]", [1, -1]),
    ],
)
def test_explicit_small_molecule_chemistry_including_aromatic_bonds(smiles, expected):
    molsys = msm.convert("smiles:" + smiles, to_form="molsysmt.Topology")
    result = msm.physchem.get_charge_centers(molsys)
    np.testing.assert_array_equal(_values(result), expected)
