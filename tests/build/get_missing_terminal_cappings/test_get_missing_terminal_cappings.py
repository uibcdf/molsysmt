"""
Unit and regression tests for get_missing_terminal_cappings on molsysmt.MolSys systems.

Tests cover both engine='MolSysMT' (native, default) and engine='PDBFixer'.
"""

import pytest

import molsysmt as msm
from molsysmt._private.smonitor import UnassessedPeptideBackboneWarning


@pytest.fixture(scope="module")
def barnase_barstar():
    return msm.convert(msm.systems["Barnase-Barstar"]["1brs.bcif.gz"])


@pytest.fixture(scope="module")
def t4_lysozyme():
    return msm.convert(msm.systems["T4 lysozyme L99A"]["181l.h5msm"])


def test_get_missing_terminal_cappings_native_barnase(barnase_barstar):
    """Native observed bonds leave the two interrupted Barstar chains unassessed."""
    with pytest.warns(UnassessedPeptideBackboneWarning) as caught:
        result = msm.build.get_missing_terminal_cappings(
            barnase_barstar, engine="MolSysMT"
        )
    assert result == {}
    assert len(caught) == 2
    report = msm.chemical_states.get_peptide_termini(
        barnase_barstar, on_ambiguous="report"
    )
    assert report["unassessed_chain_indices"].tolist() == [3, 4]
    assert report["c_terminal_group_indices"].tolist() == [107, 217, 325, 587]


def test_get_missing_terminal_cappings_pdbfixer_barnase(barnase_barstar):
    """PDBFixer engine finds the same missing OXT (regression test)."""
    result = msm.build.get_missing_terminal_cappings(barnase_barstar, engine="PDBFixer")
    assert len(result) == 1
    assert result[412] == ["OXT"]


def test_get_missing_terminal_cappings_native_t4(t4_lysozyme):
    """MolSysMT engine finds OXT missing at group 161 (LYS, C-terminus of T4)."""
    result = msm.build.get_missing_terminal_cappings(t4_lysozyme, engine="MolSysMT")
    assert len(result) == 1
    assert result[161] == ["OXT"]


def test_get_missing_terminal_cappings_pdbfixer_t4(t4_lysozyme):
    """PDBFixer engine agrees with native on T4 lysozyme."""
    result = msm.build.get_missing_terminal_cappings(t4_lysozyme, engine="PDBFixer")
    assert len(result) == 1
    assert result[161] == ["OXT"]


def test_get_missing_terminal_cappings_returns_dict(barnase_barstar):
    """Return value is always a dict."""
    with pytest.warns(UnassessedPeptideBackboneWarning):
        result = msm.build.get_missing_terminal_cappings(barnase_barstar)
    assert isinstance(result, dict)


def test_get_missing_terminal_cappings_capped_peptide():
    """NME-capped peptide returns empty dict (no missing OXT)."""
    molsys = msm.build.build_peptide("AceAlaTrpLysNme")
    result = msm.build.get_missing_terminal_cappings(molsys, engine="MolSysMT")
    assert result == {}


def test_get_missing_terminal_cappings_engines_agree(barnase_barstar):
    """Historical parity selector now guards explicit native/PDBFixer scope divergence."""
    with pytest.warns(UnassessedPeptideBackboneWarning):
        native = msm.build.get_missing_terminal_cappings(
            barnase_barstar, engine="MolSysMT"
        )
    pdbfixer = msm.build.get_missing_terminal_cappings(
        barnase_barstar, engine="PDBFixer"
    )
    assert native == {}
    assert pdbfixer == {412: ["OXT"]}


def test_unknown_legacy_chain_cannot_establish_a_peptide_terminus():
    molsys = msm.convert(msm.systems["pentalanine"]["traj_pentalanine.h5msm"])
    assert molsys.topology.atoms["chain_index"].isna().all()
    with pytest.raises(msm.StructuralInconsistencyError, match="known chain_index"):
        msm.build.get_missing_terminal_cappings(molsys)
    assert molsys.topology.atoms["chain_index"].isna().all()


def test_chain_free_non_amino_acid_groups_have_no_peptide_terminal_audit():
    builder = msm.MolSysBuilder()
    atom = builder.add_atom(atom_name="O", atom_type="O")
    builder.add_group([atom], group_name="HOH")
    assert msm.build.get_missing_terminal_cappings(builder.build()) == {}
