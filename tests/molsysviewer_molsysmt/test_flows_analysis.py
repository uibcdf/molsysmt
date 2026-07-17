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
# Contacts adapter/facade/panel — computes pairs and renders links
# ---------------------------------------------------------------------------

def test_contact_pairs_adapter_reads_from_view():
    pytest.importorskip("molsysmt")
    from molsysviewer_molsysmt.adapters.structure import contact_pairs

    view = molsysviewer.demo["dialanine"]

    result = contact_pairs(view, threshold="3 angstroms")

    assert result.n_contacts > 0
    assert result.atom_pairs == result.structures[0]
    assert all(len(pair) == 2 for pair in result.atom_pairs)


def test_contact_pairs_adapter_raises_without_system():
    from molsysviewer_molsysmt.adapters.structure import contact_pairs

    view = molsysviewer.MolSysView()
    with pytest.raises(ValueError, match="No molecular system"):
        contact_pairs(view)


def test_structure_analysis_adapters_raise_without_system():
    from molsysviewer_molsysmt.adapters.structure import pca, rmsd, rmsf

    view = molsysviewer.MolSysView()

    with pytest.raises(ValueError, match="No molecular system"):
        rmsd(view)
    with pytest.raises(ValueError, match="No molecular system"):
        rmsf(view)
    with pytest.raises(ValueError, match="No molecular system"):
        pca(view)


def test_pca_adapter_maps_flat_pc1_to_selected_atom_vectors():
    msm = pytest.importorskip("molsysmt")
    from molsysviewer_molsysmt.adapters.structure import pca

    view = molsysviewer.demo["dialanine"]
    result = pca(view, selection='atom_name=="CA"')
    expected_atom_indices = msm.select(view, element="atom", selection='atom_name=="CA"')

    assert result.pc1_vectors.shape == (len(result.atom_indices), 3)
    assert result.atom_indices == list(expected_atom_indices)
    assert result.principal_components.shape[1] == 3 * len(result.atom_indices)


def test_show_facade_contacts_renders_links_and_tracks_tag():
    pytest.importorskip("molsysmt")
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]
    tag = "test-molsysmt-contacts"
    view.shapes.clear(tag=tag)

    result = view.addons.molsysmt.show.contacts(threshold="3 angstroms", tag=tag)

    assert result.n_contacts > 0
    assert view.addons.molsysmt.contacts_result is result
    assert view.addons.molsysmt.contacts_tag == tag
    assert view.shapes.contains(tag)

    view.addons.molsysmt.show.clear_contacts(tag=tag)
    assert not view.shapes.contains(tag)
    molsysviewer.addons.clear()


def test_structure_panel_contacts_uses_loaded_view_not_runtime_seed():
    pytest.importorskip("molsysmt")
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]
    view.shapes.clear(tag="molsysmt-contacts")

    widget = view.addons.resolve_panel_widget("molsysmt", "structure")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    runtime = ensure_runtime(view)

    widget.handle_action(view, "compute_contacts", {"threshold_angstroms": 3.0})
    final = widget.state
    assert final["status"] == "done"
    assert final["contacts_n"] > 0
    assert runtime.contacts_tag == "molsysmt-contacts"
    assert view.shapes.contains("molsysmt-contacts")

    view.shapes.clear(tag="molsysmt-contacts")
    molsysviewer.addons.clear()


def test_structure_panel_clear_contacts_removes_viewer_links():
    pytest.importorskip("molsysmt")
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]
    view.shapes.clear(tag="molsysmt-contacts")
    view.addons.molsysmt.show.contacts(threshold="3 angstroms")
    assert view.shapes.contains("molsysmt-contacts")

    widget = view.addons.resolve_panel_widget("molsysmt", "structure")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "clear_contacts", {})
    final = widget.state
    assert final["status"] == "idle"
    assert final["contacts_n"] is None
    assert not view.shapes.contains("molsysmt-contacts")
    assert view.addons.molsysmt.contacts_tag is None

    molsysviewer.addons.clear()


# ---------------------------------------------------------------------------
# H-Bonds panel — no-system error
# ---------------------------------------------------------------------------

def test_hbond_links_adapter_reads_from_view():
    pytest.importorskip("molsysmt")
    from molsysviewer_molsysmt.adapters.hbonds import buch_hbond_links

    view = molsysviewer.demo["dialanine"]

    result = buch_hbond_links(view)

    assert result.method == "buch"
    assert result.n_hbonds > 0
    assert result.structures[0] == [[6, 15]]


def test_hbond_links_adapter_raises_without_system():
    from molsysviewer_molsysmt.adapters.hbonds import buch_hbond_links

    view = molsysviewer.MolSysView()
    with pytest.raises(ValueError, match="No molecular system"):
        buch_hbond_links(view)


def test_show_facade_hbonds_renders_links_and_tracks_tag():
    pytest.importorskip("molsysmt")
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]
    tag = "test-molsysmt-hbonds"
    view.shapes.clear(tag=tag)

    result = view.addons.molsysmt.show.hbonds(tag=tag)

    assert result.n_hbonds > 0
    assert view.addons.molsysmt.hbonds_result is result
    assert view.addons.molsysmt.hbonds_tag == tag
    assert view.shapes.contains(tag)

    view.addons.molsysmt.show.clear_hbonds(tag=tag)
    assert not view.shapes.contains(tag)
    molsysviewer.addons.clear()


def test_hbonds_panel_compute_with_no_molsys_pushes_error():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("molsysmt", "hbonds")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "compute_hbonds", {})
    molsysviewer.addons.clear()
    assert widget.state["status"] == "error"


def test_hbonds_panel_uses_loaded_view_not_runtime_seed():
    pytest.importorskip("molsysmt")
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]
    view.shapes.clear(tag="msmt-hbonds")

    widget = view.addons.resolve_panel_widget("molsysmt", "hbonds")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    runtime = ensure_runtime(view)

    widget.handle_action(view, "compute_hbonds", {})
    final = widget.state
    assert final["status"] == "done"
    assert final["n_hbonds"] > 0
    assert runtime.hbonds_tag == "msmt-hbonds"
    assert view.shapes.contains("msmt-hbonds")

    view.shapes.clear(tag="msmt-hbonds")
    molsysviewer.addons.clear()


def test_hbonds_panel_clear_removes_viewer_links():
    pytest.importorskip("molsysmt")
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.demo["dialanine"]
    view.shapes.clear(tag="msmt-hbonds")
    view.addons.molsysmt.show.hbonds()
    assert view.shapes.contains("msmt-hbonds")

    widget = view.addons.resolve_panel_widget("molsysmt", "hbonds")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "clear_hbonds", {})
    final = widget.state
    assert final["status"] == "idle"
    assert final["n_hbonds"] is None
    assert not view.shapes.contains("msmt-hbonds")
    assert view.addons.molsysmt.hbonds_tag is None

    molsysviewer.addons.clear()


# ---------------------------------------------------------------------------
# Topology adapter/panel — bond graph and standard dihedrals from the view
# ---------------------------------------------------------------------------

def test_topology_bond_graph_adapter_reads_from_view():
    pytest.importorskip("molsysmt")
    from molsysviewer_molsysmt.adapters.topology import bond_graph_links

    view = molsysviewer.demo["dialanine"]

    result = bond_graph_links(view)

    assert result.n_bonds == 21
    assert all(len(pair) == 2 for pair in result.atom_pairs)
    assert result.graph.number_of_edges() == result.n_bonds


def test_topology_dihedral_quartets_adapter_reads_from_view():
    pytest.importorskip("molsysmt")
    from molsysviewer_molsysmt.adapters.topology import dihedral_quartets

    view = molsysviewer.demo["dialanine"]

    result = dihedral_quartets(view, dihedral_types=("phi", "psi"))

    assert result.dihedral_types == ("phi", "psi")
    assert result.n_dihedrals > 0
    assert all(len(quartet) == 4 for quartet in result.quartets)


def test_topology_adapters_raise_without_system():
    from molsysviewer_molsysmt.adapters.topology import bond_graph_links, dihedral_quartets

    view = molsysviewer.MolSysView()

    with pytest.raises(ValueError, match="No molecular system"):
        bond_graph_links(view)
    with pytest.raises(ValueError, match="No molecular system"):
        dihedral_quartets(view)
