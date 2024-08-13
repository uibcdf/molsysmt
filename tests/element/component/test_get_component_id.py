"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_component_id_1():
    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    output = msm.element.component.get_component_id(molsys, element='component', selection='all', redefine_components=True,
                                                   redefine_ids=True)
    assert [ii for ii in range(1350)] == output

