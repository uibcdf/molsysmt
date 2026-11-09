"""Publish complete new files without replacing existing or racing outputs."""

import errno
import os
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest

from molsysmt._private.files_and_directories import atomic_new_file


def test_staging_is_private_until_successful_publication(tmp_path):
    target = tmp_path / "result.h5"
    with atomic_new_file(target) as staged:
        assert staged.parent == target.parent and not target.exists()
        staged.write_bytes(b"complete result")
        assert not target.exists()
    assert target.read_bytes() == b"complete result"
    assert not staged.exists()
    assert list(tmp_path.iterdir()) == [target]


def test_failure_cleans_staging_and_publishes_nothing(tmp_path):
    target = tmp_path / "result.h5"
    with pytest.raises(RuntimeError, match="simulated"):
        with atomic_new_file(target) as staged:
            staged.write_bytes(b"partial")
            raise RuntimeError("simulated failure")
    assert not target.exists() and not staged.exists()
    assert not list(tmp_path.iterdir())


def test_existing_destination_is_never_replaced(tmp_path):
    target = tmp_path / "result.h5"
    target.write_bytes(b"existing")
    with pytest.raises(FileExistsError):
        with atomic_new_file(target):
            pytest.fail("An existing output must refuse before staging.")
    assert target.read_bytes() == b"existing"
    assert list(tmp_path.iterdir()) == [target]


def test_publication_race_has_one_complete_winner(tmp_path):
    target = tmp_path / "race.h5"
    barrier = Barrier(2)

    def writer(contents):
        try:
            with atomic_new_file(target) as staged:
                staged.write_bytes(contents)
                barrier.wait(timeout=10)
            return contents
        except FileExistsError:
            return None

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(writer, [b"a" * 4096, b"b" * 4096]))
    winners = [result for result in results if result is not None]
    assert len(winners) == 1 and target.read_bytes() == winners[0]
    assert list(tmp_path.iterdir()) == [target]


def test_unsupported_publication_does_not_fall_back_to_a_partial_copy(
    tmp_path, monkeypatch
):
    target = tmp_path / "result.h5"

    def unavailable(*args, **kwargs):
        raise OSError(errno.ENOTSUP, "simulated missing hard-link support")

    monkeypatch.setattr(os, "link", unavailable)
    with pytest.raises(OSError, match="hard-link"):
        with atomic_new_file(target) as staged:
            staged.write_bytes(b"complete")
    assert not target.exists() and not staged.exists()


def test_dangling_symlink_is_an_existing_destination(tmp_path):
    target = tmp_path / "linked.h5"
    try:
        target.symlink_to(tmp_path / "absent")
    except OSError:
        pytest.skip("This platform does not permit an unprivileged symlink.")
    with pytest.raises(FileExistsError):
        with atomic_new_file(target):
            pytest.fail("A dangling symlink must not be followed or replaced.")
    assert target.is_symlink() and not target.exists()
