"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_get_molecule_name_from_molsysmt_MolSys_1(hp35_solvated_molsys):

    molsys = hp35_solvated_molsys
    names = msm.element.molecule.get_molecule_name(molsys, element='molecule', selection='all')
    assert len(names) == 1257
    assert names[0] == 'VILLIN'
    assert all(np.array(names[-2:])=='CL')
    assert all(np.array(names[1:-2])=='water')

def test_get_molecule_name_from_molsysmt_MolSys_2(hp35_solvated_molsys):

    molsys = hp35_solvated_molsys
    names1 = msm.element.molecule.get_molecule_name(molsys, element='atom', selection='all')
    names2 = msm.element.molecule.get_molecule_name(molsys, element='atom', selection='all',
                                                  redefine_indices=True, redefine_names=True)
    n_VILLIN = sum(np.array(names1)=='VILLIN')
    assert all(np.array(names2[:n_VILLIN])=='peptide 0')
    assert all(np.array(names2[n_VILLIN:-2])=='water')
    assert all(np.array(names2[-2:])=='CL')

def test_get_molecule_name_from_molsysmt_MolSys_3(hp35_solvated_molsys):

    molsys = hp35_solvated_molsys
    names1 = msm.element.molecule.get_molecule_name(molsys, element='group', selection='all')
    names2 = msm.element.molecule.get_molecule_name(molsys, element='group', selection='all',
                                                  redefine_indices=True, redefine_names=True)
    n_VILLIN = sum(np.array(names1)=='VILLIN')
    assert all(np.array(names2[:n_VILLIN])=='peptide 0')
    assert all(np.array(names2[n_VILLIN:-2])=='water')
    assert all(np.array(names2[-2:])=='CL')

def test_get_molecule_name_from_molsysmt_MolSys_4(hp35_solvated_molsys):

    molsys = hp35_solvated_molsys
    names1 = msm.element.molecule.get_molecule_name(molsys, element='component', selection='all')
    names2 = msm.element.molecule.get_molecule_name(molsys, element='component', selection='all',
                                                  redefine_indices=True, redefine_names=True)
    n_VILLIN = sum(np.array(names1)=='VILLIN')
    assert all(np.array(names2[:n_VILLIN])=='peptide 0')
    assert all(np.array(names2[n_VILLIN:-2])=='water')
    assert all(np.array(names2[-2:])=='CL')

def test_get_molecule_name_from_molsysmt_MolSys_5(hp35_solvated_molsys):

    molsys = hp35_solvated_molsys
    names1 = msm.element.molecule.get_molecule_name(molsys, element='molecule', selection='all')
    names2 = msm.element.molecule.get_molecule_name(molsys, element='molecule', selection='all',
                                                  redefine_indices=True, redefine_names=True)
    n_VILLIN = sum(np.array(names1)=='VILLIN')
    assert all(np.array(names2[:n_VILLIN])=='peptide 0')
    assert all(np.array(names2[n_VILLIN:-2])=='water')
    assert all(np.array(names2[-2:])=='CL')


