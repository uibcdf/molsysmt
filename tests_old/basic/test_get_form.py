"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

## Files

def test_file_pdb():
    molsys = systems['chicken villin HP35']['1vii.pdb']
    output = msm.get_form(molsys)
    assert output == 'file:pdb'

def test_file_bcif():
    molsys = systems['chicken villin HP35']['1vii.bcif']
    output = msm.get_form(molsys)
    assert output == 'file:bcif'

def test_file_bcif_gz():
    molsys = systems['chicken villin HP35']['1vii.bcif.gz']
    output = msm.get_form(molsys)
    assert output == 'file:bcif.gz'

def test_file_inpcrd_prmtop():
    molsys1 = systems['pentalanine']['pentalanine.inpcrd']
    molsys2 = systems['pentalanine']['pentalanine.prmtop']
    output = msm.get_form([molsys1, molsys2])
    assert output == ['file:inpcrd', 'file:prmtop']

def test_file_xyznpy():
    molsys = systems['particles 4']['traj_particles_4.xyznpy']
    output = msm.get_form(molsys)
    assert output == 'file:xyznpy'

def test_file_h5msm():
    molsys = systems['chicken villin HP35']['chicken_villin_HP35.h5msm']
    output = msm.get_form(molsys)
    assert output == 'file:h5msm'

## Strings

def test_string_pdb_id():
    molsys = 'pdb_id:1VII'
    output = msm.get_form(molsys)
    assert output == 'string:pdb_id'

def test_string_pdb_id_automatic_detection():
    molsys = '1VII'
    output = msm.get_form(molsys)
    assert output == 'string:pdb_id'

def test_string_amino_acids_3():
    molsys = 'amino_acids_3:ACEALAGLYVALNME'
    output = msm.get_form(molsys)
    assert output == 'string:amino_acids_3'

def test_string_amino_acids_3_automatic_detection():
    molsys = 'ACEALAGLYVALNME'
    output = msm.get_form(molsys)
    assert output == 'string:amino_acids_3'

def test_string_amino_acids_1():
    molsys = 'amino_acids_1:ALYDERRRT'
    output = msm.get_form(molsys)
    assert output == 'string:amino_acids_1'

def test_string_amino_acids_1_automatic_detection():
    molsys = 'ALYDERRRT'
    output = msm.get_form(molsys)
    assert output == 'string:amino_acids_1'

def test_string_pdb_text():
    molsys = systems['benzamidine']['benzamidine.pdb']
    molsys = msm.convert(molsys, 'string:pdb_text')
    molsys = 'pdb_text:'+molsys
    output = msm.get_form(molsys)
    assert output == 'string:pdb_text'

def test_string_pdb_text_2():
    fff=open(systems['T4 lysozyme L99A']['181l.pdb'],'r')
    molsys = fff.read()
    fff.close()
    output = msm.get_form(molsys)
    assert output == 'string:pdb_text'

def test_string_pdb_automatic_detection():
    molsys = systems['benzamidine']['benzamidine.pdb']
    molsys = msm.convert(molsys, 'string:pdb_text')
    output = msm.get_form(molsys)
    assert output == 'string:pdb_text'

## Classes

def test_class_XYZ():
    molsys = np.zeros(shape=[10,4,3])*msm.pyunitwizard.unit('nanometers')
    output = msm.get_form(molsys)
    assert output == 'XYZ'

def test_molsysmt_MolSys():
    molsys = systems['chicken villin HP35']['chicken_villin_HP35.h5msm']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    output = msm.get_form(molsys)
    assert output == 'molsysmt.MolSys'

def test_nglview_NGLWidget():
    molsys = systems['chicken villin HP35']['chicken_villin_HP35.h5msm']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    molsys = msm.view(molsys)
    output = msm.get_form(molsys)
    assert output == 'nglview.NGLWidget'

