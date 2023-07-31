"""
Unit and regression test for the get_contacts module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
from molsysmt import pyunitwizard as puw
import numpy as np

# Distance between atoms in space and time

def test_get_contacts_from_molsysmt_MolSys_1():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    CA_atoms = msm.select(molsys, selection='atom_name=="CA"')
    contact_map = msm.structure.get_contacts(molsys, selection=CA_atoms, threshold='1.2 nm')
    check_shape_1 = ((1, 497, 497)==contact_map.shape)
    check_value_1 = (False==contact_map[0,100,120])
    check_value_2 = (True==contact_map[0,200,0])
    check_value_3 = (True==contact_map[0,490,493])
    assert check_shape_1 and check_value_1 and check_value_2 and check_value_3

def test_get_contacts_from_molsysmt_MolSys_2():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    CA_atoms_chain_0 = msm.get(molsys, element='atom', selection="atom_name=='CA' and chain_index==0", atom_index=True)
    CA_atoms_chain_1 = msm.get(molsys, element='atom', selection="atom_name=='CA' and chain_index==1", atom_index=True)
    contact_map = msm.structure.get_contacts(molsys, selection=CA_atoms_chain_0, selection_2=CA_atoms_chain_1,
                              threshold=1.2*puw.unit('nm'))
    check_shape_1 = ((1, 248, 249)==contact_map.shape)
    check_value_1 = np.all(np.array([False, False, False, False,  True, False, False,  True, False, False])==contact_map[0,48,40:50])
    assert check_shape_1 and check_value_1

def test_get_contacts_from_molsysmt_MolSys_3():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    atoms_in_residues_chain_0 = msm.get(molsys, element='group',
                                        selection="molecule_type=='protein' and chain_index==0", atom_index=True)
    atoms_in_residues_chain_1 = msm.get(molsys, element='group',
                                        selection="molecule_type=='protein' and chain_index==1", atom_index=True)
    contact_map = msm.structure.get_contacts(molsys,
                              selection=atoms_in_residues_chain_0,
                              selection_2=atoms_in_residues_chain_1,
                              threshold=1.2*puw.unit('nm'))
    check_shape_1 = ((1, 248, 249)==contact_map.shape)
    check_value_1 = np.all(np.array([False, False, False, False,  True, False, False,  True, False, False])==contact_map[0,48,40:50])
    assert check_shape_1 and check_value_1

