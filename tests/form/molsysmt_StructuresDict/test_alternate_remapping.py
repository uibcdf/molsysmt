"""Conversions create local alternate-site keys; queries retain source keys."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import Structures


@pytest.mark.parametrize(
    "source_form, target_form",
    [
        ("molsysmt.Structures", "molsysmt.Structures"),
        ("molsysmt.Structures", "molsysmt.StructuresDict"),
        ("molsysmt.StructuresDict", "molsysmt.Structures"),
    ],
)
def test_selected_conversion_remaps_alternate_atom_indices(source_form, target_form):
    molsys = Structures(
        coordinates=msm.pyunitwizard.quantity(np.arange(30).reshape(2, 5, 3), "nm")
    )
    molsys.alternate_location = [
        {4: {"location_id": ["A"]}},
        {2: {"location_id": ["B"]}},
    ]
    source = msm.convert(molsys, to_form=source_form)
    selected = msm.convert(
        source, to_form=target_form, selection=[4, 2], structure_indices=[1, 0, 1]
    )
    sites = msm.get(selected, alternate_location=True)
    assert [list(row) for row in sites] == [[1], [0], [1]]
    coords = msm.get(selected, coordinates=True)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(coords, to_unit="nm"),
        np.arange(30).reshape(2, 5, 3)[[1, 0, 1]][:, [4, 2], :],
    )
    assert [
        list(row) for row in msm.get(source, selection=[4, 2], alternate_location=True)
    ] == [[4], [2]]
