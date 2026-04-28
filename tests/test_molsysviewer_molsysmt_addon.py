"""Tests for the molsysviewer_molsysmt addon."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import molsysviewer
import pytest

from molsysviewer_molsysmt import get_addon, lifecycle, on_enable, on_disable, on_context_action
from molsysviewer_molsysmt.runtime import MolSysMTAddonRuntime, ensure_runtime


# ---------------------------------------------------------------------------
# Addon spec contract
# ---------------------------------------------------------------------------

def test_addon_spec_matches_molsysviewer_contract():
    addon = get_addon()

    assert addon.name == "molsysmt"
    assert addon.package == "molsysviewer-molsysmt"
    assert addon.workspaces[0].id == "molsysmt"
    assert addon.workspaces[0].entry_panel == "system"
    assert [p.id for p in addon.panels] == ["system"]
    assert addon.panels[0].widget_class == "molsysviewer_molsysmt.panels.system.MolSysMTSystemPanel"
    assert addon.context_actions[0].id == "inspect-system"
    assert addon.workbench_sections[0].id == "system-info"
    assert addon.export_helpers[0].id == "system-export"


def test_addon_registers_with_molsysviewer_host_registry():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon(), lifecycle=lifecycle)

    assert molsysviewer.addons.contains("molsysmt") is True
    assert molsysviewer.addons.lifecycle_for("molsysmt") is lifecycle

    molsysviewer.addons.clear()


# ---------------------------------------------------------------------------
# Lifecycle / runtime
# ---------------------------------------------------------------------------

def test_lifecycle_records_runtime_on_view():
    view = molsysviewer.MolSysView()

    on_enable(view)
    runtime = view._molsysmt_addon_runtime
    assert runtime.enabled is True
    assert runtime.workspace == "molsysmt"
    assert runtime.event_log[-1]["event"] == "enable"

    on_context_action(view, "inspect-system", {"target": "structure"})
    assert runtime.last_context_action["action_id"] == "inspect-system"
    assert runtime.event_log[-1]["event"] == "context_action"

    on_disable(view)
    assert runtime.enabled is False
    assert runtime.event_log[-1]["event"] == "disable"


def test_lifecycle_info_reports_all_handlers():
    info = lifecycle.info()
    assert info["has_on_enable"] is True
    assert info["has_on_disable"] is True
    assert info["has_on_context_action"] is True


# ---------------------------------------------------------------------------
# Runtime dataclass
# ---------------------------------------------------------------------------

def test_ensure_runtime_creates_and_reuses_instance():
    view = molsysviewer.MolSysView()

    r1 = ensure_runtime(view)
    r2 = ensure_runtime(view)

    assert r1 is r2
    assert isinstance(r1, MolSysMTAddonRuntime)
    assert r1.molecular_system is None
    assert r1.n_atoms is None


# ---------------------------------------------------------------------------
# Panel widget — system panel
# ---------------------------------------------------------------------------

def test_system_panel_widget_class_is_resolvable():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", "system")

    molsysviewer.addons.clear()
    assert widget is not None
    assert type(widget).__name__ == "MolSysMTSystemPanel"
    assert isinstance(widget, molsysviewer.AddonPanelWidget)


def test_system_panel_on_mount_pushes_initial_state():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", "system")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.on_mount(view)
    molsysviewer.addons.clear()

    assert len(sent) == 1
    state = sent[0]["state"]
    assert state["n_atoms"] is None
    assert state["n_residues"] is None
    assert state["status"] == "idle"


def test_system_panel_inspect_action_with_no_molsys_pushes_error():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", "system")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "inspect", {})
    molsysviewer.addons.clear()

    states = [m for m in sent if m.get("type") == "state"]
    assert states[-1]["state"]["status"] == "error"
    assert "No molecular system" in states[-1]["state"]["error"]


def test_system_panel_inspect_action_with_molsys_refreshes_counts():
    msm = pytest.importorskip("molsysmt")

    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    runtime = ensure_runtime(view)
    runtime.molecular_system = msm.convert("pdb_id:1tcd", to_form="molsysmt.MolSys")

    widget = view.addons.resolve_panel_widget("molsysmt", "system")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "inspect", {})
    molsysviewer.addons.clear()

    states = [m for m in sent if m.get("type") == "state"]
    final = states[-1]["state"]
    assert final["status"] == "done"
    assert final["n_atoms"] is not None and final["n_atoms"] > 0
    assert final["n_residues"] is not None and final["n_residues"] > 0
