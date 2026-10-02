"""Checking explicit V3000 coordination roles independently of endpoint sorting."""

import importlib.util

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import FormatError, NotCompatibleConversionError

COORDINATION = """copper ammine
  Independent       2D

  0  0  0     0  0            999 V3000
M  V30 BEGIN CTAB
M  V30 COUNTS 5 4 0 0 0
M  V30 BEGIN ATOM
M  V30 10 Cu 0 0 0 0 CHG=2
M  V30 30 N 2 0 0 0
M  V30 40 H 3 0 0 0
M  V30 50 H 2 1 0 0
M  V30 60 H 2 -1 0 0
M  V30 END ATOM
M  V30 BEGIN BOND
M  V30 12 9 30 10
M  V30 14 1 30 40
M  V30 16 1 30 50
M  V30 18 1 30 60
M  V30 END BOND
M  V30 END CTAB
M  END
$$$$
"""


@pytest.fixture
def source(tmp_path):
    path = tmp_path / "coordination.sdf"
    path.write_text(COORDINATION)
    return path


@pytest.mark.parametrize("display", ["", " DISP=COORD", " DISP=DATIVE"])
def test_coordination_roles_and_components(source, tmp_path, display):
    source.write_text(COORDINATION.replace("12 9 30 10", "12 9 30 10" + display))
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    bonds = molsys.topology.bonds
    dative = bonds[bonds.bond_type == "dative"].iloc[0]
    assert (dative.atom1_index, dative.atom2_index) == (0, 1)
    assert (dative.donor_atom_index, dative.acceptor_atom_index) == (1, 0)
    assert pd.isna(dative.bond_order)
    assert not dative.joins_components
    assert molsys.topology.n_components == 2
    np.testing.assert_array_equal(
        msm.get(molsys, element="atom", component_index=True), [0, 1, 1, 1, 1]
    )
    assert msm.has_attribute(source, "bond_donor_atom_index")
    assert msm.has_attribute(source, "bond_acceptor_atom_index")
    assert msm.has_attribute(source, "bond_joins_components")
    np.testing.assert_array_equal(
        msm.get(source, element="bond", selection=[0], bond_donor_atom_index=True), [1]
    )
    target = tmp_path / "roundtrip.sdf"
    msm.convert(molsys, to_form=target, ctfile_version="V3000")
    assert "M  V30 1 9 2 1" in target.read_text()
    again = msm.convert(target, to_form="molsysmt.MolSys")
    after = again.topology.bonds[again.topology.bonds.bond_type == "dative"].iloc[0]
    assert (after.donor_atom_index, after.acceptor_atom_index) == (1, 0)
    assert again.topology.n_components == 2


def test_display_style_loss_is_reported_but_identity_copies_are_exact(source, tmp_path):
    source.write_text(COORDINATION.replace("12 9 30 10", "12 9 30 10 DISP=COORD"))
    _, report = msm.convert(source, to_form="molsysmt.MolSys", return_report=True)
    assert "sdf_bond_display" in {issue.attribute for issue in report.issues}
    with pytest.raises(NotCompatibleConversionError):
        msm.convert(source, to_form="molsysmt.MolSys", strict=True)
    copied = tmp_path / "copied.sdf"
    _, report = msm.convert(source, to_form=copied, strict=True, return_report=True)
    assert copied.read_bytes() == source.read_bytes()
    assert report.outcome == "exact" and report.is_exhaustive


def test_selection_remaps_direction_and_removes_incident_bonds(source, tmp_path):
    subset = msm.convert(source, selection=[1, 0], to_form="molsysmt.MolSys")
    target = tmp_path / "subset.sdf"
    msm.convert(subset, to_form=target, ctfile_version="V3000")
    again = msm.convert(target, to_form="molsysmt.MolSys")
    assert again.topology.n_atoms == 2 and again.topology.n_bonds == 1
    assert msm.get(again, element="bond", bond_donor_atom_index=True) == [1]
    assert msm.get(again, element="bond", bond_acceptor_atom_index=True) == [0]
    ligand = msm.convert(source, selection=[1, 2, 3, 4], to_form="molsysmt.MolSys")
    msm.convert(ligand, to_form=tmp_path / "ligand.sdf", ctfile_version="V2000")
    assert ligand.topology.n_bonds == 3
    assert not msm.has_attribute(ligand, "bond_donor_atom_index")


def test_coordination_requires_v3000_before_opening_destination(source, tmp_path):
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    target = tmp_path / "untouched.sdf"
    target.write_text("original")
    with pytest.raises(FormatError, match="require.*V3000"):
        msm.convert(molsys, to_form=target)
    assert target.read_text() == "original"


@pytest.mark.parametrize("missing", ["donor_atom_index", "acceptor_atom_index"])
def test_coordination_output_does_not_guess_roles(source, tmp_path, missing):
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    bonds = molsys.topology.bonds.copy()
    bonds.loc[bonds.bond_type == "dative", missing] = pd.NA
    molsys.topology._set_chemical_state_bonds(bonds)
    with pytest.raises(FormatError, match="explicit donor and acceptor"):
        msm.convert(molsys, to_form=tmp_path / "bad.sdf", ctfile_version="V3000")


def test_numeric_dative_order_is_reported_as_lost(source, tmp_path):
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    bonds = molsys.topology.bonds.copy()
    bonds.loc[bonds.bond_type == "dative", "bond_order"] = 1
    molsys.topology._set_chemical_state_bonds(bonds)
    target = tmp_path / "numeric-order.sdf"
    with pytest.raises(NotCompatibleConversionError):
        msm.convert(molsys, to_form=target, ctfile_version="V3000", strict=True)
    _, report = msm.convert(
        molsys, to_form=target, ctfile_version="V3000", return_report=True
    )
    assert "bond_order" in {issue.attribute for issue in report.issues}
    restored = msm.convert(target, to_form="molsysmt.MolSys")
    assert pd.isna(restored.topology.bonds.iloc[0].bond_order)


def test_missing_native_bond_type_fails_clearly_without_guessing(source, tmp_path):
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    bonds = molsys.topology.bonds.drop(columns="bond_type")
    molsys.topology._set_chemical_state_bonds(bonds)
    target = tmp_path / "untyped.sdf"
    target.write_text("original")
    with pytest.raises(FormatError, match="Only covalent and directed dative"):
        msm.convert(molsys, to_form=target, ctfile_version="V3000")
    assert target.read_text() == "original"


@pytest.mark.parametrize("field", ["donor_atom_index", "acceptor_atom_index"])
def test_covalent_output_does_not_silently_drop_directional_roles(
    source, tmp_path, field
):
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    bonds = molsys.topology.bonds.copy()
    row = bonds.index[bonds.bond_type == "covalent"][0]
    bonds.loc[row, field] = bonds.loc[row, "atom1_index"]
    molsys.topology._set_chemical_state_bonds(bonds)
    target = tmp_path / "roles.sdf"
    target.write_text("original")
    with pytest.raises(FormatError, match="covalent bond types cannot retain"):
        msm.convert(molsys, to_form=target, ctfile_version="V3000")
    assert target.read_text() == "original"


@pytest.mark.parametrize(
    "extra", [" CFG=1", " DISP=HBOND1", " ENDPTS=(2 10 30)", " DISP=COORD DISP=DATIVE"]
)
def test_coordination_does_not_swallow_other_bond_properties(source, extra):
    source.write_text(COORDINATION.replace("12 9 30 10", "12 9 30 10" + extra))
    with pytest.raises(FormatError):
        msm.convert(source, to_form="molsysmt.MolSys")


def test_component_overrides_are_reported_and_strictly_rejected(source, tmp_path):
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    bonds = molsys.topology.bonds.copy()
    bonds.loc[bonds.bond_type == "dative", "joins_components"] = True
    molsys.topology._set_chemical_state_bonds(bonds)
    target = tmp_path / "strict.sdf"
    with pytest.raises(NotCompatibleConversionError):
        msm.convert(molsys, to_form=target, ctfile_version="V3000", strict=True)
    assert not target.exists()
    _, report = msm.convert(
        molsys, to_form=target, ctfile_version="V3000", return_report=True
    )
    assert "bond_joins_components" in {issue.attribute for issue in report.issues}


@pytest.mark.skipif(
    importlib.util.find_spec("rdkit") is None, reason="optional RDKit reference reader"
)
def test_reference_reader_retains_dative_direction(source, tmp_path):
    from rdkit import Chem

    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    output = tmp_path / "reference.sdf"
    msm.convert(molsys, to_form=output, ctfile_version="V3000")
    for path in [source, output]:
        reference = Chem.SDMolSupplier(
            str(path), sanitize=False, removeHs=False, strictParsing=True
        )[0]
        assert reference is not None
        dative = [
            bond
            for bond in reference.GetBonds()
            if bond.GetBondType() == Chem.BondType.DATIVE
        ]
        assert len(dative) == 1
        assert (dative[0].GetBeginAtomIdx(), dative[0].GetEndAtomIdx()) == (1, 0)
