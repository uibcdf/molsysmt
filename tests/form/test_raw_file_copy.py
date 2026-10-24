"""Keep raw file-copy adapters on one explicit-destination filesystem contract."""

import importlib
import os
from pathlib import Path

import pytest

from molsysmt._private.smonitor import ArgumentError, FormatError

RAW_FORMS = [
    "crd",
    "dcd",
    "fasta",
    "gro",
    "h5",
    "h5msm",
    "inpcrd",
    "mdcrd",
    "pdb",
    "pir",
    "prmtop",
    "psf",
    "smi",
    "top",
    "trjpk",
    "xtc",
    "xyz",
    "xyznpy",
]


@pytest.mark.parametrize("form", RAW_FORMS)
def test_raw_adapters_copy_opaque_bytes_and_reject_source_aliases(form, tmp_path):
    # These routes copy bytes without certifying molecular syntax. Validated
    # PDBQT/SDF envelopes keep their own separate consumers and tests.
    copy = importlib.import_module(f"molsysmt.form.file_{form}.copy").copy
    source, destination = tmp_path / f"source.{form}", tmp_path / f"copy.{form}"
    payload = b"opaque molecular-format payload\x00\xff\n" * 100
    source.write_bytes(payload)
    automatic = copy(str(source), skip_digestion=True)
    assert not os.path.samefile(source, automatic)
    assert os.path.splitext(automatic)[1] == source.suffix
    assert Path(automatic).read_bytes() == payload
    with pytest.raises(ArgumentError, match="output_filename"):
        copy(str(source), output_filename=str(source), skip_digestion=True)
    assert copy(
        str(source), output_filename=str(destination), skip_digestion=True
    ) == str(destination)
    assert destination.read_bytes() == payload == source.read_bytes()
    assert not os.path.samefile(source, destination)
    # Keep the existing explicit-overwrite contract for a distinct file.
    destination.write_bytes(b"old contents")
    copy(str(source), output_filename=str(destination), skip_digestion=True)
    assert destination.read_bytes() == payload == source.read_bytes()


@pytest.mark.parametrize("form", ["sdf", "pdbqt"])
@pytest.mark.parametrize("alias", ["same", "hardlink"])
def test_validating_adapters_check_destination_before_decoding(form, alias, tmp_path):
    copy = importlib.import_module(f"molsysmt.form.file_{form}.copy").copy
    source = tmp_path / f"source.{form}"
    source.write_bytes(b"Not yet decoded: invalid destinations reject first.")
    destination = str(source)
    if alias == "hardlink":
        target = tmp_path / f"linked.{form}"
        try:
            os.link(source, target)
        except (OSError, NotImplementedError) as error:
            pytest.skip(f"Filesystem does not support hard links: {error}")
        destination = str(target)
    before = source.read_bytes()
    with pytest.raises(ArgumentError, match="output_filename"):
        copy(str(source), output_filename=destination, skip_digestion=True)
    assert source.read_bytes() == before


@pytest.mark.parametrize("form", ["sdf", "pdbqt"])
def test_validating_adapter_failure_retires_its_automatic_reservation(
    form, tmp_path, monkeypatch
):
    from molsysmt._private import session_files

    copy = importlib.import_module(f"molsysmt.form.file_{form}.copy").copy
    source = tmp_path / f"invalid.{form}"
    source.write_text("invalid molecular contents\n")
    before = set(session_files._paths)
    allocated = []
    reserve = session_files.reserve_copy_path

    def record(source):
        path = reserve(source)
        allocated.append(path)
        return path

    monkeypatch.setattr(session_files, "reserve_copy_path", record)
    with pytest.raises(FormatError):
        copy(str(source), skip_digestion=True)
    assert len(allocated) == 1
    assert not Path(allocated[0]).exists()
    assert session_files._paths == before


@pytest.mark.parametrize("form", ["sdf", "pdbqt"])
def test_validated_automatic_copies_keep_real_source_bytes(form, tmp_path):
    sdf = (
        "carbon\n  MolSysMT\n\n"
        "  1  0  0  0  0  0  0  0  0  0999 V2000\n"
        "    0.0000    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n"
        "M  END\n$$$$\n"
    )
    pdbqt = "ATOM     17   C1 LIG B   7       1.000   2.000   3.000  1.00 20.00     0.125 C\nEND\n"
    source = tmp_path / f"source.{form}"
    source.write_text(sdf if form == "sdf" else pdbqt)
    result = importlib.import_module(f"molsysmt.form.file_{form}.copy").copy(
        str(source)
    )
    assert Path(result).read_bytes() == source.read_bytes()
    assert not os.path.samefile(source, result)
