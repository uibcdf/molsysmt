"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed

import molsysmt as msm


def test_group_names():

    assert type(msm.element.group.ion.group_names) is list
    assert "K" in msm.element.group.ion.group_names
    assert "CL" in msm.element.group.ion.group_names
    assert "NA" in msm.element.group.ion.group_names
