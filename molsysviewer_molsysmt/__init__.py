"""MolSysViewer addon for MolSysMT — molecular system inspection."""

from .addon import ADDON, addon, get_addon, lifecycle, on_enable, on_disable, on_context_action
from .runtime import MolSysMTAddonRuntime, ensure_runtime, record_event
from .panels import MolSysMTSystemPanel

__all__ = [
    "ADDON",
    "addon",
    "get_addon",
    "lifecycle",
    "on_enable",
    "on_disable",
    "on_context_action",
    "MolSysMTAddonRuntime",
    "ensure_runtime",
    "record_event",
    "MolSysMTSystemPanel",
]
