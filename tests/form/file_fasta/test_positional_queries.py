"""Checking source chain/entity positions for sequence-only files."""

from importlib import import_module

import numpy as np
import pytest

import molsysmt as msm


@pytest.fixture(params=["fasta", "pir"])
def sequence_file(request, tmp_path):
    pytest.importorskip("Bio")
    from Bio import SeqIO
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord

    records = [
        SeqRecord(Seq("ACD"), id="alpha", description="first chain"),
        SeqRecord(Seq("GK"), id="beta", description="second chain"),
    ]
    path = tmp_path / f"sequences.{request.param}"
    SeqIO.write(records, path, request.param)
    return str(path), request.param


@pytest.mark.parametrize("element", ["chain", "entity"])
@pytest.mark.parametrize(
    "selection, expected", [("all", [0, 1]), ([1, 0, 1], [1, 0, 1]), ([], [])]
)
def test_positional_queries_preserve_source_order(
    sequence_file, element, selection, expected
):
    path, _ = sequence_file
    attribute = f"{element}_index"
    assert (
        msm.get(path, element=element, selection=selection, **{attribute: True})
        == expected
    )
    result = msm.get(
        path,
        element=element,
        selection=selection,
        output_type="dictionary",
        **{attribute: True, f"{element}_id": True},
    )
    assert result[attribute] == expected
    assert result[f"{element}_id"] == [["alpha", "beta"][i] for i in expected]


@pytest.mark.parametrize("element", ["chain", "entity"])
def test_adapter_indices_accept_arrays_and_none(sequence_file, element):
    path, extension = sequence_file
    adapter = import_module(f"molsysmt.form.file_{extension}")
    getter = getattr(adapter, f"get_{element}_index_from_{element}")
    assert getter(path, indices=np.array([1, 0, 1])) == [1, 0, 1]
    assert getter(path, indices=None) is None


def test_empty_sequence_file_has_empty_positional_axes(sequence_file):
    path, _ = sequence_file
    from pathlib import Path

    Path(path).write_text("", encoding="utf-8")
    for element in ("chain", "entity"):
        assert msm.get(path, element=element, **{f"{element}_index": True}) == []
