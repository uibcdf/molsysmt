"""Identify rejected structures in the molecular-system index space."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys, Structures


@pytest.mark.parametrize("form", ["structures", "molsys"])
@pytest.mark.parametrize("principal_axes_type", ["inertia", "geometric"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize(
    "indices, bad_index, position",
    [
        ([2, 0], 0, 1),
        ([0, 2], 0, 0),
        ([2, 2, 0, 0], 0, 2),
        ("all", 2, 2),
        (0, 0, 0),
        (2, 2, 0),
    ],
)
def test_degenerate_moments_name_source_index_and_selected_position(
    form, principal_axes_type, in_place, indices, bad_index, position
):
    points = np.array(
        [[3, 0, 0], [-3, 0, 0], [0, 2, 0], [0, -2, 0], [0, 0, 1], [0, 0, -1]],
        dtype=float,
    )
    coordinates = np.stack([points + [i, 2 * i, -i] for i in range(3)])
    coordinates[bad_index] = np.column_stack([np.arange(6), np.zeros((6, 2))])
    structures = Structures(
        coordinates=msm.pyunitwizard.quantity(coordinates, "nm"),
        structure_id=["100", "200", "300"],
    )
    source = structures
    if form == "molsys":
        source = MolSys(n_atoms=6)
        source.structures = structures
        source.interactions = {
            "existing": msm.Interactions.from_records(
                [],
                n_atoms=6,
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="existing-analysis",
            )
        }
    before = msm.pyunitwizard.get_value(structures.coordinates, to_unit="nm").copy()

    with pytest.raises(StructuralInconsistencyError) as captured:
        msm.structure.align_principal_axes(
            source,
            principal_axes_type=principal_axes_type,
            structure_indices=indices,
            in_place=in_place,
        )

    error = captured.value
    assert error.code == "MSM-ERR-STRUCT-003"
    reason = error.extra["reason"]
    assert f"structure_index {bad_index}" in reason
    assert f"selection position {position}" in reason
    assert "degenerate principal moments" in reason
    assert "100" not in reason and "200" not in reason and "300" not in reason
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(structures.coordinates, to_unit="nm"), before
    )
    assert list(structures.structure_id) == ["100", "200", "300"]
    if form == "molsys":
        np.testing.assert_array_equal(
            source.interactions["existing"].evaluated_structure_indices, [0, 1, 2]
        )


@pytest.mark.parametrize("index", [-1, 3])
def test_out_of_range_scope_keeps_existing_index_validation(index):
    source = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((3, 6, 3)), "nm")
    )
    before = msm.pyunitwizard.get_value(source.coordinates, to_unit="nm").copy()
    with pytest.raises(ArgumentError, match="out-of-range structure indices"):
        msm.structure.align_principal_axes(
            source, structure_indices=[index], in_place=True
        )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(source.coordinates, to_unit="nm"), before
    )
