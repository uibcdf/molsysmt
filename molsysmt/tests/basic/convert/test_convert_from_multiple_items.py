"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import os

def test_convert_file_prmtop_and_file_inpcrd_to_molsysmt_MolSys():
    prmtop_file = msm.demo['pentalanine']['pentalanine.prmtop']
    inpcrd_file = msm.demo['pentalanine']['pentalanine.inpcrd']
    molsys = msm.convert([prmtop_file, inpcrd_file], to_form='molsysmt.MolSys')
    form = msm.get_form(molsys)
    assert 'molsysmt.MolSys'==form

def test_convert_molsysmt_Topology_and_molsysmt_Structures_to_string_pdb_text():
    molsys = msm.convert(msm.demo['T4 lysozyme L99A']['181l.pdb'], to_form='molsysmt.MolSys')
    molsys = msm.convert(molsys, to_form=['molsysmt.Topology', 'molsysmt.Structures'])
    molsys = msm.convert(molsys, to_form='string:pdb_text')
    form = msm.get_form(molsys)
    assert 'string:pdb_text'==form

#def test_convert_file_gro_and_file_xtc_to_molsysmt_MolSys():
#    import warnings
#    warnings.filterwarnings('ignore')
#    molsys_1 = msm.demo['nglview']['1u19.gro']
#    molsys_2 = msm.demo['nglview']['1u19.xtc']
#    molsys = msm.convert([molsys_1, molsys_2], to_form='molsysmt.MolSys')
#    warnings.resetwarnings()
#    form = msm.get_form(molsys)
#    assert 'molsysmt.MolSys'==form
#
#def test_convert_file_gro_and_file_xtc_to_mdtraj_Structures():
#    import warnings
#    warnings.filterwarnings('ignore')
#    molsys_1 = msm.demo['nglview']['1u19.gro']
#    molsys_2 = msm.demo['nglview']['1u19.xtc']
#    molsys = msm.convert([molsys_1, molsys_2], to_form='mdtraj.Trajectory')
#    warnings.resetwarnings()
#    form = msm.get_form(molsys)
#    assert 'mdtraj.Trajectory'==form

