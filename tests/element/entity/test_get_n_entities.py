"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_component_type_1():
    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    n_entities_1 = msm.element.entity.get_n_entities(molsys, selection='all', redefine_entities=False)
    n_entities_2 = msm.element.entity.get_n_entities(molsys, selection='all', redefine_entities=True)
    assert 3 == n_entities_1
    assert 3 == n_entities_2

