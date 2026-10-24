"""Checking physical lengths independently of streaming and presentation units."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import Structures


@pytest.fixture
def source_geometry():
    coordinates = (
        np.array(
            [
                [[0, 1, 0], [2, 0, 1], [4, 3, 2], [7, 1, 0]],
                [[1, 0, 2], [3, 2, 0], [5, 1, 3], [8, 2, 1]],
                [[2, 2, 1], [4, 3, 2], [6, 0, 4], [9, 3, 2]],
                [[3, 3, 0], [5, 1, 3], [7, 2, 1], [6, 4, 3]],
                [[4, 0, 3], [6, 4, 1], [8, 1, 2], [5, 0, 4]],
            ],
            dtype=float,
        )
        / 10
    )
    return Structures(coordinates=puw.quantity(coordinates * 10, "angstrom"))


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("chunk_size", [1, 2])
@pytest.mark.parametrize("form", ["native", "h5msm"])
@pytest.mark.parametrize(
    "observable, weights",
    [
        ("get_radius_of_gyration", None),
        ("get_radius_of_gyration", [1.0, 4.0, 2.0]),
        ("get_rmsf", None),
    ],
)
def test_chunked_observables_retain_physical_scale(
    source_geometry, unit, chunk_size, form, observable, weights, tmp_path
):
    atoms, structures = [3, 0, 2], [4, 0, 4, 2, 1]
    original = puw.get_value(source_geometry.coordinates, to_unit="nm").copy()
    selected = original[np.ix_(structures, atoms)]
    if observable == "get_radius_of_gyration":
        center = np.average(selected, axis=1, weights=weights)
        squared = np.sum((selected - center[:, None]) ** 2, axis=2)
        expected = np.sqrt(np.average(squared, axis=1, weights=weights))
    else:
        expected = np.sqrt(
            np.mean(np.sum((selected - selected.mean(axis=0)) ** 2, axis=2), axis=0)
        )
    source = source_geometry
    if form == "h5msm":
        source = str(tmp_path / "coordinates.h5msm")
        msm.convert(source_geometry, to_form=source)
    options = {"weights": weights} if observable == "get_radius_of_gyration" else {}
    function = getattr(msm.structure, observable)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        policy = dict(puw.configure.get_standard_units())
        with msm.configure.context(chunk_size=chunk_size, chunk_memory_fraction=None):
            eager = function(
                source,
                selection=atoms,
                structure_indices=structures,
                heavy_mode="off",
                **options,
            )
            result = function(
                source,
                selection=atoms,
                structure_indices=structures,
                heavy_mode="force",
                **options,
            )
        assert puw.configure.get_standard_units() == policy
        assert puw.get_unit(result) == puw.unit(unit)
        np.testing.assert_allclose(
            puw.get_value(result, to_unit="nm"), expected, rtol=1e-13, atol=1e-14
        )
        np.testing.assert_allclose(
            puw.get_value(eager, to_unit="nm"), expected, rtol=1e-13, atol=1e-14
        )
    np.testing.assert_array_equal(
        puw.get_value(source_geometry.coordinates, to_unit="nm"), original
    )


@pytest.mark.parametrize("observable", ["get_radius_of_gyration", "get_rmsf"])
def test_automatic_route_reaches_multiple_nm_blocks(
    source_geometry, observable, monkeypatch
):
    from importlib import import_module

    module = import_module("molsysmt.structure." + observable)
    reducer = getattr(
        module,
        "_RadiusOfGyrationReducer"
        if observable == "get_radius_of_gyration"
        else "_RMSFReducer",
    )
    sizes = []
    consume = reducer.consume

    def observe(self, chunk):
        sizes.append(len(chunk["coordinates"]))
        return consume(self, chunk)

    monkeypatch.setattr(reducer, "consume", observe)
    original = puw.get_value(source_geometry.coordinates, to_unit="nm")
    source = Structures(coordinates=puw.quantity(np.tile(original, (10, 1, 1)), "nm"))
    options = dict(selection=[3, 0, 2], structure_indices=[4, 0, 4, 2, 1])
    with puw.context(standard_units=["pm", "ps", "radians"]):
        reference = getattr(msm.structure, observable)(
            source_geometry, heavy_mode="off", **options
        )
        with msm.configure.context(
            max_ram_usage=1024, chunk_size=2, chunk_memory_fraction=None
        ):
            actual = getattr(msm.structure, observable)(
                source, heavy_mode="auto", **options
            )
    assert sizes == [2, 2, 1]
    np.testing.assert_allclose(
        puw.get_value(actual, to_unit="nm"),
        puw.get_value(reference, to_unit="nm"),
        rtol=1e-13,
        atol=1e-14,
    )
