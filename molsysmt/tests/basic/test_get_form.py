"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np

## Files

def test_file_pdb():
    molsys = tests_systems['chicken villin HP35']['1vii.pdb']
    output = msm.get_form(molsys)
    assert output == 'file:pdb'

def test_file_mmtf():
    molsys = tests_systems['chicken villin HP35']['1vii.mmtf']
    output = msm.get_form(molsys)
    assert output == 'file:mmtf'

def test_file_inpcrd_prmtop():
    molsys1 = tests_systems['pentalanine']['pentalanine.inpcrd']
    molsys2 = tests_systems['pentalanine']['pentalanine.prmtop']
    output = msm.get_form([molsys1, molsys2])
    assert output == ['file:inpcrd', 'file:prmtop']

def test_file_xyznpy():
    molsys = tests_systems['particles 4']['traj_particles_4.xyznpy']
    output = msm.get_form(molsys)
    assert output == 'file:xyznpy'

def test_file_msmpk():
    molsys = tests_systems['chicken villin HP35']['chicken_villin_HP35.msmpk']
    output = msm.get_form(molsys)
    assert output == 'file:msmpk'

## Strings

def test_string_pdb_id():
    molsys = 'pdb_id:1VII'
    output = msm.get_form(molsys)
    assert output == 'string:pdb_id'

def test_string_pdb_id_automatic_detection():
    molsys = '1VII'
    output = msm.get_form(molsys)
    assert output == 'string:pdb_id'

def test_string_aminoacids3():
    molsys = 'aminoacids3:ACEALAGLYVALNME'
    output = msm.get_form(molsys)
    assert output == 'string:aminoacids3'

def test_string_aminoacids3_automatic_detection():
    molsys = 'ACEALAGLYVALNME'
    output = msm.get_form(molsys)
    assert output == 'string:aminoacids3'

def test_string_aminoacids1():
    molsys = 'aminoacids1:ALYDERRRT'
    output = msm.get_form(molsys)
    assert output == 'string:aminoacids1'

def test_string_aminoacids1_automatic_detection():
    molsys = 'ALYDERRRT'
    output = msm.get_form(molsys)
    assert output == 'string:aminoacids1'

def test_string_pdb_text():
    molsys = tests_systems['benzamidine']['benzamidine.pdb']
    molsys = msm.convert(molsys, 'string:pdb_text')
    molsys = 'pdb_text:'+molsys
    output = msm.get_form(molsys)
    assert output == 'string:pdb_text'

def test_string_pdb_text_2():
    fff=open(tests_systems['T4 lysozyme L99A']['181l.pdb'],'r')
    molsys = fff.read()
    fff.close()
    output = msm.get_form(molsys)
    assert output == 'string:pdb_text'

def test_string_pdb_automatic_detection():
    molsys = tests_systems['benzamidine']['benzamidine.pdb']
    molsys = msm.convert(molsys, 'string:pdb_text')
    output = msm.get_form(molsys)
    assert output == 'string:pdb_text'

## Classes

def test_class_XYZ():
    molsys = np.zeros(shape=[10,4,3])*msm.pyunitwizard.unit('nanometers')
    output = msm.get_form(molsys)
    assert output == 'XYZ'

def test_molsysmt_MolSys():
    molsys = tests_systems['chicken villin HP35']['chicken_villin_HP35.msmpk']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    output = msm.get_form(molsys)
    assert output == 'molsysmt.MolSys'

def test_nglview_NGLWidget():
    molsys = tests_systems['chicken villin HP35']['chicken_villin_HP35.msmpk']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    molsys = msm.view(molsys)
    output = msm.get_form(molsys)
    assert output == 'nglview.NGLWidget'

