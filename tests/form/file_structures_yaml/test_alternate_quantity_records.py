"""Quantity integrity at the public structures-YAML boundary."""

import json
import subprocess
import sys
from copy import deepcopy

import numpy as np
import pytest
import yaml

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import FormatError
from molsysmt.native import Structures


@pytest.fixture()
def alternate_structures():
    molsys = Structures(
        coordinates=puw.quantity(np.arange(45).reshape(3, 5, 3), "angstrom"),
        box=puw.quantity(np.repeat(np.eye(3)[None], 3, axis=0) * 30, "angstrom"),
        time=puw.quantity([0, 1, 2], "ns"),
        structure_id=["100", "200", "300"],
    )
    molsys.alternate_location = [
        {
            np.int64(4): {
                "location_id": np.array(["A", "B"]),
                "atom_id": ["42", "300"],
                "occupancy": np.array([0.6, 0.4]),
                "b_factor": puw.quantity(np.array([1.0, 2.0]), "angstrom**2"),
                "coordinates": puw.quantity(np.arange(6).reshape(2, 3), "angstrom"),
            }
        },
        {},
        {
            2: {
                "location_id": np.array(["A"]),
                "atom_id": None,
                "occupancy": None,
                "b_factor": None,
                "coordinates": None,
            }
        },
    ]
    return molsys


def write_source(molsys, tmp_path, **kwargs):
    path = tmp_path / "alternate.yaml"
    msm.convert(
        molsys, to_form="file:structures_yaml", output_filename=str(path), **kwargs
    )
    return str(path)


@pytest.mark.parametrize("policy", ["nm", "pm"])
def test_public_yaml_preserves_alternate_quantity_records(
    alternate_structures, tmp_path, policy
):
    original = deepcopy(alternate_structures.alternate_location)
    with puw.context(standard_units=[policy, "ps"]):
        path = write_source(alternate_structures, tmp_path)
        recovered = msm.convert(path, to_form="molsysmt.Structures")
        query = msm.get(
            path, selection=[4], structure_indices=[0], alternate_location=True
        )
    payload = yaml.safe_load(open(path))
    assert payload["version"] == "0.2"
    record = payload["structures"]["alternate_location"][0][4]["coordinates"]
    assert record["manifest"]["field"] == "alternate_location.coordinates"
    assert record["manifest"]["unit"] == "nanometer"
    assert [list(sites) for sites in recovered.alternate_location] == [[4], [], [2]]
    entry = recovered.alternate_location[0][4]
    np.testing.assert_array_equal(entry["location_id"], ["A", "B"])
    assert entry["atom_id"] == ["42", "300"]
    np.testing.assert_allclose(
        puw.get_value(entry["coordinates"], to_unit="angstrom"),
        np.arange(6).reshape(2, 3),
    )
    np.testing.assert_allclose(
        puw.get_value(entry["b_factor"], to_unit="angstrom**2"), [1, 2]
    )
    np.testing.assert_array_equal(entry["occupancy"], [0.6, 0.4])
    np.testing.assert_allclose(puw.get_value(recovered.time, to_unit="ns"), [0, 1, 2])
    np.testing.assert_allclose(
        puw.get_value(query[0][4]["coordinates"], to_unit="angstrom"),
        np.arange(6).reshape(2, 3),
    )
    np.testing.assert_array_equal(
        puw.get_value(
            alternate_structures.alternate_location[0][4]["coordinates"],
            to_unit="angstrom",
        ),
        puw.get_value(original[0][4]["coordinates"], to_unit="angstrom"),
    )


def test_yaml_selection_remaps_sites_to_the_selected_atom_domain(
    alternate_structures, tmp_path
):
    path = write_source(
        alternate_structures, tmp_path, selection=[4, 2], structure_indices=[2, 0, 2, 1]
    )
    recovered = msm.convert(path, to_form="molsysmt.Structures")
    assert recovered.coordinates.shape == (4, 2, 3)
    assert [list(sites) for sites in recovered.alternate_location] == [
        [1],
        [0],
        [1],
        [],
    ]
    assert list(recovered.structure_id) == ["300", "100", "300", "200"]
    np.testing.assert_allclose(
        puw.get_value(recovered.coordinates, to_unit="angstrom"),
        np.arange(45).reshape(3, 5, 3)[[2, 0, 2, 1]][:, [4, 2], :],
    )
    assert [list(sites) for sites in alternate_structures.alternate_location] == [
        [4],
        [],
        [2],
    ]


@pytest.mark.parametrize(
    "defect",
    [
        "missing_unit",
        "changed_unit",
        "changed_si",
        "wrong_dimensions",
        "wrong_field",
        "bare_values",
        "shape",
        "index",
        "version",
        "missing_version",
        "location_labels",
        "atom_ids",
        "occupancy",
    ],
)
def test_yaml_rejects_invalid_alternate_records(alternate_structures, tmp_path, defect):
    from pyunitwizard.record import QuantityRecord

    path = write_source(alternate_structures, tmp_path)
    with open(path) as handle:
        data = yaml.safe_load(handle)
    entry = data["structures"]["alternate_location"][0][4]
    record = entry["coordinates"]
    if defect == "missing_unit":
        del record["manifest"]["unit"]
    elif defect == "changed_unit":
        record["manifest"]["unit"] = "angstrom"
    elif defect == "changed_si":
        record["manifest"]["si"] = {}
    elif defect in ("wrong_dimensions", "wrong_field", "shape"):
        values, unit, field = np.zeros((2, 3)), "nm", "alternate_location.coordinates"
        if defect == "wrong_dimensions":
            unit = "ps"
        elif defect == "wrong_field":
            field = "alternate_location.b_factor"
        else:
            values = np.zeros((2, 2))
        entry["coordinates"] = QuantityRecord.from_quantity(
            puw.quantity(values, unit), field=field
        ).to_dict()
    elif defect == "bare_values":
        entry["coordinates"] = [[0, 0, 0], [0, 0, 0]]
    elif defect == "index":
        data["structures"]["alternate_location"][0][5] = data["structures"][
            "alternate_location"
        ][0].pop(4)
    elif defect == "version":
        data["version"] = "99.0"
    elif defect == "missing_version":
        del data["version"]
    elif defect == "location_labels":
        entry["location_id"] = 42
    elif defect == "atom_ids":
        entry["atom_id"] = 42
    else:
        entry["occupancy"] = "not a number"
    with open(path, "w") as handle:
        yaml.safe_dump(data, handle)
    with pytest.raises(FormatError):
        msm.convert(path, to_form="molsysmt.Structures")


def test_legacy_yaml_retains_canonical_units_and_label_only_alternates(tmp_path):
    data = {
        "format": "molsysmt",
        "kind": "structures",
        "version": "0.1",
        "structures": {
            "coordinates": np.zeros((1, 2, 3)).tolist(),
            "alternate_location": [
                {1: {"location_id": ["A", "B"], "atom_id": [10, 11]}}
            ],
        },
    }
    path = tmp_path / "legacy.yaml"
    with path.open("w") as handle:
        yaml.safe_dump(data, handle)
    recovered = msm.convert(str(path), to_form="molsysmt.Structures")
    assert str(puw.get_unit(recovered.coordinates)) == "nanometer"
    assert recovered.alternate_location[0][1]["atom_id"] == ["10", "11"]
    assert recovered.alternate_location[0][1]["coordinates"] is None
    new = write_source(recovered, tmp_path)
    assert yaml.safe_load(open(new))["version"] == "0.2"
    data["structures"]["alternate_location"][0][1]["coordinates"] = [
        [0, 0, 0],
        [0, 0, 0],
    ]
    with path.open("w") as handle:
        yaml.safe_dump(data, handle)
    with pytest.raises(FormatError, match="no negotiated unit"):
        msm.convert(str(path), to_form="molsysmt.Structures")


def test_yaml_empty_axes_and_nonfinite_b_factors(tmp_path, alternate_structures):
    molsys = {
        "coordinates": puw.quantity(np.empty((0, 2, 3)), "nm"),
        "alternate_location": [],
    }
    recovered = msm.convert(
        write_source(molsys, tmp_path), to_form="molsysmt.StructuresDict"
    )
    assert recovered["coordinates"].shape == (0, 2, 3)
    assert recovered["alternate_location"] == []
    alternate_structures.alternate_location[0][4]["b_factor"] = puw.quantity(
        np.array([np.nan, 1.0]), "nm**2"
    )
    recovered = msm.convert(
        write_source(alternate_structures, tmp_path), to_form="molsysmt.Structures"
    )
    np.testing.assert_array_equal(
        puw.get_value(recovered.alternate_location[0][4]["b_factor"], to_unit="nm**2"),
        [np.nan, 1.0],
    )


def test_invalid_writer_quantity_keeps_an_existing_file(alternate_structures, tmp_path):
    path = write_source(alternate_structures, tmp_path)
    original = (tmp_path / "alternate.yaml").read_bytes()
    alternate_structures.alternate_location[0][4]["coordinates"] = puw.quantity(
        np.zeros((2, 3)), "ps"
    )
    with pytest.raises(FormatError, match="requires units"):
        msm.convert(
            alternate_structures, to_form="file:structures_yaml", output_filename=path
        )
    assert (tmp_path / "alternate.yaml").read_bytes() == original


def test_fresh_reader_uses_record_units(alternate_structures, tmp_path):
    path = write_source(alternate_structures, tmp_path)
    code = """
import json, sys
import molsysmt as msm
puw = msm.pyunitwizard
with puw.context(standard_units=['pm', 'ps']):
    molsys = msm.convert(sys.argv[1], to_form='molsysmt.Structures')
    sites = molsys.alternate_location[0][4]
    print(json.dumps({'coordinates': puw.get_value(sites['coordinates'], to_unit='angstrom').tolist(),
                      'b_factor': puw.get_value(sites['b_factor'], to_unit='angstrom**2').tolist()}))
"""
    completed = subprocess.run(
        [sys.executable, "-c", code, path], capture_output=True, text=True, check=True
    )
    result = json.loads(completed.stdout)
    np.testing.assert_allclose(result["coordinates"], np.arange(6).reshape(2, 3))
    np.testing.assert_allclose(result["b_factor"], [1, 2])
