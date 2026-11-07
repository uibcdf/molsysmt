"""Protect descriptor reference CTABs across supported RDKit writer variants."""

import re
import shlex

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import FormatError
from tests.physchem._sdf_reference import rdkit_v3000_with_declared_valences


def _writer_variant(molecule, block, explicit):
    """Model writer omission or retention without changing other CTAB fields."""
    lines = block.splitlines()
    in_atoms = False
    for index, line in enumerate(lines):
        if line == "M  V30 BEGIN ATOM":
            in_atoms = True
        elif line == "M  V30 END ATOM":
            in_atoms = False
        elif in_atoms:
            lines[index] = re.sub(r"\sVAL=[+-]?\d+(?=\s|$)", "", line)
            if explicit:
                atom = molecule.GetAtomWithIdx(int(line.split()[2]) - 1)
                valence = atom.GetTotalValence()
                lines[index] += f" VAL={valence if valence else -1}"
    return "\n".join(lines) + "\n"


def _atom_lines(block):
    lines = block.splitlines()
    return lines[lines.index("M  V30 BEGIN ATOM") + 1 : lines.index("M  V30 END ATOM")]


@pytest.mark.parametrize("explicit", [False, True], ids=["omitted", "already_explicit"])
@pytest.mark.parametrize("smiles", ["[NH3+]CC(=O)[O-]", "C[N+](=O)[O-]"])
def test_writer_valence_variants_retain_one_field_and_native_descriptor_fidelity(
    tmp_path, monkeypatch, explicit, smiles
):
    Chem = pytest.importorskip("rdkit.Chem")
    from rdkit.Chem import rdMolDescriptors

    molecule = Chem.MolFromSmiles(smiles)
    expected_tpsa = rdMolDescriptors.CalcTPSA(molecule, force=True)
    expected_logp = rdMolDescriptors.CalcCrippenDescriptors(
        molecule, includeHs=True, force=True
    )[0]
    writer_block = _writer_variant(molecule, Chem.MolToV3KMolBlock(molecule), explicit)
    before = molecule.ToBinary()
    monkeypatch.setattr(Chem, "MolToV3KMolBlock", lambda _: writer_block)
    block = rdkit_v3000_with_declared_valences(molecule)
    if explicit:
        assert block == writer_block
    for atom, line in zip(molecule.GetAtoms(), _atom_lines(block)):
        valence = atom.GetTotalValence()
        assert [
            field for field in shlex.split(line)[8:] if field.startswith("VAL=")
        ] == [f"VAL={valence if valence else -1}"]
    path = tmp_path / "reference.sdf"
    path.write_text(block + "$$$$\n")
    native = msm.convert(path, to_form="molsysmt.MolSys")
    assert native.topology.n_atoms == molecule.GetNumAtoms()
    assert msm.get(native, formal_charge=True) == [
        atom.GetFormalCharge() for atom in molecule.GetAtoms()
    ]
    assert msm.get(native, n_explicit_hydrogens=True) == [
        atom.GetTotalNumHs() for atom in molecule.GetAtoms()
    ]
    assert msm.get(native, n_implicit_hydrogens=True) == [0] * molecule.GetNumAtoms()
    assert (
        msm.get(native, allows_implicit_hydrogens=True)
        == [False] * molecule.GetNumAtoms()
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(
            msm.physchem.get_tpsa(native), to_unit="angstrom**2"
        ),
        [expected_tpsa],
        atol=1e-12,
        rtol=0,
    )
    np.testing.assert_allclose(
        msm.physchem.get_lipophilicity(native), [expected_logp], atol=1e-12, rtol=0
    )
    assert molecule.ToBinary() == before


def test_matching_writer_valence_preserves_unrelated_fields_verbatim(monkeypatch):
    Chem = pytest.importorskip("rdkit.Chem")
    molecule = Chem.MolFromSmiles("CC[NH3+]")
    block = _writer_variant(molecule, Chem.MolToV3KMolBlock(molecule), True)
    atom_line = _atom_lines(block)[0]
    block = block.replace(
        atom_line, atom_line + ' NOTE="VAL=99 retained" EXTRA=opaque', 1
    )
    monkeypatch.setattr(Chem, "MolToV3KMolBlock", lambda _: block)
    assert rdkit_v3000_with_declared_valences(molecule) == block


@pytest.mark.parametrize("bad_value", ["VAL=3", "VAL=4 VAL=4"])
def test_conflicting_or_duplicate_writer_valence_is_not_silently_repaired(
    tmp_path, monkeypatch, bad_value
):
    Chem = pytest.importorskip("rdkit.Chem")
    molecule = Chem.MolFromSmiles("CC[NH3+]")
    block = _writer_variant(molecule, Chem.MolToV3KMolBlock(molecule), True)
    atom_line = _atom_lines(block)[0]
    invalid_line = atom_line.replace("VAL=4", bad_value)
    block = block.replace(atom_line, invalid_line, 1)
    before = molecule.ToBinary()
    monkeypatch.setattr(Chem, "MolToV3KMolBlock", lambda _: block)
    with pytest.raises(ValueError, match="conflicts|Repeated VAL"):
        rdkit_v3000_with_declared_valences(molecule)
    if bad_value == "VAL=4 VAL=4":
        path = tmp_path / "duplicate.sdf"
        path.write_text(block + "$$$$\n")
        with pytest.raises(FormatError, match="repeated V3000 atom property 'VAL="):
            msm.convert(path, to_form="molsysmt.MolSys")
    assert molecule.ToBinary() == before
