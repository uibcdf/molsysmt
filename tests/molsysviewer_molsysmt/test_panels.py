"""Tests for the molsysviewer_molsysmt addon."""

import sys
import tomllib
from pathlib import Path
from importlib import import_module

import molsysviewer
import pytest

from molsysviewer_molsysmt import (
    get_addon,
    lifecycle,
    on_enable,
    on_disable,
    on_context_action,
    create_molsysmt_state,
    system_for_verbs,
    system_object,
    has_system,
)
from molsysviewer_molsysmt.runtime import MolSysMTAddonRuntime, ensure_runtime


_EXPECTED_PANELS = [
    "basic", "topology", "structure", "hbonds",
    "pbc", "physchem", "molecular_mechanics", "build",
]
_EXPECTED_CONTEXT_ACTIONS = [
    "inspect-system", "select-and-highlight", "color-by-property",
    "compute-contacts",
]
_EXPECTED_PANEL_SECTION_IDS = {
    "basic": ("basic-inspect", "basic-select"),
    "topology": ("topology-bonds", "topology-dihedrals"),
    "structure": ("structure-contacts", "structure-rms", "structure-pca"),
    "hbonds": ("hbonds-buch",),
    "pbc": ("pbc-status", "pbc-wrapping"),
    "physchem": ("physchem-color",),
    "molecular_mechanics": ("mechanics-forces", "mechanics-energy", "mechanics-minimization"),
    "build": ("build-preparation", "build-solvation"),
}


# ---------------------------------------------------------------------------
# Panel widget classes — public MolSysMT namespace panels must be resolvable
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("panel_id,cls_name", [
    ("basic", "MolSysMTBasicPanel"),
    ("topology", "MolSysMTTopologyPanel"),
    ("structure", "MolSysMTStructurePanel"),
    ("hbonds", "MolSysMTHBondsPanel"),
    ("pbc", "MolSysMTPBCPanel"),
    ("physchem", "MolSysMTColorPanel"),
    ("molecular_mechanics", "MolSysMTMechanicsPanel"),
    ("build", "MolSysMTBuildPanel"),
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
# Panel on_mount — each must write an initial addon_states snapshot
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("panel_id", _EXPECTED_PANELS)
def test_panel_on_mount_sets_addon_state(panel_id):
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", panel_id)

    widget.on_mount(view)
    molsysviewer.addons.clear()

    assert view.widget.addon_states["molsysmt"] == widget.state
    assert widget.state["status"] == "idle"


@pytest.mark.parametrize("panel_id,section_ids", _EXPECTED_PANEL_SECTION_IDS.items())
def test_panel_esm_declares_addon_section_containers(panel_id, section_ids):
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", panel_id)
    esm = getattr(widget, "_esm", "")

    molsysviewer.addons.clear()
    for section_id in section_ids:
        assert f'data-molsysviewer-addon-section="molsysmt:{section_id}"' in esm


@pytest.mark.parametrize("panel_id", _EXPECTED_PANELS)
def test_panel_esm_uses_addon_states_sync(panel_id):
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", panel_id)
    esm = getattr(widget, "_esm", "")

    molsysviewer.addons.clear()
    assert "model.get(" in esm
    assert "change:${key}" in esm
    assert 'msg:custom' not in esm


# ---------------------------------------------------------------------------
# Basic panel — system inspection state and action
# ---------------------------------------------------------------------------

def test_basic_panel_on_mount_sets_initial_addon_state():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", "basic")

    widget.on_mount(view)
    molsysviewer.addons.clear()

    state = widget.state
    assert state["n_atoms"] is None
    assert state["n_residues"] is None
    assert state["status"] == "idle"


def test_basic_panel_inspect_action_with_no_molsys_sets_error():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", "basic")
    widget.handle_action(view, "inspect", {})
    molsysviewer.addons.clear()

    assert widget.state["status"] == "error"
    assert "No molecular system" in widget.state["error"]


def test_basic_panel_inspect_action_with_molsys_refreshes_counts():
    pytest.importorskip("molsysmt")

    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]

    widget = view.addons.resolve_panel_widget("molsysmt", "basic")
    widget.handle_action(view, "inspect", {})
    molsysviewer.addons.clear()
    final = widget.state
    assert final["status"] == "done"
    assert final["n_atoms"] is not None and final["n_atoms"] > 0
    assert final["n_residues"] is not None and final["n_residues"] > 0
