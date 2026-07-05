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
    pytest.importorskip("pytraj")

    molsys = msm.convert(msm.systems['nglview']['md_1u19.pdb'], to_form='molsysmt.MolSys')
    molsys.topology.remove_bonds('all', skip_digestion=True)
    bonds1 = msm.build.get_missing_bonds(molsys)
    bonds2 = msm.build.get_missing_bonds(molsys, engine='pytraj')

    bonds1_not_in_bonds2 = [item for item in bonds1 if item not in bonds2]
    bonds2_not_in_bonds1 = [item for item in bonds2 if item not in bonds1]

    assert len(bonds1)==5632
    assert len(bonds2)==5632
    assert len(bonds1_not_in_bonds2)==0
    assert len(bonds2_not_in_bonds1)==0


def test_get_missing_bonds_with_selection_preserves_pairs():

    molsys = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    molsys = msm.convert(molsys)
    molsys.topology.remove_bonds('all', skip_digestion=True)

    bonds = msm.build.get_missing_bonds(molsys, selection='group_index==1')

    assert len(bonds)==9
    assert all(len(bond)==2 for bond in bonds)
    assert bonds == [[6, 7], [6, 8], [8, 9], [8, 10], [8, 14],
                     [10, 11], [10, 12], [10, 13], [14, 15]]
