"""Tests for the molsysviewer_molsysmt addon."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import molsysviewer
import pytest

from molsysviewer_molsysmt import get_addon, lifecycle, on_enable, on_disable, on_context_action
from molsysviewer_molsysmt.runtime import MolSysMTAddonRuntime, ensure_runtime


_EXPECTED_PANELS = [
    "system", "select", "color", "structure", "transform",
    "hbonds", "topology", "pbc", "mechanics", "build",
]
_EXPECTED_CONTEXT_ACTIONS = [
    "inspect-system", "select-and-highlight", "color-by-property",
    "compute-contacts", "fit-to-reference", "compute-hbonds",
    "wrap-to-pbc", "build-bioassembly",
]


# ---------------------------------------------------------------------------
# Addon spec contract
# ---------------------------------------------------------------------------

def test_addon_spec_matches_molsysviewer_contract():
    addon = get_addon()

    assert addon.name == "molsysmt"
    assert addon.package == "molsysviewer-molsysmt"
    assert addon.workspaces[0].id == "molsysmt"
    assert addon.workspaces[0].entry_panel == "system"
    assert [p.id for p in addon.panels] == _EXPECTED_PANELS
    assert addon.panels[0].widget_class == "molsysviewer_molsysmt.panels.system.MolSysMTSystemPanel"
    assert [a.id for a in addon.context_actions] == _EXPECTED_CONTEXT_ACTIONS
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


def test_runtime_has_all_panel_fields():
    runtime = MolSysMTAddonRuntime()
    for field in [
        "n_atoms", "n_residues", "n_chains", "n_frames",
        "last_selection", "last_selection_element", "last_selection_indices",
        "last_color_property", "last_color_element", "last_color_palette",
        "contacts_result", "rmsd_result", "rmsf_result", "pca_result",
        "hbonds_result", "hbonds_tag",
        "bondgraph_result", "dihedral_quartets_result",
        "pbc_status",
        "forces_result", "energy_result", "forces_tag",
        "last_build_op", "build_log",
    ]:
        assert hasattr(runtime, field), f"Runtime missing field: {field!r}"


# ---------------------------------------------------------------------------
# Panel widget classes — all 10 must be resolvable
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("panel_id,cls_name", [
    ("system",    "MolSysMTSystemPanel"),
    ("select",    "MolSysMTSelectPanel"),
    ("color",     "MolSysMTColorPanel"),
    ("structure", "MolSysMTStructurePanel"),
    ("transform", "MolSysMTTransformPanel"),
    ("hbonds",    "MolSysMTHBondsPanel"),
    ("topology",  "MolSysMTTopologyPanel"),
    ("pbc",       "MolSysMTPBCPanel"),
    ("mechanics", "MolSysMTMechanicsPanel"),
    ("build",     "MolSysMTBuildPanel"),
])
def test_panel_widget_class_is_resolvable(panel_id, cls_name):
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", panel_id)

    molsysviewer.addons.clear()
    assert widget is not None
    assert type(widget).__name__ == cls_name
    assert isinstance(widget, molsysviewer.AddonPanelWidget)


# ---------------------------------------------------------------------------
# Panel on_mount — each must push an initial state
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("panel_id", _EXPECTED_PANELS)
def test_panel_on_mount_pushes_state(panel_id):
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", panel_id)
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.on_mount(view)
    molsysviewer.addons.clear()

    assert len(sent) == 1
    assert "state" in sent[0]


# ---------------------------------------------------------------------------
# System panel — legacy detailed tests
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Select panel — no-system error
# ---------------------------------------------------------------------------

def test_select_panel_run_with_no_molsys_pushes_error():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", "select")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "run_selection", {"selection": "backbone", "element": "atom"})
    molsysviewer.addons.clear()

    states = [m for m in sent if m.get("type") == "state"]
    assert states[-1]["state"]["status"] == "error"
    assert "No molecular system" in states[-1]["state"]["error"]


# ---------------------------------------------------------------------------
# Color panel — no-system error
# ---------------------------------------------------------------------------

def test_color_panel_apply_with_no_molsys_pushes_error():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", "color")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "apply_color", {"property": "charge", "palette": "viridis"})
    molsysviewer.addons.clear()

    states = [m for m in sent if m.get("type") == "state"]
    assert states[-1]["state"]["status"] == "error"


# ---------------------------------------------------------------------------
# H-Bonds panel — no-system error
# ---------------------------------------------------------------------------

def test_hbonds_panel_compute_with_no_molsys_pushes_error():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", "hbonds")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "compute_hbonds", {})
    molsysviewer.addons.clear()

    states = [m for m in sent if m.get("type") == "state"]
    assert states[-1]["state"]["status"] == "error"


# ---------------------------------------------------------------------------
# PBC panel — check_pbc with no-system error
# ---------------------------------------------------------------------------

def test_pbc_panel_check_with_no_molsys_pushes_error():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", "pbc")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "check_pbc", {})
    molsysviewer.addons.clear()

    states = [m for m in sent if m.get("type") == "state"]
    assert states[-1]["state"]["status"] == "error"


# ---------------------------------------------------------------------------
# Build panel — no-system error
# ---------------------------------------------------------------------------

def test_build_panel_action_with_no_molsys_pushes_error():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", "build")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "add_hydrogens", {})
    molsysviewer.addons.clear()

    states = [m for m in sent if m.get("type") == "state"]
    assert states[-1]["state"]["status"] == "error"
