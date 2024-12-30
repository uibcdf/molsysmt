"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_is_element():
    assert True == msm.element.is_element('atom')
    assert True == msm.element.is_element('group')
    assert True == msm.element.is_element('component')
    assert True == msm.element.is_element('molecule')
    assert True == msm.element.is_element('chain')
    assert True == msm.element.is_element('entity')
    assert True == msm.element.is_element('bond')
    assert True == msm.element.is_element('system')

def test_is_element_with_plurals():
    assert True == msm.element.is_element('atoms')
    assert True == msm.element.is_element('groups')
    assert True == msm.element.is_element('components')
    assert True == msm.element.is_element('molecules')
    assert True == msm.element.is_element('chains')
    assert True == msm.element.is_element('entities')
    assert True == msm.element.is_element('bonds')

def test_is_not_element():
    assert False == msm.element.is_element('systems')
    assert False == msm.element.is_element('zzz')
