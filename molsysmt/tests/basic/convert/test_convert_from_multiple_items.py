"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import os

def test_convert_file_prmtop_and_file_inpcrd_to_molsysmt_MolSys():
    prmtop_file = msm.demo.files['pentalanine.prmtop']
    inpcrd_file = msm.demo.files['pentalanine.inpcrd']
    molsys = msm.convert([prmtop_file, inpcrd_file], to_form='molsysmt.MolSys')
    form = msm.get_form(molsys)
    assert 'molsysmt.MolSys'==form

def test_convert_molsysmt_Topology_and_molsysmt_Trajectory_to_string_pdb_text():
    molsys = msm.demo.classes.T4_Lysozyme_L99A_in_pdbid_181l(to_form='molsysmt.MolSys')
    molsys = msm.convert(molsys, to_form=['molsysmt.Topology', 'molsysmt.Trajectory'])
    molsys = msm.convert(molsys, to_form='string:pdb')
    form = msm.get_form(molsys)
    assert 'string:pdb'==form

def test_convert_file_gro_and_file_xtc_to_molsysmt_MolSys():
    import warnings
    warnings.filterwarnings('ignore')
    molsys_1 = msm.demo.files['nglview_demo_md_1u19.gro']
    molsys_2 = msm.demo.files['nglview_demo_md_1u19.xtc']
    molsys = msm.convert([molsys_1, molsys_2], to_form='molsysmt.MolSys')
    warnings.resetwarnings()
    form = msm.get_form(molsys)
    assert 'molsysmt.MolSys'==form

def test_convert_file_gro_and_file_xtc_to_mdtraj_Trajectory():
    import warnings
    warnings.filterwarnings('ignore')
    molsys_1 = msm.demo.files['nglview_demo_md_1u19.gro']
    molsys_2 = msm.demo.files['nglview_demo_md_1u19.xtc']
    molsys = msm.convert([molsys_1, molsys_2], to_form='mdtraj.Trajectory')
    warnings.resetwarnings()
    form = msm.get_form(molsys)
    assert 'mdtraj.Trajectory'==form

