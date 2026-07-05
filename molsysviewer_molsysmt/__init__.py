"""MolSysViewer addon for MolSysMT — full molecular system workspace.

Importing this package is light: it does not pull MolSysViewer. The addon spec,
lifecycle, and panel widgets (all of which import MolSysViewer) are resolved
lazily through the module-level ``__getattr__`` on first access.
"""

from __future__ import annotations

import importlib

# Light imports only (runtime/access pull nothing heavy at import time).
from .runtime import (
    MolSysMTAddonRuntime,
    create_molsysmt_state,
    ensure_runtime,
    record_event,
)
from .access import (
    has_system,
    materialize_system,
    system_for_verbs,
    system_object,
)

_ADDON_EXPORTS = (
    "addon",
    "ADDON",
    "get_addon",
    "lifecycle",
    "on_enable",
    "on_disable",
    "on_context_action",
    "on_active_selection_changed",
)

_PANEL_EXPORTS = (
    "MolSysMTBasicPanel",
    "MolSysMTColorPanel",
    "MolSysMTStructurePanel",
    "MolSysMTHBondsPanel",
    "MolSysMTTopologyPanel",
    "MolSysMTPBCPanel",
    "MolSysMTMechanicsPanel",
    "MolSysMTBuildPanel",
)

_resolving = False


def __getattr__(name: str):
    # Resolve MolSysViewer-coupled surfaces lazily so a bare
    # ``import molsysviewer_molsysmt`` stays light. The reentrancy guard breaks
    # the submodule/attribute name collision (``addon`` submodule vs the ``addon``
    # spec export); resolved values are cached into globals so later access does
    # not hit __getattr__ and the package ``addon`` attribute is the spec, not the
    # submodule (host discovery relies on this).
    global _resolving
    if _resolving:
        raise AttributeError(name)

    if name in _ADDON_EXPORTS:
        _resolving = True
        try:
            mod = importlib.import_module(f"{__name__}.addon")
            for key in _ADDON_EXPORTS:
                globals()[key] = getattr(mod, key)
        finally:
            _resolving = False
        return globals()[name]

    if name in _PANEL_EXPORTS:
        _resolving = True
        try:
            mod = importlib.import_module(f"{__name__}.panels")
            for key in _PANEL_EXPORTS:
                globals()[key] = getattr(mod, key)
        finally:
            _resolving = False
        return globals()[name]

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "MolSysMTAddonRuntime",
    "create_molsysmt_state",
    "ensure_runtime",
    "record_event",
    "has_system",
    "materialize_system",
    "system_for_verbs",
    "system_object",
    *_ADDON_EXPORTS,
    *_PANEL_EXPORTS,
]
