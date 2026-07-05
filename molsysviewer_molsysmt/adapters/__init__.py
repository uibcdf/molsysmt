"""Adapter layer for the MolSysMT MolSysViewer addon.

Adapters hold all the scientific logic as pure functions that operate on the
MolSysViewer view as a MolSysMT form (``msm.<verb>(view, ...)``). Panels, context
actions, and the public Python surface all call these same adapters, so a GUI
action and its Python equivalent are guaranteed to do the same thing. Adapters
never take a ``molecular_system`` argument and never reach into viewer internals.
"""

from .color import ColorValues, property_values, supported_properties
from .hbonds import HBondLinks, buch_hbond_links
from .select import SelectionResult, select_indices
from .structure import ContactPairs, contact_pairs

__all__ = [
    "ColorValues",
    "ContactPairs",
    "HBondLinks",
    "SelectionResult",
    "buch_hbond_links",
    "contact_pairs",
    "property_values",
    "select_indices",
    "supported_properties",
]
