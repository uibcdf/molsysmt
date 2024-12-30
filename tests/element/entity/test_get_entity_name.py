"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_entity_name_1():
    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    names = msm.element.entity.get_entity_name(molsys, element='entity', selection='all',
                                                redefine_entities=False, redefine_names=True)
    assert ['peptide 0', 'water', 'CL'] == names

def test_get_entity_name_2():
    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    names = msm.element.entity.get_entity_name(molsys, element='entity', selection='all',
                                                redefine_entities=False, redefine_names=False)
    assert ['VILLIN', 'water', 'CL'] == names
