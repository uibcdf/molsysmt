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


class StructuralAttributeDropWarning(UserMolSysMTWarning):
    """Warning about one-sided structural series discarded by intersection."""

    catalog_key = "StructuralAttributeDropWarning"

    def __init__(self, attributes, caller='molsysmt.append_structures'):
        if isinstance(attributes, str):
            Warning.__init__(self, attributes)
            return
        super().__init__(extra={
            "attributes": ", ".join(attributes),
            "caller": caller,
        })


class SlowChunkIOWarning(MolSysMTCatalogWarning):
    catalog_key = "SlowChunkIOWarning"

    def __init__(self, chunk_index, io_time_s):
        super().__init__(extra={"chunk_index": chunk_index, "io_time_s": io_time_s})


class MemoryPressureWarning(MolSysMTCatalogWarning):
    catalog_key = "MemoryPressureWarning"

    def __init__(self, chunk_index, rss_bytes, budget_bytes, pressure_pct):
        super().__init__(extra={
            "chunk_index": chunk_index,
            "rss_bytes": rss_bytes,
            "budget_bytes": budget_bytes,
            "pressure_pct": pressure_pct,
        })


class UnknownAtomNameWarning(MolSysMTCatalogWarning):
    catalog_key = "UnknownAtomNameWarning"

    def __init__(self, atom_name):
        super().__init__(extra={"atom_name": atom_name})


class WarmupFailureWarning(MolSysMTCatalogWarning):
    catalog_key = "WarmupFailureWarning"

    def __init__(self, attribute, error_type, reason):
        super().__init__(extra={
            "attribute": attribute,
            "error_type": error_type,
            "reason": reason,
        })


class GpuNotAvailableWarning(MolSysMTCatalogWarning):
    """Emitted when the GPU is requested but is not accessible."""
    catalog_key = "GpuNotAvailableWarning"

    def __init__(self, reason="no CUDA GPU is accessible"):
        # 'reason' is the only free datum; the message around it comes from MSM-WARN-GPU-001
        super().__init__(extra={"reason": reason})


__all__ = [
    "UserMolSysMTWarning",
    "SelectionWarning",
    "MolSysMTDeprecationWarning",
    "CrossChainCovalentBondsWarning",
    "DownloadWarning",
    "NotDigestedArgumentWarning",
    "MolecularSystemMismatchWarning",
    "StructuralAttributeDropWarning",
    "SlowChunkIOWarning",
    "MemoryPressureWarning",
    "UnknownAtomNameWarning",
    "WarmupFailureWarning",
    "GpuNotAvailableWarning",
    "warn",
    "warn_once",
]
