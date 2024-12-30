"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_get_group_type_from_molsysmt_MolSys_1():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    types = msm.element.group.get_group_type(molsys, element='group', selection='all')
    assert len(types) == 1273
    assert types[0] == 'terminal capping'
    assert all(np.array(types[1:37])=='amino acid')
    assert types[37] == 'terminal capping'
    assert all(np.array(types[38:-2])=='water')
    assert all(np.array(types[-2:])=='ion')

def test_get_group_type_from_molsysmt_MolSys_2():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    types = msm.element.group.get_group_type(molsys, element='atom', selection='all', redefine_types=True)

    assert all(np.array(types[:6])=='terminal capping')
    assert all(np.array(types[6:599])=='amino acid')
    assert all(np.array(types[599:605])=='terminal capping')
    assert all(np.array(types[605:4304])=='water')
    assert all(np.array(types[-2:])=='ion')

def test_get_group_type_from_molsysmt_MolSys_3():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    types = msm.element.group.get_group_type(molsys, element='group', selection='all')
    types2 = msm.element.group.get_group_type(molsys, element='group', selection='all', redefine_types=True)

    assert types==types2

