"""Shared SMonitor telemetry helper for the addon adapters.

The heavy panel-only adapter functions (energy minimization, build operations,
PBC transforms, structure analyses) are decorated with ``@signal`` so SMonitor's
slow-signal profiling reports how big the system was. All adapter entry points
take the ``view`` as their first positional argument, so a single ``extra_factory``
works for all of them.
"""

from __future__ import annotations

from typing import Any


def adapter_n_atoms(args: tuple, kwargs: dict[str, Any]) -> dict[str, int]:
    """``@signal`` extra_factory: ``{"n_atoms": ...}`` from the adapter's view arg.

    Reads ``view.molsys`` from the first positional argument (or the ``view``
    keyword). Never raises; returns ``{"n_atoms": 0}`` if unavailable.
    """
    view = args[0] if args else kwargs.get("view")
    try:
        if view is not None and getattr(view, "molsys", None) is not None:
            return {"n_atoms": int(view.molsys.get_n_atoms())}
    except Exception:
        pass
    return {"n_atoms": 0}
