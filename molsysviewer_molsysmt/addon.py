"""Addon definition for the MolSysMT MolSysViewer integration.

Built lazily: importing this module does not import MolSysViewer. The
``AddonSpec`` and lifecycle are constructed on first access through
``get_addon()`` / ``get_lifecycle()`` (and the module-level ``__getattr__``),
and every MolSysViewer import happens inside those functions and the lifecycle
callbacks. This keeps ``import molsysviewer_molsysmt`` light.
"""

from __future__ import annotations

from .runtime import ensure_runtime, record_event


def on_enable(view) -> None:
    runtime = ensure_runtime(view)
    runtime.enabled = True
    record_event(view, "enable", workspace=runtime.workspace)


def on_disable(view) -> None:
    runtime = ensure_runtime(view)
    runtime.enabled = False
    record_event(view, "disable", workspace=runtime.workspace)


def on_context_action(view, action_id: str, payload: dict) -> None:
    runtime = ensure_runtime(view)
    runtime.last_context_action = {"action_id": action_id, "payload": dict(payload)}
    record_event(view, "context_action", action_id=action_id)
    from . import context

    handlers = {
        "inspect-system": context.inspect_system,
        "select-and-highlight": context.select_and_highlight,
        "color-by-property": context.color_by_property,
        "compute-contacts": context.compute_contacts,
        "molsysmt-expand-residues": context.expand_selection_to_residues,
    }
    handler = handlers.get(action_id)
    if handler is not None:
        handler(view, payload)


def on_active_selection_changed(view, selection):
    """Map the current atom selection to dynamic MolSysMT context-menu items.

    Called by the host on every active-selection change; returns a list of item
    dicts (empty when nothing is selected). Clicks route back through
    ``on_context_action``.
    """
    selection = selection or {}
    atom_indices = list(selection.get("atom_indices") or [])
    if not atom_indices:
        return []
    return [
        {
            "id": "molsysmt-expand-residues",
            "title": f"MolSysMT: expand to whole residues ({len(atom_indices)} atoms)",
            "group": "molsysmt",
            "order": 10,
            "enabled": True,
            "target_kinds": ["structure"],
            "payload": {"atom_indices": atom_indices},
        },
    ]


_addon_instance = None
_lifecycle_instance = None


def _accepts_keyword(callable_obj, keyword: str) -> bool:
    import inspect

    try:
        return keyword in inspect.signature(callable_obj).parameters
    except (TypeError, ValueError):
        return False


_PANEL_SECTIONS = (
    ("basic-inspect", "Inspect", "basic", 10),
    ("basic-select", "Select", "basic", 20),
    ("topology-bonds", "Bond Graph", "topology", 10),
    ("topology-dihedrals", "Dihedral Quartets", "topology", 20),
    ("structure-contacts", "Contacts", "structure", 10),
    ("structure-rms", "RMSD / RMSF", "structure", 20),
    ("structure-pca", "PCA", "structure", 30),
    ("hbonds-buch", "Buch H-Bonds", "hbonds", 10),
    ("pbc-status", "PBC Status", "pbc", 10),
    ("pbc-wrapping", "Wrapping", "pbc", 20),
    ("physchem-color", "Color", "physchem", 10),
    ("mechanics-forces", "Forces", "molecular_mechanics", 10),
    ("mechanics-energy", "Energy", "molecular_mechanics", 20),
    ("mechanics-minimization", "Minimization", "molecular_mechanics", 30),
    ("build-preparation", "Preparation", "build", 10),
    ("build-solvation", "Solvation", "build", 20),
)


def get_lifecycle():
    global _lifecycle_instance
    if _lifecycle_instance is not None:
        return _lifecycle_instance

    from molsysviewer.addons import AddonLifecycleSpec

    kwargs = dict(
        on_enable=on_enable,
        on_disable=on_disable,
        on_context_action=on_context_action,
    )
    # Capability-guarded: only pass the selection hook if the host supports it.
    if _accepts_keyword(AddonLifecycleSpec, "on_active_selection_changed"):
        kwargs["on_active_selection_changed"] = on_active_selection_changed

    _lifecycle_instance = AddonLifecycleSpec(**kwargs)
    return _lifecycle_instance


def get_addon():
    global _addon_instance
    if _addon_instance is not None:
        return _addon_instance

    from molsysviewer.addons import (
        AddonContextActionSpec,
        AddonExportHelperSpec,
        AddonPanelSpec,
        AddonSpec,
        AddonSectionSpec,
        AddonWorkspaceSpec,
    )

    from .runtime import create_molsysmt_state

    addon_kwargs = dict(
        name="molsysmt",
        package="molsysviewer-molsysmt",
        version="0.1.0",
        description=(
            "MolSysMT workspace organized as a mirror of the MolSysMT public "
            "namespaces: basic, topology, structure, H-bonds, PBC, physchem, "
            "molecular mechanics, and build."
        ),
    )
    # Capability guard: only pass state_factory if the host AddonSpec accepts it.
    if _accepts_keyword(AddonSpec, "state_factory"):
        addon_kwargs["state_factory"] = create_molsysmt_state

    _addon_instance = AddonSpec(
        **addon_kwargs,
        workspaces=(
            AddonWorkspaceSpec(
                id="molsysmt",
                title="MolSysMT",
                entry_panel="basic",
                description="Workspace mirroring the MolSysMT public namespaces.",
                order=10,
            ),
        ),
        panels=(
            AddonPanelSpec(
                id="basic",
                title="Basic",
                entry="molsysviewer_molsysmt.panels.basic",
                description="Basic MolSysMT verbs: inspect, select, add, remove, and conversion-oriented workflows.",
                order=10,
                widget_class="molsysviewer_molsysmt.panels.basic.MolSysMTBasicPanel",
            ),
            AddonPanelSpec(
                id="topology",
                title="Topology",
                entry="molsysviewer_molsysmt.panels.topology",
                description="Topology namespace: bond graph, dihedrals, chains, and sequence analysis.",
                order=20,
                widget_class="molsysviewer_molsysmt.panels.topology.MolSysMTTopologyPanel",
            ),
            AddonPanelSpec(
                id="structure",
                title="Structure",
                entry="molsysviewer_molsysmt.panels.structure",
                description="Structure namespace: contacts, distances, RMSD/RMSF, PCA, centering, and fitting.",
                order=30,
                widget_class="molsysviewer_molsysmt.panels.structure.MolSysMTStructurePanel",
            ),
            AddonPanelSpec(
                id="hbonds",
                title="H-Bonds",
                entry="molsysviewer_molsysmt.panels.hbonds",
                description="H-bonds namespace: Buch and Luzar-Chandler hydrogen-bond workflows.",
                order=40,
                widget_class="molsysviewer_molsysmt.panels.hbonds.MolSysMTHBondsPanel",
            ),
            AddonPanelSpec(
                id="pbc",
                title="PBC",
                entry="molsysviewer_molsysmt.panels.pbc",
                description="PBC namespace: box inspection, wrapping, unwrapping, and MIC operations.",
                order=50,
                widget_class="molsysviewer_molsysmt.panels.pbc.MolSysMTPBCPanel",
            ),
            AddonPanelSpec(
                id="physchem",
                title="Physchem",
                entry="molsysviewer_molsysmt.panels.color",
                description="Physchem namespace: charge, mass, SASA, hydrophobicity, polarity, and related coloring.",
                order=60,
                widget_class="molsysviewer_molsysmt.panels.color.MolSysMTColorPanel",
            ),
            AddonPanelSpec(
                id="molecular_mechanics",
                title="Molecular Mechanics",
                entry="molsysviewer_molsysmt.panels.mechanics",
                description="Molecular mechanics namespace: forces, potential energy, and minimization.",
                order=70,
                widget_class="molsysviewer_molsysmt.panels.mechanics.MolSysMTMechanicsPanel",
            ),
            AddonPanelSpec(
                id="build",
                title="Build",
                entry="molsysviewer_molsysmt.panels.build",
                description="Build namespace: hydrogens, bonds, missing atoms, solvation, mutation, and bioassemblies.",
                order=80,
                widget_class="molsysviewer_molsysmt.panels.build.MolSysMTBuildPanel",
            ),
        ),
        context_actions=(
            AddonContextActionSpec(
                id="inspect-system",
                title="Inspect System",
                entry="molsysviewer_molsysmt.context.inspect_system",
                target_kinds=("structure",),
                group="molsysmt",
                order=10,
            ),
            AddonContextActionSpec(
                id="select-and-highlight",
                title="Select & Highlight",
                entry="molsysviewer_molsysmt.context.select_and_highlight",
                target_kinds=("structure",),
                group="molsysmt",
                order=20,
            ),
            AddonContextActionSpec(
                id="color-by-property",
                title="Color by Property",
                entry="molsysviewer_molsysmt.context.color_by_property",
                target_kinds=("structure",),
                group="molsysmt",
                order=30,
            ),
            AddonContextActionSpec(
                id="compute-contacts",
                title="Compute Contacts",
                entry="molsysviewer_molsysmt.context.compute_contacts",
                target_kinds=("structure",),
                group="molsysmt",
                order=40,
            ),
        ),
        addon_sections=(
            AddonSectionSpec(
                id="system-info",
                title="System Info",
                entry="molsysviewer_molsysmt.workbench.system_info",
                target_panel="addons",
                order=10,
            ),
            AddonSectionSpec(
                id="mvp-overlays",
                title="MVP Overlays",
                entry="molsysviewer_molsysmt.workbench.mvp_overlays",
                target_panel="addons",
                order=20,
            ),
            *tuple(
                AddonSectionSpec(
                    id=section_id,
                    title=title,
                    entry=f"molsysviewer_molsysmt.workbench.{section_id.replace('-', '_')}",
                    target_panel="addons",
                    order=order,
                    meta={"panel": panel_id},
                )
                for section_id, title, panel_id, order in _PANEL_SECTIONS
            ),
        ),
        export_helpers=(
            AddonExportHelperSpec(
                id="system-export",
                title="MolSysMT System Export",
                entry="molsysviewer_molsysmt.exports.export_system",
                formats=("json",),
                order=10,
            ),
        ),
        meta={
            "domain": "molecular_systems",
            "status": "alpha",
            "rendering_ready": True,
        },
    )
    return _addon_instance


def __getattr__(name: str):
    if name in ("addon", "ADDON"):
        return get_addon()
    if name == "lifecycle":
        return get_lifecycle()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
