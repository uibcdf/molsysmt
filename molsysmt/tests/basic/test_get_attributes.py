"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_get_attributes_string_pdb():
    molsys = '181L'
    attributes = msm.get_attributes(molsys)
    assert attributes['group_name']==True
    assert attributes['entity_name']==True
    assert attributes['box']==True

def test_get_attributes_molsysmt_MolSys():
    molsys = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'])
    attributes = msm.get_attributes(molsys)
    assert attributes['group_name']==True
    assert attributes['entity_name']==True
    assert attributes['box']==True

def test_get_attributes_openmm_Topology():
    molsys = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'], to_form='openmm.Topology')
    attributes = msm.get_attributes(molsys)
    assert attributes['group_name']==True
    assert attributes['entity_name']==False
    assert attributes['box']==True

def test_get_attributes_string_amino_acids_1():
    molsys = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'], to_form='string:amino_acids_1', selection='molecule_type=="protein"')
    attributes = msm.get_attributes(molsys)
    assert attributes['group_name']==True
    assert attributes['entity_name']==False
    assert attributes['box']==False



