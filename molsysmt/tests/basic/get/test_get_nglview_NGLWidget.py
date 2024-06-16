"""
Unit and regression test for the get module of the molsysmt package on xtc file systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np


def test_get_nglview_NGLWidget_1():
    molsys = msm.convert([msm.systems['nglview']['md_1u19.gro'], msm.systems['nglview']['md_1u19.xtc']],
                         to_form='molsysmt.MolSys')
    view = msm.convert(molsys, to_form='nglview.NGLWidget')
    check_comparison = msm.compare(molsys, view, attribute_type='topological', rule='equal')
    assert check_comparison

