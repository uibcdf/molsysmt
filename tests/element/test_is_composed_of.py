"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_system_is_composed_of():

    assert msm.element.is_composed_of("system", "atom")
    assert msm.element.is_composed_of("system", "group")
    assert msm.element.is_composed_of("system", "component")
    assert msm.element.is_composed_of("system", "molecule")
    assert msm.element.is_composed_of("system", "entity")
    assert msm.element.is_composed_of("system", "bond")
    assert msm.element.is_composed_of("system", "chain")

    assert msm.element.is_composed_of("system", "atoms")
    assert msm.element.is_composed_of("system", "groups")
    assert msm.element.is_composed_of("system", "components")
    assert msm.element.is_composed_of("system", "molecules")
    assert msm.element.is_composed_of("system", "entities")
    assert msm.element.is_composed_of("system", "bonds")
    assert msm.element.is_composed_of("system", "chains")


def test_chain_is_composed_of():

    assert msm.element.is_composed_of("chains", "atom")
    assert msm.element.is_composed_of("chain", "group")
    assert msm.element.is_composed_of("chain", "component")
    assert msm.element.is_composed_of("chain", "molecule")
    assert msm.element.is_composed_of("chain", "entity")
    assert not msm.element.is_composed_of("chain", "bonds")
    assert not msm.element.is_composed_of("chain", "chains")


def test_entity_is_composed_of():

    assert msm.element.is_composed_of("entities", "atom")
    assert msm.element.is_composed_of("entity", "group")
    assert msm.element.is_composed_of("entity", "component")
    assert msm.element.is_composed_of("entity", "molecule")
    assert not msm.element.is_composed_of("entity", "entity")
    assert not msm.element.is_composed_of("entity", "bonds")
    assert not msm.element.is_composed_of("entity", "chains")


def test_molecule_is_composed_of():

    assert msm.element.is_composed_of("molecules", "atom")
    assert msm.element.is_composed_of("molecule", "group")
    assert msm.element.is_composed_of("molecule", "component")
    assert not msm.element.is_composed_of("molecule", "molecule")
    assert not msm.element.is_composed_of("molecule", "entity")
    assert not msm.element.is_composed_of("molecule", "bonds")
    assert not msm.element.is_composed_of("molecule", "chains")


def test_component_is_composed_of():

    assert msm.element.is_composed_of("components", "atom")
    assert msm.element.is_composed_of("component", "group")
    assert not msm.element.is_composed_of("component", "component")
    assert not msm.element.is_composed_of("component", "molecule")
    assert not msm.element.is_composed_of("component", "entity")
    assert not msm.element.is_composed_of("component", "bonds")
    assert not msm.element.is_composed_of("component", "chains")


def test_group_is_composed_of():

    assert msm.element.is_composed_of("groups", "atom")
    assert not msm.element.is_composed_of("group", "group")
    assert not msm.element.is_composed_of("group", "component")
    assert not msm.element.is_composed_of("group", "molecule")
    assert not msm.element.is_composed_of("group", "entity")
    assert not msm.element.is_composed_of("group", "bonds")
    assert not msm.element.is_composed_of("group", "chains")
