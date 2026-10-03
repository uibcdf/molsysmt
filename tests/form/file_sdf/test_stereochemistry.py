"""Checking explicitly enabled SDF stereo against independent chemical labels."""

from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import FormatError

Chem = pytest.importorskip("rdkit.Chem")
rdDepictor = pytest.importorskip("rdkit.Chem.rdDepictor")


def test_parity_only_without_interpretable_geometry_is_rejected(tmp_path):
    molecule = Chem.MolFromSmiles("N[C@@H](C)C(=O)O")
    rdDepictor.Compute2DCoords(molecule)
    Chem.RemoveStereochemistry(molecule)
    lines = Chem.MolToMolBlock(molecule).splitlines()
    lines[5] = lines[5][:39] + "  1" + lines[5][42:]
    source = tmp_path / "parity.sdf"
    source.write_text("\n".join(lines) + "\n$$$$\n")
    with pytest.raises(FormatError, match="parity-only"):
        msm.convert(source, to_form="molsysmt.MolSys", stereo_engine="rdkit")


@pytest.mark.parametrize("version", ["V2000", "V3000"])
@pytest.mark.parametrize(
    "smiles,index,label",
    [
        ("N[C@@H](C)C(=O)O", 1, "S"),
        ("N[C@@H](CS)C(=O)O", 1, "R"),
    ],
)
def test_explicit_stereo_engine_read_write_and_selection(
    tmp_path, version, smiles, index, label
):
    molecule = Chem.MolFromSmiles(smiles)
    rdDepictor.Compute2DCoords(molecule)
    source = tmp_path / "source.sdf"
    source.write_text(
        Chem.MolToMolBlock(molecule, forceV3000=version == "V3000") + "$$$$\n"
    )
    with pytest.raises(FormatError):
        msm.convert(source, to_form="molsysmt.MolSys")
    native = msm.convert(
        source, to_form="molsysmt.MolSys", stereo_engine="rdkit", structure_indices=[0]
    )
    assert (
        native.chemical_states._states[0].atom_attributes.loc[index, "stereochemistry"]
        == label
    )
    assert native.topology.n_atoms == molecule.GetNumAtoms()
    before = msm.pyunitwizard.get_value(
        native.structures.coordinates, to_unit="angstrom"
    ).copy()
    assert (
        msm.physchem.get_cip_stereochemistry(native)["atom_stereochemistry"][index]
        == label
    )
    target = tmp_path / "roundtrip.sdf"
    _, converted_report = msm.convert(
        native,
        to_form=target,
        ctfile_version=version,
        stereo_engine="rdkit",
        return_report=True,
    )
    assert "atom_stereochemistry" not in {
        issue.attribute for issue in converted_report.issues
    }
    default_report = msm.get_conversion_report(native, to_form=target)
    assert "atom_stereochemistry" in {
        issue.attribute for issue in default_report.issues
    }
    restored = msm.convert(target, to_form="molsysmt.MolSys", stereo_engine="rdkit")
    assert (
        restored.chemical_states._states[0].atom_attributes.loc[
            index, "stereochemistry"
        ]
        == label
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(restored.structures.coordinates, to_unit="angstrom"),
        before,
        atol=1e-4,
    )
    copy = tmp_path / "copy.sdf"
    msm.convert(source, to_form=copy)
    assert copy.read_bytes() == source.read_bytes()
    subset = msm.convert(
        source, to_form="molsysmt.MolSys", selection=[index], stereo_engine="rdkit"
    )
    assert subset.topology.atoms["atom_id"].tolist() == [str(index + 1)]


@pytest.mark.parametrize("version", ["V2000", "V3000"])
@pytest.mark.parametrize("smiles,label", [("F/C=C/F", "E"), ("F/C=C\\F", "Z")])
def test_double_bond_stereo_roundtrip(tmp_path, version, smiles, label):
    molecule = Chem.MolFromSmiles(smiles)
    rdDepictor.Compute2DCoords(molecule)
    source = tmp_path / "double.sdf"
    source.write_text(
        Chem.MolToMolBlock(molecule, forceV3000=version == "V3000") + "$$$$\n"
    )
    native = msm.convert(source, to_form="molsysmt.MolSys", stereo_engine="rdkit")
    report = msm.physchem.get_cip_stereochemistry(native)
    assert label in report["bond_stereochemistry"]
    target = tmp_path / "double_out.sdf"
    msm.convert(native, to_form=target, ctfile_version=version, stereo_engine="rdkit")
    assert label in msm.physchem.get_cip_stereochemistry(target)["bond_stereochemistry"]


def test_stereo_writer_failure_preserves_existing_destination(tmp_path):
    molecule = Chem.MolFromSmiles("N[C@@H](C)C(=O)O")
    rdDepictor.Compute2DCoords(molecule)
    native = msm.convert(molecule, to_form="molsysmt.MolSys")
    target = tmp_path / "protected.sdf"
    target.write_text("protected bytes")
    with pytest.raises(FormatError):
        msm.convert(native, to_form=target)
    assert Path(target).read_text() == "protected bytes"
