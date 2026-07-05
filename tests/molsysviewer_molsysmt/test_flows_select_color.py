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


# ---------------------------------------------------------------------------
# System adapter — public Python equivalent, reads from the view-as-form
# ---------------------------------------------------------------------------

def test_system_counts_adapter_reads_from_view():
    pytest.importorskip("molsysmt")
    from molsysviewer_molsysmt.adapters.system import system_counts

    view = molsysviewer.demo["dialanine"]
    counts = system_counts(view)
    assert set(counts) == {"n_atoms", "n_residues", "n_chains", "n_frames"}
    assert counts["n_atoms"] > 0
    assert counts["n_residues"] > 0


def test_system_counts_adapter_raises_without_system():
    from molsysviewer_molsysmt.adapters.system import system_counts

    view = molsysviewer.MolSysView()
    with pytest.raises(ValueError):
        system_counts(view)


# ---------------------------------------------------------------------------
# Select adapter/facade/panel — creates active viewer selections
# ---------------------------------------------------------------------------

def test_select_indices_adapter_reads_from_view_and_resolves_atoms():
    pytest.importorskip("molsysmt")
    from molsysviewer_molsysmt.adapters.select import select_indices

    view = molsysviewer.demo["dialanine"]

    atoms = select_indices(view, 'atom_name=="CA"', element="atom")
    groups = select_indices(view, "all", element="group")

    assert atoms.indices == atoms.atom_indices
    assert atoms.n_selected == 1
    assert groups.n_selected == 3
    assert len(groups.atom_indices) == 22


def test_select_indices_adapter_raises_without_system():
    from molsysviewer_molsysmt.adapters.select import select_indices

    view = molsysviewer.MolSysView()
    with pytest.raises(ValueError, match="No molecular system"):
        select_indices(view, "all")


def test_show_facade_select_creates_and_activates_viewer_selection():
    pytest.importorskip("molsysmt")
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]
    tag = "test-molsysmt-selection"
    if view.selections.contains(tag):
        view.selections.clear(tag=tag)
    view.active_selection.clear()

    result = view.addons.molsysmt.show.select(
        'atom_name=="CA"',
        element="atom",
        tag=tag,
    )

    assert result.n_selected == 1
    assert view.selections.contains(tag)
    assert view.active_selection.atom_indices == result.atom_indices
    assert view.addons.molsysmt.last_selection_tag == tag

    view.addons.molsysmt.show.clear_selection(tag=tag)
    assert not view.selections.contains(tag)
    assert view.active_selection.is_empty()
    molsysviewer.addons.clear()


def test_select_panel_run_with_no_molsys_pushes_error():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", "basic")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "run_selection", {"selection": "backbone", "element": "atom"})
    molsysviewer.addons.clear()
    assert widget.state["status"] == "error"
    assert "No molecular system" in widget.state["error"]


def test_select_panel_uses_loaded_view_not_runtime_seed():
    pytest.importorskip("molsysmt")
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]
    if view.selections.contains("molsysmt-selection"):
        view.selections.clear(tag="molsysmt-selection")
    view.active_selection.clear()

    widget = view.addons.resolve_panel_widget("molsysmt", "basic")
    sent = []
    widget.send = lambda msg: sent.append(msg)
    runtime = ensure_runtime(view)

    widget.handle_action(view, "run_selection", {
        "selection": 'atom_name=="CA"',
        "element": "atom",
    })
    final = widget.state
    assert final["status"] == "done"
    assert final["n_selected"] == 1
    assert runtime.last_selection_tag == "molsysmt-selection"
    assert view.selections.contains("molsysmt-selection")
    assert view.active_selection.atom_indices == runtime.last_selection_indices

    runtime.show.clear_selection(tag="molsysmt-selection")
    molsysviewer.addons.clear()


def test_select_panel_clear_selection_removes_viewer_selection():
    pytest.importorskip("molsysmt")
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]
    view.addons.molsysmt.show.select(
        'atom_name=="CA"',
        element="atom",
        tag="molsysmt-selection",
    )

    widget = view.addons.resolve_panel_widget("molsysmt", "basic")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "clear_selection", {})
    final = widget.state
    assert final["status"] == "idle"
    assert final["n_selected"] is None
    assert not view.selections.contains("molsysmt-selection")
    assert view.active_selection.is_empty()

    molsysviewer.addons.clear()


# ---------------------------------------------------------------------------
# Color adapter/facade/panel — reads from view and applies viewer colors
# ---------------------------------------------------------------------------

def test_color_property_values_adapter_reads_from_view():
    pytest.importorskip("molsysmt")
    from molsysviewer_molsysmt.adapters.color import property_values, supported_properties

    view = molsysviewer.demo["dialanine"]

    assert supported_properties() == ("charge", "mass", "atomic_radius")
    charge = property_values(view, "charge")
    radius = property_values(view, "atomic_radius")

    assert charge.property == "charge"
    assert charge.element == "group"
    assert len(charge.values) == 3
    assert radius.property == "atomic_radius"
    assert radius.element == "atom"
    assert len(radius.values) == 22


def test_color_property_values_adapter_raises_without_system():
    from molsysviewer_molsysmt.adapters.color import property_values

    view = molsysviewer.MolSysView()
    with pytest.raises(ValueError, match="No molecular system"):
        property_values(view, "charge")


def test_show_facade_color_by_applies_whole_color_values():
    pytest.importorskip("molsysmt")
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]
    view.whole.reset_colors()

    result = view.addons.molsysmt.show.color_by("mass", palette=["#111111", "#eeeeee"])

    assert result.property == "mass"
    assert result.element == "group"
    assert view.addons.molsysmt.last_color_property == "mass"
    assert view.addons.molsysmt.last_color_element == "group"
    assert view._atom_color_map  # noqa: SLF001

    view.whole.reset_colors()
    molsysviewer.addons.clear()


def test_color_panel_apply_with_no_molsys_pushes_error():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", "physchem")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "apply_color", {"property": "charge", "palette": "viridis"})
    molsysviewer.addons.clear()
    assert widget.state["status"] == "error"


def test_color_panel_apply_uses_loaded_view_not_runtime_seed():
    pytest.importorskip("molsysmt")
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]
    view.whole.reset_colors()

    widget = view.addons.resolve_panel_widget("molsysmt", "physchem")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    runtime = ensure_runtime(view)

    widget.handle_action(view, "apply_color", {
        "property": "mass",
        "palette": ["#111111", "#eeeeee"],
    })
    final = widget.state
    assert final["status"] == "done"
    assert final["property"] == "mass"
    assert final["element"] == "group"
    assert runtime.last_color_property == "mass"
    assert view._atom_color_map  # noqa: SLF001

    view.whole.reset_colors()
    molsysviewer.addons.clear()


def test_color_panel_reset_colors_clears_viewer_color_map():
    pytest.importorskip("molsysmt")
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]
    view.addons.molsysmt.show.color_by("mass", palette=["#111111", "#eeeeee"])
    assert view._atom_color_map  # noqa: SLF001

    widget = view.addons.resolve_panel_widget("molsysmt", "physchem")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "reset_colors", {})
    final = widget.state
    assert final["status"] == "idle"
    assert final["property"] is None
    assert view._atom_color_map == {}  # noqa: SLF001
    assert view.addons.molsysmt.last_color_property is None

    molsysviewer.addons.clear()


# ---------------------------------------------------------------------------
# Selection-driven context items (on_active_selection_changed) + expand handler
# ---------------------------------------------------------------------------

def test_active_selection_hook_returns_items_for_selection():
    from molsysviewer_molsysmt.addon import on_active_selection_changed

    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon(), lifecycle=lifecycle)
    view = molsysviewer.demo["dialanine"]

    items = on_active_selection_changed(view, {"atom_indices": [5]})
    assert [item["id"] for item in items] == ["molsysmt-expand-residues"]
    assert items[0]["payload"]["atom_indices"] == [5]
    # nothing selected -> no items
    assert on_active_selection_changed(view, {"atom_indices": []}) == []

    molsysviewer.addons.clear()


def test_lifecycle_exposes_active_selection_hook():
    assert lifecycle.info().get("has_on_active_selection_changed") is True


def test_context_expand_residues_sets_whole_residue_active_selection():
    pytest.importorskip("molsysmt")
    from molsysviewer_molsysmt.addon import on_context_action

    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon(), lifecycle=lifecycle)
    view = molsysviewer.demo["dialanine"]

    import molsysmt as msm

    # one atom of a residue -> expand the active selection to the whole residue
    on_context_action(view, "molsysmt-expand-residues", {"atom_indices": [5]})

    expected = sorted(int(i) for i in msm.select(view, selection="group_index==0"))
    assert sorted(view.active_selection.atom_indices) == expected

    molsysviewer.addons.clear()


