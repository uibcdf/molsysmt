"""Runtime state for the MolSysMT MolSysViewer addon."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MolSysMTAddonRuntime:
    # Core
    enabled: bool = False
    workspace: str = "molsysmt"
    molecular_system: Any = None
    last_context_action: dict[str, Any] | None = None
    event_log: list[dict[str, Any]] = field(default_factory=list)

    # System panel
    n_atoms: int | None = None
    n_residues: int | None = None
    n_chains: int | None = None
    n_frames: int | None = None

    # Select panel
    last_selection: str | None = None
    last_selection_element: str = "atom"
    last_selection_indices: list[int] | None = None

    # Color panel
    last_color_property: str | None = None
    last_color_element: str = "group"
    last_color_palette: str = "viridis"

    # Structure panel
    contacts_result: Any = None
    rmsd_result: Any = None
    rmsf_result: Any = None
    pca_result: Any = None

    # H-Bonds panel
    hbonds_result: Any = None
    hbonds_tag: str | None = None

    # Topology panel
    bondgraph_result: Any = None
    dihedral_quartets_result: Any = None

    # PBC panel
    pbc_status: bool | None = None

    # Mechanics panel
    forces_result: Any = None
    energy_result: Any = None
    forces_tag: str | None = None

    # Build panel
    last_build_op: str | None = None
    build_log: list[str] = field(default_factory=list)


def ensure_runtime(view: Any) -> MolSysMTAddonRuntime:
    runtime = getattr(view, "_molsysmt_addon_runtime", None)
    if runtime is None:
        runtime = MolSysMTAddonRuntime()
        setattr(view, "_molsysmt_addon_runtime", runtime)
    return runtime


def record_event(view: Any, event: str, **payload: Any) -> MolSysMTAddonRuntime:
    runtime = ensure_runtime(view)
    runtime.event_log.append({"event": event, **payload})
    return runtime
