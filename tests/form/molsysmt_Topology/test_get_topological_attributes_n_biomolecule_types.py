"""
Tests for the 21 biomolecule-type counting functions in
molsysmt_Topology/get_topological_attributes.py that were not covered by
test_get_topological_attributes_from_pdb.py.

All tests use the hp35 (chicken villin HP35, 1vii.pdb) topology fixture —
a pure-peptide system with 1 chain, 1 molecule, 1 entity, 1 component.
Zero-valued results (no small molecules, no DNA, etc.) still exercise the
full code path and count toward coverage.

Return-type notes
-----------------
- get_n_small_molecules_from_{component,chain,entity,molecule}   → list[int]
- get_total_n_small_molecules_from_{component,chain,entity,molecule} → int (scalar)
- get_n_{peptides,proteins,dnas,rnas,polysaccharides}_from_component → int (scalar)
- get_total_n_{peptides,proteins}_from_{chain,component}             → int (scalar)
- get_total_n_{dnas,rnas,polysaccharides}_from_component             → int (scalar)
- get_inner_bond_index_from_system                                   → list
"""

import pytest
import molsysmt as msm
from molsysmt.form.molsysmt_Topology import get_topological_attributes as aux

N_CHAINS     = 1
N_MOLECULES  = 1
N_ENTITIES   = 1
N_COMPONENTS = 1
N_BONDS      = 602


@pytest.fixture(scope="module")
def topo():
    molsys = msm.convert(msm.systems['chicken villin HP35']['1vii.pdb'], to_form='molsysmt.MolSys')
    return msm.convert(molsys, to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# get_inner_bond_index_from_system
# ---------------------------------------------------------------------------

def test_inner_bond_index_from_system_is_list(topo):
    result = aux.get_inner_bond_index_from_system(topo)
    assert isinstance(result, list)


def test_inner_bond_index_from_system_length(topo):
    result = aux.get_inner_bond_index_from_system(topo)
    assert len(result) == N_BONDS


# ---------------------------------------------------------------------------
# get_n_*_from_component  (return a scalar int for indices='all')
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name, expected", [
    ("get_n_peptides_from_component",       1),
    ("get_n_proteins_from_component",       0),
    ("get_n_dnas_from_component",           0),
    ("get_n_rnas_from_component",           0),
    ("get_n_polysaccharides_from_component", 0),
])
def test_n_biomolecule_type_from_component_scalar(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, int)
    assert result == expected


# ---------------------------------------------------------------------------
# get_total_n_*_from_component  (scalar int for indices='all')
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name, expected", [
    ("get_total_n_peptides_from_component",        1),
    ("get_total_n_proteins_from_component",        0),
    ("get_total_n_dnas_from_component",            0),
    ("get_total_n_rnas_from_component",            0),
    ("get_total_n_polysaccharides_from_component", 0),
])
def test_total_n_biomolecule_type_from_component_scalar(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, int)
    assert result == expected


# ---------------------------------------------------------------------------
# get_n_small_molecules_from_* (return a list, one entry per element)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name, n_elements", [
    ("get_n_small_molecules_from_component", N_COMPONENTS),
    ("get_n_small_molecules_from_chain",     N_CHAINS),
    ("get_n_small_molecules_from_entity",    N_ENTITIES),
    ("get_n_small_molecules_from_molecule",  N_MOLECULES),
])
def test_n_small_molecules_returns_list(topo, func_name, n_elements):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == n_elements
    assert result[0] == 0


# ---------------------------------------------------------------------------
# get_total_n_small_molecules_from_* (scalar int for indices='all')
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_total_n_small_molecules_from_component",
    "get_total_n_small_molecules_from_chain",
    "get_total_n_small_molecules_from_entity",
    "get_total_n_small_molecules_from_molecule",
])
def test_total_n_small_molecules_scalar(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, int)
    assert result == 0


# ---------------------------------------------------------------------------
# get_total_n_peptides_from_chain / get_total_n_proteins_from_chain
# (scalar int for indices='all')
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name, expected", [
    ("get_total_n_peptides_from_chain", 1),
    ("get_total_n_proteins_from_chain", 0),
])
def test_total_n_biomolecule_type_from_chain_scalar(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, int)
    assert result == expected
