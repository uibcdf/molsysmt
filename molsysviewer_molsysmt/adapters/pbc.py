"""Pure MolSysMT PBC adapters for the MolSysViewer addon."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from smonitor import signal

from ..access import has_system, materialize_system, system_for_verbs
from ._telemetry import adapter_n_atoms

PBCOperation = Literal["wrap_pbc", "wrap_mic", "unwrap_pbc"]


@dataclass(frozen=True)
class PBCStatus:
    """Periodic-boundary status for the active viewer system."""

    has_pbc: bool


@dataclass(frozen=True)
class PBCTransform:
    """Result of a PBC coordinate transform.

    PBC wrapping/unwrapping changes only coordinates (atoms unchanged), so the
    viewer can reconcile it with ``view.set_coordinates`` — which preserves
    regions, selections, colors and shapes — instead of a destructive reload.
    """

    operation: PBCOperation
    molecular_system: Any
    coordinates: Any = None


def pbc_status(view: Any) -> PBCStatus:
    """Return whether the active viewer system has PBC information."""
    if not has_system(view):
        raise ValueError("No molecular system attached.")

    import molsysmt as msm

    return PBCStatus(has_pbc=bool(msm.pbc.has_pbc(system_for_verbs(view))))


@signal(
    tags=["molsysmt-addon", "adapter", "structure"],
    extra_factory=adapter_n_atoms,
)
def transform_pbc(view: Any, operation: PBCOperation) -> PBCTransform:
    """Materialize the viewer system and apply a MolSysMT PBC transform."""
    if not has_system(view):
        raise ValueError("No molecular system attached.")

    import molsysmt as msm

    ms = materialize_system(view)
    if operation == "wrap_pbc":
        new_ms = msm.pbc.wrap_to_pbc(ms)
    elif operation == "wrap_mic":
        new_ms = msm.pbc.wrap_to_mic(ms)
    elif operation == "unwrap_pbc":
        new_ms = msm.pbc.unwrap(ms)
    else:
        raise ValueError(f"Unsupported PBC operation: {operation!r}")

    coordinates = msm.get(new_ms, coordinates=True)
    return PBCTransform(operation=operation, molecular_system=new_ms, coordinates=coordinates)
