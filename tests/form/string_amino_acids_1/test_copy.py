"""Check one-letter sequence copy dispatch and the trusted adapter contract."""

import pytest

import molsysmt as msm
from molsysmt.form.string_amino_acids_1 import copy


@pytest.mark.parametrize("sequence", ["ACD", "amino_acids_1:ACD"])
def test_public_copy_preserves_the_immutable_sequence(sequence):
    assert msm.copy(sequence) == sequence


@pytest.mark.parametrize("sequence", ["ACD", "amino_acids_1:ACD"])
@pytest.mark.parametrize("skip_digestion", [False, True])
def test_adapter_copy_accepts_the_common_digestion_argument(sequence, skip_digestion):
    assert copy(sequence, skip_digestion=skip_digestion) == sequence
