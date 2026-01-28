"""
Unit and regression test for the view module of the molsysmt package on molsysmt.MolSys with MolSysViewer.
"""

import molsysmt as msm


def test_view_molsysmt_MolSys_with_MolSysViewer_form(alanine_molsys):

    view = msm.view(alanine_molsys)
    assert msm.get_form(view) == 'molsysviewer.MolSysView'


def test_view_molsysmt_MolSys_with_MolSysViewer_compare(alanine_molsys):

    view = msm.view(alanine_molsys)
    assert msm.compare(view, alanine_molsys, coordinates=True, box=True)
