"""
Unit and regression test for the box_shape_from_box module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time


def test_box_shape_from_box_cubic_geometry():
    molsys = msm.convert(msm.demo['Met-enkephalin']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.build.solvate(molsys, box_geometry='cubic', clearance='14.0 angstroms', engine='PDBFixer')
    box = msm.get(molsys, element='system', box=True)
    shape = msm.pbc.box_shape_from_box(box)
    assert (shape == 'cubic')


def test_box_shape_from_box_octahedral_geometry():
    molsys = msm.convert(msm.demo['Met-enkephalin']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.build.solvate(molsys, box_geometry='truncated octahedral', clearance='14.0 angstroms', engine='PDBFixer')
    box = msm.get(molsys, element='system', box=True)
    shape = msm.pbc.box_shape_from_box(box)
    assert (shape == 'truncated octahedral')


def test_box_shape_from_box_dodecahedral_geometry():
    molsys = msm.convert(msm.demo['Met-enkephalin']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.build.solvate(molsys, box_geometry='rhombic dodecahedral', clearance='14.0 angstroms', engine='PDBFixer')
    box = msm.get(molsys, element='system', box=True)
    shape = msm.pbc.box_shape_from_box(box)
    assert (shape == 'rhombic dodecahedral')

