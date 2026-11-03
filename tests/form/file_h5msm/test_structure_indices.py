"""Protecting metadata-only structure-index queries on legacy H5MSM files."""

from contextlib import contextmanager
from hashlib import sha256
from importlib import import_module

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, FormatError
from molsysmt.native import H5MSMFileHandler, Structures


@pytest.fixture(params=["0.3", "0.4"])
def legacy_file(tmp_path, request):
    path = tmp_path / "indices.h5msm"
    with h5py.File(path, "w") as file:
        file.attrs.update(type="h5msm", version=request.param, length_unit="angstrom")
        structures = file.create_group("structures")
        structures.attrs.update(n_structures_written=4)
        structures.create_dataset("coordinates", data=np.zeros((4, 2, 3)))
        structures.create_dataset("id", data=[17, 31, 8, 99])
    return path


@contextmanager
def _source(path, route):
    if route == "file":
        yield path
    else:
        with H5MSMFileHandler(path) as handler:
            yield handler
            assert handler.file, "Queries must leave caller-owned handlers open."


@pytest.mark.parametrize("route", ["file", "handler"])
@pytest.mark.parametrize(
    ("requested", "expected"),
    [
        ("all", [0, 1, 2, 3]),
        (0, [0]),
        ([3, 0, 3, 1], [3, 0, 3, 1]),
        (range(1, 4, 2), [1, 3]),
        ([], []),
        (None, None),
    ],
)
def test_structure_indices_preserve_requested_axis(
    legacy_file, route, requested, expected
):
    before = sha256(legacy_file.read_bytes()).hexdigest()
    with _source(legacy_file, route) as source:
        observed = msm.get(source, structure_indices=requested, structure_index=True)
    assert observed == expected
    assert observed is None or isinstance(observed, list)
    assert sha256(legacy_file.read_bytes()).hexdigest() == before


@pytest.mark.parametrize("route", ["file", "handler"])
@pytest.mark.parametrize("requested", [-1, 4, [0, 4], True, [False, 1], [0.5], [[0]]])
def test_invalid_structure_indices_rejected(legacy_file, route, requested):
    with _source(legacy_file, route) as source:
        with pytest.raises(ArgumentError, match="structure_indices"):
            msm.get(source, structure_indices=requested, structure_index=True)


@pytest.mark.parametrize("route", ["file", "handler"])
def test_index_query_never_reads_dataset_payload(legacy_file, route, monkeypatch):
    def forbid_payload(*args, **kwargs):
        pytest.fail("An index query must not materialize any HDF5 dataset.")

    monkeypatch.setattr(h5py.Dataset, "__getitem__", forbid_payload)
    with _source(legacy_file, route) as source:
        assert msm.get(source, structure_indices=[3, 1, 3], structure_index=True) == [
            3,
            1,
            3,
        ]


def test_original_bundled_file_query():
    source = msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"]
    assert msm.get(source, structure_indices=0, structure_index=True) == [0]


@pytest.mark.parametrize("route", ["file", "handler"])
def test_zero_written_structures_return_empty_axis(legacy_file, route):
    with h5py.File(legacy_file, "r+") as file:
        file["structures"].attrs["n_structures_written"] = 0
    with _source(legacy_file, route) as source:
        assert msm.get(source, structure_index=True) == []
        with pytest.raises(ArgumentError, match="structure_indices"):
            msm.get(source, structure_indices=0, structure_index=True)


def test_direct_file_getter_closes_owned_handler_on_error(legacy_file, monkeypatch):
    from molsysmt.form.file_h5msm import get_structure_index_from_system

    conversion = import_module("molsysmt.form.file_h5msm.to_molsysmt_H5MSMFileHandler")
    handler = H5MSMFileHandler(legacy_file)
    monkeypatch.setattr(
        conversion, "to_molsysmt_H5MSMFileHandler", lambda *a, **k: handler
    )
    try:
        with pytest.raises(ArgumentError, match="structure_indices"):
            get_structure_index_from_system(legacy_file, structure_indices=[4])
        assert not handler.file
    finally:
        handler.close()


def test_index_query_retains_legacy_unit_validation(legacy_file):
    with h5py.File(legacy_file, "r+") as file:
        file["structures/coordinates"].attrs["unit"] = "nm"
    before = sha256(legacy_file.read_bytes()).hexdigest()
    with pytest.raises(FormatError, match="Conflicting unit declarations"):
        msm.get(legacy_file, structure_index=True)
    assert sha256(legacy_file.read_bytes()).hexdigest() == before


@pytest.mark.parametrize("requested", ["all", [3, 0, 3], [], None])
def test_modular_query_retains_resident_parity(tmp_path, requested):
    structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((4, 2, 3)), "angstrom")
    )
    path = tmp_path / "modular.h5msm"
    msm.convert(structures, to_form="file:h5msm", output_filename=path)
    before = sha256(path.read_bytes()).hexdigest()
    assert msm.get(path, structure_indices=requested, structure_index=True) == msm.get(
        structures, structure_indices=requested, structure_index=True
    )
    assert sha256(path.read_bytes()).hexdigest() == before
