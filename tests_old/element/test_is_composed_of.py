"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_system_is_composed_of():

    assert True == msm.element.is_composed_of('system','atom')
    assert True == msm.element.is_composed_of('system','group')
    assert True == msm.element.is_composed_of('system','component')
    assert True == msm.element.is_composed_of('system','molecule')
    assert True == msm.element.is_composed_of('system','entity')
    assert True == msm.element.is_composed_of('system','bond')
    assert True == msm.element.is_composed_of('system','chain')

    assert True == msm.element.is_composed_of('system','atoms')
    assert True == msm.element.is_composed_of('system','groups')
    assert True == msm.element.is_composed_of('system','components')
    assert True == msm.element.is_composed_of('system','molecules')
    assert True == msm.element.is_composed_of('system','entities')
    assert True == msm.element.is_composed_of('system','bonds')
    assert True == msm.element.is_composed_of('system','chains')

def test_chain_is_composed_of():

    assert True == msm.element.is_composed_of('chains','atom')
    assert True == msm.element.is_composed_of('chain','group')
    assert True == msm.element.is_composed_of('chain','component')
    assert True == msm.element.is_composed_of('chain','molecule')
    assert True == msm.element.is_composed_of('chain','entity')
    assert False == msm.element.is_composed_of('chain','bonds')
    assert False == msm.element.is_composed_of('chain','chains')

def test_entity_is_composed_of():

    assert True == msm.element.is_composed_of('entities','atom')
    assert True == msm.element.is_composed_of('entity','group')
    assert True == msm.element.is_composed_of('entity','component')
    assert True == msm.element.is_composed_of('entity','molecule')
    assert False == msm.element.is_composed_of('entity','entity')
    assert False == msm.element.is_composed_of('entity','bonds')
    assert False == msm.element.is_composed_of('entity','chains')

def test_molecule_is_composed_of():

    assert True == msm.element.is_composed_of('molecules','atom')
    assert True == msm.element.is_composed_of('molecule','group')
    assert True == msm.element.is_composed_of('molecule','component')
    assert False == msm.element.is_composed_of('molecule','molecule')
    assert False == msm.element.is_composed_of('molecule','entity')
    assert False == msm.element.is_composed_of('molecule','bonds')
    assert False == msm.element.is_composed_of('molecule','chains')

def test_component_is_composed_of():

    assert True == msm.element.is_composed_of('components','atom')
    assert True == msm.element.is_composed_of('component','group')
    assert False == msm.element.is_composed_of('component','component')
    assert False == msm.element.is_composed_of('component','molecule')
    assert False == msm.element.is_composed_of('component','entity')
    assert False == msm.element.is_composed_of('component','bonds')
    assert False == msm.element.is_composed_of('component','chains')

def test_group_is_composed_of():

    assert True == msm.element.is_composed_of('groups','atom')
    assert False == msm.element.is_composed_of('group','group')
    assert False == msm.element.is_composed_of('group','component')
    assert False == msm.element.is_composed_of('group','molecule')
    assert False == msm.element.is_composed_of('group','entity')
    assert False == msm.element.is_composed_of('group','bonds')
    assert False == msm.element.is_composed_of('group','chains')

