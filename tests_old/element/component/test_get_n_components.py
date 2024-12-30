"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_component_type_1():
    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    n_components_1 = msm.element.component.get_n_components(molsys, selection='all', redefine_components=False)
    n_components_2 = msm.element.component.get_n_components(molsys, selection='all', redefine_components=True)
    assert 1236 == n_components_1
    assert 1236 == n_components_2

