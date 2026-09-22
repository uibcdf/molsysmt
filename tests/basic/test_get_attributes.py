"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed

import molsysmt as msm
from molsysmt import systems


def test_get_attributes_string_pdb():
    molsys = "181L"
    attributes = msm.get_attributes(molsys, output_type="dictionary")
    assert attributes["group_name"]
    assert attributes["entity_name"]
    assert attributes["box"]


def test_get_attributes_molsysmt_MolSys():
    molsys = msm.convert(systems["T4 lysozyme L99A"]["181l.h5msm"])
    attributes = msm.get_attributes(molsys, output_type="dictionary")
    assert attributes["group_name"]
    assert attributes["entity_name"]
    assert attributes["box"]


def test_get_attributes_openmm_Topology():
    molsys = msm.convert(
        systems["T4 lysozyme L99A"]["181l.h5msm"], to_form="openmm.Topology"
    )
    attributes = msm.get_attributes(molsys, output_type="dictionary")
    assert attributes["group_name"]
    assert not attributes["entity_name"]
    assert attributes["box"]


def test_get_attributes_string_amino_acids_1():
    molsys = msm.convert(
        systems["T4 lysozyme L99A"]["181l.h5msm"],
        to_form="string:amino_acids_1",
        selection='molecule_type=="protein"',
    )
    attributes = msm.get_attributes(molsys, output_type="dictionary")
    assert attributes["group_name"]
    assert not attributes["entity_name"]
    assert not attributes["box"]


def test_get_attributes_default_list():
    molsys = "181L"
    attributes = msm.get_attributes(molsys)
    assert isinstance(attributes, list)
    assert "group_name" in attributes
    assert "box" in attributes
