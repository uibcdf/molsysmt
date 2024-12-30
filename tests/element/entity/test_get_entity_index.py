"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_component_index_1():
    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    output = msm.element.entity.get_entity_index(molsys, element='entity', selection='all',
                                                       redefine_molecules=False, redefine_indices=True)
    assert [0,1,2]==output

def test_get_component_index_2():
    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    output = msm.element.entity.get_entity_index(molsys, element='entity', selection='all',
                                                       redefine_molecules=False, redefine_indices=False)
    assert [0,1,2]==output


