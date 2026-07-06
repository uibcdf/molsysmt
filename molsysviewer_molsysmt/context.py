"""Context-action entry points for the MolSysMT MolSysViewer addon."""

from __future__ import annotations

from typing import Any

from .runtime import ensure_runtime, record_event


def inspect_system(view: Any, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """Inspect the active viewer system through the shared system adapter."""
    from .adapters.system import system_counts

    counts = system_counts(view)
    runtime = ensure_runtime(view)
    runtime.n_atoms = counts["n_atoms"]
    runtime.n_residues = counts["n_residues"]
    runtime.n_chains = counts["n_chains"]
    runtime.n_frames = counts["n_frames"]
    record_event(view, "context_inspect_system", **counts)
    return counts


def select_and_highlight(view: Any, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """Run a MolSysMT selection and activate it in the viewer."""
    payload = dict(payload or {})
    selection = payload.get("selection", "all")
    element = payload.get("element", "atom")
    result = ensure_runtime(view).show.select(selection=selection, element=element)
    return {
        "selection": selection,
        "element": element,
        "n_selected": result.n_selected,
        "n_atoms": len(result.atom_indices),
    }


def color_by_property(view: Any, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """Color the active viewer system by a supported MolSysMT property."""
    payload = dict(payload or {})
    property_name = payload.get("property", "charge")
    palette = payload.get("palette", "viridis")
    result = ensure_runtime(view).show.color_by(property_name, palette=palette)
    return {
        "property": result.property,
        "element": result.element,
        "n_values": len(result.values),
        "unit": result.unit,
    }


def compute_contacts(view: Any, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """Compute MolSysMT contacts and render them as viewer links."""
    payload = dict(payload or {})
    threshold = payload.get("threshold", "4 angstroms")
    selection = payload.get("selection", "all")
    result = ensure_runtime(view).show.contacts(selection=selection, threshold=threshold)
    return {
        "selection": selection,
        "threshold": result.threshold,
        "n_contacts": result.n_contacts,
    }


def remove_selected_atoms(view: Any, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """Remove selected atoms through the MolSysMT addon facade."""
    payload = dict(payload or {})
    atom_indices = payload.get("atom_indices")
    if not atom_indices:
        atom_indices = (payload.get("addon_action_payload") or {}).get("atom_indices")
    if not atom_indices:
        active_selection = getattr(view, "active_selection", None)
        atom_indices = [] if active_selection is None else list(active_selection.atom_indices)
    atom_indices = list(atom_indices or [])
    if not atom_indices:
        raise ValueError("MolSysMT remove-selected-atoms requires a non-empty atom selection.")

    ensure_runtime(view).basic.remove(selection=atom_indices)
    record_event(view, "context_remove_selected_atoms", n_atoms=len(atom_indices))
    return {"n_removed": len(atom_indices)}


def expand_selection_to_residues(view: Any, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """Expand the selected atoms to their whole residues and highlight them.

    Drives the selection-driven context item produced by
    ``on_active_selection_changed``. The dynamic item's payload may arrive nested
    under ``addon_action_payload`` depending on the host, so both are accepted.
    """
    payload = dict(payload or {})
    atom_indices = payload.get("atom_indices")
    if not atom_indices:
        atom_indices = (payload.get("addon_action_payload") or {}).get("atom_indices")
    atom_indices = list(atom_indices or [])
    if not atom_indices:
        return {"n_atoms": 0, "n_residues": 0}

    import molsysmt as msm

    groups = sorted(
        {int(g) for g in msm.get(view, element="atom", selection=atom_indices, group_index=True)}
    )
    view.active_selection.set(f"group_index in {groups}")
    n_atoms = len(view.active_selection.atom_indices)
    record_event(view, "context_expand_residues", n_atoms=n_atoms, n_residues=len(groups))
    return {"n_atoms": n_atoms, "n_residues": len(groups)}
