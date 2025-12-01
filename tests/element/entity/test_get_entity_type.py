"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_entity_type_1(hp35_solvated_molsys):
    molsys = hp35_solvated_molsys
    types = msm.element.entity.get_entity_type(molsys, element='entity', selection='all',
                                                redefine_indices=False, redefine_types=True)
    assert ['peptide', 'water', 'ion'] == types

def test_get_entity_type_2(hp35_solvated_molsys):
    molsys = hp35_solvated_molsys
    types = msm.element.entity.get_entity_type(molsys, element='entity', selection='all',
                                                redefine_indices=False, redefine_types=False)
    assert ['peptide', 'water', 'ion'] == types
