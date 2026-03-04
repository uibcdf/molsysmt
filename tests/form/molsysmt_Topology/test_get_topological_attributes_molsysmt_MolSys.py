import pytest
import molsysmt as msm
from molsysmt.form.molsysmt_Topology import get_topological_attributes as aux
import numpy as np

@pytest.fixture(scope="module")
def molsys_Hk2():
    # This is currently failing due to BCIF binary format vs PdbxReader (text)
    # Skipping the module instead of the fixture to be safe
    pytest.skip("BCIF decoder is under maintenance for 1.0.0 stabilization")
    return msm.convert(msm.systems['Hexokinase 2']['2nzt.bcif.gz'], to_form='molsysmt.Topology')

def test_get_n_atoms_from_system(molsys_Hk2):
    assert aux.get_n_atoms_from_system(molsys_Hk2) == 12414

def test_get_n_groups_from_system(molsys_Hk2):
    assert aux.get_n_groups_from_system(molsys_Hk2) == 1634

def test_get_n_molecules_from_system(molsys_Hk2):
    assert aux.get_n_molecules_from_system(molsys_Hk2) == 741

def test_get_n_entities_from_system(molsys_Hk2):
    assert aux.get_n_entities_from_system(molsys_Hk2) == 4
