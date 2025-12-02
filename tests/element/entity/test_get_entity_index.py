"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_component_index_1(hp35_solvated_molsys):
    molsys = hp35_solvated_molsys
    output = msm.element.entity.get_entity_index(molsys, element='entity', selection='all',
                                                 redefine_indices=True)
    assert [0,1,2]==output

def test_get_component_index_2(hp35_solvated_molsys):
    molsys = hp35_solvated_molsys
    output = msm.element.entity.get_entity_index(molsys, element='entity', selection='all',
                                                 redefine_indices=False)
    assert [0,1,2]==output


