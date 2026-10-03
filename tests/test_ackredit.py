"""Protecting scientific outcomes when optional attribution diagnostics are strict."""

import warnings
from contextlib import contextmanager

import pytest

from molsysmt import _ackredit
from molsysmt._private.smonitor.warnings import AckreditTrackingWarning


class BrokenProvider:
    def __init__(self, failure):
        self.failure = failure

    @contextmanager
    def scope(self, target):
        if self.failure == "enter":
            raise RuntimeError("provider enter failure")
        try:
            yield
        finally:
            if self.failure == "exit":
                raise RuntimeError("provider exit failure")

    def register_item(self, **item):
        if self.failure == "register":
            raise RuntimeError("provider register failure")

    def track_item(self, item_id, used_by):
        if self.failure == "track":
            raise RuntimeError("provider track failure")


@pytest.mark.parametrize("failure", ["backend", "enter", "register", "track", "exit"])
def test_strict_attribution_warning_preserves_result_and_diagnostic(
    monkeypatch, failure
):
    import smonitor
    from smonitor.handlers import MemoryHandler

    provider = BrokenProvider(failure)

    def backend():
        if failure == "backend":
            raise RuntimeError("provider backend failure")
        return provider

    monkeypatch.setattr(_ackredit, "backend", backend)
    # Observe emitted catalog events, rather than merely calls to a warn helper.
    manager = smonitor.get_manager()
    handler = MemoryHandler()
    manager.add_handler(handler)
    result = {"observations": [1, 2], "bibliography": [{"id": "software:control"}]}
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", AckreditTrackingWarning)
            with _ackredit.scope("scientific-control") as reached:
                _ackredit.credit(reached, result["bibliography"], "scientific-control")
            completed = result
    finally:
        manager.remove_handler(handler)
    assert completed is result
    diagnostics = [
        event for event in handler.events if event.get("code") == "MSM-WARN-ATTR-001"
    ]
    assert len(diagnostics) == 1
    assert f"provider {failure} failure" in diagnostics[0]["extra"]["reason"]


@pytest.mark.parametrize("failure", ["backend", "enter", "exit"])
def test_tracking_failure_never_replaces_scientific_exception(monkeypatch, failure):
    def backend():
        if failure == "backend":
            raise RuntimeError("provider backend failure")
        return BrokenProvider(failure)

    monkeypatch.setattr(_ackredit, "backend", backend)
    scientific_error = ValueError("original scientific failure")
    with warnings.catch_warnings():
        warnings.simplefilter("error", AckreditTrackingWarning)
        with pytest.raises(ValueError) as raised:
            with _ackredit.scope("scientific-control"):
                raise scientific_error
    assert raised.value is scientific_error


def test_unrelated_scientific_warning_still_obeys_strict_filter(monkeypatch):
    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)
        with pytest.raises(UserWarning, match="scientific warning"):
            with _ackredit.scope("scientific-control"):
                warnings.warn("scientific warning", UserWarning)


def test_diagnostic_failure_during_cleanup_preserves_original_scientific_error(
    monkeypatch, caplog
):
    from molsysmt._private.smonitor import emitter

    monkeypatch.setattr(_ackredit, "backend", lambda: BrokenProvider("exit"))

    def failed_diagnostic(*args, **kwargs):
        raise RuntimeError("controlled diagnostic emission failure")

    monkeypatch.setattr(emitter, "warn", failed_diagnostic)
    scientific_error = ValueError("original scientific failure")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        with pytest.raises(ValueError) as raised:
            with _ackredit.scope("scientific-control"):
                raise scientific_error
    assert raised.value is scientific_error
    records = [
        record
        for record in caplog.records
        if getattr(record, "code", None) == "MSM-WARN-ATTR-001"
    ]
    assert len(records) == 1
    assert records[0].operation == "finish attribution tracking"
    assert "provider exit failure" in records[0].provider_error
