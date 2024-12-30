"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems


def test_get_molecule_index_from_molsysmt_MolSys_1():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    indices = msm.element.molecule.get_molecule_index(molsys, element='molecule', selection='all')
    assert indices == list(range(1236))

def test_get_molecule_index_from_molsysmt_MolSys_2():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    indices1 = msm.element.molecule.get_molecule_index(molsys, element='atom', selection='all',
                                                  redefine_indices=True)
    indices2 = msm.element.molecule.get_molecule_index(molsys, element='atom', selection='all',
                                                  redefine_indices=True, redefine_componets=True)
    assert len(indices1)==4306
    assert indices1==indices2

def test_get_molecule_index_from_molsysmt_MolSys_3():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    indices1 = msm.element.molecule.get_molecule_index(molsys, element='group', selection='all',
                                                  redefine_indices=True)
    indices2 = msm.element.molecule.get_molecule_index(molsys, element='group', selection='all',
                                                  redefine_indices=True, redefine_componets=True)
    assert len(indices1)==1273
    assert indices1==indices2

def test_get_molecule_index_from_molsysmt_MolSys_4():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    indices1 = msm.element.molecule.get_molecule_index(molsys, element='component', selection='all',
                                                  redefine_indices=True)
    indices2 = msm.element.molecule.get_molecule_index(molsys, element='component', selection='all',
                                                  redefine_indices=True, redefine_componets=True)
    assert len(indices1)==1236
    assert indices1==indices2

def test_get_molecule_index_from_molsysmt_MolSys_5():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    indices1 = msm.element.molecule.get_molecule_index(molsys, element='molecule', selection='all',
                                                  redefine_indices=True)
    indices2 = msm.element.molecule.get_molecule_index(molsys, element='molecule', selection='all',
                                                  redefine_indices=True, redefine_componets=True)
    assert len(indices1)==1236
    assert indices1==indices2

def test_get_molecule_index_from_molsysmt_MolSys_6():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    indices1 = msm.element.molecule.get_molecule_index(molsys, element='entity', selection='all',
                                                  redefine_indices=True)
    assert len(indices1)==3

