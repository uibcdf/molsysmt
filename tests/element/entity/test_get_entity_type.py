"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_entity_type_1():
    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    types = msm.element.entity.get_entity_type(molsys, element='entity', selection='all',
                                                redefine_entities=False, redefine_types=True)
    assert ['peptide', 'water', 'ion'] == types

def test_get_entity_type_2():
    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    types = msm.element.entity.get_entity_type(molsys, element='entity', selection='all',
                                                redefine_entities=False, redefine_types=False)
    assert ['peptide', 'water', 'ion'] == types
