"""Own automatic file copies until the creating Python process exits normally."""

import atexit
import os
import tempfile
import threading
from pathlib import Path

_owner_pid = os.getpid()
_directory = None
_paths = set()
_lock = threading.RLock()


def _after_fork():
    """Detach inherited ownership before the child starts additional threads."""
    global _owner_pid, _directory, _paths, _lock
    _directory, _paths, _lock = None, set(), threading.RLock()
    _owner_pid = os.getpid()


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_after_fork)


def reserve_copy_path(source):
    """Reserve a unique same-suffix path in this process's private workspace."""
    global _directory
    if os.getpid() != _owner_pid:
        _after_fork()
    with _lock:
        if _directory is None:
            _directory = str(
                Path(tempfile.mkdtemp(prefix="molsysmt-copies-")).resolve()
            )
        descriptor, path = tempfile.mkstemp(
            prefix="copy-", suffix="".join(Path(source).suffixes), dir=_directory
        )
        os.close(descriptor)
        _paths.add(path)
        return path


def make_persistent(path):
    """Relinquish an automatic path explicitly chosen as a persistent destination."""
    if os.getpid() == _owner_pid:
        with _lock:
            _paths.discard(str(Path(path).resolve()))


def discard_copy(path):
    """Retire only a file registered to this process; retry locked files at exit."""
    if os.getpid() != _owner_pid:
        return
    with _lock:
        path = str(path)
        if path in _paths:
            try:
                Path(path).unlink(missing_ok=True)
            except OSError:
                return
            _paths.remove(path)


def cleanup():
    """Best-effort normal-exit cleanup, preserving files supplied by callers."""
    global _directory
    if os.getpid() != _owner_pid or not _lock.acquire(blocking=False):
        return
    try:
        for path in tuple(_paths):
            discard_copy(path)
        if _directory is not None:
            try:
                # Never recursively delete unregistered persistent destinations.
                Path(_directory).rmdir()
            except OSError:
                return
            _directory = None
    finally:
        _lock.release()


atexit.register(cleanup)
