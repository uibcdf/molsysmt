"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_component_index_1(hp35_solvated_molsys):
    molsys = hp35_solvated_molsys
    output = msm.element.component.get_component_index(molsys, element='group', selection='all',
                                                       redefine_indices=True)
    assert [0 for ii in range(38)] + [1,2] == output[:40]

def test_get_component_index_2(hp35_solvated_molsys):
    molsys = hp35_solvated_molsys
    output = msm.element.component.get_component_index(molsys, element='component', selection='all',
                                                       redefine_indices=True)
    assert [ii for ii in range(1257)] == output

