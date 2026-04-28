"""Addon definition for the MolSysMT MolSysViewer integration."""

from molsysviewer import (
    AddonContextActionSpec,
    AddonExportHelperSpec,
    AddonLifecycleSpec,
    AddonPanelSpec,
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
    description="MolSysMT workspace for molecular system inspection in MolSysViewer.",
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
            description="Summary panel with loaded molecular system info.",
            order=10,
            widget_class="molsysviewer_molsysmt.panels.system.MolSysMTSystemPanel",
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
    ),
    workbench_sections=(
        AddonWorkbenchSectionSpec(
            id="system-info",
            title="System Info",
            entry="molsysviewer_molsysmt.workbench.system_info",
            target_panel="workbench",
            order=10,
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
        "status": "skeleton",
        "rendering_ready": False,
    },
)

ADDON = addon


def get_addon() -> AddonSpec:
    return addon
