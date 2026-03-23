"""
Tests for file_fasta/get_topological_attributes.py.

Oracle: two-chain FASTA (HP35-like: 35 residues + a 7-residue tag)
- chain A: LSDEDFKAVFGMTRSAFANLPLWKQQNLKKEKGLF  (35 aa)
- chain B: MKKKKKKM  (8 aa)

Expected:
  n_chains   = 2
  n_entities = 2
  n_groups   = 43  (35 + 8)
  n_amino_acids = 43
"""

import pytest
import molsysmt as msm


FASTA_TWO_CHAINS = (
    ">chain_A HP35-like\n"
    "LSDEDFKAVFGMTRSAFANLPLWKQQNLKKEKGLF\n"
    ">chain_B short_tag\n"
    "MKKKKKKM\n"
)

CHAIN_A_LEN = 35
CHAIN_B_LEN = 8
N_CHAINS = 2
N_GROUPS = CHAIN_A_LEN + CHAIN_B_LEN


@pytest.fixture(scope="module")
def fasta_two_chains(tmp_path_factory):
    p = tmp_path_factory.mktemp("file_fasta_assets") / "two_chains.fasta"
    p.write_text(FASTA_TWO_CHAINS)
    return str(p)


def test_get_form(fasta_two_chains):
    assert msm.get_form(fasta_two_chains) == 'file:fasta'


def test_n_chains_from_system(fasta_two_chains):
    assert msm.get(fasta_two_chains, element='system', n_chains=True) == N_CHAINS


def test_n_entities_from_system(fasta_two_chains):
    assert msm.get(fasta_two_chains, element='system', n_entities=True) == N_CHAINS


def test_n_groups_from_system(fasta_two_chains):
    assert msm.get(fasta_two_chains, element='system', n_groups=True) == N_GROUPS


def test_n_amino_acids_from_system(fasta_two_chains):
    assert msm.get(fasta_two_chains, element='system', n_amino_acids=True) == N_GROUPS


def test_chain_id_from_chain(fasta_two_chains):
    ids = msm.get(fasta_two_chains, element='chain', chain_id=True)
    assert ids[0] == 'chain_A'
    assert ids[1] == 'chain_B'


def test_chain_type_from_chain(fasta_two_chains):
    types_ = msm.get(fasta_two_chains, element='chain', chain_type=True)
    assert all(t == 'protein' for t in types_)


def test_n_groups_from_chain(fasta_two_chains):
    lengths = msm.get(fasta_two_chains, element='chain', n_groups=True)
    assert lengths[0] == CHAIN_A_LEN
    assert lengths[1] == CHAIN_B_LEN


def test_group_name_from_group(fasta_two_chains):
    names = msm.get(fasta_two_chains, element='group', group_name=True)
    assert len(names) == N_GROUPS
    # L -> LEU (first residue of chain A)
    assert names[0] == 'LEU'
    # M -> MET (first residue of chain B)
    assert names[CHAIN_A_LEN] == 'MET'


def test_group_type_from_group(fasta_two_chains):
    types_ = msm.get(fasta_two_chains, element='group', group_type=True)
    assert len(types_) == N_GROUPS
    assert all(t == 'amino acid' for t in types_)
