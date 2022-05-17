"""
Unit and regression test for the get_bondgraph module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_get_bondgraph_molsysmt_MolSys_1():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    graph = msm.topology.get_bondgraph(molsys, selection='molecule_index==0', to_form='networkx.Graph')
    n_nodes = graph.number_of_nodes()
    n_edges = graph.number_of_edges()
    check_n_nodes = (n_nodes==3818)
    check_n_edges = (n_edges==3890)
    assert check_n_nodes and check_n_edges


