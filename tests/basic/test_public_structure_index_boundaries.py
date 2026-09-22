"""Stable structure-index validation across the basic public API."""

import pytest

import molsysmt as msm


@pytest.mark.parametrize("structure_indices", [[1], [-1]])
@pytest.mark.parametrize(
    "operation",
    ["convert", "extract", "remove", "set", "view", "info", "iterator"],
)
def test_basic_operations_reject_out_of_range_structure_indices(
    t4_h5msm_molsys,
    operation,
    structure_indices,
):
    molecular_system = t4_h5msm_molsys

    if operation == "convert":

        def call():
            return msm.convert(
                molecular_system,
                to_form="molsysmt.MolSys",
                structure_indices=structure_indices,
            )
    elif operation == "extract":

        def call():
            return msm.extract(
                molecular_system,
                structure_indices=structure_indices,
            )
    elif operation == "remove":

        def call():
            return msm.remove(
                molecular_system,
                structure_indices=structure_indices,
            )
    elif operation == "set":
        coordinates = msm.get(molecular_system, coordinates=True)

        def call():
            return msm.set(
                molecular_system.copy(),
                structure_indices=structure_indices,
                coordinates=coordinates,
            )
    elif operation == "view":

        def call():
            return msm.view(
                molecular_system,
                structure_indices=structure_indices,
            )
    elif operation == "info":

        def call():
            return msm.info(
                molecular_system,
                structure_indices=structure_indices,
                output_type="dictionary",
            )
    else:

        def call():
            return msm.Iterator(
                molecular_system,
                structure_indices=structure_indices,
                coordinates=True,
            )

    with pytest.raises(msm.ArgumentError, match="out-of-range structure indices"):
        call()
