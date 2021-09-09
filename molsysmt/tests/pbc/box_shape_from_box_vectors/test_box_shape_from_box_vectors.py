"""
Unit and regression test for the box_shape_from_box_vectors module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_box_shape_from_box_vectors_1():
    molsys = msm.demo.classes.metenkephalin()
    molsys = msm.build.solvate(molsys, box_geometry='cubic', clearance='14.0 angstroms', engine='PDBFixer')
    box = msm.get(molsys, target='system', box=True)
    shape = msm.pbc.box_shape_from_box_vectors(box)
    assert (shape == 'cubic')

def test_box_shape_from_box_vectors_2():
    molsys = msm.demo.classes.metenkephalin()
    molsys = msm.build.solvate(molsys, box_geometry='truncated octahedral', clearance='14.0 angstroms', engine='PDBFixer')
    box = msm.get(molsys, target='system', box=True)
    shape = msm.pbc.box_shape_from_box_vectors(box)
    assert (shape == 'truncated octahedral')

def test_box_shape_from_box_vectors_3():
    molsys = msm.demo.classes.metenkephalin()
    molsys = msm.build.solvate(molsys, box_geometry='rhombic dodecahedral', clearance='14.0 angstroms', engine='PDBFixer')
    box = msm.get(molsys, target='system', box=True)
    shape = msm.pbc.box_shape_from_box_vectors(box)
    assert (shape == 'rhombic dodecahedral')

