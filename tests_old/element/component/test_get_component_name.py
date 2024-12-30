"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_component_name_1():
    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    n_waters, n_ions = msm.get(molsys, n_waters=True, n_ions=True)
    output_t_t = msm.element.component.get_component_name(molsys, element='component', selection='all',
                                                          redefine_indices=True, redefine_names=True)
    output_t_f = msm.element.component.get_component_name(molsys, element='component', selection='all',
                                                          redefine_indices=True, redefine_names=False)
    output_f_t = msm.element.component.get_component_name(molsys, element='component', selection='all',
                                                          redefine_indices=False, redefine_names=True)
    output_f_f = msm.element.component.get_component_name(molsys, element='component', selection='all',
                                                          redefine_indices=False, redefine_names=False)
    good_output = ['peptide 0'] + ['water' for ii in range(n_waters)] + ['CL' for ii in range(n_ions)]
    good_output_2 = ['VILLIN'] + ['water' for ii in range(n_waters)] + ['CL' for ii in range(n_ions)]
    assert output_t_t == good_output
    assert output_f_t == good_output
    assert output_t_f == good_output
    assert output_f_f == good_output_2

