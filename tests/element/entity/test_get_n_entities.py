"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_component_type_1(hp35_solvated_molsys):
    molsys = hp35_solvated_molsys
    n_entities_1 = msm.element.entity.get_n_entities(molsys, selection='all', redefine_entities=False)
    n_entities_2 = msm.element.entity.get_n_entities(molsys, selection='all', redefine_entities=True)
    assert 3 == n_entities_1
    assert 3 == n_entities_2

