"""Independent whole-file outputs and source-safe selected coordinate exports."""

import importlib
import os
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.session_files import discard_copy
from molsysmt._private.smonitor import ArgumentError

AFFECTED = [
    "file_bcif",
    "file_bcif_gz",
    "file_cif",
    "file_cif_gz",
    "file_crd",
    "file_fasta",
    "file_gro",
    "file_h5",
    "file_inpcrd",
    "file_mdcrd",
    "file_pdb",
    "file_pir",
    "file_prmtop",
    "file_psf",
    "file_smi",
    "file_top",
    "file_xyz",
    "file_xyznpy",
]
GRO_TEXT = (
    "Local atom\n    1\n"
    "    1LIG      C    1   0.100   0.200   0.300\n"
    "   2.00000   2.00000   2.00000\n"
)


@contextmanager
def _managed_output():
    outputs = []
    try:
        yield outputs
    finally:
        for output in outputs:
            discard_copy(output)


@pytest.fixture(params=AFFECTED)
def byte_source(request, tmp_path):
    # Byte copying must not invoke a molecular decoder. These payloads are not
    # evidence that arbitrary bytes conform to any of the represented formats.
    if request.param == "file_h5":
        pytest.importorskip("mdtraj")
    adapter = importlib.import_module("molsysmt.form." + request.param)
    suffix = adapter.form_name.removeprefix("file:")
    source = tmp_path / ("input." + suffix)
    source.write_bytes(b"Original raw bytes\x00\xff\n")
    return adapter, str(source)


def test_default_whole_file_extraction_is_independent(byte_source):
    adapter, source = byte_source
    before = Path(source).read_bytes()
    with _managed_output() as outputs:
        output = adapter.extract(source)
        outputs.append(output)
        assert isinstance(output, str) and Path(output).suffix == Path(source).suffix
        assert Path(output).resolve() != Path(source).resolve()
        assert Path(output).read_bytes() == before
        Path(output).write_bytes(b"changed output")
        assert Path(source).read_bytes() == before


def test_explicit_no_copy_retains_source(byte_source):
    adapter, source = byte_source
    assert adapter.extract(source, copy_if_all=False) == source
    assert adapter.extract(source, output_filename=source, copy_if_all=False) == source


@pytest.mark.parametrize("copy_if_all", [True, False])
def test_explicit_destination_is_honored(byte_source, tmp_path, copy_if_all):
    adapter, source = byte_source
    destination = tmp_path / ("output" + "".join(Path(source).suffixes))
    output = adapter.extract(
        source, output_filename=str(destination), copy_if_all=copy_if_all
    )
    assert (
        Path(output) == destination
        and destination.read_bytes() == Path(source).read_bytes()
    )
    destination.write_bytes(b"caller-owned output")
    assert Path(source).read_bytes() == b"Original raw bytes\x00\xff\n"


@pytest.mark.parametrize("alias_kind", ["same", "symlink", "hardlink"])
def test_copying_onto_source_alias_is_rejected(byte_source, tmp_path, alias_kind):
    adapter, source = byte_source
    alias = (
        Path(source)
        if alias_kind == "same"
        else tmp_path / ("alias" + "".join(Path(source).suffixes))
    )
    if alias_kind != "same":
        try:
            (os.symlink if alias_kind == "symlink" else os.link)(source, alias)
        except (OSError, NotImplementedError) as error:
            pytest.skip(f"{alias_kind} unavailable on this test filesystem: {error}")
    with pytest.raises(ArgumentError):
        adapter.extract(source, output_filename=str(alias))
    assert Path(source).read_bytes() == b"Original raw bytes\x00\xff\n"


@pytest.mark.parametrize("suffix", ["gro", "xyz"])
def test_public_default_whole_file_extraction(tmp_path, suffix):
    source = tmp_path / ("source." + suffix)
    source.write_text(GRO_TEXT if suffix == "gro" else "1 1\n0.1 0.2 0.3\n")
    before = source.read_bytes()
    with _managed_output() as outputs:
        output = msm.extract(str(source))
        outputs.append(output)
        assert Path(output).resolve() != source.resolve()
        assert Path(output).read_bytes() == before and source.read_bytes() == before
    assert msm.extract(str(source), copy_if_all=False) == str(source)


def test_public_xyz_subset_keeps_source_and_requested_axes(tmp_path):
    source = tmp_path / "source.xyz"
    coordinates = np.arange(18, dtype=float).reshape(2, 3, 3)
    source.write_text(
        "2 3\n"
        + "".join(" ".join(map(str, row)) + "\n" for row in coordinates.reshape(-1, 3))
    )
    before = source.read_bytes()
    with _managed_output() as outputs:
        output = msm.extract(str(source), selection=[2, 0], structure_indices=[1])
        outputs.append(output)
        xyz = msm.get(output, element="atom", coordinates=True)
        assert xyz.shape == (1, 2, 3)
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(xyz, to_unit="nm"), coordinates[[1]][:, [2, 0]]
        )
        assert source.read_bytes() == before


@pytest.mark.parametrize("alias_kind", ["same", "symlink", "hardlink"])
def test_xyz_subset_rejects_source_alias(tmp_path, alias_kind):
    from molsysmt.form.file_xyz.extract import extract

    source = tmp_path / "source.xyz"
    source.write_text("1 2\n0.1 0.2 0.3\n0.4 0.5 0.6\n")
    before = source.read_bytes()
    alias = source if alias_kind == "same" else tmp_path / "alias.xyz"
    if alias_kind != "same":
        (os.symlink if alias_kind == "symlink" else os.link)(source, alias)
    with pytest.raises(ArgumentError):
        extract(str(source), atom_indices=[1], output_filename=str(alias))
    assert source.read_bytes() == before


def test_hdf5_subset_requires_distinct_destination_before_opening(tmp_path):
    pytest.importorskip("mdtraj")
    from molsysmt.form.file_h5.extract import extract

    source = tmp_path / "source.h5"
    source.write_bytes(b"unchanged sentinel before decoder")
    for destination in [None, str(source)]:
        with pytest.raises(ArgumentError):
            extract(str(source), atom_indices=[0], output_filename=destination)
        assert source.read_bytes() == b"unchanged sentinel before decoder"


def test_hdf5_subset_preserves_values_order_and_source(tmp_path):
    md = pytest.importorskip("mdtraj")
    pytest.importorskip("tables")
    from molsysmt.form.file_h5.extract import extract

    source = tmp_path / "source.h5"
    destination = tmp_path / "selected.h5"
    coordinates = np.arange(18, dtype=np.float32).reshape(2, 3, 3) / 10
    topology = md.Topology()
    chain = topology.add_chain()
    group = topology.add_residue("LIG", chain)
    for index in range(3):
        topology.add_atom(f"C{index}", md.element.carbon, group)
    with md.formats.HDF5TrajectoryFile(str(source), "w") as writer:
        writer.write(coordinates=coordinates, time=np.array([1, 2], dtype=np.float32))
        writer.topology = topology
    before = source.read_bytes()
    result = extract(
        str(source),
        atom_indices=[0, 2],
        structure_indices=[1, 0],
        output_filename=str(destination),
    )
    with md.formats.HDF5TrajectoryFile(result, "r") as reader:
        selected = reader.read()
        np.testing.assert_array_equal(
            selected.coordinates, coordinates[[1, 0]][:, [0, 2]]
        )
        np.testing.assert_array_equal(selected.time, [2, 1])
        assert reader.topology.n_atoms == 2
    assert source.read_bytes() == before
