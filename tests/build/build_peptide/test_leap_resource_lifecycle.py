"""Scratch ownership at the public LEaP peptide-building boundary."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

import molsysmt as msm


@pytest.mark.parametrize("stage", ["setup", "run", "convert", "success"])
def test_leap_builder_retires_owned_scratch(monkeypatch, tmp_path, stage):
    """Retire intermediate files when preparation, execution or conversion fails."""
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    monkeypatch.setattr("tempfile.tempdir", str(scratch))
    observed = {}
    tleap = MagicMock()

    def prepare(unit_name, filename):
        observed["directory"] = Path(filename).parent
        assert observed["directory"].is_dir()
        if stage == "setup":
            raise RuntimeError("setup failed")

    def run(working_directory, verbose):
        assert Path(working_directory) == observed["directory"]
        if stage == "run":
            raise RuntimeError("run failed")

    output = object()

    def convert(files, to_form):
        assert all(Path(file).parent == observed["directory"] for file in files)
        assert observed["directory"].exists()
        if stage == "convert":
            raise RuntimeError("convert failed")
        return output

    tleap.save_unit.side_effect = prepare
    tleap.run.side_effect = run
    monkeypatch.setattr("molsysmt.third_party.tleap.TLeap", lambda: tleap)
    monkeypatch.setattr("molsysmt.basic.convert", convert)
    if stage == "success":
        assert (
            msm.build.build_peptide("GG", engine="LEaP", to_form="molsysmt.Structures")
            is output
        )
    else:
        with pytest.raises(RuntimeError, match=f"{stage} failed"):
            msm.build.build_peptide("GG", engine="LEaP", to_form="molsysmt.Structures")
    assert not observed["directory"].exists()
    assert list(scratch.iterdir()) == []
