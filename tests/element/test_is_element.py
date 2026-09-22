"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_is_element():
    assert msm.element.is_element("atom")
    assert msm.element.is_element("group")
    assert msm.element.is_element("component")
    assert msm.element.is_element("molecule")
    assert msm.element.is_element("chain")
    assert msm.element.is_element("entity")
    assert msm.element.is_element("bond")
    assert msm.element.is_element("system")


def test_is_element_with_plurals():
    assert msm.element.is_element("atoms")
    assert msm.element.is_element("groups")
    assert msm.element.is_element("components")
    assert msm.element.is_element("molecules")
    assert msm.element.is_element("chains")
    assert msm.element.is_element("entities")
    assert msm.element.is_element("bonds")


def test_is_not_element():
    assert not msm.element.is_element("systems")
    assert not msm.element.is_element("zzz")
