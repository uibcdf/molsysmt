"""Retaining strict positional meaning at shared atom-map validation boundaries."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.argdigest.argument.atom_correspondence import (
    digest_atom_correspondence,
)


@pytest.mark.parametrize(
    "pairs",
    [
        [[False, 1], [True, 0]],
        [[0, np.bool_(True)], [1, np.bool_(False)]],
        [[0, 0], [1, 2**64]],
        np.asarray([[0, 0], [1, 2**63]], dtype=np.uint64),
    ],
)
def test_correspondence_rejects_coercion_that_loses_positional_meaning(pairs):
    with pytest.raises(msm.ArgumentError):
        digest_atom_correspondence(pairs, caller="declared map consumer")


@pytest.mark.parametrize("wrapped", ["whole", "scalar"])
def test_correspondence_indices_cannot_carry_units(wrapped):
    pairs = (
        msm.pyunitwizard.quantity([[0, 1], [1, 0]], "dimensionless")
        if wrapped == "whole"
        else [[msm.pyunitwizard.quantity(0, "dimensionless"), 1], [1, 0]]
    )
    with pytest.raises(msm.ArgumentError):
        digest_atom_correspondence(pairs, caller="declared map consumer")


@pytest.mark.parametrize("dtype", [np.int32, np.int64, np.uint32])
def test_correspondence_normalizes_valid_detached_pairs_to_signed_indices(dtype):
    source = np.asarray([[1, 0], [0, 1]], dtype=dtype)
    pairs = digest_atom_correspondence(source, caller="declared map consumer")
    np.testing.assert_array_equal(pairs, source)
    assert pairs.dtype == np.int64
    assert not np.shares_memory(pairs, source)


def test_empty_correspondence_has_a_defined_two_column_integer_axis():
    pairs = digest_atom_correspondence(np.empty((0, 2), dtype=np.int64))
    assert pairs.shape == (0, 2) and pairs.dtype == np.int64
