"""Protect full-graph hydrophobic typing separately from residue scales."""

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt._private.smonitor import UnsupportedHeavyOperationError


@pytest.mark.parametrize("form", ["rdkit", "native", "topology", "h5msm"])
def test_sites_are_form_agnostic_and_not_all_carbon(form, tmp_path):
    source = Chem.MolFromSmiles("CCC.CSC.CF.CC.C[NH3+]")
    if form != "rdkit":
        source = msm.convert(source, to_form="molsysmt.MolSys")
        if form == "topology":
            source = source.topology
        elif form == "h5msm":
            path = str(tmp_path / "chemistry.h5msm")
            msm.convert(source, to_form=path)
            source = path
    sites = msm.physchem.get_hydrophobic_sites(source)
    assert sites["hydrophobic_atom_indices"].tolist() == [1, 4]
    assert sites["hydrophobic_atom_indices"].dtype == np.int64
    assert sites["method"] == "smarts_hydrophobic_atoms"
    assert "rdkit" in sites["software"]
    assert any(
        item["doi"] == "10.1186/s13321-021-00548-6"
        for item in sites["attribution"]["items"]
        if "doi" in item
    )


def test_recognize_full_neighborhood_before_selecting_and_keep_hydrogen_semantics():
    molecule = Chem.MolFromSmiles("n1ccccc1.Br.I.CS.CSC")
    sites = msm.physchem.get_hydrophobic_sites(molecule)
    assert sites["hydrophobic_atom_indices"].tolist() == [2, 3, 4, 6, 7, 11]
    # Aromatic C next to N remains excluded after selecting away that neighbor.
    assert msm.physchem.get_hydrophobic_sites(molecule, selection=[1])[
        "hydrophobic_atom_indices"
    ].shape == (0,)
    explicit = msm.physchem.get_hydrophobic_sites(Chem.AddHs(molecule))
    np.testing.assert_array_equal(
        explicit["hydrophobic_atom_indices"], sites["hydrophobic_atom_indices"]
    )


def test_missing_chemistry_is_not_repaired_by_completeness_assumption():
    source = msm.convert(Chem.MolFromSmiles("CCC"), to_form="molsysmt.MolSys")
    state = source.chemical_states._states[0]
    state.connectivity_completeness = "partial"
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.physchem.get_hydrophobic_sites(source)
    assert msm.physchem.get_hydrophobic_sites(
        source, assume_complete_connectivity=True
    )["assume_complete_connectivity"]
    state.atom_attributes["formal_charge"] = None
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.physchem.get_hydrophobic_sites(source, assume_complete_connectivity=True)


def test_caps_are_checked_before_selection_and_unknown_method_fails():
    molecule = Chem.MolFromSmiles("c1ccccc1")
    with pytest.raises(UnsupportedHeavyOperationError):
        msm.physchem.get_hydrophobic_sites(molecule, selection=[0], max_matches=2)
    with pytest.raises(msm.ArgumentError):
        msm.physchem.get_hydrophobic_sites(molecule, method="prolif")
