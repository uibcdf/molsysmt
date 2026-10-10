"""Verifying the existing TRJPK layout through public queries and export."""

import pickle

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError

puw = msm.pyunitwizard


@pytest.fixture
def payload():
    return {
        "coordinates": puw.quantity(np.arange(36.0).reshape(3, 4, 3), "nm"),
        "box": puw.quantity(np.array([np.eye(3) * n for n in [1, 2, 3]]), "nm"),
        "time": puw.quantity([0.5, 1.5, 2.5], "ps"),
        "structure_id": np.array(["s7", "s2", "s4"]),
    }


@pytest.fixture
def legacy_file(tmp_path, payload):
    """Writing independently of the production writer, so reader bugs cannot cancel."""
    filename = str(tmp_path / "legacy.trjpk")
    with open(filename, "wb") as stream:
        for value in [
            4,
            3,
            puw.get_value(payload["coordinates"], to_unit="nm"),
            puw.get_value(payload["box"], to_unit="nm"),
            puw.get_value(payload["time"], to_unit="ps"),
            payload["structure_id"],
        ]:
            pickle.dump(value, stream)
    return filename


@pytest.mark.parametrize(
    "attribute,unit",
    [("coordinates", "nm"), ("box", "nm"), ("time", "ps"), ("structure_id", None)],
)
def test_queries_retain_nonconsecutive_structure_order(
    legacy_file, payload, attribute, unit
):
    result = msm.get(legacy_file, structure_indices=[2, 0, 2], **{attribute: True})
    expected = payload[attribute][[2, 0, 2]]
    if unit:
        np.testing.assert_allclose(
            puw.get_value(result, to_unit=unit), puw.get_value(expected, to_unit=unit)
        )
    else:
        np.testing.assert_array_equal(result, expected)


def test_counts_positions_and_bulk_coordinates(legacy_file, payload):
    assert msm.get(legacy_file, n_atoms=True) == 4
    assert msm.get(legacy_file, n_structures=True) == 3
    assert msm.get(legacy_file, selection=[3, 1, 3], atom_index=True) == [3, 1, 3]
    coordinates, box, time, labels = msm.get(
        legacy_file,
        selection=[3, 1],
        structure_indices=[2, 0],
        coordinates=True,
        box=True,
        time=True,
        structure_id=True,
    )
    np.testing.assert_allclose(
        puw.get_value(coordinates, to_unit="nm"),
        puw.get_value(payload["coordinates"], to_unit="nm")[[2, 0]][:, [3, 1]],
    )
    np.testing.assert_allclose(
        puw.get_value(box, to_unit="nm"),
        puw.get_value(payload["box"], to_unit="nm")[[2, 0]],
    )
    np.testing.assert_allclose(puw.get_value(time, to_unit="ps"), [2.5, 0.5])
    np.testing.assert_array_equal(labels, ["s4", "s7"])


@pytest.mark.parametrize("atoms", [[3, 1], np.array([3, 1]), [], [2, 2, 0]])
@pytest.mark.parametrize("structures", [[2, 0], np.array([2, 0]), [], [1, 1, 0]])
def test_export_selects_both_axes_with_consistent_header(
    tmp_path, payload, atoms, structures
):
    filename = str(tmp_path / "subset.trjpk")
    msm.convert(
        payload, to_form=filename, selection=atoms, structure_indices=structures
    )
    with open(filename, "rb") as stream:
        assert pickle.load(stream) == len(atoms)
        assert pickle.load(stream) == len(structures)
        raw = pickle.load(stream)
    expected = puw.get_value(payload["coordinates"], to_unit="nm")[list(structures)][
        :, list(atoms)
    ]
    assert raw.shape == (len(structures), len(atoms), 3)
    np.testing.assert_array_equal(raw, expected)
    restored = msm.convert(filename, to_form="molsysmt.StructuresDict")
    np.testing.assert_array_equal(
        puw.get_value(restored["coordinates"], to_unit="nm"), expected
    )
    np.testing.assert_array_equal(
        restored["structure_id"], payload["structure_id"][list(structures)]
    )
    np.testing.assert_array_equal(
        puw.get_value(restored["box"], to_unit="nm"),
        puw.get_value(payload["box"], to_unit="nm")[list(structures)],
    )
    np.testing.assert_array_equal(
        puw.get_value(restored["time"], to_unit="ps"),
        puw.get_value(payload["time"], to_unit="ps")[list(structures)],
    )
    assert payload["coordinates"].shape == (3, 4, 3)


def test_fixed_storage_units_under_nondefault_policy(tmp_path, payload):
    with puw.context(standard_units=["angstrom", "fs", "degree"]):
        filename = str(tmp_path / "units.trjpk")
        msm.convert(
            payload, to_form=filename, selection=[3, 1], structure_indices=[2, 0]
        )
        with open(filename, "rb") as stream:
            pickle.load(stream)
            pickle.load(stream)
            np.testing.assert_allclose(
                pickle.load(stream),
                puw.get_value(payload["coordinates"], to_unit="nm")[[2, 0]][:, [3, 1]],
            )
            pickle.load(stream)
            np.testing.assert_allclose(pickle.load(stream), [2.5, 0.5])
        coordinates, time = msm.get(filename, coordinates=True, time=True)
        assert puw.get_unit(coordinates) == puw.get_unit(puw.quantity(1.0, "angstrom"))
        assert puw.get_unit(time) == puw.get_unit(puw.quantity(1.0, "fs"))
        np.testing.assert_allclose(
            puw.get_value(coordinates, to_unit="nm"),
            puw.get_value(payload["coordinates"], to_unit="nm")[[2, 0]][:, [3, 1]],
        )
        np.testing.assert_allclose(puw.get_value(time, to_unit="ps"), [2.5, 0.5])


@pytest.mark.parametrize("coordinates", ["absent", None])
def test_absent_fields_and_metadata_only_export(tmp_path, coordinates):
    filename = str(tmp_path / "time_only.trjpk")
    data = {"time": puw.quantity([1.0, 2.0, 3.0], "ps")}
    if coordinates is None:
        data["coordinates"] = None
    msm.convert(
        data,
        to_form=filename,
        structure_indices=[2, 0],
    )
    assert msm.get(filename, n_atoms=True) == 0
    assert msm.get(filename, n_structures=True) == 2
    assert msm.get(filename, coordinates=True) is None
    assert msm.get(filename, box=True) is None
    assert msm.get(filename, structure_id=True) is None
    np.testing.assert_allclose(
        puw.get_value(msm.get(filename, time=True), to_unit="ps"), [3.0, 1.0]
    )


def test_invalid_indices_are_rejected(legacy_file):
    with pytest.raises(ArgumentError, match="index|indices|range"):
        msm.get(legacy_file, structure_indices=[3], time=True)


def test_identity_conversion_copies_to_requested_filename(legacy_file, tmp_path):
    from pathlib import Path

    destination = str(tmp_path / "copy.trjpk")
    assert msm.convert(legacy_file, to_form=destination) == destination
    assert Path(destination).read_bytes() == Path(legacy_file).read_bytes()


def test_identity_conversion_without_destination_keeps_source(legacy_file):
    from pathlib import Path

    original = Path(legacy_file).read_bytes()
    assert msm.convert(legacy_file, to_form="file:trjpk") == legacy_file
    assert (
        msm.convert(legacy_file, to_form="file:trjpk", copy_if_all=False) == legacy_file
    )
    assert Path(legacy_file).read_bytes() == original


def test_identity_conversion_accepts_legacy_output_name(legacy_file, tmp_path):
    from pathlib import Path

    from molsysmt.form.file_trjpk.to_file_trjpk import to_file_trjpk

    destination = str(tmp_path / "alias.trjpk")
    import warnings

    with warnings.catch_warnings(record=True) as events:
        assert to_file_trjpk(legacy_file, output_name=Path(destination)) == destination
    assert not any(
        event.category.__name__ == "DigestNotDigestedWarning" for event in events
    )
    assert Path(destination).read_bytes() == Path(legacy_file).read_bytes()


def test_identity_conversion_rejects_invalid_or_conflicting_aliases(
    legacy_file, tmp_path
):
    from molsysmt.form.file_trjpk.to_file_trjpk import to_file_trjpk

    with pytest.raises(ArgumentError):
        to_file_trjpk(legacy_file, output_name=3)
    with pytest.raises(ValueError, match="not both"):
        to_file_trjpk(
            legacy_file,
            output_name=str(tmp_path / "a.trjpk"),
            output_filename=str(tmp_path / "b.trjpk"),
        )
