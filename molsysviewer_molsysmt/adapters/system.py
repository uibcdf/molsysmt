"""System adapter — molecular-system summary counts for a view.

Pure functions operating on the view as a MolSysMT form. This is also the public
Python equivalent of the Basic panel's "inspect" action:

    >>> from molsysviewer_molsysmt.adapters.system import system_counts
    >>> system_counts(view)
    {'n_atoms': ..., 'n_residues': ..., 'n_chains': ..., 'n_frames': ...}
"""

from __future__ import annotations

from typing import Any

from ..access import has_system


def system_counts(view: Any) -> dict[str, int]:
    """Return atom / residue / chain / structure counts for the view's system.

    Operates on the view-as-form (``msm.get(view, ...)``); holds nothing. Raises
    ``ValueError`` if the view has no molecular system loaded.
    """
    if not has_system(view):
        raise ValueError("No molecular system attached.")

    import molsysmt as msm

    return {
        "n_atoms": int(msm.get(view, n_atoms=True)),
        "n_residues": int(msm.get(view, element="group", n_groups=True)),
        "n_chains": int(msm.get(view, element="chain", n_chains=True)),
        "n_frames": int(msm.get(view, element="system", n_structures=True)),
    }
