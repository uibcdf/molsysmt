"""Tests for the molsysviewer_molsysmt addon."""

import sys
import tomllib
from pathlib import Path
from importlib import import_module
from types import SimpleNamespace

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
# PBC adapter/panel — status reads from the active view
# ---------------------------------------------------------------------------

def test_pbc_status_adapter_reads_from_view():
    pytest.importorskip("molsysmt")
    from molsysviewer_molsysmt.adapters.pbc import pbc_status

    view = molsysviewer.demo["dialanine"]

    result = pbc_status(view)

    assert result.has_pbc is False


def test_pbc_adapters_raise_without_system():
    from molsysviewer_molsysmt.adapters.pbc import pbc_status, transform_pbc

    view = molsysviewer.MolSysView()

    with pytest.raises(ValueError, match="No molecular system"):
        pbc_status(view)
    with pytest.raises(ValueError, match="No molecular system"):
        transform_pbc(view, "wrap_pbc")


# ---------------------------------------------------------------------------
# Molecular mechanics adapter/panel — no-system contract and payload hygiene
# ---------------------------------------------------------------------------

def test_molecular_mechanics_adapters_raise_without_system():
    from molsysviewer_molsysmt.adapters.molecular_mechanics import compute_forces
    from molsysviewer_molsysmt.adapters.molecular_mechanics import minimize_energy
    from molsysviewer_molsysmt.adapters.molecular_mechanics import potential_energy

    view = molsysviewer.MolSysView()

    with pytest.raises(ValueError, match="No molecular system"):
        compute_forces(view)
    with pytest.raises(ValueError, match="No molecular system"):
        potential_energy(view)
    with pytest.raises(ValueError, match="No molecular system"):
        minimize_energy(view)


def test_molecular_mechanics_panel_accepts_only_real_platform_payload():
    from molsysviewer_molsysmt.panels.mechanics import _platform_from_payload

    assert _platform_from_payload({}) == "CPU"
    assert _platform_from_payload({"platform": "Reference"}) == "Reference"
    with pytest.raises(ValueError, match="Unsupported molecular-mechanics argument"):
        _platform_from_payload({"forcefield": "AMBER14"})


# ---------------------------------------------------------------------------
# Build adapter/panel — materialized operations from the active view
# ---------------------------------------------------------------------------

def test_build_adapter_raises_without_system():
    from molsysviewer_molsysmt.adapters.build import run_build_operation

    view = molsysviewer.MolSysView()

    with pytest.raises(ValueError, match="No molecular system"):
        run_build_operation(view, "add_hydrogens")


def test_build_add_bonds_adapter_replaces_topology_when_bonds_are_added():
    pytest.importorskip("molsysmt")
    from molsysviewer_molsysmt.adapters.build import run_build_operation
    import molsysmt as msm

    molsys = msm.convert(msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'])
    molsys.topology.remove_bonds('all', skip_digestion=True)
    view = molsysviewer.MolSysView()
    view.load(molsys)

    result = run_build_operation(view, "add_bonds")

    assert result.mode == "replace"
    assert result.n_added == 0
    assert int(msm.get(result.molecular_system, n_bonds=True)) == 21


# ---------------------------------------------------------------------------
# Shape cleanup actions — use the real ShapesManager.clear(tag=...) API
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("panel_id,action_id,runtime_field", [
    ("hbonds", "clear_hbonds", "hbonds_tag"),
    ("molecular_mechanics", "clear_forces", "forces_tag"),
])
def test_shape_cleanup_panel_actions_use_clear_api(panel_id, action_id, runtime_field):
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()
    runtime = ensure_runtime(view)
    setattr(runtime, runtime_field, f"test-{panel_id}-shape")

    widget = view.addons.resolve_panel_widget("molsysmt", panel_id)
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, action_id, {})
    molsysviewer.addons.clear()
    assert widget.state["status"] == "idle"
    assert getattr(runtime, runtime_field) is None


def test_topology_clear_bonds_uses_clear_api():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", "topology")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "clear_bonds", {})
    molsysviewer.addons.clear()
    assert widget.state["status"] == "idle"


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
    assert widget.state["status"] == "error"


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
    assert widget.state["status"] == "error"


# ---------------------------------------------------------------------------
# Atom-appending mutations (build) reconcile via view.add and preserve overlays
# ---------------------------------------------------------------------------

def test_build_solvate_appends_and_preserves_overlays():
    """Solvate adds atoms at the end, so the panel applies it with ``view.add``
    (overlay-preserving), not a destructive ``view.load(..., mode="replace")``.
    """
    pytest.importorskip("molsysmt")

    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]

    import molsysmt as msm

    ns = view.addons.molsysmt
    ns.show.select('atom_name=="CA"', tag="ca")
    ns.show.color_by("mass")
    n0 = int(msm.get(view, n_atoms=True))
    n_colors = len(view._atom_color_map)  # noqa: SLF001
    assert n_colors > 0

    widget = view.addons.resolve_panel_widget("molsysmt", "build")
    sent = []
    widget.send = lambda msg: sent.append(msg)
    widget.handle_action(view, "solvate", {})
    assert widget.state["status"] == "done", widget.state.get("error")
    assert widget.state["update_mode"] == "append"
    assert widget.state["n_added"] > 0
    assert "overlays preserved" in widget.state["mutation_warning"]
    # the system grew (solvent appended) ...
    assert int(msm.get(view, n_atoms=True)) > n0
    # ... and the overlays on the original atoms survived
    assert view.selections.contains("ca"), "selection lost after solvate"
    assert len(view._atom_color_map) == n_colors, "per-atom colors lost after solvate"  # noqa: SLF001

    molsysviewer.addons.clear()


def test_molecular_mechanics_minimize_reports_coordinate_update(monkeypatch):
    from molsysviewer_molsysmt.panels import mechanics as mechanics_panel

    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]
    calls = []

    def fake_minimize_energy(view_arg, *, platform):
        calls.append(("minimize", view_arg, platform))
        return SimpleNamespace(coordinates=[[[0.0, 0.0, 0.0]]])

    def fake_set_coordinates(coordinates):
        calls.append(("set_coordinates", coordinates))

    monkeypatch.setattr(mechanics_panel, "minimize_energy", fake_minimize_energy)
    monkeypatch.setattr(view, "set_coordinates", fake_set_coordinates)

    widget = view.addons.resolve_panel_widget("molsysmt", "molecular_mechanics")
    sent = []
    widget.send = lambda msg: sent.append(msg)
    widget.handle_action(view, "minimize_energy", {"platform": "Reference"})
    molsysviewer.addons.clear()
    assert calls[0] == ("minimize", view, "Reference")
    assert calls[1] == ("set_coordinates", [[[0.0, 0.0, 0.0]]])
    assert widget.state["status"] == "done"
    assert widget.state["update_mode"] == "coordinates"
    assert "overlays preserved" in widget.state["mutation_warning"]


def test_build_replace_reports_destructive_update(monkeypatch):
    from molsysviewer_molsysmt.panels import build as build_panel

    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]
    calls = []

    def fake_build_operation(view_arg, operation):
        calls.append(("build", view_arg, operation))
        return SimpleNamespace(
            operation=operation,
            molecular_system="new-system",
            label="Make Bioassembly",
            log_message="Make Bioassembly: replaced system.",
            mode="replace",
            added_system=None,
            n_added=0,
        )

    def fake_load(molecular_system, *, mode):
        calls.append(("load", molecular_system, mode))

    monkeypatch.setattr(build_panel, "run_build_operation", fake_build_operation)
    monkeypatch.setattr(view, "load", fake_load)

    widget = view.addons.resolve_panel_widget("molsysmt", "build")
    sent = []
    widget.send = lambda msg: sent.append(msg)
    widget.handle_action(view, "bioassembly", {})
    molsysviewer.addons.clear()
    assert calls == [
        ("build", view, "bioassembly"),
        ("load", "new-system", "replace"),
    ]
    assert widget.state["status"] == "done"
    assert widget.state["update_mode"] == "replace"
    assert widget.state["n_added"] == 0
    assert "overlays reset" in widget.state["mutation_warning"]


def test_build_noop_reports_no_structural_change(monkeypatch):
    from molsysviewer_molsysmt.panels import build as build_panel

    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]
    calls = []

    def fake_build_operation(view_arg, operation):
        calls.append(("build", view_arg, operation))
        return SimpleNamespace(
            operation=operation,
            molecular_system=view_arg,
            label="Add Missing Bonds",
            log_message="Add Missing Bonds: no changes.",
            mode="noop",
            added_system=None,
            n_added=0,
        )

    monkeypatch.setattr(build_panel, "run_build_operation", fake_build_operation)

    widget = view.addons.resolve_panel_widget("molsysmt", "build")
    sent = []
    widget.send = lambda msg: sent.append(msg)
    widget.handle_action(view, "add_bonds", {})
    molsysviewer.addons.clear()
    assert calls == [("build", view, "add_bonds")]
    assert widget.state["status"] == "done"
    assert widget.state["update_mode"] == "noop"
    assert widget.state["n_added"] == 0
    assert "No structural changes" in widget.state["mutation_warning"]
