"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import os

# Whole systems (selection='all' and frame_indices='all')

def test_string_pdbid_to_molsysmt_MolSys():
    molsys_ref = msm.demo.classes.T4_lysozyme_L99A_in_pdbid_181l(to_form='molsysmt.MolSys')
    molsys = msm.convert('pdbid:181l', to_form='molsysmt.MolSys')
    output = msm.compare(molsys, molsys_ref, comparison='all', rule='A_eq_B')
    assert output == True

def test_string_pdbid_to_molsysmt_MolSys_2():
    molsys = msm.convert('pdbid:1tcd', to_form='molsysmt.MolSys')
    form = msm.get_form(molsys)
    assert 'molsysmt.MolSys'==form

def test_string_pdbid_to_file_pdb():
    molsys = msm.convert('pdbid:1sux', to_form='1sux.pdb')
    form = msm.get_form(molsys)
    os.remove(molsys)
    assert 'file:pdb'==form

def test_string_pdbid_to_file_mmtf():
    molsys = msm.convert('pdbid:1sux', to_form='1sux.mmtf')
    form = msm.get_form(molsys)
    os.remove(molsys)
    assert 'file:mmtf'==form

def test_file_pdb_to_mdtraj_Trajectory():
    molsys = msm.demo.files['1tcd.pdb']
    molsys = msm.convert(molsys, to_form='mdtraj.Trajectory')
    form = msm.get_form(molsys)
    assert 'mdtraj.Trajectory'==form

def test_mdtraj_Trajectory_to_string_aminoacids1():
    molsys = msm.demo.files['1tcd.pdb']
    molsys = msm.convert(molsys, to_form='mdtraj.Trajectory')
    molsys = msm.convert(molsys, to_form='string:aminoacids1')
    form = msm.get_form(molsys)
    assert 'string:aminoacids1'==form

def test_file_pdb_to_openmm_Topology():
    molsys = msm.demo.files['1tcd.pdb']
    molsys = msm.convert(molsys, to_form='openmm.Topology')
    form = msm.get_form(molsys)
    assert 'openmm.Topology'==form

def test_file_pdb_to_string_pdb():
    molsys = msm.demo.files['1tcd.pdb']
    molsys = msm.convert(molsys, to_form='string:pdb')
    form = msm.get_form(molsys)
    assert 'string:pdb'==form

def test_file_pdb_to_pdbfixer_PDBFixer():
    molsys = msm.demo.files['1tcd.pdb']
    molsys = msm.convert(molsys, to_form='pdbfixer.PDBFixer')
    form = msm.get_form(molsys)
    assert 'pdbfixer.PDBFixer'==form

def test_file_pdb_to_parmed_Structure():
    molsys = msm.demo.files['1tcd.pdb']
    molsys = msm.convert(molsys, to_form='parmed.Structure')
    form = msm.get_form(molsys)
    assert 'parmed.Structure'==form

def test_file_mol2_to_openmm_Modeller():
    molsys = msm.demo.files['caffeine.mol2']
    molsys = msm.convert(molsys, to_form='openmm.Modeller')
    form = msm.get_form(molsys)
    assert 'openmm.Modeller'==form

def test_file_mol2_to_mdtraj_Trajectory():
    molsys = msm.demo.files['caffeine.mol2']
    molsys = msm.convert(molsys, to_form='mdtraj.Trajectory')
    form = msm.get_form(molsys)
    assert 'mdtraj.Trajectory'==form

def test_file_mmtf_to_string_aminoacids1():
    molsys = msm.demo.files['1tcd.mmtf']
    molsys = msm.convert(molsys, to_form='string:aminoacids1')
    form = msm.get_form(molsys)
    assert 'string:aminoacids1'==form

def test_file_mmtf_to_molsysmt_MolSys():
    molsys = msm.demo.files['1tcd.mmtf']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    form = msm.get_form(molsys)
    assert 'molsysmt.MolSys'==form

def test_string_pdbid_to_mdtraj_Trajectory():
    molsys = msm.convert('pdbid:1sux', to_form='mdtraj.Trajectory')
    form = msm.get_form(molsys)
    assert 'mdtraj.Trajectory'==form

# Selection

def string_pdb_file_to_openmm_Topology_selection():
    molsys = msm.demo.files['181l.pdb']
    molsys = msm.convert(molsys, to_form='string:pdb')
    molsys = msm.convert(molsys, to_form='openmm.Topology', selection='molecule_type=="protein"')
    is_composed_of = msm.is_composed_of(molsys, proteins=1)
    form = msm.get_form(molsys)
    assert ('openmm.Topology'==form) and (is_composed_of==True)

## Multiple inputs

def file_prmtop_and_file_inpcrd_to_molsysmt_MolSys():
    prmtop_file = msm.demo.files['pentalanine.prmtop']
    inpcrd_file = msm.demo.files['pentalanine.inpcrd']
    molsys = msm.convert([prmtop_file, inpcrd_file], to_form='molsysmt.MolSys')
    form = msm.get_form(molsys)
    assert 'molsysmt.MolSys'==form

def molsysmt_Topology_and_molsysmt_Trajectory_to_string_pdb():
    molsys = msm.demo.classes.T4_lysozyme_L99A_in_pdbid_181l(to_form='molsysmt.MolSys')
    molsys = msm.convert(molsys, to_form=['molsysmt.Topology', 'molsysmt.Trajectory'])
    molsys = msm.convert(molsys, to_form='string:pdb')
    form = msm.get_form(molsys)
    assert 'string:pdb'==form

## Multiple outputs

def file_h5_to_molsysmt_Topology_and_molsysmt_Trajectory():
    molsys = msm.demo.files['pentalanine.h5']
    molsys = msm.convert(molsys, to_form=['molsysmt.Topology', 'molsysmt.Trajectory'])
    form = msm.get_form(molsys)
    assert ['molsysmt.Topology', 'molsysmt.Trajectory']==form


