"""Protecting compressed CIF inputs during concurrent and failed parsing."""

import gzip
import io
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier

import numpy as np
import pytest

import molsysmt as msm


@pytest.fixture(params=["default", "python"])
def reader_backend(request, monkeypatch):
    import mmcif.io
    from mmcif.io.IoAdapterPy import IoAdapterPy

    if request.param == "python":
        monkeypatch.setattr(mmcif.io, "IoAdapter", IoAdapterPy)
    return mmcif.io.IoAdapter


def test_read_preserves_existing_input_neighbors(
    hp35_cif_gz_file, tmp_path, reader_backend
):
    source = tmp_path / "observed.cif.gz"
    original = Path(hp35_cif_gz_file).read_bytes()
    source.write_bytes(original)
    neighbor = source.with_suffix("")
    sentinel = b"An independent existing file must survive reading its neighbor.\n"
    neighbor.write_bytes(sentinel)

    molsys = msm.convert(source, to_form="molsysmt.MolSys")

    assert molsys.get_n_atoms() == 596
    assert neighbor.exists() and neighbor.read_bytes() == sentinel
    assert source.read_bytes() == original
    assert {path.name for path in tmp_path.iterdir()} == {
        "observed.cif",
        "observed.cif.gz",
    }


def test_concurrent_read_only_input_preserves_coordinates(
    hp35_cif_gz_file, tmp_path, monkeypatch, reader_backend
):
    from mmcif.io.IoAdapterBase import IoAdapterBase

    input_dir = tmp_path / "read_only"
    input_dir.mkdir()
    source = input_dir / "observed.cif.gz"
    original = Path(hp35_cif_gz_file).read_bytes()
    source.write_bytes(original)
    reference = msm.convert(hp35_cif_gz_file, to_form="molsysmt.MolSys")
    expected = msm.pyunitwizard.get_value(
        msm.get(reference, coordinates=True), to_unit="nm"
    )
    open_file = io.open
    decompress = IoAdapterBase._uncompress
    barrier = Barrier(2)
    work_directories = []

    def deny_input_writes(file, mode="r", *args, **kwargs):
        # Enforce directory permissions even when pytest runs as root.
        if not isinstance(file, int) and set(mode).intersection("wax+"):
            if (
                Path(file).resolve().is_relative_to(input_dir.resolve())
                or Path(file).resolve().parent == Path.cwd().resolve()
            ):
                raise PermissionError("The molecular input directory is read-only.")
        return open_file(file, mode, *args, **kwargs)

    def overlap_decompression(self, input_path, output_dir):
        work_directories.append(Path(output_dir))
        result = decompress(self, input_path, output_dir)
        barrier.wait(timeout=15)
        return result

    monkeypatch.setattr(io, "open", deny_input_writes)
    monkeypatch.setattr(IoAdapterBase, "_uncompress", overlap_decompression)
    input_dir.chmod(0o555)
    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(msm.convert, source, to_form="molsysmt.MolSys")
                for _ in range(2)
            ]
            outputs = [future.result(timeout=30) for future in futures]
    finally:
        input_dir.chmod(0o755)

    for output in outputs:
        assert output.get_n_atoms() == 596
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(msm.get(output, coordinates=True), to_unit="nm"),
            expected,
        )
        assert output.topology.atoms.atom_id.tolist() == (
            reference.topology.atoms.atom_id.tolist()
        )
    assert source.read_bytes() == original
    assert list(input_dir.iterdir()) == [source]
    assert len(set(work_directories)) == 2
    assert all(not path.exists() for path in work_directories)


def test_parser_temporary_directory_is_removed_on_failure(
    hp35_cif_gz_file, monkeypatch, reader_backend
):
    import mmcif.io

    work_directories = []

    class FailingReader(reader_backend):
        def readFile(self, item, **options):
            work = Path(options["outDirPath"])
            work_directories.append(work)
            (work / "unfinished.cif").write_text("unfinished parser output")
            raise RuntimeError("Parser failure after creating temporary data.")

    monkeypatch.setattr(mmcif.io, "IoAdapter", FailingReader)
    with pytest.raises(RuntimeError, match="Parser failure"):
        msm.convert(hp35_cif_gz_file, to_form="mmcif.PdbxContainers.DataContainer")
    assert work_directories
    assert all(not path.exists() for path in work_directories)


def test_multiple_containers_keep_the_existing_warning(
    tmp_path, reader_backend, monkeypatch
):
    import smonitor.integrations

    emitted = []
    original_emit = smonitor.integrations.emit_from_catalog

    def capture_emission(entry, **options):
        emitted.append((entry, options))
        return original_emit(entry, **options)

    monkeypatch.setattr(smonitor.integrations, "emit_from_catalog", capture_emission)
    source = tmp_path / "multiple.cif.gz"
    with gzip.open(source, "wt") as handle:
        handle.write(
            "data_first\n_entry.id first\n#\ndata_second\n_entry.id second\n#\n"
        )
    container = msm.convert(source, to_form="mmcif.PdbxContainers.DataContainer")
    assert len(emitted) == 1
    assert emitted[0][0]["code"] == "MSM-WARN-IO-002"
    assert container.getName() == "first"
    assert list(tmp_path.iterdir()) == [source]
