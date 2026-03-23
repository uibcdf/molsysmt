"""
Tests for file_pir/get_topological_attributes.py.

Oracle: two-chain PIR (PIR/NBRF format via BioPython)
- chain A: ACDEFGHIKL  (10 aa)
- chain B: MKKKKK       (6 aa)

Expected:
  n_chains      = 2
  n_entities    = 2
  n_groups      = 16  (10 + 6)
  n_amino_acids = 16
"""

import pytest
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio import SeqIO
import molsysmt as msm


CHAIN_A_SEQ = 'ACDEFGHIKL'
CHAIN_B_SEQ = 'MKKKKK'
N_CHAINS = 2
N_GROUPS = len(CHAIN_A_SEQ) + len(CHAIN_B_SEQ)


@pytest.fixture(scope="module")
def pir_two_chains(tmp_path_factory):
    records = [
        SeqRecord(Seq(CHAIN_A_SEQ), id='chain_A', name='chain_A', description='first chain'),
        SeqRecord(Seq(CHAIN_B_SEQ), id='chain_B', name='chain_B', description='second chain'),
    ]
    p = tmp_path_factory.mktemp("file_pir_assets") / "two_chains.pir"
    with open(str(p), 'w') as fff:
        SeqIO.write(records, fff, 'pir')
    return str(p)


def test_get_form(pir_two_chains):
    assert msm.get_form(pir_two_chains) == 'file:pir'


def test_n_chains_from_system(pir_two_chains):
    assert msm.get(pir_two_chains, element='system', n_chains=True) == N_CHAINS


def test_n_entities_from_system(pir_two_chains):
    assert msm.get(pir_two_chains, element='system', n_entities=True) == N_CHAINS


def test_n_groups_from_system(pir_two_chains):
    assert msm.get(pir_two_chains, element='system', n_groups=True) == N_GROUPS


def test_n_amino_acids_from_system(pir_two_chains):
    assert msm.get(pir_two_chains, element='system', n_amino_acids=True) == N_GROUPS


def test_chain_id_from_chain(pir_two_chains):
    ids = msm.get(pir_two_chains, element='chain', chain_id=True)
    assert ids[0] == 'chain_A'
    assert ids[1] == 'chain_B'


def test_chain_type_from_chain(pir_two_chains):
    types_ = msm.get(pir_two_chains, element='chain', chain_type=True)
    assert all(t == 'protein' for t in types_)


def test_n_groups_from_chain(pir_two_chains):
    lengths = msm.get(pir_two_chains, element='chain', n_groups=True)
    assert lengths[0] == len(CHAIN_A_SEQ)
    assert lengths[1] == len(CHAIN_B_SEQ)


def test_group_name_from_group(pir_two_chains):
    names = msm.get(pir_two_chains, element='group', group_name=True)
    assert len(names) == N_GROUPS
    # A -> ALA (first of chain A)
    assert names[0] == 'ALA'
    # M -> MET (first of chain B)
    assert names[len(CHAIN_A_SEQ)] == 'MET'


def test_group_type_from_group(pir_two_chains):
    types_ = msm.get(pir_two_chains, element='group', group_type=True)
    assert len(types_) == N_GROUPS
    assert all(t == 'amino acid' for t in types_)
