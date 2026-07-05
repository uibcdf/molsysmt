"""Pure MolSysMT build adapters for the MolSysViewer addon."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from ..access import has_system, materialize_system


BuildOperation = Literal["add_hydrogens", "add_bonds", "bioassembly", "solvate"]
ReconcileMode = Literal["append", "replace", "noop"]


@dataclass(frozen=True)
class BuildResult:
    """Result of a MolSysMT build operation.

    ``mode`` tells the caller how to apply it to the viewer without needlessly
    losing overlays:

    - ``"append"``: the operation only added atoms at the end (original atoms
      keep their indices), so apply it with ``view.add(added_system)`` — which
      reconciles regions/selections/colors instead of resetting them.
    - ``"replace"``: the operation restructured the system, so apply it with
      ``view.load(molecular_system, mode="replace")`` (destructive — overlays are
      cleared).
    - ``"noop"``: nothing changed.
    """

    operation: BuildOperation
    molecular_system: Any
    label: str
    log_message: str
    mode: ReconcileMode
    added_system: Any = None
    n_added: int = 0


def _prefix_unchanged(original: Any, new: Any, n0: int) -> bool:
    """True when the first ``n0`` atoms of ``new`` match ``original`` (append)."""
    import molsysmt as msm

    if int(msm.get(new, n_atoms=True)) < n0:
        return False
    original_names = list(msm.get(original, element="atom", atom_name=True))
    new_names = list(msm.get(new, element="atom", atom_name=True))
    return new_names[:n0] == original_names


def run_build_operation(view: Any, operation: BuildOperation) -> BuildResult:
    """Materialize the active viewer system and run one build operation.

    Detects whether the operation is a pure append so the caller can reconcile
    the viewer with ``view.add`` (overlay-preserving) instead of a destructive
    reload.
    """
    if not has_system(view):
        raise ValueError("No molecular system attached.")

    import molsysmt as msm

    ms = materialize_system(view)
    n0 = int(msm.get(ms, n_atoms=True))

    n_bonds0 = int(msm.get(ms, n_bonds=True))

    if operation == "add_hydrogens":
        new_ms = msm.build.add_missing_hydrogens(ms)
        label = "add hydrogens"
        log_message = "Added missing hydrogens."
    elif operation == "add_bonds":
        new_ms = msm.build.add_missing_bonds(ms, in_place=False)
        label = "add bonds"
        log_message = "Added missing bonds."
    elif operation == "bioassembly":
        new_ms = msm.build.make_bioassembly(ms)
        label = "make bioassembly"
        log_message = "Biological assembly expanded."
    elif operation == "solvate":
        new_ms = msm.build.solvate(ms)
        label = "solvate"
        log_message = "System solvated."
    else:
        raise ValueError(f"Unsupported build operation: {operation!r}")

    n_added = int(msm.get(new_ms, n_atoms=True)) - n0

    if operation == "add_bonds":
        mode = "replace" if int(msm.get(new_ms, n_bonds=True)) > n_bonds0 else "noop"
        added = None
    elif _prefix_unchanged(ms, new_ms, n0):
        if n_added <= 0:
            mode: ReconcileMode = "noop"
            added = None
        else:
            mode = "append"
            added = msm.extract(new_ms, selection=f"atom_index>={n0}")
    else:
        mode = "replace"
        added = None

    return BuildResult(
        operation=operation,
        molecular_system=new_ms,
        label=label,
        log_message=log_message,
        mode=mode,
        added_system=added,
        n_added=max(n_added, 0),
    )
