"""Runtime state for the MolSysMT MolSysViewer addon."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MolSysMTAddonRuntime:
    enabled: bool = False
    workspace: str = "molsysmt"
    molecular_system: Any = None
    n_atoms: int | None = None
    n_residues: int | None = None
    n_chains: int | None = None
    n_frames: int | None = None
    last_context_action: dict[str, Any] | None = None
    event_log: list[dict[str, Any]] = field(default_factory=list)


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
