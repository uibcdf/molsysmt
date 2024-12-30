"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_entity_id_1():
    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    ids = msm.element.entity.get_entity_id(molsys, element='entity', selection='all', redefine_entities=True,
                                      redefine_ids=True)
    assert [0,1,2]==ids

def test_get_entity_id_1():
    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    ids = msm.element.entity.get_entity_id(molsys, element='entity', selection='all', redefine_entities=False,
                                      redefine_ids=False)
    assert [0,1,2]==ids
