"""
Tests for file_smi/get_topological_attributes.py.

Oracle: single-molecule .smi file with caffeine (C8H10N4O2)
  n_atoms (heavy) = 14
  n_bonds         = 15

Multi-molecule test: caffeine + ethanol (CCO, 3 heavy atoms)
  n_atoms = 17
"""

import pytest
import molsysmt as msm

try:
    import rdkit
    HAS_RDKIT = True
except ImportError:
    HAS_RDKIT = False

needs_rdkit = pytest.mark.skipif(not HAS_RDKIT, reason="rdkit not installed")

CAFFEINE_SMILES = 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C'
ETHANOL_SMILES  = 'CCO'


@pytest.fixture(scope="module")
def smi_caffeine(tmp_path_factory):
    p = tmp_path_factory.mktemp("file_smi_assets") / "caffeine.smi"
    p.write_text(f"{CAFFEINE_SMILES} caffeine\n")
    return str(p)


@pytest.fixture(scope="module")
def smi_two_mols(tmp_path_factory):
    p = tmp_path_factory.mktemp("file_smi_assets") / "two_mols.smi"
    p.write_text(f"{CAFFEINE_SMILES} caffeine\n{ETHANOL_SMILES} ethanol\n")
    return str(p)


# ---------------------------------------------------------------------------
# Form recognition
# ---------------------------------------------------------------------------

def test_get_form(smi_caffeine):
    assert msm.get_form(smi_caffeine) == 'file:smi'


# ---------------------------------------------------------------------------
# to_string_smiles (no rdkit needed)
# ---------------------------------------------------------------------------

def test_to_string_smiles_single(smi_caffeine):
    result = msm.convert(smi_caffeine, to_form='string:smiles')
    assert result == f'smiles:{CAFFEINE_SMILES}'


def test_to_string_smiles_multi(smi_two_mols):
    result = msm.convert(smi_two_mols, to_form='string:smiles')
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == f'smiles:{CAFFEINE_SMILES}'
    assert result[1] == f'smiles:{ETHANOL_SMILES}'


# ---------------------------------------------------------------------------
# Getter tests — require rdkit
# ---------------------------------------------------------------------------

@needs_rdkit
@pytest.mark.redundant
def test_n_atoms_caffeine(smi_caffeine):
    assert msm.get(smi_caffeine, element='system', n_atoms=True) == 14


@needs_rdkit
@pytest.mark.redundant
def test_n_bonds_caffeine(smi_caffeine):
    assert msm.get(smi_caffeine, element='system', n_bonds=True) == 15


@needs_rdkit
@pytest.mark.redundant
def test_n_atoms_two_mols(smi_two_mols):
    # caffeine (14) + ethanol (3) = 17
    assert msm.get(smi_two_mols, element='system', n_atoms=True) == 17


@needs_rdkit
def test_roundtrip_rdkit_mol(smi_caffeine, tmp_path):
    mol = msm.convert(smi_caffeine, to_form='rdkit.Mol')
    out = str(tmp_path / 'out.smi')
    result = msm.convert(mol, to_form='file:smi', output_filename=out)
    assert msm.get_form(result) == 'file:smi'
    assert msm.get(result, element='system', n_atoms=True) == 14


@needs_rdkit
def test_multi_record_file_converts_to_one_disconnected_rdkit_graph(smi_two_mols):
    molecule = msm.convert(smi_two_mols, to_form='rdkit.Mol')
    topology = msm.convert(smi_two_mols, to_form='molsysmt.Topology')

    assert msm.get_form(molecule) == 'rdkit.Mol'
    assert molecule.GetNumAtoms() == 17
    assert topology.n_components == 2


@needs_rdkit
def test_invalid_smiles_record_fails_with_public_format_error(tmp_path):
    from molsysmt._private.smonitor import FormatError

    path = tmp_path / 'invalid.smi'
    path.write_text('CCO ethanol\nthis-is-not-smiles broken\n')

    with pytest.raises(FormatError, match='line 2'):
        msm.convert(str(path), to_form='rdkit.Mol')
