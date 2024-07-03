"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_is_component_type_1():
    assert msm.element.component.is_component_type('water')
    assert msm.element.component.is_component_type('ion')
    assert msm.element.component.is_component_type('small molecule')
    assert msm.element.component.is_component_type('peptide')
    assert msm.element.component.is_component_type('protein')
    assert msm.element.component.is_component_type('dna')
    assert msm.element.component.is_component_type('rna')
    assert msm.element.component.is_component_type('lipid')
    assert msm.element.component.is_component_type('oligosaccharide')

def test_is_component_type_2():
    assert msm.element.component.is_component_type('waters')
    assert msm.element.component.is_component_type('ions')
    assert msm.element.component.is_component_type('small molecules')
    assert msm.element.component.is_component_type('peptides')
    assert msm.element.component.is_component_type('proteins')
    assert msm.element.component.is_component_type('lipids')
    assert msm.element.component.is_component_type('oligosaccharides')

def test_is_component_type_3():
    assert not msm.element.component.is_component_type('nothing')
