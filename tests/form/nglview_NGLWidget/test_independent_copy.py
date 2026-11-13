"""Copy molecular NGL payloads without sharing widget communication or arrays."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize("route", ["copy", "extract", "convert"])
@pytest.mark.parametrize("length,time", [("nm", "ps"), ("pm", "fs")])
def test_copying_an_ngl_widget_owns_its_payload_and_communication(
    nglview_ensemble_widget, route, length, time
):
    source = nglview_ensemble_widget
    puw.configure.set_standard_units(
        [length, time, "K", "mole", "dalton", "e", "kJ/mol", "radians"]
    )
    original_coordinates = np.array(
        [source._trajlist[0].get_coordinates(i).copy() for i in range(3)]
    )
    original_frame = source.frame
    original_topology = source._trajlist[0]._molsysmt_topology
    original_name = original_topology.atoms.loc[0, "atom_name"]
    if route == "copy":
        result = msm.copy(source)
    elif route == "extract":
        result = msm.extract(source)
    else:
        result = msm.convert(source, to_form="nglview.NGLWidget")
    try:
        assert result is not source
        assert result.comm is not source.comm
        assert result._trajlist is not source._trajlist
        assert result._trajlist[0] is not source._trajlist[0]
        actual = result._trajlist[0].coordinates
        assert actual.shape == (3, 4, 3)
        np.testing.assert_allclose(actual, original_coordinates)
        assert not np.shares_memory(actual, source._trajlist[0].coordinates)
        result._trajlist[0].coordinates[0, 0] += 7.0
        result._trajlist[0]._molsysmt_topology.atoms.loc[0, "atom_name"] = "edited"
        np.testing.assert_array_equal(
            source._trajlist[0].coordinates, original_coordinates
        )
        assert original_topology.atoms.loc[0, "atom_name"] == original_name
        assert source.frame == original_frame
        np.testing.assert_array_equal(
            msm.get(result, bonded_atom_pairs=True), [[0, 1], [1, 2]]
        )
    finally:
        # The broken shallow copy shares the source Comm: close it only once.
        if result.comm is not source.comm:
            result.close()


@pytest.mark.parametrize("route", ["extract", "convert"])
def test_unrestricted_ngl_reuse_remains_explicit(nglview_ensemble_widget, route):
    source = nglview_ensemble_widget
    if route == "extract":
        result = msm.extract(source, copy_if_all=False)
    else:
        result = msm.convert(source, to_form="nglview.NGLWidget", copy_if_all=False)
    assert result is source
    assert source.frame == 1


def test_selected_ngl_extraction_keeps_native_axes_and_source(nglview_ensemble_widget):
    source = nglview_ensemble_widget
    before = source._trajlist[0].coordinates.copy()
    result = msm.extract(source, selection=[3, 1], structure_indices=[2, 0])
    try:
        actual = result._trajlist[0].coordinates
        np.testing.assert_allclose(actual, before[[2, 0]][:, [1, 3]])
        assert result.comm is not source.comm
        np.testing.assert_array_equal(source._trajlist[0].coordinates, before)
        assert source.frame == 1
    finally:
        result.close()
