"""
Unit and regression test for the add_terminal_cappings of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np
import os


def test_solve_atoms_with_alternate_location_molsysmt_MolSys_1():

    alt_loc = msm.get('1BRS', alternate_location=True)
    assert np.all(list(alt_loc[0].keys())==[2686,2687])

    alt_loc_1 = alt_loc[0][2686]
    assert np.all(alt_loc_1['location_id']==np.array(['A','B']))
    assert np.all(alt_loc_1['occupancy']==np.array([0.5,0.5]))
    assert np.all(alt_loc_1['atom_id']==np.array([2687,2688]))
    aux_coors = puw.quantity(np.array([[3.2742, 2.2579, 0.1536], [3.2757, 2.2571, 0.1533]]),'nm')
    assert puw.are_close(alt_loc_1['coordinates'], aux_coors)
    aux_b_factor = puw.quantity(np.array([0.2466, 0.2467]),'nm**2')
    assert puw.are_close(alt_loc_1['b_factor'], aux_b_factor)

    alt_loc_2 = alt_loc[0][2687]
    assert np.all(alt_loc_2['location_id']==np.array(['A','B']))
    assert np.all(alt_loc_2['occupancy']==np.array([0.5,0.5]))
    assert np.all(alt_loc_2['atom_id']==np.array([2689,2690]))
    aux_coors = puw.quantity(np.array([[3.1412, 2.241 , 0.1076], [3.3396, 2.192 , 0.2619]]),'nm')
    assert puw.are_close(alt_loc_2['coordinates'], aux_coors)
    aux_b_factor = puw.quantity(np.array([0.2594, 0.2596]),'nm**2')
    assert puw.are_close(alt_loc_2['b_factor'], aux_b_factor)

def test_solve_atoms_with_alternate_location_molsysmt_MolSys_2():

    molecular_system = msm.convert(systems['Barnase-Barstar']['1brs.bcif'], to_form='molsysmt.MolSys')
    msm.build.solve_atoms_with_alternate_location(molecular_system, location_id='B')
    atom_id, b_factor, coordinates = msm.get(molecular_system, element='atom', selection=[2686,2687],
            atom_id=True, b_factor=True, coordinates=True)
    assert np.all(atom_id==np.array([2688,2690]))
    aux_coors = puw.quantity(np.array([[[3.2757, 2.2571, 0.1533], [3.3396, 2.192 , 0.2619]]]),'nm')
    assert puw.are_close(coordinates, aux_coors)

def test_solve_atoms_with_alternate_location_molsysmt_MolSys_3():

    molecular_system = msm.convert(systems['Barnase-Barstar']['1brs.bcif'], to_form='molsysmt.MolSys')
    msm.build.solve_atoms_with_alternate_location(molecular_system, selection=[2686,2687], location_id=['A','B'])
    atom_id, b_factor, coordinates = msm.get(molecular_system, element='atom', selection=[2686,2687],
            atom_id=True, b_factor=True, coordinates=True)
    assert np.all(atom_id==np.array([2687,2690]))
    aux_coors = puw.quantity(np.array([[[3.2742, 2.2579, 0.1536], [3.3396, 2.192 , 0.2619]]]),'nm')
    assert puw.are_close(coordinates, aux_coors)

def test_solve_atoms_with_alternate_location_molsysmt_MolSys_4():

    molecular_system = msm.convert(systems['Barnase-Barstar']['1brs.bcif'], to_form='molsysmt.MolSys')
    msm.build.solve_atoms_with_alternate_location(molecular_system, selection=[2686,2687], location_id='occupancy')
    atom_id, b_factor, coordinates = msm.get(molecular_system, element='atom', selection=[2686,2687],
            atom_id=True, b_factor=True, coordinates=True)
    assert np.all(atom_id==np.array([2687,2689]))
    aux_coors = puw.quantity(np.array([[[3.2742, 2.2579, 0.1536], [3.1412, 2.241 , 0.1076]]]),'nm')
    assert puw.are_close(coordinates, aux_coors)

def test_solve_atoms_with_alternate_location_molsysmt_MolSys_5():

    molecular_system = msm.convert(systems['Barnase-Barstar']['1brs.bcif'], to_form='molsysmt.MolSys')
    molecular_system.structures.alternate_location[0][2686]['occupancy'][:]=[0.4,0.6]
    molecular_system.structures.alternate_location[0][2687]['occupancy'][:]=[0.4,0.6]
    msm.build.solve_atoms_with_alternate_location(molecular_system, selection=[2686,2687], location_id='occupancy')
    atom_id, b_factor, coordinates = msm.get(molecular_system, element='atom', selection=[2686,2687],
            atom_id=True, b_factor=True, coordinates=True)
    assert np.all(atom_id==np.array([2688,2690]))
    aux_coors = puw.quantity(np.array([[[3.2757, 2.2571, 0.1533], [3.3396, 2.192 , 0.2619]]]),'nm')
    assert puw.are_close(coordinates, aux_coors)




