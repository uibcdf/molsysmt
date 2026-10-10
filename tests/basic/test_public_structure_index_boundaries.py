"""Stable structure-index validation across the basic public API."""

import pytest

import molsysmt as msm


def test_modular_h5msm_axis_validation_reads_only_metadata(tmp_path, monkeypatch):
    import numpy as np

    from molsysmt import pyunitwizard as puw
    from molsysmt.basic._index_validation import (
        validate_element_indices,
        validate_structure_indices,
    )
    from molsysmt.form import _h5msm05_modular
    from molsysmt.native import Structures

    path = str(tmp_path / "axes.h5msm")
    msm.convert(
        Structures(coordinates=puw.quantity(np.zeros((4, 3, 3)), "nm")), to_form=path
    )

    def forbidden(*args, **kwargs):
        pytest.fail("Axis validation must not materialize H5MSM molecular domains.")

    monkeypatch.setattr(_h5msm05_modular, "read_molsys_file", forbidden)
    assert validate_structure_indices(path, [3, 0], "test") == [3, 0]
    assert validate_element_indices(path, [2, 0], "atom", "selection", "test") == [2, 0]
    with pytest.raises(msm.ArgumentError):
        validate_structure_indices(path, [4], "test")
    with pytest.raises(msm.ArgumentError):
        validate_element_indices(path, [3], "atom", "selection", "test")


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
