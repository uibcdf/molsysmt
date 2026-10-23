"""Protecting byte-indexed PDBQT reads, ownership and bounded file output."""

from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, FormatError
from molsysmt.native import PDBQTFileHandler
from tests.native.test_pdbqt_file_handler import poses


@pytest.fixture
def indexed_source(tmp_path):
    path = tmp_path / "ensemble.pdbqt"
    text = poses(7).replace("REMARK shared", "REMARK café shared").replace("\n", "\r\n")
    path.write_bytes(text.encode("utf-8"))
    return path, text


def test_indexed_bytes_match_resident_text_under_nondefault_units(indexed_source):
    path, text = indexed_source
    with (
        PDBQTFileHandler(path, storage_mode="indexed") as indexed,
        PDBQTFileHandler("pdbqt_text:" + text) as resident,
    ):
        assert indexed.storage_mode == "indexed"
        assert not hasattr(indexed._document, "_text")
        assert indexed._document.offsets.dtype == np.int64
        assert not indexed._document.offsets.flags.writeable
        with msm.pyunitwizard.context(standard_units=["pm", "ps", "radians"]):
            actual = indexed.get_coordinates(
                indices=[3, 0], structure_indices=[6, 1, 6]
            )
            expected = resident.get_coordinates(
                indices=[3, 0], structure_indices=[6, 1, 6]
            )
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(actual, to_unit="nm"),
            msm.pyunitwizard.get_value(expected, to_unit="nm"),
        )
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(actual, to_unit="nm")[:, 1, 0], [6.1, 1.1, 6.1]
        )
        assert indexed.get(structure_indices=[6, 1, 6], structure_id=True) == [
            "77",
            "27",
            "77",
        ]
        assert indexed.get_coordinates(structure_indices=[]).shape == (0, 4, 3)
        assert indexed.get_coordinates(indices=[]).shape == (7, 0, 3)
        assert msm.convert(indexed, to_form="string:pdbqt_text") == "pdbqt_text:" + text


@pytest.mark.parametrize("operation", ["overwrite", "replace", "remove"])
def test_changed_or_unavailable_sources_are_rejected_without_leaking(
    indexed_source, operation
):
    path, _ = indexed_source
    handler = PDBQTFileHandler(path, storage_mode="indexed")
    document = handler._document

    def mutate():
        if operation == "overwrite":
            path.write_bytes(poses(7).encode())
        elif operation == "replace":
            replacement = path.with_name("replacement.pdbqt")
            replacement.write_text(poses(7))
            replacement.replace(path)
        else:
            path.unlink()

    try:
        mutate()
    except PermissionError:
        import sys

        if sys.platform != "win32":
            raise
        # Windows may prevent replacing/unlinking an open source outright.
        # In that case no changed source exists and the original remains usable.
        assert handler.get_coordinates().shape == (7, 4, 3)
        handler.close()
        assert document._file.closed
        return
    for query in [
        lambda: handler.get_coordinates(),
        lambda: handler.get_torsion_tree(),
        lambda: handler.copy(),
    ]:
        with pytest.raises(FormatError, match="source"):
            query()
    assert "indexed" in repr(handler)
    handler.close()
    handler.close()
    assert document._file.closed


def test_copies_and_concurrent_reads_have_independent_close_ownership(indexed_source):
    path, _ = indexed_source
    original = PDBQTFileHandler(path, storage_mode="indexed")
    copied = original.copy()
    document = original._document
    assert copied._document is document
    original.close()
    assert not document._file.closed
    with ThreadPoolExecutor(max_workers=4) as pool:
        values = list(
            pool.map(
                lambda i: msm.pyunitwizard.get_value(
                    copied.get_coordinates(structure_indices=[i]), to_unit="nm"
                )[0, 0, 0],
                [6, 1, 4, 0] * 3,
            )
        )
    np.testing.assert_allclose(values, [6.1, 1.1, 4.1, 0.1] * 3)
    copied.close()
    assert document._file.closed


def test_direct_and_public_file_iterators_do_not_load_whole_source(
    indexed_source, monkeypatch
):
    from pathlib import Path

    from molsysmt.form.file_pdbqt.iterators import StructuresIterator

    path, _ = indexed_source
    original = Path.read_bytes

    def forbid_complete_read(source):
        if source == path:
            raise AssertionError("A file iterator must not use resident read_bytes")
        return original(source)

    monkeypatch.setattr(Path, "read_bytes", forbid_complete_read)
    with StructuresIterator(
        path, structure_indices=[6, 1, 6], chunk=2, coordinates=True
    ) as iterator:
        assert iterator._handler.storage_mode == "indexed"
        document = iterator._handler._document
        values = [
            msm.pyunitwizard.get_value(x, to_unit="nm")[:, 0, 0] for x in iterator
        ]
    np.testing.assert_allclose(np.concatenate(values), [6.1, 1.1, 6.1])
    assert document._file.closed
    values = [
        msm.pyunitwizard.get_value(x, to_unit="nm")[:, 0, 0]
        for x in msm.Iterator(
            path, coordinates=True, structure_indices=[6, 1, 6], chunk=2
        )
    ]
    np.testing.assert_allclose(np.concatenate(values), [6.1, 1.1, 6.1])


def test_selected_blocks_read_only_requested_ranges_and_share_attribute_reads(
    indexed_source, monkeypatch
):
    from molsysmt.form.molsysmt_PDBQTFileHandler.iterators import StructuresIterator

    path, _ = indexed_source
    with PDBQTFileHandler(path, storage_mode="indexed") as handler:
        reads = []
        original = handler._document._bytes

        def observed(start, stop):
            reads.append((start, stop))
            return original(start, stop)

        monkeypatch.setattr(handler._document, "_bytes", observed)
        with StructuresIterator(
            handler,
            structure_indices=[6, 1, 6],
            chunk=2,
            coordinates=True,
            occupancy=True,
            output_type="dictionary",
        ) as iterator:
            first = next(iterator)
            assert first["coordinates"].shape == (2, 4, 3)
            assert reads == [tuple(handler._document.offsets[i]) for i in [6, 1]]
        assert not handler.closed


@pytest.mark.parametrize("structures", ["all", [6, 1]])
def test_file_output_streams_identity_or_selected_models_atomically(
    indexed_source, tmp_path, structures, monkeypatch
):
    from molsysmt._private.pdbqt_indexed_document import PDBQTIndexedDocument

    path, text = indexed_source
    target = tmp_path / "output.pdbqt"

    def forbidden(self):
        raise AssertionError(
            "A file output must not materialize the complete text payload"
        )

    monkeypatch.setattr(PDBQTIndexedDocument, "payload", property(forbidden))
    with PDBQTFileHandler(path, storage_mode="indexed") as handler:
        msm.convert(handler, to_form=target, structure_indices=structures)
    if structures == "all":
        assert target.read_bytes() == text.encode("utf-8")
    else:
        assert msm.get(target, structure_id=True) == ["77", "27"]
    assert not list(tmp_path.glob(".molsysmt-pdbqt-*"))


def test_source_change_during_file_output_preserves_existing_destination(
    indexed_source, tmp_path, monkeypatch
):
    path, _ = indexed_source
    target = tmp_path / "protected.pdbqt"
    target.write_bytes(b"original destination")
    with PDBQTFileHandler(path, storage_mode="indexed") as handler:
        original = handler._document._bytes

        def changed(start, stop):
            result = original(start, stop)
            path.write_text("changed during output")
            return result

        monkeypatch.setattr(handler._document, "_bytes", changed)
        with pytest.raises(FormatError, match="changed"):
            msm.convert(handler, to_form=target)
    assert target.read_bytes() == b"original destination"
    assert not list(tmp_path.glob(".molsysmt-pdbqt-*"))


def test_storage_policy_rejects_text_indexing_and_unknown_modes():
    text = "pdbqt_text:" + poses(2)
    with pytest.raises(ArgumentError):
        PDBQTFileHandler(text, storage_mode="indexed")
    with pytest.raises(ArgumentError):
        PDBQTFileHandler(text, storage_mode="guess")


def test_indexed_coordinates_feed_existing_chunked_executor(
    indexed_source, monkeypatch
):
    path, _ = indexed_source
    with PDBQTFileHandler(path, storage_mode="indexed") as handler:
        monkeypatch.setattr(msm.configure, "heavy_mode", "off")
        expected = msm.structure.get_center(handler, structure_indices=[6, 1, 6])
        monkeypatch.setattr(msm.configure, "heavy_mode", "force")
        actual = msm.structure.get_center(handler, structure_indices=[6, 1, 6])
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(actual, to_unit="nm"),
        msm.pyunitwizard.get_value(expected, to_unit="nm"),
    )


def test_invalid_late_model_closes_descriptor_before_constructor_returns(
    tmp_path, monkeypatch
):
    from pathlib import Path

    path = tmp_path / "invalid.pdbqt"
    path.write_text(poses(2).replace("MODEL 27", "MODEL 17"))
    original = Path.open
    opened = []

    def tracked(source, *args, **kwargs):
        file = original(source, *args, **kwargs)
        if source == path and args and args[0] == "rb":
            opened.append(file)
        return file

    monkeypatch.setattr(Path, "open", tracked)
    with pytest.raises(FormatError, match="Repeated"):
        PDBQTFileHandler(path, storage_mode="indexed")
    assert opened and all(file.closed for file in opened)


def test_file_atom_and_structure_projection_is_blocked_and_source_aligned(
    indexed_source, tmp_path, monkeypatch
):
    from molsysmt._private.pdbqt_indexed_document import PDBQTIndexedDocument

    path, _ = indexed_source
    target = tmp_path / "subsystem.pdbqt"

    def forbidden(self):
        raise AssertionError("A selected file output must not load the full payload")

    monkeypatch.setattr(PDBQTIndexedDocument, "payload", property(forbidden))
    msm.convert(path, to_form=target, selection=[3, 0], structure_indices=[5, 1])
    assert msm.get(target, n_atoms=True) == 2
    assert msm.get(target, structure_id=True) == ["67", "27"]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(
            msm.get(target, element="atom", coordinates=True), to_unit="nm"
        )[:, 0, 0],
        [5.1, 1.1],
    )


def test_indexed_first_block_does_not_allocate_a_source_sized_text_copy(tmp_path):
    import gc
    import tracemalloc

    from devtools.scripts.benchmark_pdbqt_storage import write_fixture
    from molsysmt.form.file_pdbqt.iterators import StructuresIterator

    warm = tmp_path / "warm.pdbqt"
    source = tmp_path / "large.pdbqt"
    write_fixture(warm, 2, 512)
    write_fixture(source, 128, 512)
    with StructuresIterator(warm, coordinates=True) as iterator:
        next(iterator)
    gc.collect()
    own_trace = not tracemalloc.is_tracing()
    if own_trace:
        tracemalloc.start()
    baseline = tracemalloc.get_traced_memory()[0]
    tracemalloc.reset_peak()
    try:
        with StructuresIterator(
            source, structure_indices=[127, 0], coordinates=True
        ) as iterator:
            first = next(iterator)
            assert first.shape == (1, 512, 3)
            assert iterator._handler.storage_mode == "indexed"
            peak = tracemalloc.get_traced_memory()[1] - baseline
        assert peak < source.stat().st_size, (peak, source.stat().st_size)
    finally:
        if own_trace:
            tracemalloc.stop()


def test_python_copies_and_abandoned_handles_release_their_own_leases(
    indexed_source, tmp_path
):
    import copy
    import gc

    path, _ = indexed_source
    original = PDBQTFileHandler(path, storage_mode="indexed")
    document = original._document
    shallow, deep = copy.copy(original), copy.deepcopy(original)
    assert document._owners == 3
    shallow.close()
    del deep
    gc.collect()
    assert document._owners == 1 and not document._file.closed
    msm.convert(original, to_form=tmp_path / "copy.pdbqt")
    gc.collect()
    assert document._owners == 1
    del original
    gc.collect()
    assert document._file.closed


@pytest.mark.parametrize("borrowed", [False, True])
def test_interrupted_block_read_releases_owned_but_not_borrowed_file(
    indexed_source, monkeypatch, borrowed
):
    from molsysmt.form.file_pdbqt.iterators import StructuresIterator as FileIterator
    from molsysmt.form.molsysmt_PDBQTFileHandler.iterators import (
        StructuresIterator as HandlerIterator,
    )

    path, _ = indexed_source
    handle = PDBQTFileHandler(path, storage_mode="indexed") if borrowed else None
    iterator = (
        HandlerIterator(handle, structure_indices=[1], coordinates=True)
        if borrowed
        else FileIterator(path, structure_indices=[1], coordinates=True)
    )
    document = iterator._handler._document

    def interrupted(start, stop):
        raise KeyboardInterrupt("controlled interrupted read")

    monkeypatch.setattr(document, "_bytes", interrupted)
    with pytest.raises(KeyboardInterrupt):
        next(iterator)
    assert iterator.closed
    assert document._file.closed == (not borrowed)
    if borrowed:
        assert not handle.closed
        handle.close()
        assert document._file.closed
