"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

## Files

def test_file_pdb():
    molsys = msm.demo.files['1sux.pdb']
    output = msm.get_form(molsys)
    assert output == 'file:pdb'

def test_file_mmtf():
    molsys = msm.demo.files['1sux.mmtf']
    output = msm.get_form(molsys)
    assert output == 'file:mmtf'

def test_files_inpcrd_prmtop():
    molsys1 = msm.demo.files['pentalanine.inpcrd']
    molsys2 = msm.demo.files['pentalanine.prmtop']
    output = msm.get_form([molsys1, molsys2])
    assert output == ['file:inpcrd', 'file:prmtop']

## Strings

def test_string_pdbid():
    molsys = 'pdbid:2LAO'
    output = msm.get_form(molsys)
    assert output == 'string:pdbid'

def test_string_pdbid_automatic_detection():
    molsys = '2LAO'
    output = msm.get_form(molsys)
    assert output == 'string:pdbid'

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

def test_string_pdb():
    molsys = msm.demo.strings.pdb_benzamidine
    molsys = 'pdb:'+molsys
    output = msm.get_form(molsys)
    assert output == 'string:pdb'

def test_string_pdb_automatic_detection():
    molsys = msm.demo.strings.pdb_benzamidine
    output = msm.get_form(molsys)
    assert output == 'string:pdb'

## Classes

def test_class_XYZ():
    molsys = np.zeros(shape=[10,4,3])*msm.puw.unit('nanometers')
    output = msm.get_form(molsys)
    assert output == 'XYZ'

def test_nglview_NGLWidget():
    molsys = msm.demo.classes.valine_dipeptide_vacuum(to_form='molsysmt.MolSys')
    molsys = msm.view(molsys)
    output = msm.get_form(molsys)
    assert output == 'nglview.NGLWidget'

