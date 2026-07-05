"""Export-helper payloads for the MolSysMT MolSysViewer addon."""

from __future__ import annotations

from typing import Any

from .access import has_system
from .runtime import ensure_runtime


def export_system(view: Any) -> dict[str, Any]:
    """Return a lightweight export recipe for the active MolSysMT view state."""
    payload: dict[str, Any] = {
        "title": "MolSysMT system summary",
        "has_system": has_system(view),
    }
    if has_system(view):
        from .adapters.system import system_counts

        payload["counts"] = system_counts(view)

    runtime = ensure_runtime(view)
    payload["molsysmt_addon"] = {
        "last_color_property": runtime.last_color_property,
        "last_color_element": runtime.last_color_element,
        "contacts_tag": runtime.contacts_tag,
        "last_selection_tag": runtime.last_selection_tag,
    }
    return payload
