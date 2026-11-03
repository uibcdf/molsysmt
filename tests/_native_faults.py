"""Scoped native-fault diagnostics for #527's process-abort investigation."""

import faulthandler

import pytest


@pytest.fixture(autouse=True)
def current_thread_native_fault(pytestconfig):
    """Keep the active native call visible among background widget threads."""
    from _pytest.faulthandler import fault_handler_stderr_fd_key

    descriptor = pytestconfig.stash.get(fault_handler_stderr_fd_key, None)
    if descriptor is None or not faulthandler.is_enabled():
        yield
        return
    # Pytest owns this duplicated descriptor beyond per-test FD capture.
    # Keep its lifetime and restore the plugin's all-thread setting afterward.
    faulthandler.enable(file=descriptor, all_threads=False)
    try:
        yield
    finally:
        faulthandler.enable(file=descriptor, all_threads=True)
