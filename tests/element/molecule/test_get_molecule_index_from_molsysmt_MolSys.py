"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems


def test_get_molecule_index_from_molsysmt_MolSys_1(hp35_solvated_molsys):

    molsys = hp35_solvated_molsys
    indices = msm.element.molecule.get_molecule_index(molsys, element='molecule', selection='all')
    assert indices == list(range(1257))

def test_get_molecule_index_from_molsysmt_MolSys_2(hp35_solvated_molsys):

    molsys = hp35_solvated_molsys
    indices1 = msm.element.molecule.get_molecule_index(molsys, element='atom', selection='all',
                                                  redefine_indices=True)
    indices2 = msm.element.molecule.get_molecule_index(molsys, element='atom', selection='all',
                                                  redefine_indices=True)
    assert len(indices1)==4369
    assert indices1==indices2

def test_get_molecule_index_from_molsysmt_MolSys_3(hp35_solvated_molsys):

    molsys = hp35_solvated_molsys
    indices1 = msm.element.molecule.get_molecule_index(molsys, element='group', selection='all',
                                                  redefine_indices=True)
    assert len(indices1)==1294

def test_get_molecule_index_from_molsysmt_MolSys_4(hp35_solvated_molsys):

    molsys = hp35_solvated_molsys
    indices1 = msm.element.molecule.get_molecule_index(molsys, element='component', selection='all',
                                                  redefine_indices=True)
    assert len(indices1)==1257

def test_get_molecule_index_from_molsysmt_MolSys_5(hp35_solvated_molsys):

    molsys = hp35_solvated_molsys
    indices1 = msm.element.molecule.get_molecule_index(molsys, element='molecule', selection='all',
                                                  redefine_indices=True)
    assert len(indices1)==1257

def test_get_molecule_index_from_molsysmt_MolSys_6(hp35_solvated_molsys):

    molsys = hp35_solvated_molsys
    indices1 = msm.element.molecule.get_molecule_index(molsys, element='entity', selection='all',
                                                  redefine_indices=True)
    assert len(indices1)==3

