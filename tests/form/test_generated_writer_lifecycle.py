"""Distinguishing generated writer custody from explicitly requested outputs."""

import io
from importlib import import_module
from pathlib import Path

import pytest


class FailingWriter:
    def __init__(self, file, error, stage):
        self.file = file
        self.error = error
        self.stage = stage

    def __enter__(self):
        return self

    def write(self, content):
        self.file.write(content[:4])
        if self.stage == "write":
            raise self.error

    def __exit__(self, *args):
        self.file.close()
        if self.stage == "close":
            raise self.error


@pytest.mark.parametrize("form", ["pdb_text", "uniprot_id"])
@pytest.mark.parametrize("generated", [False, True])
@pytest.mark.parametrize("stage", ["write", "close"])
@pytest.mark.parametrize("error_type", [OSError, KeyboardInterrupt])
def test_failed_writer_retires_generated_outputs_only(
    monkeypatch, tmp_path, form, generated, stage, error_type
):
    import os
    import urllib.request

    scratch = tmp_path / "scratch"
    scratch.mkdir()
    monkeypatch.setattr("tempfile.tempdir", str(scratch))
    monkeypatch.setattr(
        urllib.request,
        "urlopen",
        lambda *args, **kwargs: io.BytesIO(b">P12345\nACDE\n"),
    )
    extension = "pdb" if form == "pdb_text" else "fasta"
    adapter = import_module(f"molsysmt.form.string_{form}.to_file_{extension}")
    error = error_type(f"{stage} failed")
    original_open = open

    def fail_open(*args, **kwargs):
        return FailingWriter(original_open(*args, **kwargs), error, stage)

    monkeypatch.setattr(adapter, "open", fail_open, raising=False)
    original_fdopen = os.fdopen
    monkeypatch.setattr(
        os,
        "fdopen",
        lambda *args, **kwargs: FailingWriter(
            original_fdopen(*args, **kwargs), error, stage
        ),
    )
    destination = tmp_path / f"caller.{extension}"
    destination.write_text("caller result\n")
    item = "HEADER    TEST\nEND\n" if form == "pdb_text" else "uniprot_id:P12345"
    with pytest.raises(error_type) as caught:
        getattr(adapter, f"to_file_{extension}")(
            item,
            output_filename=None if generated else str(destination),
            skip_digestion=True,
        )
    assert caught.value is error
    assert list(scratch.iterdir()) == []
    assert destination.read_text() == (
        "caller result\n" if generated else item[:4] if form == "pdb_text" else ">P12"
    )


@pytest.mark.parametrize("form", ["pdb_text", "uniprot_id"])
def test_generated_success_survives_public_adapter(monkeypatch, tmp_path, form):
    import urllib.request

    import molsysmt as msm

    monkeypatch.setattr("tempfile.tempdir", str(tmp_path))
    monkeypatch.setattr(
        urllib.request,
        "urlopen",
        lambda *args, **kwargs: io.BytesIO(b">P12345\nACDE\n"),
    )
    if form == "pdb_text":
        item = Path(msm.systems["T4 lysozyme L99A"]["181l.pdb"]).read_text()
        expected = item
        target = "file:pdb"
    else:
        item = "uniprot_id:P12345"
        expected = ">P12345\nACDE\n"
        target = "file:fasta"
    extension = target.split(":")[1]
    adapter = import_module(f"molsysmt.form.string_{form}.to_file_{extension}")
    result = Path(getattr(adapter, f"to_file_{extension}")(item))
    assert result.read_text() == expected
    assert list(tmp_path.iterdir()) == [result]

    explicit_destination = tmp_path / f"requested.{extension}"
    assert msm.convert(
        item, to_form=target, output_filename=str(explicit_destination)
    ) == str(explicit_destination)
    assert explicit_destination.read_text() == expected


def test_generated_writer_exposes_retirement_failure(monkeypatch, tmp_path):
    monkeypatch.setattr("tempfile.tempdir", str(tmp_path))
    adapter = import_module("molsysmt.form.string_pdb_text.to_file_pdb")
    error = OSError("write denied")

    def reject_write(*args, **kwargs):
        Path(args[0]).touch()
        raise error

    def reject_unlink(*args, **kwargs):
        raise OSError("retirement denied")

    monkeypatch.setattr(adapter, "open", reject_write, raising=False)
    with monkeypatch.context() as retirement:
        retirement.setattr(Path, "unlink", reject_unlink)
        with pytest.raises(OSError, match="retirement denied") as caught:
            adapter.to_file_pdb("HEADER    TEST\nEND\n", skip_digestion=True)
        assert caught.value.__context__ is error
    for file in tmp_path.iterdir():
        file.unlink()


def test_uniprot_descriptor_preparation_failure_closes_owned_descriptor(
    monkeypatch, tmp_path
):
    import os
    import tempfile
    import urllib.request

    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path))
    monkeypatch.setattr(
        urllib.request,
        "urlopen",
        lambda *args, **kwargs: io.BytesIO(b">P12345\nACDE\n"),
    )
    original_mkstemp = tempfile.mkstemp
    observed = {}

    def allocate(*args, **kwargs):
        descriptor, filename = original_mkstemp(*args, **kwargs)
        observed["descriptor"] = descriptor
        return descriptor, filename

    error = OSError("descriptor wrapping failed")

    def reject(*args, **kwargs):
        raise error

    monkeypatch.setattr(tempfile, "mkstemp", allocate)
    monkeypatch.setattr(os, "fdopen", reject)
    adapter = import_module("molsysmt.form.string_uniprot_id.to_file_fasta")
    with pytest.raises(OSError) as caught:
        adapter.to_file_fasta("uniprot_id:P12345")
    assert caught.value is error
    assert list(tmp_path.iterdir()) == []
    with pytest.raises(OSError):
        os.fstat(observed["descriptor"])
