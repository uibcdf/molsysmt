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
# Phase 1 foundation — public namespace, state_factory, dual ensure_runtime,
# access helpers, and lazy import
# ---------------------------------------------------------------------------

def test_state_factory_exposes_public_view_namespace():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    ns = view.addons.molsysmt
    assert isinstance(ns, MolSysMTAddonRuntime)
    # public namespace and legacy private alias are the SAME object
    assert view._molsysmt_addon_runtime is ns
    assert ns._view is view
    # ensure_runtime resolves the public namespace
    assert ensure_runtime(view) is ns

    molsysviewer.addons.clear()


def test_addon_spec_declares_state_factory():
    addon = get_addon()
    assert getattr(addon, "state_factory", None) is create_molsysmt_state


def test_ensure_runtime_falls_back_to_private_without_registration():
    molsysviewer.addons.clear()
    view = molsysviewer.MolSysView()

    runtime = ensure_runtime(view)
    assert isinstance(runtime, MolSysMTAddonRuntime)
    assert view._molsysmt_addon_runtime is runtime
    assert ensure_runtime(view) is runtime


def test_create_molsysmt_state_reuses_existing_private_runtime():
    view = molsysviewer.MolSysView()
    first = MolSysMTAddonRuntime()
    view._molsysmt_addon_runtime = first
    assert create_molsysmt_state(view) is first
    assert first._view is view


def test_runtime_supports_dict_style_lookup():
    runtime = MolSysMTAddonRuntime()
    assert runtime["workspace"] == "molsysmt"
    assert runtime["n_atoms"] is None


def test_runtime_facade_attributes_are_not_dataclass_fields():
    from dataclasses import asdict, fields

    runtime = MolSysMTAddonRuntime()
    runtime.attach_view(object())

    field_names = {field.name for field in fields(runtime)}
    assert "_view" not in field_names
    assert "basic" not in field_names
    assert "structure" not in field_names
    assert "show" not in field_names
    assert "overlays" not in field_names

    serialized = asdict(runtime)
    assert "_view" not in serialized
    assert "basic" not in serialized
    assert "show" not in serialized


def test_public_namespace_exposes_active_facade_shape():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    ns = view.addons.molsysmt
    assert ns.basic is not None
    assert ns.structure.name == "structure"
    assert ns.show.name == "show"
    assert ns.overlays is ns.show

    molsysviewer.addons.clear()


def test_basic_facade_remove_uses_apply_system_edit_on_real_view():
    pytest.importorskip("molsysmt")
    import molsysmt as msm

    molsysviewer.addons.clear()


def test_basic_facade_set_uses_apply_system_edit_on_real_view():
    pytest.importorskip("molsysmt")

    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]
    calls = []
    original_apply = view.apply_system_edit

    def recording_apply(new_molsys, **kwargs):
        calls.append((new_molsys, kwargs))
        return original_apply(new_molsys, **kwargs)

    view.apply_system_edit = recording_apply

    view.addons.molsysmt.basic.set(element="group", selection=[0], group_name="ACE2")

    assert len(calls) == 1
    assert calls[0][1]["visible_atom_indices"] == list(range(22))
    payload_msg = next(msg for msg in view._message_history if msg.get("op") == "load_molsys_payload")
    assert payload_msg["payload"]["atoms"]["residue_name"][:5] == ["ACE2"] * 5
    assert view.addons.molsysmt.event_log[-1]["event"] == "facade_basic_set"

    molsysviewer.addons.clear()


def test_basic_facade_append_structures_uses_apply_system_edit_on_real_view():
    pytest.importorskip("molsysmt")

    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]
    calls = []
    original_apply = view.apply_system_edit

    def recording_apply(new_molsys, **kwargs):
        calls.append((new_molsys, kwargs))
        return original_apply(new_molsys, **kwargs)

    view.apply_system_edit = recording_apply

    view.addons.molsysmt.basic.append_structures(molsysviewer.demo["dialanine"]._molsys)  # noqa: SLF001

    assert len(calls) == 1
    assert calls[0][1]["visible_atom_indices"] == list(range(22))
    payload_msg = next(msg for msg in view._message_history if msg.get("op") == "load_molsys_payload")
    assert payload_msg["multiple_structures"] is True
    assert len(payload_msg["payload"]["structures"]) == 2
    assert view.addons.molsysmt.event_log[-1]["event"] == "facade_basic_append_structures"

    molsysviewer.addons.clear()


def test_access_helpers_on_view_without_system():
    view = molsysviewer.MolSysView()
    assert system_for_verbs(view) is view
    assert system_object(view) is None
    assert has_system(view) is False


def test_importing_addon_does_not_import_molsysviewer():
    import os
    import subprocess

    code = "import sys; import molsysviewer_molsysmt; print('molsysviewer' in sys.modules)"
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(sys.path)
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "False", result.stdout + result.stderr


# ---------------------------------------------------------------------------
# Coordinate-only mutations reconcile via set_coordinates and preserve overlays
# ---------------------------------------------------------------------------

def test_pbc_wrap_preserves_viewer_overlays():
    """A coordinate-only mutation (PBC wrap) must NOT reset viewer overlays.

    The panel routes through ``view.set_coordinates`` (rebuild with no
    atom_index_map, preserving regions/selections/colors), not a destructive
    ``view.load(..., mode="replace")``.
    """
    pytest.importorskip("molsysmt")

    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["pentalanine"]  # has a PBC box

    ns = view.addons.molsysmt
    ns.show.select('atom_name=="CA"', tag="ca")
    ns.show.color_by("mass")
    assert view.selections.contains("ca")
    n_colors = len(view._atom_color_map)  # noqa: SLF001
    assert n_colors > 0

    widget = view.addons.resolve_panel_widget("molsysmt", "pbc")
    sent = []
    widget.send = lambda msg: sent.append(msg)
    widget.handle_action(view, "wrap_pbc", {})
    assert widget.state["status"] == "done", widget.state.get("error")
    assert widget.state["update_mode"] == "coordinates"
    assert "overlays preserved" in widget.state["mutation_warning"]
    # overlays survive the coordinate-only mutation
    assert view.selections.contains("ca"), "selection lost after PBC wrap"
    assert len(view._atom_color_map) == n_colors, "per-atom colors lost after PBC wrap"  # noqa: SLF001

    molsysviewer.addons.clear()
