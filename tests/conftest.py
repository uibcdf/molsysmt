import pytest
import molsysmt as msm
from molsysmt import systems

# Base loaders (session scope) to avoid repeated IO/parsing

@pytest.fixture(scope="session")
def _base_hp35_solvated_molsys():
    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'], to_form='molsysmt.MolSys')
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_hp35_molsys():
    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35.h5msm'], to_form='molsysmt.MolSys')
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_hp35_bcif_molsys():
    molsys = msm.convert(systems['chicken villin HP35']['1vii.bcif.gz'], to_form='molsysmt.MolSys')
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_met_enkephalin_molsys():
    molsys = msm.convert(systems['Met-enkephalin']['met_enkephalin.pdb'], to_form='molsysmt.MolSys')
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_traj_pentalanine_h5():
    path = systems['pentalanine']['traj_pentalanine.h5']
    assert path is not None
    return path

@pytest.fixture(scope="session")
def _base_barnase_barstar_molsys():
    molsys = msm.convert(msm.systems['Barnase-Barstar']['barnase_barstar.h5msm'])
    assert molsys is not None
    return molsys

# Small systems for structure/geometry tests

@pytest.fixture(scope="session")
def _base_alanine_molsys():
    molsys = msm.convert(systems['alanine dipeptide']['alanine_dipeptide.h5msm'], to_form='molsysmt.MolSys')
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_proline_molsys():
    molsys = msm.convert(systems['proline dipeptide']['proline_dipeptide.h5msm'], to_form='molsysmt.MolSys')
    assert molsys is not None
    return molsys

# Alternate formats for HP35

@pytest.fixture(scope="session")
def _base_hp35_pdb_molsys():
    molsys = msm.convert(systems['chicken villin HP35']['1vii.pdb'], to_form='molsysmt.MolSys')
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_hp35_mmtf_molsys():
    molsys = msm.convert(systems['chicken villin HP35']['1vii.bcif'], to_form='molsysmt.MolSys')
    assert molsys is not None
    return molsys

# T4 lysozyme variants

@pytest.fixture(scope="session")
def _base_t4_h5msm_molsys():
    molsys = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_t4_pdb_molsys():
    molsys = msm.convert(systems['T4 lysozyme L99A']['181l.pdb'], to_form='molsysmt.MolSys')
    assert molsys is not None
    return molsys

# TcTIM systems

@pytest.fixture(scope="session")
def _base_tctim_h5msm_molsys():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_tctim_bcif_molsys():
    molsys = msm.convert(systems['TcTIM']['1tcd.bcif.gz'], to_form='molsysmt.MolSys')
    assert molsys is not None
    return molsys

# POPC systems

@pytest.fixture(scope="session")
def _base_popc_psf():
    path = systems['POPC']['popc.psf']
    assert path is not None
    return path


@pytest.fixture(scope="session")
def _base_popc_membrane_molsys():
    molsys = msm.convert(systems['POPC membrane']['popc_membrane.dcd'], to_form='molsysmt.Structures')
    assert molsys is not None
    return molsys


# Function-scoped copies to keep tests isolated

@pytest.fixture()
def hp35_solvated_molsys(_base_hp35_solvated_molsys):
    return _base_hp35_solvated_molsys.copy()


@pytest.fixture()
def hp35_molsys(_base_hp35_molsys):
    return _base_hp35_molsys.copy()


@pytest.fixture()
def hp35_bcif_molsys(_base_hp35_bcif_molsys):
    return _base_hp35_bcif_molsys.copy()


@pytest.fixture()
def met_enkephalin_molsys(_base_met_enkephalin_molsys):
    return _base_met_enkephalin_molsys.copy()


@pytest.fixture()
def barnase_barstar_molsys(_base_barnase_barstar_molsys):
    return _base_barnase_barstar_molsys.copy()

@pytest.fixture()
def alanine_molsys(_base_alanine_molsys):
    return _base_alanine_molsys.copy()

@pytest.fixture()
def proline_molsys(_base_proline_molsys):
    return _base_proline_molsys.copy()

@pytest.fixture()
def hp35_pdb_molsys(_base_hp35_pdb_molsys):
    return _base_hp35_pdb_molsys.copy()

@pytest.fixture()
def hp35_mmtf_molsys(_base_hp35_mmtf_molsys):
    return _base_hp35_mmtf_molsys.copy()

@pytest.fixture()
def t4_h5msm_molsys(_base_t4_h5msm_molsys):
    return _base_t4_h5msm_molsys.copy()

@pytest.fixture()
def t4_pdb_molsys(_base_t4_pdb_molsys):
    return _base_t4_pdb_molsys.copy()

@pytest.fixture()
def tctim_h5msm_molsys(_base_tctim_h5msm_molsys):
    return _base_tctim_h5msm_molsys.copy()

@pytest.fixture()
def tctim_bcif_molsys(_base_tctim_bcif_molsys):
    return _base_tctim_bcif_molsys.copy()

@pytest.fixture()
def popc_psf(_base_popc_psf):
    return _base_popc_psf

@pytest.fixture()
def popc_membrane_structures(_base_popc_membrane_molsys):
    return _base_popc_membrane_molsys.copy()
