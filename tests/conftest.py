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
def _base_met_enkephalin_pdb_molsys():
    molsys = msm.convert(systems['Met-enkephalin']['met_enkephalin.pdb'], to_form='molsysmt.MolSys')
    assert molsys is not None
    return molsys

@pytest.fixture(scope="session")
def _base_met_enkephalin_h5msm_molsys():
    molsys = msm.convert(systems['Met-enkephalin']['met_enkephalin.h5msm'], to_form='molsysmt.MolSys')
    assert molsys is not None
    return molsys

@pytest.fixture(scope="session")
def _base_traj_pentalanine_h5_molsys():
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    assert molsys is not None
    return molsys

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

@pytest.fixture(scope="session")
def _base_valine_molsys():
    molsys = msm.convert(systems['valine dipeptide']['valine_dipeptide.h5msm'], to_form='molsysmt.MolSys')
    assert molsys is not None
    return molsys

@pytest.fixture(scope="session")
def _base_lysine_molsys():
    molsys = msm.convert(systems['lysine dipeptide']['lysine_dipeptide.h5msm'], to_form='molsysmt.MolSys')
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


@pytest.fixture(scope="session")
def _base_t4_pdb_text():
    pdb_text = msm.convert(systems['T4 lysozyme L99A']['181l.pdb'], to_form='string:pdb_text')
    assert pdb_text is not None
    return pdb_text


@pytest.fixture(scope="session")
def _base_t4_written_pdb_text(_base_t4_pdb_molsys):
    pdb_text = msm.convert(_base_t4_pdb_molsys, to_form='string:pdb_text')
    assert pdb_text is not None
    return pdb_text


@pytest.fixture(scope="session")
def _base_md_1u19_pdb_molsys():
    molsys = msm.convert(systems['nglview']['md_1u19.pdb'], to_form='molsysmt.MolSys')
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_md_1u19_pdb_text():
    pdb_text = msm.convert(systems['nglview']['md_1u19.pdb'], to_form='string:pdb_text')
    assert pdb_text is not None
    return pdb_text

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
def hp35_bcif_file():
    return systems['chicken villin HP35']['1vii.bcif']


@pytest.fixture()
def hp35_bcif_gz_file():
    return systems['chicken villin HP35']['1vii.bcif.gz']


@pytest.fixture(scope="session")
def _base_hp35_cif_file(tmp_path_factory):
    import gzip
    import shutil
    from mmcif.io.IoAdapterCore import IoAdapterCore

    tmp_dir = tmp_path_factory.mktemp('hp35_cif_assets')
    cif_path = tmp_dir / '1vii.cif'
    if not cif_path.exists():
        container = msm.convert(systems['chicken villin HP35']['1vii.bcif.gz'], to_form='mmcif.PdbxContainers.DataContainer')
        io = IoAdapterCore()
        io.writeFile(str(cif_path), [container])

    return str(cif_path)


@pytest.fixture()
def hp35_cif_file(_base_hp35_cif_file):
    return _base_hp35_cif_file


@pytest.fixture(scope="session")
def _base_hp35_cif_gz_file(tmp_path_factory, _base_hp35_cif_file):
    import gzip
    import shutil

    tmp_dir = tmp_path_factory.mktemp('hp35_cif_gz_assets')
    cif_gz_path = tmp_dir / '1vii.cif.gz'
    if not cif_gz_path.exists():
        with open(_base_hp35_cif_file, 'rb') as source, gzip.open(cif_gz_path, 'wb') as destination:
            shutil.copyfileobj(source, destination)

    return str(cif_gz_path)


@pytest.fixture()
def hp35_cif_gz_file(_base_hp35_cif_gz_file):
    return _base_hp35_cif_gz_file

@pytest.fixture()
def met_enkephalin_pdb_molsys(_base_met_enkephalin_pdb_molsys):
    return _base_met_enkephalin_pdb_molsys.copy()

@pytest.fixture()
def met_enkephalin_h5msm_molsys(_base_met_enkephalin_h5msm_molsys):
    return _base_met_enkephalin_h5msm_molsys.copy()

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
def valine_molsys(_base_valine_molsys):
    return _base_valine_molsys.copy()

@pytest.fixture()
def lysine_molsys(_base_lysine_molsys):
    return _base_lysine_molsys.copy()

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
def t4_pdb_file():
    return systems['T4 lysozyme L99A']['181l.pdb']


@pytest.fixture()
def t4_pdb_text(_base_t4_pdb_text):
    return _base_t4_pdb_text


@pytest.fixture()
def t4_written_pdb_text(_base_t4_written_pdb_text):
    return _base_t4_written_pdb_text


@pytest.fixture()
def t4_pdb_handler(t4_pdb_text):
    handler = msm.convert(t4_pdb_text, to_form='molsysmt.PDBFileHandler')
    yield handler
    handler.close()


@pytest.fixture()
def md_1u19_pdb_molsys(_base_md_1u19_pdb_molsys):
    return _base_md_1u19_pdb_molsys.copy()


@pytest.fixture()
def md_1u19_pdb_file():
    return systems['nglview']['md_1u19.pdb']


@pytest.fixture()
def md_1u19_pdb_text(_base_md_1u19_pdb_text):
    return _base_md_1u19_pdb_text

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

@pytest.fixture()
def traj_pentalanine_h5_molsys(_base_traj_pentalanine_h5_molsys):
    return _base_traj_pentalanine_h5_molsys.copy()
