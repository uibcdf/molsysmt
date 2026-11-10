"""Bound worker failure/IPC and keep native preparation out of inherited locks."""

import multiprocessing
import threading

import pytest

from benchmarks.harness import BenchmarkHarness


def _require_fork():
    if "fork" not in multiprocessing.get_all_start_methods():
        pytest.skip("This control exercises only the explicitly legacy fork path.")


def test_inherited_lock_cannot_leave_a_worker_waiting_forever():
    _require_fork()
    lock = threading.Lock()
    lock.acquire()
    try:
        harness = BenchmarkHarness(
            "inherited-lock", iterations=1, repeats=3, worker_timeout=0.2
        )
        with pytest.raises(RuntimeError, match="timed out"):
            harness.run(lambda: lock.acquire(), lambda: None)
    finally:
        lock.release()
    assert not any(
        child.name.startswith("ForkProcess")
        for child in multiprocessing.active_children()
    )


def test_raw_sample_payload_is_drained_before_joining_the_worker():
    _require_fork()
    result = BenchmarkHarness(
        "large-pipe", iterations=1, repeats=20_000, worker_timeout=10
    ).run(lambda: None, lambda: sum(range(3)))
    assert len(result["samples_seconds"]) == 20_000
    assert result["median_seconds"] > 0


def test_worker_failure_remains_a_diagnostic_not_a_zero_timing():
    _require_fork()

    def fail():
        raise RuntimeError("controlled worker failure")

    with pytest.raises(RuntimeError, match="exit code"):
        BenchmarkHarness("failed", iterations=1, repeats=3, worker_timeout=5).run(
            fail, lambda: None
        )


@pytest.mark.parametrize("value", [True, 0, -1, float("nan"), float("inf"), "1"])
def test_invalid_worker_deadlines_are_rejected_before_execution(value):
    with pytest.raises(ValueError):
        BenchmarkHarness("invalid-timeout", worker_timeout=value)
