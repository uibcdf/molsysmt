"""
Unit and regression test for the copy module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np
from matplotlib.pyplot import colormaps


def test_set_color_by_value_1():

    molsys = msm.systems['T4 lysozyme L99A']['181l.h5msm']

    molecular_system = msm.convert(molsys, selection='molecule_type=="protein"')

    charge_residues = msm.physchem.get_charge(molecular_system, element='group', definition='physical_pH7')

    view = msm.view(molecular_system)
    view.clear()

    blue_white_red = colormaps['bwr']
    msm.thirds.nglview.set_color_by_value(view, charge_residues, element='group', cmap=blue_white_red,
                                          representation='cartoon')

    assert view._ngl_msg_archive[-1]['reconstruc_color_scheme'] == True
    assert 'sele' in view._ngl_msg_archive[-1]['kwargs']
    assert 'color' in view._ngl_msg_archive[-1]['kwargs']
    assert len(view._ngl_msg_archive[-1]['kwargs']['color']) == 162

def test_set_color_by_value_2():

    molecular_system = msm.convert('181L', selection='molecule_type=="protein"')

    b_factors = msm.get(molecular_system, element='atom', b_factor=True)

    view = msm.view(molecular_system)
    view.clear()

    white_blue_purple = colormaps['BuPu']

    msm.thirds.nglview.set_color_by_value(view, b_factors[0], element='atom', cmap=white_blue_purple,
                                          representation='ball_and_stick', min_value=0.0,
                                          max_value=max(b_factors[0]))

    assert view._ngl_msg_archive[-1]['reconstruc_color_scheme'] == True
    assert 'sele' in view._ngl_msg_archive[-1]['kwargs']
    assert 'color' in view._ngl_msg_archive[-1]['kwargs']
    assert len(view._ngl_msg_archive[-1]['kwargs']['color']) == len(b_factors[0])

