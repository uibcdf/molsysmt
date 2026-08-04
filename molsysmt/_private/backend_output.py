"""Silencing third-party parsers that write straight to the C standard output.

Some backends report format details with `printf` and offer no verbosity switch.
MDTraj's DCD reader is the case that motivated this: it prints two lines on every
open, which turns any loop over trajectories into a wall of noise. The messages are
not diagnostics a caller can act on, and biotraj -- the same plugin, forked -- ships
them commented out.

Because the writer is C, `contextlib.redirect_stdout` does not reach it: that only
rebinds `sys.stdout`. The file descriptor has to be redirected, and the C stream
flushed *before* it is restored, or the buffered bytes simply appear later.

The redirection is process-wide while it is held, so it must wrap the narrowest
possible call. Anything another thread writes to file descriptor 1 during that window
is lost. Set `molsysmt.configure.silence_backend_stdout` to False to disable it.
"""

from __future__ import annotations

import contextlib
import ctypes
import os
import sys

_libc = None


def _c_library():
    global _libc
    if _libc is None:
        _libc = ctypes.CDLL(None)
    return _libc


@contextlib.contextmanager
def silence_backend_stdout():
    """Discarding whatever the enclosed call writes to file descriptor 1."""

    from molsysmt import configure

    if not configure.silence_backend_stdout:
        yield
        return

    try:
        library = _c_library()
    except Exception:
        # Without libc there is no way to flush the C stream, and redirecting the
        # descriptor alone would only delay the output rather than remove it.
        yield
        return

    sys.stdout.flush()
    library.fflush(None)

    saved = os.dup(1)
    devnull = os.open(os.devnull, os.O_WRONLY)
    try:
        os.dup2(devnull, 1)
        yield
    finally:
        # Flush while descriptor 1 still points at /dev/null: the C stream is block
        # buffered, so anything left in it would otherwise reach the real stdout.
        library.fflush(None)
        os.dup2(saved, 1)
        os.close(saved)
        os.close(devnull)
