"""
Unit and regression test for the mutate module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_mutate_molsysmt_MolSys_1():
    molsys = msm.convert(msm.demo['Met-enkephalin']['vacuum.pdb'], to_form='molsysmt.MolSys')
    molsys = msm.build.mutate(molsys, mutations={1:'ALA', 2:'VAL'}, keys='group_index')
    seq = msm.convert(molsys, to_form='string:aminoacids3')
    check = (seq == 'TyrAlaValPheMet')
    assert check

def test_mutate_molsysmt_MolSys_2():
    molsys = msm.convert(msm.demo['Met-enkephalin']['vacuum.pdb'], to_form='molsysmt.MolSys')
    molsys = msm.build.mutate(molsys, mutations={2:'ALA', 3:'VAL'}, keys='group_id')
    seq = msm.convert(molsys, to_form='string:aminoacids3')
    check = (seq == 'TyrAlaValPheMet')
    assert check

def test_mutate_molsysmt_MolSys_3():
    molsys = msm.convert(msm.demo['Met-enkephalin']['vacuum.pdb'], to_form='molsysmt.MolSys')
    molsys = msm.build.mutate(molsys, mutations={'GLY':'ALA'}, keys='group_name')
    seq = msm.convert(molsys, to_form='string:aminoacids3')
    check = (seq == 'TyrAlaAlaPheMet')
    assert check

# From https://github.com/openmm/pdbfixer/blob/master/pdbfixer/tests/test_mutate.py
def test_mutate_molsysmt_MolSys_4():
    molsys = msm.convert(msm.demo['chicken villin HP35']['1vii.mmtf'], to_form='molsysmt.MolSys')
    molsys = msm.build.mutate(molsys, mutations="ALA-57-GLY")
    group_name, group_id = msm.get(molsys, element='group', selection="group_index==16", group_name=True, group_id=True)
    atoms = msm.get(molsys, element='atom', selection="group_index==16", atom_name=True)
    assert group_name[0]=='GLY'
    assert group_id[0]==57
    assert set(['N', 'H', 'CA', 'HA2', 'HA3', 'C', 'O'])==set(atoms)


