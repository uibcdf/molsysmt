"""PDB copies accept the dispatcher filename and preserve the input bytes."""

import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt.form.file_pdb.to_file_pdb import to_file_pdb
from tests.conversion_truth.test_declared_pdb_edges import _pdb_text


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("argument", ["output_filename", "output_name"])
def test_pdb_identity_conversion_copies_to_explicit_path(tmp_path, route, argument):
    source = tmp_path / "source.pdb"
    target = tmp_path / "copy.pdb"
    source.write_text(_pdb_text())
    kwargs = {argument: str(target)}
    result = (
        to_file_pdb(str(source), **kwargs)
        if route == "direct"
        else msm.convert(str(source), to_form="file:pdb", **kwargs)
    )
    assert result == str(target)
    assert target.read_bytes() == source.read_bytes() == _pdb_text().encode()


def test_pdb_copy_rejects_two_destination_arguments(tmp_path):
    source = tmp_path / "source.pdb"
    source.write_text(_pdb_text())
    with pytest.raises(ArgumentError, match="Supply only"):
        to_file_pdb(
            str(source),
            output_filename=str(tmp_path / "first.pdb"),
            output_name=str(tmp_path / "second.pdb"),
        )
    assert not (tmp_path / "first.pdb").exists()
    assert not (tmp_path / "second.pdb").exists()


def test_pdb_copy_retains_original_positional_destination(tmp_path):
    source = tmp_path / "source.pdb"
    target = tmp_path / "copy.pdb"
    source.write_text(_pdb_text())
    assert to_file_pdb(str(source), "all", "all", str(target), True, False) == str(
        target
    )
    assert target.read_bytes() == source.read_bytes()


def test_pdb_copy_keeps_legacy_slot_and_adds_only_a_destination_keyword():
    from inspect import Parameter, signature

    parameters = signature(to_file_pdb).parameters
    positional = [
        name
        for name, value in parameters.items()
        if value.kind == Parameter.POSITIONAL_OR_KEYWORD
    ]
    assert positional == [
        "item",
        "atom_indices",
        "structure_indices",
        "output_name",
        "copy_if_all",
        "skip_digestion",
    ]
    assert parameters["output_filename"].kind == Parameter.KEYWORD_ONLY
