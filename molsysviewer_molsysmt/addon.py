"""Addon definition for the MolSysMT MolSysViewer integration."""

from molsysviewer import (
    AddonContextActionSpec,
    AddonExportHelperSpec,
    AddonLifecycleSpec,
    AddonPanelSpec,
    AddonShapeProviderSpec,
    AddonSpec,
    AddonWorkbenchSectionSpec,
    AddonWorkspaceSpec,
)

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


lifecycle = AddonLifecycleSpec(
    on_enable=on_enable,
    on_disable=on_disable,
    on_context_action=on_context_action,
)

addon = AddonSpec(
    name="molsysmt",
    package="molsysviewer-molsysmt",
    version="0.1.0",
    description="Full MolSysMT workspace: select, color, structure, transform, H-bonds, topology, PBC, mechanics, build.",
    workspaces=(
        AddonWorkspaceSpec(
            id="molsysmt",
            title="MolSysMT",
            entry_panel="system",
            description="Workspace for MolSysMT molecular system exploration.",
            order=10,
        ),
    ),
    panels=(
        AddonPanelSpec(
            id="system",
            title="System",
            entry="molsysviewer_molsysmt.panels.system",
            description="Loaded molecular system summary with inspect trigger.",
            order=10,
            widget_class="molsysviewer_molsysmt.panels.system.MolSysMTSystemPanel",
        ),
        AddonPanelSpec(
            id="select",
            title="Select",
            entry="molsysviewer_molsysmt.panels.select",
            description="Run MolSysMT selections and highlight in viewer.",
            order=20,
            widget_class="molsysviewer_molsysmt.panels.select.MolSysMTSelectPanel",
        ),
        AddonPanelSpec(
            id="color",
            title="Color",
            entry="molsysviewer_molsysmt.panels.color",
            description="Color atoms by physchem properties, RMSF, or secondary structure.",
            order=30,
            widget_class="molsysviewer_molsysmt.panels.color.MolSysMTColorPanel",
        ),
        AddonPanelSpec(
            id="structure",
            title="Structure",
            entry="molsysviewer_molsysmt.panels.structure",
            description="Contacts, RMSD, RMSF, and PCA analysis.",
            order=40,
            widget_class="molsysviewer_molsysmt.panels.structure.MolSysMTStructurePanel",
        ),
        AddonPanelSpec(
            id="transform",
            title="Transform",
            entry="molsysviewer_molsysmt.panels.transform",
            description="Center, RMSD-fit, and align principal axes with viewer reload.",
            order=50,
            widget_class="molsysviewer_molsysmt.panels.transform.MolSysMTTransformPanel",
        ),
        AddonPanelSpec(
            id="hbonds",
            title="H-Bonds",
            entry="molsysviewer_molsysmt.panels.hbonds",
            description="Compute Baker-Hubbard H-bonds and render as links.",
            order=60,
            widget_class="molsysviewer_molsysmt.panels.hbonds.MolSysMTHBondsPanel",
        ),
        AddonPanelSpec(
            id="topology",
            title="Topology",
            entry="molsysviewer_molsysmt.panels.topology",
            description="Bond graph, dihedral quartets, and sequence analysis.",
            order=70,
            widget_class="molsysviewer_molsysmt.panels.topology.MolSysMTTopologyPanel",
        ),
        AddonPanelSpec(
            id="pbc",
            title="PBC",
            entry="molsysviewer_molsysmt.panels.pbc",
            description="Periodic boundary conditions: wrap, unwrap, and MIC.",
            order=80,
            widget_class="molsysviewer_molsysmt.panels.pbc.MolSysMTPBCPanel",
        ),
        AddonPanelSpec(
            id="mechanics",
            title="Mechanics",
            entry="molsysviewer_molsysmt.panels.mechanics",
            description="Force computation, potential energy, and energy minimization.",
            order=90,
            widget_class="molsysviewer_molsysmt.panels.mechanics.MolSysMTMechanicsPanel",
        ),
        AddonPanelSpec(
            id="build",
            title="Build",
            entry="molsysviewer_molsysmt.panels.build",
            description="Add missing atoms/hydrogens, make bioassembly, solvate.",
            order=100,
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
        AddonContextActionSpec(
            id="fit-to-reference",
            title="RMSD Fit to Reference",
            entry="molsysviewer_molsysmt.context.fit_to_reference",
            target_kinds=("structure",),
            group="molsysmt",
            order=50,
        ),
        AddonContextActionSpec(
            id="compute-hbonds",
            title="Compute H-Bonds",
            entry="molsysviewer_molsysmt.context.compute_hbonds",
            target_kinds=("structure",),
            group="molsysmt",
            order=60,
        ),
        AddonContextActionSpec(
            id="wrap-to-pbc",
            title="Wrap to PBC",
            entry="molsysviewer_molsysmt.context.wrap_to_pbc",
            target_kinds=("structure",),
            group="molsysmt",
            order=70,
        ),
        AddonContextActionSpec(
            id="build-bioassembly",
            title="Make Bioassembly",
            entry="molsysviewer_molsysmt.context.build_bioassembly",
            target_kinds=("structure",),
            group="molsysmt",
            order=80,
        ),
    ),
    shape_providers=(
        AddonShapeProviderSpec(
            id="contacts-links",
            title="Contact links",
            entry="molsysviewer_molsysmt.shapes.contacts",
            order=10,
        ),
        AddonShapeProviderSpec(
            id="hbond-links",
            title="H-bond links",
            entry="molsysviewer_molsysmt.shapes.hbonds",
            order=20,
        ),
        AddonShapeProviderSpec(
            id="displacement-vectors",
            title="Displacement vectors",
            entry="molsysviewer_molsysmt.shapes.vectors",
            order=30,
        ),
        AddonShapeProviderSpec(
            id="bond-links",
            title="Bond links",
            entry="molsysviewer_molsysmt.shapes.bonds",
            order=40,
        ),
    ),
    workbench_sections=(
        AddonWorkbenchSectionSpec(
            id="system-info",
            title="System Info",
            entry="molsysviewer_molsysmt.workbench.system_info",
            target_panel="workbench",
            order=10,
        ),
        AddonWorkbenchSectionSpec(
            id="structure-stats",
            title="Structure Stats",
            entry="molsysviewer_molsysmt.workbench.structure_stats",
            target_panel="workbench",
            order=20,
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

ADDON = addon


def get_addon() -> AddonSpec:
    return addon
