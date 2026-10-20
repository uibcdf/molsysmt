"""Selection scopes must intersect membership, not duplicate occurrences."""

import pytest

import molsysmt as msm
from molsysmt.native import MolSys


@pytest.mark.parametrize(
    "selection,mask,expected",
    [
        ([0], [1, 1], []),
        ([1, 1], [0], []),
        ([2, 0, 2], [1, 2, 1, 2], [2]),
        ([2, 1, 0, 1], [2, 1, 1], [1, 2]),
    ],
)
def test_mask_intersection_never_invents_members_from_duplicates(
    selection, mask, expected
):
    molsys = MolSys(n_atoms=3)
    assert msm.select(molsys, selection=selection, mask=mask) == expected
    assert sorted(set(selection) & set(mask)) == expected
