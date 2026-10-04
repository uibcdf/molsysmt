"""Checking the single-record structure count through public dispatch."""

import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError


@pytest.mark.parametrize("frames,count", [("all", 1), ([0], 1), ([], 0), ([0, 0], 2)])
def test_public_structure_count_accepts_dispatcher_selection(frames, count):
    assert (
        msm.get(
            msm.systems["caffeine"]["caffeine.sdf"],
            structure_indices=frames,
            n_structures=True,
        )
        == count
    )


def test_public_structure_count_rejects_a_nonexistent_frame():
    with pytest.raises(ArgumentError):
        msm.get(
            msm.systems["caffeine"]["caffeine.sdf"],
            structure_indices=[1],
            n_structures=True,
        )
