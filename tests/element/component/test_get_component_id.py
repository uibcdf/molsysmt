"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_component_id_1(hp35_solvated_molsys):
    molsys = hp35_solvated_molsys
    output = msm.element.component.get_component_id(molsys, element='component', selection='all', redefine_indices=True,
                                                   redefine_ids=True)
    assert [str(ii) for ii in range(1257)] == output

