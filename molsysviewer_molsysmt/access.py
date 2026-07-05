"""System-access helpers for the MolSysMT MolSysViewer addon.

The addon holds no molecular system of its own. A MolSysViewer view is a
registered MolSysMT form (``molsysviewer.MolSysView``), so the view itself is
passed straight to the MolSysMT verbs (``msm.get(view, ...)``,
``msm.select(view, ...)``). These helpers are the single seam where that
"operate on the view, hold nothing" decision lives, so adapters never take a
``molecular_system`` argument.
"""

from __future__ import annotations

from typing import Any


def system_for_verbs(view: Any) -> Any:
    """Return the argument to pass to MolSysMT verbs for this view.

    The view is a registered ``molsysviewer.MolSysView`` form, so it is returned
    as-is: ``msm.get(system_for_verbs(view), ...)`` operates on the view's loaded
    system without holding or duplicating it.
    """
    return view


def system_object(view: Any) -> Any:
    """Return the underlying ``molsysmt.MolSys`` via the public ``view.molsys``.

    Same object the viewer owns (do not mutate it in place). Use only for the
    rare verb that does not accept the view-as-form; otherwise prefer
    :func:`system_for_verbs`.
    """
    return getattr(view, "molsys", None)


def has_system(view: Any) -> bool:
    """True when the view has a molecular system loaded."""
    return getattr(view, "molsys", None) is not None


def materialize_system(view: Any, selection: Any = "all", structure_indices: Any = "all") -> Any:
    """Materialize an independent standalone ``molsysmt.MolSys`` from the view.

    Only needed when an operation must produce a new system without mutating the
    view's own (for example a transform previewed before
    ``view.load(new_ms, mode="replace")``). Uses ``msm.extract`` on the
    underlying ``view.molsys``, which always returns a fresh object.

    Note: ``msm.extract(view, ...)`` on the view-as-form currently raises (the
    form's ``extract`` has an incompatible signature), so we extract from the
    underlying MolSys instead.
    """
    import molsysmt as msm

    return msm.extract(view.molsys, selection=selection, structure_indices=structure_indices)
