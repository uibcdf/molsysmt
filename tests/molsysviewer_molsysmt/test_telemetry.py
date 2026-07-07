"""Tests for the addon's SMonitor telemetry (breadcrumbs, slow-signal extras,
and the ``context_extra``-based panel diagnostics)."""

from __future__ import annotations

from types import SimpleNamespace

import molsysviewer
import pytest

from molsysviewer_molsysmt import get_addon
from molsysviewer_molsysmt.adapters._telemetry import adapter_n_atoms
from molsysviewer_molsysmt.diagnostics import emit_panel_exception
from molsysviewer_molsysmt.runtime import _get_n_atoms_safe, ensure_runtime

# --- extra_factory helpers -------------------------------------------------

def test_get_n_atoms_safe_reads_attached_view():
    view = molsysviewer.demo["dialanine"]
    ns = SimpleNamespace(_state=SimpleNamespace(_view=view))
    assert _get_n_atoms_safe((ns,)) == 22


def test_get_n_atoms_safe_returns_zero_when_detached_without_raising():
    ns = SimpleNamespace(_state=SimpleNamespace(_view=None))
    assert _get_n_atoms_safe((ns,)) == 0
    assert _get_n_atoms_safe((object(),)) == 0  # no _state at all
    assert _get_n_atoms_safe(()) == 0


def test_adapter_n_atoms_reads_view_from_first_arg_or_kwarg():
    view = molsysviewer.demo["dialanine"]
    assert adapter_n_atoms((view,), {}) == {"n_atoms": 22}
    assert adapter_n_atoms((), {"view": view}) == {"n_atoms": 22}
    assert adapter_n_atoms((), {}) == {"n_atoms": 0}
    assert adapter_n_atoms((object(),), {}) == {"n_atoms": 0}


# --- Part 3: emit_panel_exception -----------------------------------------

def test_emit_panel_exception_uses_context_extra_schema(monkeypatch):
    import smonitor.integrations as si

    captured: dict = {}

    def fake_emit(entry, *, extra=None, package_root=None, meta=None):
        captured["extra"] = extra

    monkeypatch.setattr(si, "emit_from_catalog", fake_emit)

    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    try:
        view = molsysviewer.demo["dialanine"]
        emit_panel_exception(view, panel="mechanics", action="minimize", exc=ValueError("boom"))

        extra = captured["extra"]
        assert extra["caller"] == "molsysviewer_molsysmt.panels.mechanics.minimize"
        assert extra["operation"] == "minimize"
        assert extra["failure_class"] == "addon-panel-action"
        assert extra["causal_chain"] == ["ValueError"]

        # The local addon event log is still updated (no regression).
        assert any(e["event"] == "panel_error" for e in ensure_runtime(view).event_log)
    finally:
        molsysviewer.addons.clear()


def test_emit_panel_exception_warns_on_real_emission_failure(monkeypatch):
    import smonitor.integrations as si

    def boom_emit(*args, **kwargs):
        raise RuntimeError("emit backend down")

    monkeypatch.setattr(si, "emit_from_catalog", boom_emit)

    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    try:
        view = molsysviewer.demo["dialanine"]
        with pytest.warns(RuntimeWarning, match="failed to emit panel diagnostics"):
            emit_panel_exception(view, panel="build", action="solvate", exc=ValueError("x"))

        # Even when SMonitor emission fails, the local event log still records it.
        assert any(e["event"] == "panel_error" for e in ensure_runtime(view).event_log)
    finally:
        molsysviewer.addons.clear()
