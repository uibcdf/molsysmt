"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_is_group_type_molsysmt_MolSys_1():

    assert msm.element.group.is_group_type('water')
    assert msm.element.group.is_group_type('ion')
    assert msm.element.group.is_group_type('small molecule')
    assert msm.element.group.is_group_type('amino acid')
    assert msm.element.group.is_group_type('terminal capping')
    assert msm.element.group.is_group_type('nucleotide')
    assert msm.element.group.is_group_type('lipid')
    assert msm.element.group.is_group_type('saccharide')
    assert msm.element.group.is_group_type('oligosaccharide')
    assert msm.element.group.is_group_type('papa')==False


def test_is_group_type_molsysmt_MolSys_2():

    assert msm.element.group.is_group_type('waters')
    assert msm.element.group.is_group_type('ions')
    assert msm.element.group.is_group_type('small molecules')
    assert msm.element.group.is_group_type('amino acids')
    assert msm.element.group.is_group_type('terminal cappings')
    assert msm.element.group.is_group_type('nucleotides')
    assert msm.element.group.is_group_type('lipids')
    assert msm.element.group.is_group_type('saccharides')
    assert msm.element.group.is_group_type('oligosaccharides')

