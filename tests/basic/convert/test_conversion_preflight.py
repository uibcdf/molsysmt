"""Testing that conversion preflight work is strictly opt-in."""

import pytest

import molsysmt as msm
from molsysmt.native import Structures, Topology


def test_ordinary_conversion_bypasses_preflight(monkeypatch):
    from molsysmt._private import conversion_report

    def fail_if_called(*args, **kwargs):
        raise AssertionError('conversion preflight should have been bypassed')

    monkeypatch.setattr(
        conversion_report,
        'build_conversion_report',
        fail_if_called,
    )

    source = Topology(n_atoms=1, skip_digestion=True)
    output = msm.convert(source, to_form='molsysmt.Topology')

    assert isinstance(output, Topology)


def test_explicit_report_runs_preflight_once(monkeypatch):
    from molsysmt._private import conversion_report

    original = conversion_report.build_conversion_report
    calls = []

    def record_call(*args, **kwargs):
        calls.append((args, kwargs))
        return original(*args, **kwargs)

    monkeypatch.setattr(
        conversion_report,
        'build_conversion_report',
        record_call,
    )

    source = Topology(n_atoms=1, skip_digestion=True)
    output, report = msm.convert(
        source,
        to_form='molsysmt.Topology',
        return_report=True,
    )

    assert isinstance(output, Topology)
    assert report.outcome == 'exact'
    assert len(calls) == 1


def test_strict_conversion_runs_preflight_and_rejects_loss(monkeypatch):
    from molsysmt._private import conversion_report

    original = conversion_report.build_conversion_report
    calls = []

    def record_call(*args, **kwargs):
        calls.append((args, kwargs))
        return original(*args, **kwargs)

    monkeypatch.setattr(
        conversion_report,
        'build_conversion_report',
        record_call,
    )

    source = Structures(bioassembly={'1': []}, skip_digestion=True)
    with pytest.raises(msm.NotCompatibleConversionError, match='bioassembly'):
        msm.convert(
            source,
            to_form='molsysmt.StructuresDict',
            strict=True,
        )

    assert len(calls) == 1
