"""Verify reusable site chemistry, source axes and explicit hydrogen rules."""

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError


@pytest.mark.parametrize("method", ["mdtraj", "cpptraj", "prolif"])
@pytest.mark.parametrize("form", ["rdkit", "native", "topology", "h5msm"])
def test_site_recognition_survives_chemical_forms(method, form, tmp_path):
    molecule = Chem.AddHs(Chem.MolFromSmiles("NC(=O)N.O.S.F"))
    expected = msm.physchem.get_hbond_sites(molecule, method=method)
    source = molecule
    if form != "rdkit":
        source = msm.convert(molecule, to_form="molsysmt.MolSys")
        if form == "topology":
            source = source.topology
        elif form == "h5msm":
            path = str(tmp_path / "chemistry.h5msm")
            msm.convert(source, to_form=path)
            source = path
    actual = msm.physchem.get_hbond_sites(source, method=method)
    for name in ("donor_hydrogen_pairs", "acceptor_atom_indices", "atom_source_indices"):
        np.testing.assert_array_equal(actual[name], expected[name])
        assert actual[name].dtype == np.int64
    assert actual["method_reference"] == expected["method_reference"]


def test_elemental_and_smarts_profiles_are_not_interchangeable():
    molecule = Chem.AddHs(Chem.MolFromSmiles("NC(=O)N.O.S.F"))
    md = msm.physchem.get_hbond_sites(molecule)
    cpp = msm.physchem.get_hbond_sites(molecule, method="cpptraj")
    prolif = msm.physchem.get_hbond_sites(molecule, method="prolif")
    nitrogens = [atom.GetIdx() for atom in molecule.GetAtoms() if atom.GetSymbol() == "N"]
    assert set(nitrogens) <= set(md["acceptor_atom_indices"])
    assert not set(nitrogens) & set(prolif["acceptor_atom_indices"])
    fluorine = next(atom.GetIdx() for atom in molecule.GetAtoms() if atom.GetSymbol() == "F")
    sulfur = next(atom.GetIdx() for atom in molecule.GetAtoms() if atom.GetSymbol() == "S")
    assert fluorine in cpp["acceptor_atom_indices"] and fluorine not in md["acceptor_atom_indices"]
    assert sulfur in prolif["donor_hydrogen_pairs"][:, 0] and sulfur not in cpp["donor_hydrogen_pairs"][:, 0]


def test_index_selection_requires_both_donor_and_hydrogen():
    molecule = Chem.AddHs(Chem.MolFromSmiles("O"))
    result = msm.physchem.get_hbond_sites(molecule, selection=[0, 1])
    assert result["donor_hydrogen_pairs"].tolist() == [[0, 1]]
    assert result["acceptor_atom_indices"].tolist() == [0]
    assert msm.physchem.get_hbond_sites(Chem.MolFromSmiles("O"))["donor_hydrogen_pairs"].shape == (0, 2)


def test_unknown_connectivity_is_not_a_silent_complete_graph():
    native = msm.convert(Chem.AddHs(Chem.MolFromSmiles("O")), to_form="molsysmt.MolSys")
    native.chemical_states._states[0].connectivity_completeness = "partial"
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.get_hbond_sites(native)
    assert msm.physchem.get_hbond_sites(native, assume_complete_connectivity=True)["assume_complete_connectivity"]


@pytest.mark.parametrize("method", [None, 1, "unknown"])
def test_invalid_site_methods_raise(method):
    with pytest.raises(ArgumentError):
        msm.physchem.get_hbond_sites(Chem.MolFromSmiles("O"), method=method)
