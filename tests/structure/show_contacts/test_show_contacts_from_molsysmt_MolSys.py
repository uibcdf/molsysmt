"""
Unit and regression test for the get_contacts module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np
from unittest.mock import patch

# Distance between atoms in space and time

def test_show_contacts_from_molsysmt_MolSys_1():

    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')

    fig = msm.structure.show_contacts(molsys, selection='atom_name=="CA"', threshold='1.2 nm',
                                      style='plotly', show=False)
    
    from plotly.graph_objects import Figure
    assert isinstance(fig, Figure)

@patch("plotly.graph_objects.Figure.show")
def test_show_contacts_from_molsysmt_MolSys_2(mock_show):

    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')

    msm.structure.show_contacts(molsys, selection='atom_name=="CA"', threshold='1.2 nm',
                                style='plotly', show=True)

    mock_show.assert_called_once()

def test_show_contacts_from_molsysmt_MolSys_3():

    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')

    fig = msm.structure.show_contacts(molsys, selection='atom_name=="CA"', threshold='1.2 nm',
                                      style='matplotlib', show=False)
    
    from matplotlib.figure import Figure
    assert isinstance(fig, Figure)

@patch("matplotlib.pyplot.show")
def test_show_contacts_from_molsysmt_MolSys_4(mock_show):

    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')

    msm.structure.show_contacts(molsys, selection='atom_name=="CA"', threshold='1.2 nm',
                                style='matplotlib', show=True)
    
    mock_show.assert_called_once()


