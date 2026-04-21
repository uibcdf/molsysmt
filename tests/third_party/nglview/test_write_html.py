"""
Unit and regression test for the copy module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np
import os

def test_write_html_1():

    molsys = msm.basic.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], selection='molecule_type=="protein"')
    nglview_htmlfile = 'test.html'
    view = msm.basic.view(molsys, viewer='NGLView')
    view.show()
    msm.thirds.nglview.write_html(view, nglview_htmlfile)

    html_file_exists = os.path.isfile(nglview_htmlfile)
    if html_file_exists:
        os.remove(nglview_htmlfile)

    assert html_file_exists
