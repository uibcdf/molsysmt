"""
Tests for molsysmt._private.smonitor.warnings classes.
"""

import pytest


def test_not_digested_argument_warning():
    from molsysmt._private.smonitor.warnings import NotDigestedArgumentWarning
    w = NotDigestedArgumentWarning(argument='selection')
    assert isinstance(w, Warning)


def test_molecular_system_mismatch_warning_basic():
    from molsysmt._private.smonitor.warnings import MolecularSystemMismatchWarning
    w = MolecularSystemMismatchWarning()
    assert isinstance(w, Warning)


def test_molecular_system_mismatch_warning_with_models():
    from molsysmt._private.smonitor.warnings import MolecularSystemMismatchWarning
    w = MolecularSystemMismatchWarning(caller='test_caller', n_models=3)
    assert isinstance(w, Warning)


def test_slow_chunk_io_warning():
    from molsysmt._private.smonitor.warnings import SlowChunkIOWarning
    w = SlowChunkIOWarning(chunk_index=2, io_time_s=1.5)
    assert isinstance(w, Warning)


def test_corrupt_frame_skipped_warning():
    from molsysmt._private.smonitor.warnings import CorruptFrameSkippedWarning
    w = CorruptFrameSkippedWarning(chunk_index=0, frame_index=10, reason='checksum mismatch')
    assert isinstance(w, Warning)


def test_memory_pressure_warning():
    from molsysmt._private.smonitor.warnings import MemoryPressureWarning
    w = MemoryPressureWarning(
        chunk_index=1, rss_bytes=1024**3, budget_bytes=2 * 1024**3, pressure_pct=50.0
    )
    assert isinstance(w, Warning)


def test_download_warning_instantiable():
    from molsysmt._private.smonitor.warnings import DownloadWarning
    w = DownloadWarning()
    assert isinstance(w, Warning)


def test_selection_warning_instantiable():
    from molsysmt._private.smonitor.warnings import SelectionWarning
    w = SelectionWarning()
    assert isinstance(w, Warning)
