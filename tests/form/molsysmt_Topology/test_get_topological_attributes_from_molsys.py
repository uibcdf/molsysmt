import pytest
import molsysmt as msm
from molsysmt.form.molsysmt_Topology import get_topological_attributes as aux

@pytest.fixture(scope="module")
def molsys_Hk2():
    return msm.convert(msm.systems['Hexokinase 2']['2nzt.bcif.gz'], to_form='molsysmt.Topology')

def test_get_n_atoms_from_system(molsys_Hk2):
    assert aux.get_n_atoms_from_system(molsys_Hk2) == 13546

def test_get_n_groups_from_system(molsys_Hk2):
    assert aux.get_n_groups_from_system(molsys_Hk2) == 1871

def test_get_n_molecules_from_system(molsys_Hk2):
    assert aux.get_n_molecules_from_system(molsys_Hk2) == 135

def test_get_n_entities_from_system(molsys_Hk2):
    assert aux.get_n_entities_from_system(molsys_Hk2) == 5
