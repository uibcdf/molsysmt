"""Protect caller destinations when a legacy schema request is unsupported."""

from pathlib import Path

import h5py
import pytest

from molsysmt._private.smonitor import FormatError
from molsysmt.native import H5MSMFileHandler


@pytest.mark.parametrize("version", ["0.5", "0.6", "1.0", "9.9"])
@pytest.mark.parametrize("destination", ["new", "ordinary", "hdf5"])
def test_unsupported_version_rejects_without_opening_destination(
    tmp_path, monkeypatch, version, destination
):
    target = tmp_path / "destination.h5msm"
    if destination == "ordinary":
        target.write_bytes(b"caller data must survive rejection")
    elif destination == "hdf5":
        with H5MSMFileHandler(target, io_mode="w", format_version="0.4"):
            pass
    before = target.read_bytes() if target.exists() else None
    opened = []
    open_file = h5py.File

    def observe(*args, **kwargs):
        result = open_file(*args, **kwargs)
        opened.append(result)
        return result

    monkeypatch.setattr(h5py, "File", observe)
    try:
        with pytest.raises(FormatError, match="unsupported H5MSM version"):
            H5MSMFileHandler(target, io_mode="w", format_version=version)
    finally:
        for file in opened:
            file.close()
    assert opened == []
    if before is None:
        assert not target.exists()
    else:
        assert target.read_bytes() == before


@pytest.mark.parametrize("version", [None, "0.3", "0.4"])
def test_supported_creation_keeps_legacy_layout_and_requested_version(
    tmp_path, version
):
    target = tmp_path / "legacy.h5msm"
    with H5MSMFileHandler(target, io_mode="w", format_version=version) as handler:
        assert handler.file.id.valid
        assert handler.format_version == (version or "0.4")
        assert isinstance(handler.file["topology/atoms"], h5py.Group)
        assert isinstance(handler.file["structures/coordinates"], h5py.Dataset)
    with h5py.File(target) as stored:
        assert stored.attrs["version"] == (version or "0.4")
    assert Path(target).is_file()
