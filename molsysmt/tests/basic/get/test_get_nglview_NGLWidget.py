"""
Unit and regression test for the get module of the molsysmt package on xtc file systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np


def test_get_nglview_NGLWidget_1():
    import warnings
    warnings.filterwarnings('ignore')
    molsys = msm.convert([msm.demo.files['nglview_demo_md_1u19.gro'], msm.demo.files['nglview_demo_md_1u19.xtc']], to_form='molsysmt.MolSys')
    view = msm.convert(molsys, to_form='nglview.NGLWidget')
    check_comparison = msm.compare(molsys, view, comparison='info_no_form', rule='A_eq_B')
    assert check_comparison

