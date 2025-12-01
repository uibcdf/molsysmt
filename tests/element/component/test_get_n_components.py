"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_n_components_1(hp35_solvated_molsys):
    molsys = hp35_solvated_molsys
    n_components_1 = msm.element.component.get_n_components(molsys, selection='all', redefine_components=False)
    n_components_2 = msm.element.component.get_n_components(molsys, selection='all', redefine_components=True)
    assert 1257 == n_components_1
    assert 1257 == n_components_2

