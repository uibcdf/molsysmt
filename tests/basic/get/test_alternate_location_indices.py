"""Public alternate-site keys identify source atom positions, not atom IDs."""

from copy import deepcopy

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import MolSys, Structures


@pytest.fixture(params=["structures", "molsys", "dictionary", "yaml", "h5msm"])
def alternate_source(request, tmp_path):
    structures = Structures(
        coordinates=puw.quantity(np.arange(45).reshape(3, 5, 3), "nm"),
        structure_id=["100", "200", "300"],
    )

    def sites(offset):
        return {
            "location_id": np.array(["A", "B"]),
            "atom_id": np.array([42 + offset, 300 + offset]),
            "occupancy": np.array([0.6, 0.4]),
            "b_factor": puw.quantity([0.01, 0.02], "nm**2"),
            "coordinates": puw.quantity(np.arange(6).reshape(2, 3) + offset, "nm"),
        }

    structures.alternate_location = [
        {np.int64(2): sites(0)},
        {},
        {np.int64(4): sites(10)},
    ]
    kind = request.param
    if kind == "structures":
        source = structures
    elif kind == "molsys":
        source = MolSys(n_atoms=5)
        source.structures = structures
    elif kind == "dictionary":
        source = msm.convert(structures, to_form="molsysmt.StructuresDict")
    else:
        extension = "yaml" if kind == "yaml" else "h5msm"
        source = str(tmp_path / f"alternate-sites.{extension}")
        msm.convert(
            structures,
            to_form=f"file:{'structures_yaml' if kind == 'yaml' else 'h5msm'}",
            output_filename=source,
        )
    return source, structures


def assert_same_sites(actual, expected):
    assert list(actual) == list(expected)
    for key in expected:
        assert isinstance(key, (int, np.integer))
        for attribute in ("location_id", "atom_id", "occupancy"):
            np.testing.assert_array_equal(
                actual[key][attribute], expected[key][attribute]
            )
        for attribute, unit in (("coordinates", "nm"), ("b_factor", "nm**2")):
            if expected[key][attribute] is None:
                assert actual[key][attribute] is None
                continue
            np.testing.assert_array_equal(
                puw.get_value(actual[key][attribute], to_unit=unit),
                puw.get_value(expected[key][attribute], to_unit=unit),
            )


@pytest.mark.parametrize("element", ["atom", "system"])
@pytest.mark.parametrize("output_type", ["values", "dictionary"])
def test_public_alternate_location_preserves_source_atom_indices(
    alternate_source, element, output_type
):
    source, structures = alternate_source
    original = deepcopy(structures.alternate_location)
    result = msm.get(
        source,
        element=element,
        selection=[4, 2],
        structure_indices=[2, 0, 2, 1],
        alternate_location=True,
        output_type=output_type,
    )
    if output_type == "dictionary":
        result = result["alternate_location"]

    assert [list(sites) for sites in result] == [[4], [2], [4], []]
    for sites, source_index in zip(result, [2, 0, 2, 1]):
        expected = deepcopy(original[source_index])
        for entry in expected.values():
            entry["atom_id"] = [str(value) for value in entry["atom_id"]]
        assert_same_sites(sites, expected)

    # Public label normalization and editing returned containers leave storage intact.
    result[0][4]["atom_id"][0] = "edited"
    result[0][4]["new_field"] = "client metadata"
    result[0][99] = {}
    for actual, expected in zip(structures.alternate_location, original):
        assert_same_sites(actual, expected)
        for entry in actual.values():
            assert "new_field" not in entry
    reread = msm.get(source, structure_indices=[2], alternate_location=True)
    assert list(reread[0]) == [4]
    assert reread[0][4]["atom_id"] == ["52", "310"]


def test_public_alternate_location_empty_selection_and_absence(alternate_source):
    source, _ = alternate_source
    assert msm.get(source, element="atom", selection=[], alternate_location=True) == [
        {},
        {},
        {},
    ]
    assert msm.get(source, structure_indices=[], alternate_location=True) == []
    empty = Structures(coordinates=puw.quantity(np.zeros((1, 5, 3)), "nm"))
    assert msm.get(empty, alternate_location=True) is None
