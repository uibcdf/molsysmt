"""Verifying eager topology custody without requiring a PyTraj installation."""

from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize("stage", ["write", "read", "bonds", "cleanup", "success"])
def test_pytraj_bridge_retires_intermediates(monkeypatch, tmp_path, stage):
    import shutil

    scratch = tmp_path / "scratch"
    scratch.mkdir()
    monkeypatch.setattr("tempfile.tempdir", str(scratch))
    observed = {}
    error = (
        OSError("cleanup denied")
        if stage == "cleanup"
        else RuntimeError(f"{stage} failed")
    )

    class EagerTopology:
        @property
        def bond_indices(self):
            assert observed["file"].is_file()
            if stage == "bonds":
                raise error
            return np.array([[1, 2], [3, 0]], dtype=int)

    def convert(item, to_form, **kwargs):
        if to_form == "pytraj.Topology":
            assert Path(item) == observed["file"]
            assert observed["file"].read_text() == "partial intermediate\n"
            if stage == "read":
                raise error
            return EagerTopology()
        path = Path(to_form)
        observed["file"] = path
        path.write_text("partial intermediate\n")
        if stage == "write":
            raise error
        return str(path)

    monkeypatch.setattr("molsysmt.basic.convert", convert)
    monkeypatch.setattr(
        "molsysmt.basic.get", lambda *args, **kwargs: np.array([[2, 1]])
    )
    options = {
        "engine": "pytraj",
        "max_bond_length": puw.quantity(2, "angstrom"),
        "skip_digestion": True,
    }

    def reject_retirement(*args, **kwargs):
        raise error

    with monkeypatch.context() as disposal:
        if stage == "cleanup":
            disposal.setattr(shutil, "rmtree", reject_retirement)
        if stage == "success":
            assert msm.build.get_missing_bonds(object(), **options) == [[0, 3]]
        else:
            with pytest.raises(type(error)) as caught:
                msm.build.get_missing_bonds(object(), **options)
            assert caught.value is error
    if stage == "cleanup":
        assert observed["file"].exists()
        for directory in scratch.iterdir():
            shutil.rmtree(directory)
    assert not observed["file"].exists()
    assert list(scratch.iterdir()) == []
