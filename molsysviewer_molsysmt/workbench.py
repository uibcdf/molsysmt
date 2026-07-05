"""Workbench section payloads for the MolSysMT MolSysViewer addon."""

from __future__ import annotations

from typing import Any

from .access import has_system
from .runtime import ensure_runtime


_PANEL_SECTION_TITLES = {
    "basic-inspect": "Inspect",
    "basic-select": "Select",
    "topology-bonds": "Bond Graph",
    "topology-dihedrals": "Dihedral Quartets",
    "structure-contacts": "Contacts",
    "structure-rms": "RMSD / RMSF",
    "structure-pca": "PCA",
    "hbonds-buch": "Buch H-Bonds",
    "pbc-status": "PBC Status",
    "pbc-wrapping": "Wrapping",
    "physchem-color": "Color",
    "mechanics-forces": "Forces",
    "mechanics-energy": "Energy",
    "mechanics-minimization": "Minimization",
    "build-preparation": "Preparation",
    "build-solvation": "Solvation",
}


def panel_section(view: Any, section_id: str) -> dict[str, Any]:
    """Return a lightweight payload for a panel subsection contribution."""
    return {
        "key": f"molsysmt:{section_id}",
        "item_title": _PANEL_SECTION_TITLES[section_id],
        "item_subtitle": "MolSysMT panel subsection.",
    }


def system_info(view: Any) -> dict[str, Any]:
    """Return a compact system summary for the Add-ons workspace."""
    if not has_system(view):
        return {
            "key": "molsysmt:system",
            "item_title": "No molecular system",
            "item_subtitle": "Load a system to inspect it with MolSysMT.",
        }

    from .adapters.system import system_counts

    counts = system_counts(view)
    return {
        "key": "molsysmt:system",
        "item_title": f"{counts['n_atoms']} atoms",
        "item_subtitle": (
            f"{counts['n_residues']} groups · {counts['n_chains']} chains · "
            f"{counts['n_frames']} frame(s)"
        ),
        **counts,
    }


def mvp_overlays(view: Any) -> dict[str, Any]:
    """Return the current MVP overlay/session state."""
    runtime = ensure_runtime(view)
    active = []
    if runtime.last_color_property is not None:
        active.append(f"color:{runtime.last_color_property}")
    if runtime.contacts_tag is not None:
        active.append("contacts")
    if runtime.last_selection_tag is not None:
        active.append("selection")

    return {
        "key": "molsysmt:mvp-overlays",
        "item_title": f"{len(active)} active MolSysMT flow(s)",
        "item_subtitle": ", ".join(active) if active else "No active overlay or selection.",
        "active": active,
        "last_color_property": runtime.last_color_property,
        "contacts_tag": runtime.contacts_tag,
        "last_selection_tag": runtime.last_selection_tag,
    }


def __getattr__(name: str):
    section_id = name.replace("_", "-")
    if section_id in _PANEL_SECTION_TITLES:
        def _section(view: Any, _section_id: str = section_id) -> dict[str, Any]:
            return panel_section(view, _section_id)

        _section.__name__ = name
        globals()[name] = _section
        return _section
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
