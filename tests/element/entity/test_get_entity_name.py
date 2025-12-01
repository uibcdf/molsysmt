"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_entity_name_1(hp35_solvated_molsys):
    molsys = hp35_solvated_molsys
    names = msm.element.entity.get_entity_name(molsys, element='entity', selection='all',
                                               redefine_indices=False, redefine_names=True)
    assert ['peptide 0', 'water', 'CL'] == names

def test_get_entity_name_2(hp35_solvated_molsys):
    molsys = hp35_solvated_molsys
    names = msm.element.entity.get_entity_name(molsys, element='entity', selection='all',
                                               redefine_indices=False, redefine_names=False)
    assert ['peptide 0', 'water', 'CL'] == names
