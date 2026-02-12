"""
Unit and regression test for the compare module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np
import warnings
import pytest
from molsysmt._private.smonitor import NotImplementedMethodError

def test_compare_all_eq_1(t4_h5msm_molsys):
    molsys_A = t4_h5msm_molsys
    molsys_B = t4_h5msm_molsys
    output = msm.compare(molsys_A, molsys_B, attributes_type='topological', coordinates=True, box=True)
    assert output == True

def test_compare_all_eq_2(t4_h5msm_molsys, hp35_molsys):
    molsys_A = t4_h5msm_molsys
    molsys_B = hp35_molsys
    output = msm.compare(molsys_A, molsys_B, attributes_type='topological', coordinates=True, box=True)
    assert output == False

def test_compare_attributes_type_alias_no_digest_warning(t4_h5msm_molsys):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        output = msm.compare(
            t4_h5msm_molsys,
            t4_h5msm_molsys,
            attributes_type='topological',
            coordinates=True,
            box=True,
        )

    assert output is True
    assert all("No digester for attributes_type" not in str(w.message) for w in caught)

def test_compare_rule_in_not_implemented(t4_h5msm_molsys):
    with pytest.raises(NotImplementedMethodError):
        msm.compare(t4_h5msm_molsys, t4_h5msm_molsys, rule='in')

def test_compare_all_eq_3():
    molsys_A = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'], to_form='openmm.Modeller')
    molsys_B = msm.convert(molsys_A, to_form='molsysmt.MolSys')
    comparison = msm.compare(molsys_A, molsys_B, output_type='dictionary')

    aux_comparison = {
        'atom_index':True,
        'atom_name':True,
        'atom_id':True,
        'atom_type':True,
        'group_index':True,
        'group_name':True,
        'group_id':True,
        'group_type':True,
        'component_index':True,
        'component_type':True,
        'chain_index':True,
        'chain_name':False,
        'chain_id':True,
        'chain_type':True,
        'molecule_index':True,
        'molecule_type':True,
        'bonded_atom_pairs':True,
        'n_atoms':True,
        'n_groups':True,
        'n_components':True,
        'n_chains':True,
        'n_molecules':True,
        'n_bonds':True,
    }


    assert comparison==aux_comparison

def test_compare_all_eq_4():

    molsys_A = msm.convert(systems['T4 lysozyme L99A']['181l.pdb'], to_form='openmm.Modeller')
    molsys_B = msm.convert(molsys_A, to_form='molsysmt.MolSys')
    molsys_C = msm.extract(molsys_B, selection='molecule_type=="protein"')


    aux_comparison = {
        'atom_index':True,
        'atom_name':True,
        'atom_id':True,
        'atom_type':True,
        'group_index':True,
        'group_name':True,
        'group_id':True,
        'group_type':True,
        'component_index':True,
        'component_type':True,
        'chain_index':True,
        'chain_name':False,
        'chain_id':True,
        'chain_type':True,
        'molecule_index':True,
        'molecule_type':True,
        'bonded_atom_pairs':True,
        'n_atoms':True,
        'n_groups':True,
        'n_components':True,
        'n_chains':True,
        'n_molecules':True,
        'n_bonds':True,
    }

    assert aux_comparison == msm.compare(molsys_A, molsys_B, output_type="dictionary")
    assert False == msm.compare(molsys_A, molsys_C)
    assert True == msm.compare(molsys_A, molsys_B, coordinates=True, box=True, n_groups=True)
    assert False == msm.compare(molsys_B, molsys_C, coordinates=True, box=True, n_groups=True)
    assert True == msm.compare(molsys_B, molsys_C, coordinates=False, box=True, n_groups=False)
