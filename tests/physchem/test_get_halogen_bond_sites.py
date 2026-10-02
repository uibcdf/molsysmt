"""Protect chemical halogen sites independently of observed geometry."""

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt._private.smonitor import UnsupportedHeavyOperationError


@pytest.mark.parametrize("form", ["rdkit", "native", "topology", "h5msm"])
def test_known_halogen_sites_are_form_agnostic(form, tmp_path):
    molecule = Chem.MolFromSmiles("CCl.C=O.CF.[Cl-].N#C")
    source = molecule
    if form != "rdkit":
        source = msm.convert(molecule, to_form="molsysmt.MolSys")
        if form == "topology":
            source = source.topology
        elif form == "h5msm":
            path = str(tmp_path / "chemistry.h5msm")
            msm.convert(source, to_form=path)
            source = path
    sites = msm.physchem.get_halogen_bond_sites(source)
    assert sites["donor_halogen_pairs"].tolist() == [[0, 1]]
    assert sites["acceptor_reference_pairs"].tolist() == [[3, 2]]
    assert sites["donor_halogen_pairs"].dtype == np.int64
    assert sites["acceptor_reference_pairs"].dtype == np.int64
    assert "rdkit" in sites["software"]
    assert any(
        item["roles"] == ["reference_implementation"]
        for item in sites["attribution"]["items"]
    )


def test_reference_neighbors_and_complete_pair_selection_are_preserved():
    molecule = Chem.MolFromSmiles("CBr.COC")
    sites = msm.physchem.get_halogen_bond_sites(molecule)
    assert sites["donor_halogen_pairs"].tolist() == [[0, 1]]
    assert sites["acceptor_reference_pairs"].tolist() == [[3, 2], [3, 4]]
    selected = msm.physchem.get_halogen_bond_sites(molecule, selection=[1, 3, 4])
    assert selected["donor_halogen_pairs"].shape == (0, 2)
    assert selected["acceptor_reference_pairs"].tolist() == [[3, 4]]


def test_positive_acceptors_and_unknown_chemistry_are_not_silently_reclassified():
    molecule = Chem.MolFromSmiles("CCl.C[NH3+]")
    assert msm.physchem.get_halogen_bond_sites(molecule)[
        "acceptor_reference_pairs"
    ].shape == (0, 2)
    native = msm.convert(Chem.MolFromSmiles("CCl.C=O"), to_form="molsysmt.MolSys")
    native.chemical_states._states[0].connectivity_completeness = "partial"
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.physchem.get_halogen_bond_sites(native)
    assert msm.physchem.get_halogen_bond_sites(
        native, assume_complete_connectivity=True
    )["assume_complete_connectivity"]
    native.chemical_states._states[0].atom_attributes["formal_charge"] = None
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.physchem.get_halogen_bond_sites(native, assume_complete_connectivity=True)


def test_invalid_site_method_and_unbounded_truncation_fail():
    molecule = Chem.MolFromSmiles("CCl.CBr.C=O")
    with pytest.raises(msm.ArgumentError):
        msm.physchem.get_halogen_bond_sites(molecule, method="unknown")
    with pytest.raises(UnsupportedHeavyOperationError):
        msm.physchem.get_halogen_bond_sites(molecule, max_matches=1)
