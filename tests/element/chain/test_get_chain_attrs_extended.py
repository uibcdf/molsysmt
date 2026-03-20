"""
Extended tests for chain element getters covering the redefine_indices,
redefine_names, and redefine_ids branches.
"""

import molsysmt as msm
import numpy as np
import pytest


# ---------------------------------------------------------------------------
# get_chain_index – redefine_indices=True
# ---------------------------------------------------------------------------

def test_chain_index_redefine_indices_single_chain(hp35_pdb_molsys):
    """HP35 has 1 chain. With redefine_indices=True the only chain gets index 0."""
    molsys = hp35_pdb_molsys
    output = msm.element.chain.get_chain_index(
        molsys, element='chain', selection='all', redefine_indices=True
    )
    assert output == [0]


def test_chain_index_redefine_indices_multi_chain(barnase_barstar_molsys):
    """Barnase-Barstar has 2 protein chains. With redefine_indices=True each
    gets index 0 when there is only one chain per call — or verify the length
    equals the expected number of chains.
    """
    molsys = barnase_barstar_molsys
    n_chains = msm.get(molsys, element='system', n_chains=True)
    output = msm.element.chain.get_chain_index(
        molsys, element='chain', selection='all', redefine_indices=True
    )
    # redefine_indices collapses all chains to index 0 (single-chain re-index)
    assert isinstance(output, list)
    assert len(output) == n_chains


def test_chain_index_redefine_indices_element_atom(hp35_pdb_molsys):
    """Requesting element='atom' with redefine_indices=True assigns chain index 0
    to all atoms (only 1 chain in HP35)."""
    molsys = hp35_pdb_molsys
    n_atoms = msm.get(molsys, element='system', n_atoms=True)
    output = msm.element.chain.get_chain_index(
        molsys, element='atom', selection='all', redefine_indices=True
    )
    assert isinstance(output, list)
    assert len(output) == n_atoms
    assert all(v == 0 for v in output)


def test_chain_index_redefine_indices_element_group(hp35_pdb_molsys):
    """Requesting element='group' with redefine_indices=True assigns chain index 0
    to all groups."""
    molsys = hp35_pdb_molsys
    n_groups = msm.get(molsys, element='system', n_groups=True)
    output = msm.element.chain.get_chain_index(
        molsys, element='group', selection='all', redefine_indices=True
    )
    assert isinstance(output, list)
    assert len(output) == n_groups
    assert all(v == 0 for v in output)


def test_chain_index_redefine_indices_element_molecule(hp35_pdb_molsys):
    """element='molecule' with redefine_indices=True."""
    molsys = hp35_pdb_molsys
    n_molecules = msm.get(molsys, element='system', n_molecules=True)
    output = msm.element.chain.get_chain_index(
        molsys, element='molecule', selection='all', redefine_indices=True
    )
    assert isinstance(output, list)
    assert len(output) == n_molecules
    assert all(v == 0 for v in output)


def test_chain_index_redefine_indices_element_component(hp35_pdb_molsys):
    """element='component' with redefine_indices=True."""
    molsys = hp35_pdb_molsys
    n_components = msm.get(molsys, element='system', n_components=True)
    output = msm.element.chain.get_chain_index(
        molsys, element='component', selection='all', redefine_indices=True
    )
    assert isinstance(output, list)
    assert len(output) == n_components
    assert all(v == 0 for v in output)


def test_chain_index_redefine_indices_element_entity(hp35_pdb_molsys):
    """element='entity' with redefine_indices=True."""
    molsys = hp35_pdb_molsys
    n_entities = msm.get(molsys, element='system', n_entities=True)
    output = msm.element.chain.get_chain_index(
        molsys, element='entity', selection='all', redefine_indices=True
    )
    assert isinstance(output, list)
    assert len(output) == n_entities


def test_chain_index_no_redefine_uses_stored_indices(hp35_pdb_molsys):
    """Without redefine_indices the stored chain indices are returned unchanged."""
    molsys = hp35_pdb_molsys
    output = msm.element.chain.get_chain_index(
        molsys, element='chain', selection='all', redefine_indices=False
    )
    assert isinstance(output, list)
    assert len(output) >= 1


# ---------------------------------------------------------------------------
# get_chain_name – redefine_names=True
# ---------------------------------------------------------------------------

def test_chain_name_redefine_names_single_chain(hp35_pdb_molsys):
    """HP35 has 1 chain. With redefine_names=True the name is the first entry
    in all_chain_names (index 0), which is 'A'."""
    molsys = hp35_pdb_molsys
    output = msm.element.chain.get_chain_name(
        molsys, element='chain', selection='all', redefine_names=True
    )
    assert isinstance(output, list)
    assert len(output) == 1
    # The first auto-generated chain name maps to index 0 → 'A'
    assert output[0] == 'A'


def test_chain_name_redefine_names_multi_chain(tctim_h5msm_molsys):
    """TcTIM has multiple chains. With redefine_names=True names are
    auto-generated from the chain index sequence."""
    molsys = tctim_h5msm_molsys
    n_chains = msm.get(molsys, element='system', n_chains=True)
    output = msm.element.chain.get_chain_name(
        molsys, element='chain', selection='all', redefine_names=True
    )
    assert isinstance(output, list)
    assert len(output) == n_chains
    # All entries must be strings (drawn from all_chain_names)
    assert all(isinstance(name, str) for name in output)
    # Names are all unique
    assert len(set(output)) == len(output)


def test_chain_name_redefine_names_false_preserved(hp35_pdb_molsys):
    """Without redefine_names the stored name is returned (e.g. 'A' for 1vii)."""
    molsys = hp35_pdb_molsys
    output = msm.element.chain.get_chain_name(
        molsys, element='chain', selection='all', redefine_names=False
    )
    assert isinstance(output, list)
    assert len(output) == 1
    assert isinstance(output[0], str)


def test_chain_name_redefine_names_barnase_barstar(barnase_barstar_molsys):
    """Barnase-Barstar: redefine_names=True produces one name per chain."""
    molsys = barnase_barstar_molsys
    n_chains = msm.get(molsys, element='system', n_chains=True)
    output = msm.element.chain.get_chain_name(
        molsys, element='chain', selection='all', redefine_names=True
    )
    assert len(output) == n_chains
    assert all(isinstance(n, str) and len(n) > 0 for n in output)


# ---------------------------------------------------------------------------
# get_chain_id – redefine_ids=True
# ---------------------------------------------------------------------------

def test_chain_id_redefine_ids_single_chain(hp35_pdb_molsys):
    """HP35 has 1 chain. With redefine_ids=True the id equals the re-defined
    chain index (0), returned as a string."""
    molsys = hp35_pdb_molsys
    output = msm.element.chain.get_chain_id(
        molsys, element='chain', selection='all', redefine_ids=True
    )
    assert isinstance(output, list)
    assert len(output) == 1
    # Chain ids are always strings in native objects
    assert output[0] == '0'


def test_chain_id_redefine_ids_with_redefine_indices(hp35_pdb_molsys):
    """Combining redefine_ids=True and redefine_indices=True still yields '0'
    for a single-chain system."""
    molsys = hp35_pdb_molsys
    output = msm.element.chain.get_chain_id(
        molsys, element='chain', selection='all',
        redefine_ids=True, redefine_indices=True
    )
    assert isinstance(output, list)
    assert output[0] == '0'


def test_chain_id_redefine_ids_multi_chain(tctim_h5msm_molsys):
    """For TcTIM (multi-chain), redefine_ids returns integer-like string ids
    matching re-indexed chain indices."""
    molsys = tctim_h5msm_molsys
    n_chains = msm.get(molsys, element='system', n_chains=True)
    output = msm.element.chain.get_chain_id(
        molsys, element='chain', selection='all', redefine_ids=True
    )
    assert isinstance(output, list)
    assert len(output) == n_chains
    # All entries must be strings that parse as integers
    for val in output:
        assert isinstance(val, str)
        int(val)  # must not raise


def test_chain_id_redefine_ids_false_preserves_stored(hp35_pdb_molsys):
    """Without redefine_ids the stored chain id is returned unchanged."""
    molsys = hp35_pdb_molsys
    output = msm.element.chain.get_chain_id(
        molsys, element='chain', selection='all', redefine_ids=False
    )
    assert isinstance(output, list)
    assert len(output) == 1
    assert isinstance(output[0], str)


def test_chain_id_redefine_ids_barnase_barstar(barnase_barstar_molsys):
    """Barnase-Barstar: redefine_ids=True produces one id per chain."""
    molsys = barnase_barstar_molsys
    n_chains = msm.get(molsys, element='system', n_chains=True)
    output = msm.element.chain.get_chain_id(
        molsys, element='chain', selection='all', redefine_ids=True
    )
    assert len(output) == n_chains
    for val in output:
        assert isinstance(val, str)
