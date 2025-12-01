"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems


def test_get_molecule_id_from_molsysmt_MolSys_1(hp35_solvated_molsys):

    molsys = hp35_solvated_molsys
    ids = msm.element.molecule.get_molecule_id(molsys, element='molecule', selection='all')
    assert ids == list([str(ii) for ii in range(1257)])

def test_get_molecule_id_from_molsysmt_MolSys_2(hp35_solvated_molsys):

    molsys = hp35_solvated_molsys
    ids = msm.element.molecule.get_molecule_id(molsys, element='molecule', selection='all',
                                               redefine_indices=True)
    assert ids == list([str(ii) for ii in range(1257)])

def test_get_molecule_id_from_molsysmt_MolSys_3(hp35_solvated_molsys):

    molsys = hp35_solvated_molsys
    ids = msm.element.molecule.get_molecule_id(molsys, element='molecule', selection='all',
                                               redefine_ids=True)
    assert ids == list([str(ii) for ii in range(1257)])
