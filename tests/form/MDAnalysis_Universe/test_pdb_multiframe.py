"""Protecting the public PDB boolean switch before writer side effects."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from tests.conversion_truth.test_declared_native_edges import _source


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("flag", [0, 1, "no", None, []])
def test_multiframe_rejects_nonboolean_before_writer_or_destination_changes(
    route, flag, tmp_path, monkeypatch
):
    mda = pytest.importorskip("MDAnalysis")
    from molsysmt.form.MDAnalysis_Universe.to_file_pdb import to_file_pdb

    source = _source("MDAnalysis.Universe")
    output = tmp_path / "guard.pdb"
    output.write_bytes(b"existing destination must survive")

    def forbidden(*args, **kwargs):
        raise AssertionError("Invalid multiframe reached the external writer")

    monkeypatch.setattr(mda.core.groups.AtomGroup, "write", forbidden)
    with pytest.raises(ArgumentError):
        if route == "direct":
            to_file_pdb(source, output_filename=output, multiframe=flag)
        else:
            msm.convert(
                source, to_form="file:pdb", output_filename=output, multiframe=flag
            )
    assert output.read_bytes() == b"existing destination must survive"


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("flag", [True, False])
def test_multiframe_true_and_false_write_the_selected_structures(route, flag, tmp_path):
    pytest.importorskip("MDAnalysis")
    from molsysmt.form.MDAnalysis_Universe.to_file_pdb import to_file_pdb

    source = _source("MDAnalysis.Universe")
    output = tmp_path / "poses.pdb"
    selected = [0, 1] if flag else [1]
    kwargs = dict(
        output_filename=str(output), structure_indices=selected, multiframe=flag
    )
    result = (
        to_file_pdb(source, **kwargs)
        if route == "direct"
        else msm.convert(source, to_form="file:pdb", **kwargs)
    )
    assert str(result) == str(output)
    text = output.read_text()
    assert sum(line.startswith("MODEL") for line in text.splitlines()) == (
        2 if flag else 0
    )
    records = [line for line in text.splitlines() if line.startswith("ATOM")]
    assert len(records) == (6 if flag else 3)
    if not flag:
        np.testing.assert_allclose(
            [float(records[0][s : s + 8]) for s in (30, 38, 46)], [1.0, 2.0, 3.0]
        )
