"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_component_type_1():
    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    n_waters, n_ions = msm.get(molsys, n_waters=True, n_ions=True)
    output_t_t = msm.element.component.get_component_type(molsys, element='component', selection='all',
                                                          redefine_indices=True, redefine_types=True)
    output_t_f = msm.element.component.get_component_type(molsys, element='component', selection='all',
                                                          redefine_indices=True, redefine_types=False)
    output_f_t = msm.element.component.get_component_type(molsys, element='component', selection='all',
                                                          redefine_indices=False, redefine_types=True)
    output_f_f = msm.element.component.get_component_type(molsys, element='component', selection='all',
                                                          redefine_indices=False, redefine_types=False)
    good_output = ['peptide'] + ['water' for ii in range(n_waters)] + ['ion' for ii in range(n_ions)]
    assert output_t_t == good_output
    assert output_f_t == good_output
    assert output_t_f == good_output
    assert output_f_f == good_output

