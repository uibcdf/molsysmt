"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_chain_type_1():
    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    output = msm.element.chain.get_chain_type(molsys, element='chain', selection='all', redefine_types=True)
    assert ['peptide', 'ions + water'] == output


def test_get_chain_type_2():
    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    msm.build.define_new_chain(molsys, selection='all', chain_id=0, chain_name='A')
    output = msm.element.chain.get_chain_type(molsys, element='chain', selection='all', redefine_types=True)
    assert ['system'] == output
