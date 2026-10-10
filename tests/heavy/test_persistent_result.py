"""
Tests for PersistentResultHandle disk-backed output.
"""

import numpy as np
import pytest

from molsysmt._private.execution import PersistentResultHandle


@pytest.mark.parametrize(
    "failure", [ValueError("invalid mapping"), OSError("disk error")]
)
def test_failed_mapping_retires_only_owned_storage(monkeypatch, tmp_path, failure):
    """Remove allocated scratch on constructor failure and preserve caller files."""
    import tempfile

    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path))

    def fail_mapping(*args, **kwargs):
        raise failure

    monkeypatch.setattr(np, "memmap", fail_mapping)
    caller = tmp_path / "caller.dat"
    caller.write_bytes(b"caller evidence")
    with pytest.raises(type(failure), match=str(failure)):
        PersistentResultHandle((2, 3))
    assert sorted(tmp_path.iterdir()) == [caller]
    with pytest.raises(type(failure), match=str(failure)):
        PersistentResultHandle((2, 3), path=caller)
    assert caller.read_bytes() == b"caller evidence"


def test_constructor_cleanup_failure_is_visible(monkeypatch, tmp_path):
    """Report a failed scratch retirement rather than losing both errors."""
    import tempfile
    from pathlib import Path

    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path))

    def fail_mapping(*args, **kwargs):
        raise ValueError("invalid mapping")

    def fail_unlink(path, *args, **kwargs):
        raise PermissionError("scratch retirement denied")

    monkeypatch.setattr(np, "memmap", fail_mapping)
    monkeypatch.setattr(Path, "unlink", fail_unlink)
    with pytest.raises(PermissionError, match="scratch retirement denied") as caught:
        PersistentResultHandle((2, 3))
    assert isinstance(caught.value.__context__, ValueError)
    assert str(caught.value.__context__) == "invalid mapping"


def test_context_failure_retires_owned_storage():
    """Remove scratch when a calculation using an established handle fails."""
    with pytest.raises(RuntimeError, match="calculation failed"):
        with PersistentResultHandle((2, 3)) as handle:
            path = handle.path
            handle[:] = 1
            raise RuntimeError("calculation failed")
    assert not path.exists()


def test_persistent_result_write_read():
    shape = (100, 50, 3)
    with PersistentResultHandle(shape) as handle:
        data = np.random.rand(*shape).astype(np.float64)
        handle[:] = data
        result = handle.to_memory()
        np.testing.assert_allclose(result, data)


def test_persistent_result_cleanup():
    shape = (10, 5, 3)
    handle = PersistentResultHandle(shape)
    path = handle.path
    assert path.exists()
    handle.cleanup()
    assert not path.exists()


def test_persistent_result_context_manager():
    shape = (20, 10, 3)
    with PersistentResultHandle(shape) as handle:
        path = handle.path
        assert path.exists()
    assert not path.exists()


def test_persistent_result_user_path_created(tmp_path):
    """PersistentResultHandle with explicit path creates the file at that location."""
    shape = (10, 5, 3)
    user_file = tmp_path / "subdir" / "output.npy"
    handle = PersistentResultHandle(shape, path=user_file)
    try:
        assert handle.path == user_file
        assert user_file.exists()
    finally:
        handle.cleanup()


def test_persistent_result_user_path_not_deleted_on_cleanup(tmp_path):
    """cleanup() must NOT delete the file when path was provided by caller."""
    shape = (10, 5, 3)
    user_file = tmp_path / "output.npy"
    handle = PersistentResultHandle(shape, path=user_file)
    assert user_file.exists()
    handle.cleanup()
    assert user_file.exists(), "User-provided file should not be deleted by cleanup()"


def test_persistent_result_user_path_data_survives_cleanup(tmp_path):
    """Data written to a user-path handle is accessible after cleanup()."""
    shape = (5, 3, 3)
    user_file = tmp_path / "traj_out.dat"
    handle = PersistentResultHandle(shape, path=user_file)
    data = np.arange(np.prod(shape), dtype=np.float64).reshape(shape)
    handle[:] = data
    handle.flush()
    handle.cleanup()

    # Re-open via memmap (raw binary file, not .npy)
    reloaded = np.memmap(str(user_file), dtype=np.float64, mode="r", shape=shape)
    np.testing.assert_allclose(reloaded, data)
