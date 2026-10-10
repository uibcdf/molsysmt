"""Keeping remote downloads private until extraction succeeds."""

import io
import json
from importlib import import_module
from pathlib import Path

import pytest


@pytest.mark.parametrize("extension", ["pdb", "cif", "bcif", "cif_gz", "bcif_gz"])
@pytest.mark.parametrize("destination_kind", ["absent", "existing", "default"])
def test_pdb_id_extraction_failure_preserves_destination(
    monkeypatch, tmp_path, extension, destination_kind
):
    import molsysmt._private.download as download

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        download, "urlopen", lambda *args, **kwargs: io.BytesIO(b"downloaded")
    )
    suffix = extension.replace("_", ".")
    destination = tmp_path / (
        f"181l.{suffix}" if destination_kind == "default" else f"caller.{suffix}"
    )
    if destination_kind != "absent":
        destination.write_bytes(b"caller evidence")
    adapter = import_module(f"molsysmt.form.string_pdb_id.to_file_{extension}")
    from molsysmt._private.smonitor import NotImplementedMethodError

    with pytest.raises(NotImplementedMethodError):
        getattr(adapter, f"to_file_{extension}")(
            "pdb_id:181l",
            atom_indices=[0],
            output_filename=None if destination_kind == "default" else str(destination),
            skip_digestion=True,
        )
    if destination_kind == "absent":
        assert list(tmp_path.iterdir()) == []
    else:
        assert destination.read_bytes() == b"caller evidence"
        assert list(tmp_path.iterdir()) == [destination]


@pytest.mark.parametrize("extension", ["pdb", "cif", "bcif", "cif_gz", "bcif_gz"])
def test_pdb_id_success_preserves_default_name(monkeypatch, tmp_path, extension):
    import molsysmt._private.download as download

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        download, "urlopen", lambda *args, **kwargs: io.BytesIO(b"downloaded")
    )
    adapter = import_module(f"molsysmt.form.string_pdb_id.to_file_{extension}")
    result = getattr(adapter, f"to_file_{extension}")(
        "pdb_id:181l", skip_digestion=True
    )
    assert result == f"181l.{extension.replace('_', '.')}"
    assert Path(result).read_bytes() == b"downloaded"
    assert list(tmp_path.iterdir()) == [tmp_path / result]


@pytest.mark.parametrize("extension", ["pdb", "bcif"])
@pytest.mark.parametrize("stage", ["download", "extract", "success"])
def test_alphafold_publication_waits_for_extraction(
    monkeypatch, tmp_path, extension, stage
):
    import urllib.request

    monkeypatch.chdir(tmp_path)
    destination = tmp_path / f"model.{extension}"
    destination.write_bytes(b"caller evidence")
    response = io.BytesIO(
        json.dumps(
            [{f"{extension}Url": f"https://example.org/model.{extension}"}]
        ).encode()
    )
    response.status = 200
    monkeypatch.setattr(urllib.request, "urlopen", lambda *args, **kwargs: response)
    error = RuntimeError("download interrupted")

    def retrieve(url, filename):
        Path(filename).write_bytes(b"downloaded")
        if stage == "download":
            raise error

    monkeypatch.setattr(urllib.request, "urlretrieve", retrieve)
    adapter = import_module(f"molsysmt.form.string_alphafold_id.to_file_{extension}")
    from molsysmt._private.smonitor import NotImplementedMethodError

    arguments = dict(
        atom_indices=[0] if stage == "extract" else "all", skip_digestion=True
    )
    if stage == "success":
        assert (
            getattr(adapter, f"to_file_{extension}")(
                "alphafold_id:AF-P12345-F1", **arguments
            )
            == destination.name
        )
        assert destination.read_bytes() == b"downloaded"
    else:
        with pytest.raises(
            RuntimeError if stage == "download" else NotImplementedMethodError
        ) as caught:
            getattr(adapter, f"to_file_{extension}")(
                "alphafold_id:AF-P12345-F1", **arguments
            )
        if stage == "download":
            assert caught.value is error
        assert destination.read_bytes() == b"caller evidence"
    assert list(tmp_path.iterdir()) == [destination]
