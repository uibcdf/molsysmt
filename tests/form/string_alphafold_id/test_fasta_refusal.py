"""Reject an unimplemented export before reporting a fictitious output file."""

import io
from importlib import import_module

import pytest

import molsysmt as msm
from molsysmt._private.smonitor import NotImplementedConversionError


@pytest.mark.parametrize("entry", ["adapter", "public"])
@pytest.mark.parametrize("existing", [False, True])
def test_unsupported_fasta_export_refuses_without_io(
    monkeypatch, tmp_path, entry, existing
):
    target = tmp_path / "model.fasta"
    if existing:
        target.write_bytes(b"caller-owned output\n")
    calls = []

    def remote(*args, **kwargs):
        calls.append((args, kwargs))
        return io.BytesIO(b"<html>synthetic entry</html>")

    monkeypatch.setattr("urllib.request.urlopen", remote)
    with pytest.raises(NotImplementedConversionError):
        if entry == "public":
            msm.convert(
                "AF-P05067-F1", to_form="file:fasta", output_filename=str(target)
            )
        else:
            module = import_module("molsysmt.form.string_alphafold_id.to_file_fasta")
            module.to_file_fasta("AF-P05067-F1", output_filename=str(target))
    assert calls == []
    assert target.exists() is existing
    if existing:
        assert target.read_bytes() == b"caller-owned output\n"
