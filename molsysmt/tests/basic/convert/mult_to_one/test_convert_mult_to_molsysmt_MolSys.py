"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt.basic.convert import _convert_multiple_to_one_with_shortcuts, _convert_multiple_to_one
import numpy as np
import os

def test_convert_file_prmtop_and_file_inpcrd_to_molsysmt_MolSys():
    prmtop_file = systems['pentalanine']['pentalanine.prmtop']
    inpcrd_file = systems['pentalanine']['pentalanine.inpcrd']
    molsys = msm.convert([prmtop_file, inpcrd_file], to_form='molsysmt.MolSys')
    form = msm.get_form(molsys)
    n_atoms, n_structures, box = msm.get(molsys, n_atoms=True, n_structures=True, box=True)
    n_atoms_prmtop = msm.get(prmtop_file, n_atoms=True)
    n_structures_inpcrd, box_inpcrd = msm.get(inpcrd_file, n_structures=True, box=True)
    assert 'molsysmt.MolSys'==form
    assert n_atoms==n_atoms_prmtop
    assert n_structures==n_structures_inpcrd
    assert np.allclose(box, box_inpcrd)

def test_convert_file_psf_and_file_dcd_to_molsysmt_MolSys():
    psf_file = systems['POPC membrane']['popc_membrane.psf']
    dcd_file = systems['POPC membrane']['popc_membrane.dcd']
    molsys = msm.convert([psf_file, dcd_file], to_form='molsysmt.MolSys')
    form = msm.get_form(molsys)
    n_atoms, n_structures = msm.get(molsys, n_atoms=True, n_structures=True)
    assert 'molsysmt.MolSys'==form
    assert n_atoms==78974
    assert n_structures==50

def test_convert_file_gro_and_file_xtc_to_molsysmt_MolSys():
    molsys_1 = systems['nglview']['md_1u19.gro']
    molsys_2 = systems['nglview']['md_1u19.xtc']
    molsys = msm.convert([molsys_1, molsys_2], to_form='molsysmt.MolSys')
    form = msm.get_form(molsys)
    assert 'molsysmt.MolSys'==form

