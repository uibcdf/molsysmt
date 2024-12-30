"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_get_molecule_type_from_molsysmt_MolSys_1():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    types = msm.element.molecule.get_molecule_type(molsys, element='molecule', selection='all')
    assert len(types) == 1236
    assert types[0] == 'peptide'
    assert all(np.array(types[-2:])=='ion')
    assert all(np.array(types[1:-2])=='water')

def test_get_molecule_type_from_molsysmt_MolSys_2():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    types1 = msm.element.molecule.get_molecule_type(molsys, element='atom', selection='all')
    types2 = msm.element.molecule.get_molecule_type(molsys, element='atom', selection='all',
                                                  redefine_indices=True)
    types3 = msm.element.molecule.get_molecule_type(molsys, element='atom', selection='all',
                                                  redefine_types=True)
    n_peptide = sum(np.array(types1)=='peptide')
    assert all(np.array(types2[:n_peptide])=='peptide')
    assert all(np.array(types2[n_peptide:-2])=='water')
    assert all(np.array(types2[-2:])=='ion')
    assert all(np.array(types3[:n_peptide])=='peptide')
    assert all(np.array(types3[n_peptide:-2])=='water')
    assert all(np.array(types3[-2:])=='ion')

def test_get_molecule_type_from_molsysmt_MolSys_3():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    types1 = msm.element.molecule.get_molecule_type(molsys, element='group', selection='all')
    types2 = msm.element.molecule.get_molecule_type(molsys, element='group', selection='all',
                                                  redefine_indices=True)
    types3 = msm.element.molecule.get_molecule_type(molsys, element='group', selection='all',
                                                  redefine_types=True)
    n_peptide = sum(np.array(types1)=='peptide')
    assert all(np.array(types2[:n_peptide])=='peptide')
    assert all(np.array(types2[n_peptide:-2])=='water')
    assert all(np.array(types2[-2:])=='ion')
    assert all(np.array(types3[:n_peptide])=='peptide')
    assert all(np.array(types3[n_peptide:-2])=='water')
    assert all(np.array(types3[-2:])=='ion')

def test_get_molecule_type_from_molsysmt_MolSys_4():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    types1 = msm.element.molecule.get_molecule_type(molsys, element='component', selection='all')
    types2 = msm.element.molecule.get_molecule_type(molsys, element='component', selection='all',
                                                  redefine_indices=True)
    types3 = msm.element.molecule.get_molecule_type(molsys, element='component', selection='all',
                                                  redefine_types=True)
    n_peptide = sum(np.array(types1)=='peptide')
    assert all(np.array(types2[:n_peptide])=='peptide')
    assert all(np.array(types2[n_peptide:-2])=='water')
    assert all(np.array(types2[-2:])=='ion')
    assert all(np.array(types3[:n_peptide])=='peptide')
    assert all(np.array(types3[n_peptide:-2])=='water')
    assert all(np.array(types3[-2:])=='ion')

def test_get_molecule_type_from_molsysmt_MolSys_5():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    types1 = msm.element.molecule.get_molecule_type(molsys, element='molecule', selection='all')
    types2 = msm.element.molecule.get_molecule_type(molsys, element='molecule', selection='all',
                                                  redefine_indices=True)
    types3 = msm.element.molecule.get_molecule_type(molsys, element='molecule', selection='all',
                                                  redefine_types=True)
    n_peptide = sum(np.array(types1)=='peptide')
    assert all(np.array(types2[:n_peptide])=='peptide')
    assert all(np.array(types2[n_peptide:-2])=='water')
    assert all(np.array(types2[-2:])=='ion')
    assert all(np.array(types3[:n_peptide])=='peptide')
    assert all(np.array(types3[n_peptide:-2])=='water')
    assert all(np.array(types3[-2:])=='ion')

