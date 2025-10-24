"""
"""

import molsysmt as msm
from molsysmt import systems
import numpy as np

topology = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.Topology')

def test_get_atom_indices_1():
    output = topology.get_atom_indices(atom_name='CA', group_name='ALA', group_id=[30,31,32])
    assert output == [204, 209, 2116, 2121]

def test_get_atom_indices_2():
    output = topology.get_atom_indices(atom_id=[100,101], molecule_type="protein", entity_index=0)
    assert output == [99, 100]

def test_get_atom_indices_3():
    output = topology.get_atom_indices(atom_id=[100,101], chain_index=0, entity_index=1)
    assert len(output) == 0
