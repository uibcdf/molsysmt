"""Protect gzip PDB parity, scientific policy and independent read lifetimes."""

import gzip
import hashlib
import io
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import FileContentError


@pytest.fixture()
def compressed(t4_pdb_file, tmp_path):
    source = Path(t4_pdb_file).read_bytes()
    path = tmp_path / "observed.pdb.gz"
    path.write_bytes(gzip.compress(source, mtime=0))
    return path, source


@pytest.mark.parametrize("as_string", [False, True])
@pytest.mark.parametrize(
    "to_form", ["molsysmt.MolSys", "molsysmt.Topology", "molsysmt.Structures"]
)
def test_plain_compressed_parity_preserves_selection_and_units(
    compressed, tmp_path, as_string, to_form
):
    path, text = compressed
    plain = tmp_path / "observed.pdb"
    plain.write_bytes(text)
    options = dict(to_form=to_form, selection=[4, 0, 2], structure_indices=[0])
    if to_form != "molsysmt.Structures":
        options["get_missing_bonds"] = False
    with msm.pyunitwizard.context(standard_units=["angstrom", "ps"]):
        expected = msm.convert(plain, **options)
        observed = msm.convert(str(path) if as_string else path, **options)
    assert msm.get_form(path) == "file:pdb.gz"
    assert msm.get_form(path.with_name("OBSERVED.PDB.GZ")) == "file:pdb.gz"
    if to_form != "molsysmt.Structures":
        a = observed.topology if to_form == "molsysmt.MolSys" else observed
        b = expected.topology if to_form == "molsysmt.MolSys" else expected
        for table in [
            "atoms",
            "groups",
            "chains",
            "components",
            "molecules",
            "entities",
            "bonds",
        ]:
            pd.testing.assert_frame_equal(getattr(a, table), getattr(b, table))
        assert all(isinstance(value, str) for value in a.atoms.atom_id)
    if to_form != "molsysmt.Topology":
        a = observed.structures if to_form == "molsysmt.MolSys" else observed
        b = expected.structures if to_form == "molsysmt.MolSys" else expected
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(a.coordinates, to_unit="angstrom"),
            msm.pyunitwizard.get_value(b.coordinates, to_unit="angstrom"),
        )
        assert msm.pyunitwizard.get_unit(a.coordinates) == msm.pyunitwizard.get_unit(
            b.coordinates
        )
    assert path.read_bytes() == gzip.compress(text, mtime=0)
    assert plain.read_bytes() == text


def test_real_3ptb_declared_connectivity_has_independent_literal_truth():
    path = Path(__file__).with_name("data") / "3PTB.pdb.gz"
    before = path.read_bytes()
    assert (
        hashlib.sha256(gzip.decompress(before)).hexdigest()
        == "288f7954d4d013fa8eab3808e1037e2958e2dcd12c9eca65a3f1014404a9f9a2"
    )
    molsys = msm.convert(path, to_form="molsysmt.MolSys", get_missing_bonds=False)
    assert msm.get(
        molsys, n_atoms=True, n_groups=True, n_structures=True, n_bonds=True
    ) == [1701, 287, 1, 21]
    protein = msm.extract(molsys, selection='molecule_type=="protein"')
    assert protein.topology.n_atoms == 1629
    assert protein.topology.n_groups == 223
    names = protein.topology.atoms.atom_name
    assert (
        sum(
            names[a] == names[b] == "SG"
            for a, b in protein.topology.bonds[
                ["atom1_index", "atom2_index"]
            ].itertuples(index=False, name=None)
        )
        == 6
    )
    assert path.read_bytes() == before


def test_get_and_raw_text_use_native_delivery_without_rewriting(compressed):
    path, text = compressed
    raw = msm.convert(path, to_form="string:pdb_text")
    assert raw == text.decode("utf-8")
    assert msm.get(path, n_atoms=True, n_structures=True) == [1441, 1]
    coordinates = msm.get(
        path, selection=[2, 0], structure_indices=[0], coordinates=True
    )
    assert coordinates.shape == (1, 2, 3)


@pytest.mark.parametrize("engine", [None, "MolSysMT", "OpenMM"])
def test_connectivity_engine_policy_matches_plain_pdb(
    builder_pdb_text, tmp_path, engine
):
    plain = tmp_path / "policy.pdb"
    path = tmp_path / "policy.pdb.gz"
    plain.write_text(builder_pdb_text)
    path.write_bytes(gzip.compress(builder_pdb_text.encode()))
    options = dict(
        to_form="molsysmt.MolSys", get_missing_bonds=True, bond_inference_engine=engine
    )
    expected = msm.convert(plain, **options)
    observed = msm.convert(path, **options)
    pd.testing.assert_frame_equal(observed.topology.bonds, expected.topology.bonds)
    from molsysmt._private.smonitor import ArgumentConflictError

    with pytest.raises(ArgumentConflictError):
        msm.convert(
            path,
            to_form="molsysmt.MolSys",
            get_missing_bonds=False,
            bond_inference_engine="MolSysMT",
        )


def test_nonconsecutive_repeated_structure_indices_match_plain_pdb(
    compressed, tmp_path
):
    _, text = compressed
    atom_lines = [
        line
        for line in text.decode().splitlines(keepends=True)
        if line.startswith(("ATOM  ", "HETATM"))
    ][:3]
    models = []
    for model in range(3):
        shifted = []
        for line in atom_lines:
            shifted.append(line[:30] + f"{float(line[30:38]) + model:8.3f}" + line[38:])
        models.extend([f"MODEL     {model + 1:4d}\n", *shifted, "ENDMDL\n"])
    payload = ("".join(models) + "END\n").encode()
    plain = tmp_path / "models.pdb"
    compressed_path = tmp_path / "models.pdb.gz"
    plain.write_bytes(payload)
    compressed_path.write_bytes(gzip.compress(payload))
    options = dict(
        to_form="molsysmt.Structures", selection=[2, 0], structure_indices=[2, 0, 2]
    )
    expected = msm.convert(plain, **options)
    observed = msm.convert(compressed_path, **options)
    actual = msm.pyunitwizard.get_value(observed.coordinates, to_unit="angstrom")
    np.testing.assert_array_equal(
        actual, msm.pyunitwizard.get_value(expected.coordinates, to_unit="angstrom")
    )
    assert actual.shape == (3, 2, 3)
    np.testing.assert_array_equal(actual[0], actual[2])
    np.testing.assert_allclose(actual[0, :, 0] - actual[1, :, 0], 2.0)


@pytest.mark.parametrize("failure", ["header", "truncated", "crc", "encoding"])
def test_bad_gzip_is_diagnosed_before_inference(failure, tmp_path, monkeypatch):
    import molsysmt.native as native

    called = []
    monkeypatch.setattr(
        native,
        "PDBFileHandler",
        lambda *a, **k: called.append(True),
    )
    data = gzip.compress(b"END\n")
    if failure == "header":
        data = b"not gzip"
    elif failure == "truncated":
        data = data[:-4]
    elif failure == "crc":
        data = data[:-8] + bytes([data[-8] ^ 1]) + data[-7:]
    else:
        data = gzip.compress(b"\xff\n")
    path = tmp_path / "bad.pdb.gz"
    path.write_bytes(data)
    with pytest.raises(FileContentError) as observed:
        msm.convert(path, to_form="molsysmt.MolSys", get_missing_bonds=False)
    assert observed.value.__cause__ is not None
    assert observed.value.extra["filename"] == str(path)
    assert not called
    assert path.read_bytes() == data
    assert list(tmp_path.iterdir()) == [path]


def test_native_handler_owns_buffer_and_closes_it_on_parse_failure(
    compressed, monkeypatch
):
    from molsysmt.native import PDBFileHandler

    path, _ = compressed
    handler = msm.convert(path, to_form="molsysmt.PDBFileHandler")
    assert not handler.file.closed
    handler.close()
    assert handler.file.closed
    buffers = []

    def fail(self):
        buffers.append(self.file)
        raise RuntimeError("Forced PDB parse failure")

    monkeypatch.setattr(PDBFileHandler, "load", fail)
    with pytest.raises(RuntimeError, match="Forced PDB parse failure"):
        msm.convert(path, to_form="molsysmt.MolSys", get_missing_bonds=False)
    assert buffers and all(buffer.closed for buffer in buffers)


def test_conversion_failure_closes_handler(compressed, monkeypatch):
    from importlib import import_module

    module = import_module("molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_MolSys")

    path, _ = compressed
    handlers = []

    def fail(handler, **kwargs):
        handlers.append(handler)
        raise RuntimeError("Forced native conversion failure")

    monkeypatch.setattr(module, "to_molsysmt_MolSys", fail)
    with pytest.raises(RuntimeError, match="Forced native conversion failure"):
        msm.convert(path, to_form="molsysmt.MolSys", get_missing_bonds=False)
    assert handlers and all(handler.file.closed for handler in handlers)


def test_concurrent_reads_do_not_write_into_read_only_input_directory(
    compressed, monkeypatch
):
    from molsysmt.form.file_pdb_gz import _read

    path, text = compressed
    before = path.read_bytes()
    neighbor = path.with_suffix("")
    neighbor.write_bytes(b"Independent PDB neighbor")
    original_open = io.open
    read_text = _read.read_text
    barrier = Barrier(2)

    def deny_writes(filename, mode="r", *args, **kwargs):
        if set(mode).intersection("wax+") and not isinstance(filename, int):
            if Path(filename).resolve().is_relative_to(path.parent.resolve()):
                raise PermissionError("Input directory is read-only")
        return original_open(filename, mode, *args, **kwargs)

    def overlap(item):
        result = read_text(item)
        barrier.wait(timeout=15)
        return result

    monkeypatch.setattr(io, "open", deny_writes)
    monkeypatch.setattr(_read, "read_text", overlap)
    path.parent.chmod(0o555)
    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(
                    msm.convert,
                    path,
                    to_form="molsysmt.MolSys",
                    get_missing_bonds=False,
                )
                for _ in range(2)
            ]
            outputs = [future.result(timeout=30) for future in futures]
    finally:
        path.parent.chmod(0o755)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(outputs[0].structures.coordinates),
        msm.pyunitwizard.get_value(outputs[1].structures.coordinates),
    )
    assert path.read_bytes() == before
    assert neighbor.read_bytes() == b"Independent PDB neighbor"
    assert set(path.parent.iterdir()) == {path, neighbor}
    outputs[0].topology.atoms.at[0, "atom_name"] = "changed"
    assert outputs[1].topology.atoms.at[0, "atom_name"] != "changed"
