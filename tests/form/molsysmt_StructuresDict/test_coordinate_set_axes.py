"""Keep public coordinate writes on their declared structure-first population."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize(
    "atoms,structures",
    [
        ([0, 2, 5], [3, 1]),
        ([1, 0], [2, 0]),
        ([4, 0, 4], [2, 0, 2]),
        ("all", [2, 0]),
        ([5, 1], "all"),
        ("all", "all"),
    ],
)
def test_public_set_keeps_explicit_axes_order_and_nonselected_coordinates(
    unit, atoms, structures
):
    before = np.arange(4 * 6 * 3, dtype=float).reshape(4, 6, 3) / 10
    boxes = np.tile(np.eye(3) * 12, (4, 1, 1))
    source = {
        "coordinates": puw.quantity(before.copy(), "nm"),
        "box": puw.quantity(boxes.copy(), "nm"),
    }
    atom_axis = list(range(6)) if isinstance(atoms, str) else atoms
    structure_axis = list(range(4)) if isinstance(structures, str) else structures
    block = np.array(
        [
            [[100 * s + 10 * a + k / 10 for k in range(3)] for a in atom_axis]
            for s in structure_axis
        ]
    )
    expected = before.copy()
    for si, s in enumerate(structure_axis):
        for ai, a in enumerate(atom_axis):
            expected[s, a] = block[si, ai]
    with puw.context(standard_units=[unit, "fs"]):
        result = msm.set(
            source,
            selection=atoms,
            structure_indices=structures,
            coordinates=puw.convert(puw.quantity(block, "nm"), to_unit="angstrom"),
        )
    assert result is None
    np.testing.assert_allclose(
        puw.get_value(source["coordinates"], to_unit="nm"), expected, atol=1e-12
    )
    np.testing.assert_array_equal(puw.get_value(source["box"], to_unit="nm"), boxes)
