"""MolSysMT warnings backed by smonitor catalogs."""

from __future__ import annotations

from smonitor.integrations import CatalogWarning
from .emitter import bundle

warn = bundle.warn
warn_once = bundle.warn_once


class MolSysMTCatalogWarning(CatalogWarning):
    def __init__(self, **kwargs):
        from . import CATALOG, META
        super().__init__(catalog=CATALOG, meta=META, **kwargs)


class UserMolSysMTWarning(MolSysMTCatalogWarning):
    pass


class SelectionWarning(UserMolSysMTWarning):
    """Warnings related to selection strings and resolved subsets."""
    catalog_key = "SelectionWarning"


class MolSysMTDeprecationWarning(DeprecationWarning):
    # DeprecationWarning is special in Python, we might not want to inherit from CatalogWarning directly
    # but we can still use the resolution logic if needed.
    pass


class CrossChainCovalentBondsWarning(MolSysMTCatalogWarning):
    catalog_key = "CrossChainCovalentBondsWarning"

    def __init__(self, molecular_system, atom_pairs, caller='CrossChainCovalentBondsWarning'):
        from molsysmt.basic import get_label

        label_pairs_reported = []

        for atom1, atom2 in atom_pairs:
            chain1 = molecular_system.topology.atoms.at[atom1, "chain_index"]
            chain2 = molecular_system.topology.atoms.at[atom2, "chain_index"]
            if chain1 != chain2:
                label1 = get_label(
                    molecular_system,
                    element="atom",
                    selection=atom1,
                    string="{atom_name} {atom_id} in {group_name}{group_id} with atom_index {atom_index}",
                    skip_digestion=True,
                )
                label2 = get_label(
                    molecular_system,
                    element="atom",
                    selection=atom2,
                    string="{atom_name} {atom_id} in {group_name}{group_id} with atom_index {atom_index}",
                    skip_digestion=True,
                )
                label_pairs_reported.append((label1, label2))

        extra = {
            "caller": caller,
            "count": len(label_pairs_reported),
            "pairs": label_pairs_reported,
        }

        super().__init__(extra=extra)


class DownloadWarning(UserMolSysMTWarning):
    catalog_key = "DownloadWarning"


class NotDigestedArgumentWarning(MolSysMTCatalogWarning):
    catalog_key = "NotDigestedArgumentWarning"

    def __init__(self, argument):
        super().__init__(extra={"argument": argument})


class MolecularSystemMismatchWarning(UserMolSysMTWarning):
    catalog_key = "MolecularSystemMismatchWarning"

    def __init__(self, caller='MolecularSystemMismatchWarning', n_models=None):
        extra = {"caller": caller}
        if n_models is not None:
            extra["count"] = n_models
        super().__init__(extra=extra)


__all__ = [
    "UserMolSysMTWarning",
    "SelectionWarning",
    "MolSysMTDeprecationWarning",
    "CrossChainCovalentBondsWarning",
    "DownloadWarning",
    "NotDigestedArgumentWarning",
    "MolecularSystemMismatchWarning",
    "warn",
    "warn_once",
]
