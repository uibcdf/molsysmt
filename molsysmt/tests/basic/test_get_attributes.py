"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np

def test_get_attributes_string_pdb():
    molsys = '181L'
    attributes = msm.get_attributes(molsys)
    assert attributes['group_name']==True
    assert attributes['entity_name']==True
    assert attributes['box']==True

def test_get_attributes_molsysmt_MolSys():
    molsys = msm.convert(tests_systems['T4 lysozyme L99A']['181l.msmpk'])
    attributes = msm.get_attributes(molsys)
    assert attributes['group_name']==True
    assert attributes['entity_name']==True
    assert attributes['box']==True

def test_get_attributes_openmm_Topology():
    molsys = msm.convert(tests_systems['T4 lysozyme L99A']['181l.msmpk'], to_form='openmm.Topology')
    attributes = msm.get_attributes(molsys)
    assert attributes['group_name']==True
    assert attributes['entity_name']==False
    assert attributes['box']==True

def test_get_attributes_string_aminoacids1():
    molsys = msm.convert(tests_systems['T4 lysozyme L99A']['181l.msmpk'], to_form='string:aminoacids1', selection='molecule_type=="protein"')
    attributes = msm.get_attributes(molsys)
    assert attributes['group_name']==True
    assert attributes['entity_name']==False
    assert attributes['box']==False



