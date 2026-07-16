"""Tests for the public warmup report and failure policy."""

import molsysmt as msm
import pytest

from molsysmt._private.smonitor import ArgumentError, LibraryNotFoundError, WarmupFailureWarning


def test_warmup_preserves_integer_return_by_default():
    assert msm.warmup(numba=False, modules=False) == 0


def test_warmup_returns_structured_report():
    report = msm.warmup(
        numba=False,
        modules=False,
        return_report=True,
    )

    assert report == {
        "compiled_kernels": 0,
        "loaded_attributes": [],
        "skipped_attributes": [],
        "failures": [],
    }


def test_warmup_reports_expected_optional_dependency_skip(monkeypatch):
    monkeypatch.setattr(msm, "_LAZY_ATTRIBUTES", {"optional_probe": ".unused"})

    def missing_optional(name):
        raise LibraryNotFoundError(library="optional-probe", caller="test_warmup")

    monkeypatch.setattr(msm, "__getattr__", missing_optional)

    report = msm.warmup(numba=False, modules=True, return_report=True)

    assert report["failures"] == []
    assert report["skipped_attributes"][0]["attribute"] == "optional_probe"
    assert report["skipped_attributes"][0]["error_type"] == "LibraryNotFoundError"


def test_warmup_warns_and_reports_unexpected_failure(monkeypatch):
    monkeypatch.setattr(msm, "_LAZY_ATTRIBUTES", {"broken_probe": ".unused"})

    def broken_import(name):
        raise RuntimeError("broken lazy import")

    monkeypatch.setattr(msm, "__getattr__", broken_import)

    with pytest.warns(WarmupFailureWarning, match="broken_probe"):
        report = msm.warmup(numba=False, modules=True, return_report=True)

    assert report["failures"] == [{
        "attribute": "broken_probe",
        "error_type": "RuntimeError",
        "reason": "broken lazy import",
    }]


def test_warmup_strict_mode_propagates_unexpected_failure(monkeypatch):
    monkeypatch.setattr(msm, "_LAZY_ATTRIBUTES", {"broken_probe": ".unused"})

    def broken_import(name):
        raise RuntimeError("broken lazy import")

    monkeypatch.setattr(msm, "__getattr__", broken_import)

    with pytest.raises(RuntimeError, match="broken lazy import"):
        msm.warmup(numba=False, modules=True, strict=True)


def test_warmup_control_arguments_are_digested():
    with pytest.raises(ArgumentError):
        msm.warmup(numba=False, modules=False, strict="yes")
