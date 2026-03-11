"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_get_chain_type_1(hp35_solvated_molsys):
    molsys = hp35_solvated_molsys
    output = msm.element.chain.get_chain_type(molsys, element='chain', selection='all', redefine_types=True)
    assert ['peptide', 'ions + water'] == output


def test_get_chain_type_2(hp35_solvated_molsys):
    molsys = hp35_solvated_molsys
    molsys.topology.reset_chains(n_chains=1)
    msm.set(molsys, element='atom', selection='all', chain_index=[0], skip_digestion=True)
    msm.set(molsys, element='chain', selection='all', chain_id=['0'], chain_name=['A'], skip_digestion=True)
    molsys.topology.rebuild_chains(redefine_indices=False, redefine_ids=False, redefine_types=True, redefine_names=False)
    output = msm.element.chain.get_chain_type(molsys, element='chain', selection='all', redefine_types=True)
    assert ['system'] == output
