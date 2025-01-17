"""
Unit and regression test for the is solvate module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import pytest
import molsysmt as msm
import numpy as np
import sys

@pytest.mark.skipif(sys.platform != "linux", reason="This test can only be run in linux")
def test_get_missing_bonds_molsysmt_MolSys_1():

    molsys = msm.convert(msm.systems['nglview']['md_1u19.pdb'], to_form='molsysmt.MolSys')
    msm.build.remove_bonds(molsys)
    bonds1 = msm.build.get_missing_bonds(molsys)
    bonds2 = msm.build.get_missing_bonds(molsys, engine='pytraj')

    bonds1_not_in_bonds2 = [item for item in bonds1 if item not in bonds2]
    bonds2_not_in_bonds1 = [item for item in bonds2 if item not in bonds1]

    assert len(bonds1)==5632
    assert len(bonds2)==5632
    assert len(bonds1_not_in_bonds2)==0
    assert len(bonds2_not_in_bonds1)==0
