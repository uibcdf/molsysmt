"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems


def test_get_molecule_id_from_molsysmt_MolSys_1():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    ids = msm.element.molecule.get_molecule_id(molsys, element='molecule', selection='all')
    assert ids == list(range(1236))

def test_get_molecule_id_from_molsysmt_MolSys_2():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    ids = msm.element.molecule.get_molecule_id(molsys, element='molecule', selection='all',
                                               redefine_molecules=True)
    assert ids == list(range(1236))

def test_get_molecule_id_from_molsysmt_MolSys_3():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    ids = msm.element.molecule.get_molecule_id(molsys, element='molecule', selection='all',
                                               redefine_ids=True)
    assert ids == list(range(1236))
