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
    "inspect-system", "select-and-highlight", "remove-selected-atoms",
    "color-by-property", "compute-contacts",
]
_EXPECTED_PANEL_SECTIONS = {
    "basic-inspect": "basic",
    "basic-select": "basic",
    "topology-bonds": "topology",
    "topology-dihedrals": "topology",
    "structure-contacts": "structure",
    "structure-rms": "structure",
    "structure-pca": "structure",
    "hbonds-buch": "hbonds",
    "pbc-status": "pbc",
    "pbc-wrapping": "pbc",
    "physchem-color": "physchem",
    "mechanics-forces": "molecular_mechanics",
    "mechanics-energy": "molecular_mechanics",
    "mechanics-minimization": "molecular_mechanics",
    "build-preparation": "build",
    "build-solvation": "build",
}


# ---------------------------------------------------------------------------
# Addon spec contract
# ---------------------------------------------------------------------------

def test_addon_spec_matches_molsysviewer_contract():
    addon = get_addon()

    assert addon.name == "molsysmt"
    assert addon.package == "molsysviewer-molsysmt"
    assert addon.workspaces[0].id == "molsysmt"
    assert addon.workspaces[0].entry_panel == "basic"
    assert [p.id for p in addon.panels] == _EXPECTED_PANELS
    assert addon.panels[0].widget_class == "molsysviewer_molsysmt.panels.basic.MolSysMTBasicPanel"
    assert [a.id for a in addon.context_actions] == _EXPECTED_CONTEXT_ACTIONS
    assert addon.shape_providers == ()
    assert addon.workbench_sections[0].id == "system-info"
    assert addon.workbench_sections[1].id == "mvp-overlays"
    panel_sections = {
        section.id: section.meta.get("panel")
        for section in addon.addon_sections
        if "panel" in section.meta
    }
    assert panel_sections == _EXPECTED_PANEL_SECTIONS
    assert addon.export_helpers[0].id == "system-export"


def test_addon_spec_entries_are_importable():
    addon = get_addon()
    entries = []
    entries.extend(panel.widget_class for panel in addon.panels if panel.widget_class)
    entries.extend(action.entry for action in addon.context_actions)
    entries.extend(section.entry for section in addon.addon_sections)
    entries.extend(provider.entry for provider in addon.shape_providers)
    entries.extend(helper.entry for helper in addon.export_helpers)

    for entry in entries:
        module_name, _, attr_name = entry.rpartition(".")
        assert module_name, entry
        module = import_module(module_name)
        assert hasattr(module, attr_name), entry


def test_addon_registers_with_molsysviewer_host_registry():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon(), lifecycle=lifecycle)

    assert molsysviewer.addons.contains("molsysmt") is True
    assert molsysviewer.addons.lifecycle_for("molsysmt") is lifecycle

    molsysviewer.addons.clear()


def test_pyproject_declares_molsysviewer_module_entry_point():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())

    entry_points = pyproject["project"]["entry-points"]["molsysviewer.addons"]
    assert entry_points["molsysmt"] == "molsysviewer_molsysmt"


def test_discovery_from_module_entry_point_preserves_lifecycle(monkeypatch):
    addons_module = import_module("molsysviewer.addons")

    class FakeEntryPoint:
        name = "molsysmt"
        value = "molsysviewer_molsysmt"

        def load(self):
            return import_module("molsysviewer_molsysmt")

    monkeypatch.setattr(addons_module, "_addon_entry_points", lambda: [FakeEntryPoint()])

    molsysviewer.addons.clear()
    discovered = molsysviewer.addons.discover(include_known_modules=False)

    assert [addon.name for addon in discovered] == ["molsysmt"]
    discovered_lifecycle = molsysviewer.addons.lifecycle_for("molsysmt")
    assert discovered_lifecycle is not None
    assert discovered_lifecycle.info()["has_on_context_action"] is True

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

    on_context_action(view, "unknown-action", {"target": "structure"})
    assert runtime.last_context_action["action_id"] == "unknown-action"
    assert runtime.event_log[-1]["event"] == "context_action"

    on_disable(view)
    assert runtime.enabled is False
    assert runtime.event_log[-1]["event"] == "disable"


def test_lifecycle_info_reports_all_handlers():
    info = lifecycle.info()
    assert info["has_on_enable"] is True
    assert info["has_on_disable"] is True
    assert info["has_on_context_action"] is True


def test_context_action_dispatches_to_mvp_facade():
    pytest.importorskip("molsysmt")
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon(), lifecycle=lifecycle)
    view = molsysviewer.demo["dialanine"]
    view.whole.reset_colors()

    handled = view.addons.handle_context_action(
        "molsysmt",
        "color-by-property",
        {"property": "mass", "palette": ["#111111", "#eeeeee"]},
    )

    assert handled is True
    assert view.addons.molsysmt.last_context_action["action_id"] == "color-by-property"
    assert view.addons.molsysmt.last_color_property == "mass"
    assert view._atom_color_map  # noqa: SLF001

    view.whole.reset_colors()
    molsysviewer.addons.clear()


def test_context_action_remove_selected_atoms_uses_basic_facade():
    pytest.importorskip("molsysmt")
    import molsysmt as msm

    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon(), lifecycle=lifecycle)
    view = molsysviewer.demo["dialanine"]
    n0 = int(msm.get(view, n_atoms=True))

    handled = view.addons.handle_context_action(
        "molsysmt",
        "remove-selected-atoms",
        {"atom_indices": [0]},
    )

    assert handled is True
    assert int(msm.get(view, n_atoms=True)) == n0 - 1
    assert view.addons.molsysmt.last_context_action["action_id"] == "remove-selected-atoms"
    assert view.addons.molsysmt.event_log[-1]["event"] == "context_remove_selected_atoms"

    molsysviewer.addons.clear()


# ---------------------------------------------------------------------------
# Runtime dataclass
# ---------------------------------------------------------------------------

def test_ensure_runtime_creates_and_reuses_instance():
    view = molsysviewer.MolSysView()

    r1 = ensure_runtime(view)
    r2 = ensure_runtime(view)

    assert r1 is r2
    assert isinstance(r1, MolSysMTAddonRuntime)
    assert r1.n_atoms is None


def test_runtime_does_not_store_a_molecular_system():
    runtime = MolSysMTAddonRuntime()
    assert not hasattr(runtime, "molecular_system")


def test_runtime_has_all_panel_fields():
    runtime = MolSysMTAddonRuntime()
    for field in [
        "n_atoms", "n_residues", "n_chains", "n_frames",
        "last_selection", "last_selection_element", "last_selection_indices", "last_selection_tag",
        "last_color_property", "last_color_element", "last_color_palette",
        "contacts_result", "contacts_tag", "rmsd_result", "rmsf_result", "pca_result",
        "hbonds_result", "hbonds_tag",
        "bondgraph_result", "dihedral_quartets_result",
        "pbc_status",
        "forces_result", "energy_result", "forces_tag",
        "last_build_op", "build_log",
    ]:
        assert hasattr(runtime, field), f"Runtime missing field: {field!r}"


# ---------------------------------------------------------------------------
# Diagnostics policy — compact panel errors, SMonitor best effort
# ---------------------------------------------------------------------------

def test_diagnostics_compact_error_message_for_optional_dependency():
    from molsysviewer_molsysmt.diagnostics import compact_error_message

    assert compact_error_message(ModuleNotFoundError("No module named 'fake_backend'")) == (
        "Missing optional dependency required for this operation."
    )
    assert compact_error_message(RuntimeError("first line\nsecond line")) == "first line"


def test_color_panel_optional_dependency_error_is_compact_and_logged(monkeypatch):
    pytest.importorskip("molsysmt")
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]

    def broken_color_by(*_args, **_kwargs):
        raise ModuleNotFoundError("No module named 'fake_backend'")

    runtime = ensure_runtime(view)
    monkeypatch.setattr(runtime.show, "color_by", broken_color_by)

    widget = view.addons.resolve_panel_widget("molsysmt", "physchem")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "apply_color", {"property": "mass"})
    final = widget.state
    assert final == {
        "status": "error",
        "error": "Missing optional dependency required for this operation.",
    }
    assert runtime.event_log[-1]["event"] == "panel_error"
    assert runtime.event_log[-1]["panel"] == "physchem"
    assert runtime.event_log[-1]["action"] == "apply_color"

    molsysviewer.addons.clear()
