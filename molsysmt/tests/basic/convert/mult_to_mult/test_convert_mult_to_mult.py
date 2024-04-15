"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt.basic.convert import _convert_multiple_to_one_with_shortcuts, _convert_multiple_to_one
import numpy as np
import os

def test_convert_file_prmtop_and_file_inpcrd_to_molsysmt_Topology_and_molsysmt_Structures():
    prmtop_file = systems['pentalanine']['pentalanine.prmtop']
    inpcrd_file = systems['pentalanine']['pentalanine.inpcrd']
    molsys = msm.convert([prmtop_file, inpcrd_file], to_form=['molsysmt.Topology', 'molsysmt.Structures'])
    form = msm.get_form(molsys)
    n_atoms, n_structures, box = msm.get(molsys, n_atoms=True, n_structures=True, box=True)
    n_atoms_prmtop = msm.get(prmtop_file, n_atoms=True)
    n_structures_inpcrd, box_inpcrd = msm.get(inpcrd_file, n_structures=True, box=True)
    assert np.all(['molsysmt.Topology','molsysmt.Structures']==form)
    assert n_atoms==n_atoms_prmtop
    assert n_structures==n_structures_inpcrd
    assert np.allclose(box, box_inpcrd)

