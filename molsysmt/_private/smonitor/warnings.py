"""MolSysMT warnings backed by smonitor catalogs."""

from __future__ import annotations

from smonitor.integrations import CatalogWarning
from .emitter import bundle

warn = bundle.warn
warn_once = bundle.warn_once


class MolSysMTCatalogWarning(CatalogWarning):
    """Base for this library's catalog warnings.

    `message` comes first and the domain fields are keyword-only, so that
    `type(w)(*w.args)` — how `pickle`, `copy.deepcopy`, pytest-xdist and
    `warnings.warn(text, category)` all rebuild a warning — hands the rendered
    text back as the message instead of as a field. Keyword-only keeps a
    misspelled field an error rather than a silently ignored one.
    """

    def __init__(self, message=None, **kwargs):
        from . import CATALOG, META
        super().__init__(message, catalog=CATALOG, meta=META, **kwargs)


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

    def __init__(self, message=None, *, molecular_system=None, atom_pairs=None,
                 caller='CrossChainCovalentBondsWarning'):
        if message is not None:
            # Already rendered: this is a rebuild — `pickle`, `copy.deepcopy`,
            # pytest-xdist or `warnings.warn(text, category)` — or a caller
            # supplying its own prose. Recomputing from the fields would either
            # fail on the absent ones or quietly render defaults.
            super().__init__(message)
            return
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

        super().__init__(message, extra=extra)


class DownloadWarning(UserMolSysMTWarning):
    catalog_key = "DownloadWarning"


class NotDigestedArgumentWarning(MolSysMTCatalogWarning):
    catalog_key = "NotDigestedArgumentWarning"

    def __init__(self, message=None, *, argument=None):
        if message is not None:
            # Already rendered: this is a rebuild — `pickle`, `copy.deepcopy`,
            # pytest-xdist or `warnings.warn(text, category)` — or a caller
            # supplying its own prose. Recomputing from the fields would either
            # fail on the absent ones or quietly render defaults.
            super().__init__(message)
            return
        super().__init__(message, extra={"argument": argument})


class MolecularSystemMismatchWarning(UserMolSysMTWarning):
    catalog_key = "MolecularSystemMismatchWarning"

    def __init__(self, message=None, *, caller='MolecularSystemMismatchWarning', n_models=None):
        if message is not None:
            # Already rendered: this is a rebuild — `pickle`, `copy.deepcopy`,
            # pytest-xdist or `warnings.warn(text, category)` — or a caller
            # supplying its own prose. Recomputing from the fields would either
            # fail on the absent ones or quietly render defaults.
            super().__init__(message)
            return
        extra = {"caller": caller}
        if n_models is not None:
            extra["count"] = n_models
        super().__init__(message, extra=extra)


class StructuralAttributeOffAxisWarning(UserMolSysMTWarning):
    """Warning about structural series held only by an item outside the structure axis."""

    catalog_key = "StructuralAttributeOffAxisWarning"

    def __init__(self, message=None, *, attributes=None, caller=None):
        if message is not None:
            # Already rendered: this is a rebuild — `pickle`, `copy.deepcopy`,
            # pytest-xdist or `warnings.warn(text, category)` — or a caller
            # supplying its own prose. Recomputing from the fields would either
            # fail on the absent ones or quietly render defaults.
            super().__init__(message)
            return
        super().__init__(message, extra={
            "attributes": ", ".join(attributes),
            "caller": caller,
        })


class StructuralAttributeDropWarning(UserMolSysMTWarning):
    """Warning about one-sided structural series discarded by intersection."""

    catalog_key = "StructuralAttributeDropWarning"

    def __init__(self, message=None, *, attributes=None, caller='molsysmt.append_structures'):
        if message is not None:
            # Already rendered: this is a rebuild — `pickle`, `copy.deepcopy`,
            # pytest-xdist or `warnings.warn(text, category)` — or a caller
            # supplying its own prose. Recomputing from the fields would either
            # fail on the absent ones or quietly render defaults.
            super().__init__(message)
            return
        super().__init__(message, extra={
            "attributes": ", ".join(attributes),
            "caller": caller,
        })


class IncompatibleBoxWarning(UserMolSysMTWarning):
    """Warning about fragments combined under disagreeing periodic boxes."""

    catalog_key = "IncompatibleBoxWarning"

    def __init__(self, message=None, *, reason=None, caller=None):
        if message is not None:
            # Already rendered: this is a rebuild — `pickle`, `copy.deepcopy`,
            # pytest-xdist or `warnings.warn(text, category)` — or a caller
            # supplying its own prose. Recomputing from the fields would either
            # fail on the absent ones or quietly render defaults.
            super().__init__(message)
            return
        if not isinstance(reason, str):
            Warning.__init__(self, reason)
            return
        super().__init__(message, extra={
            "reason": reason,
            "caller": caller,
        })


class BioassemblyIdentifierCollisionWarning(UserMolSysMTWarning):
    """Warning about incoming bioassembly identifiers renamed to avoid a collision."""

    catalog_key = "BioassemblyIdentifierCollisionWarning"

    def __init__(self, message=None, *, renamed=None, caller=None):
        if message is not None:
            # Already rendered: this is a rebuild — `pickle`, `copy.deepcopy`,
            # pytest-xdist or `warnings.warn(text, category)` — or a caller
            # supplying its own prose. Recomputing from the fields would either
            # fail on the absent ones or quietly render defaults.
            super().__init__(message)
            return
        if isinstance(renamed, str):
            Warning.__init__(self, renamed)
            return
        super().__init__(message, extra={
            "renamed": ", ".join(f'{old} -> {new}' for old, new in renamed),
            "caller": caller,
        })


class SlowChunkIOWarning(MolSysMTCatalogWarning):
    catalog_key = "SlowChunkIOWarning"

    def __init__(self, message=None, *, chunk_index=None, io_time_s=None):
        if message is not None:
            # Already rendered: this is a rebuild — `pickle`, `copy.deepcopy`,
            # pytest-xdist or `warnings.warn(text, category)` — or a caller
            # supplying its own prose. Recomputing from the fields would either
            # fail on the absent ones or quietly render defaults.
            super().__init__(message)
            return
        super().__init__(message, extra={"chunk_index": chunk_index, "io_time_s": io_time_s})


class MemoryPressureWarning(MolSysMTCatalogWarning):
    catalog_key = "MemoryPressureWarning"

    def __init__(self, message=None, *, chunk_index=None, rss_bytes=None,
                 budget_bytes=None, pressure_pct=None):
        if message is not None:
            # Already rendered: this is a rebuild — `pickle`, `copy.deepcopy`,
            # pytest-xdist or `warnings.warn(text, category)` — or a caller
            # supplying its own prose. Recomputing from the fields would either
            # fail on the absent ones or quietly render defaults.
            super().__init__(message)
            return
        super().__init__(message, extra={
            "chunk_index": chunk_index,
            "rss_bytes": rss_bytes,
            "budget_bytes": budget_bytes,
            "pressure_pct": pressure_pct,
        })


class UnknownAtomNameWarning(MolSysMTCatalogWarning):
    catalog_key = "UnknownAtomNameWarning"

    def __init__(self, message=None, *, atom_name=None):
        if message is not None:
            # Already rendered: this is a rebuild — `pickle`, `copy.deepcopy`,
            # pytest-xdist or `warnings.warn(text, category)` — or a caller
            # supplying its own prose. Recomputing from the fields would either
            # fail on the absent ones or quietly render defaults.
            super().__init__(message)
            return
        super().__init__(message, extra={"atom_name": atom_name})


class GpuNotAvailableWarning(MolSysMTCatalogWarning):
    """Emitted when the GPU is requested but is not accessible."""
    catalog_key = "GpuNotAvailableWarning"

    def __init__(self, message=None, *, reason="no CUDA GPU is accessible"):
        if message is not None:
            # Already rendered: this is a rebuild — `pickle`, `copy.deepcopy`,
            # pytest-xdist or `warnings.warn(text, category)` — or a caller
            # supplying its own prose. Recomputing from the fields would either
            # fail on the absent ones or quietly render defaults.
            super().__init__(message)
            return
        # 'reason' is the only free datum; the message around it comes from MSM-WARN-GPU-001
        super().__init__(message, extra={"reason": reason})


__all__ = [
    "UserMolSysMTWarning",
    "SelectionWarning",
    "MolSysMTDeprecationWarning",
    "CrossChainCovalentBondsWarning",
    "DownloadWarning",
    "NotDigestedArgumentWarning",
    "MolecularSystemMismatchWarning",
    "StructuralAttributeDropWarning",
    "StructuralAttributeOffAxisWarning",
    "IncompatibleBoxWarning",
    "BioassemblyIdentifierCollisionWarning",
    "SlowChunkIOWarning",
    "MemoryPressureWarning",
    "UnknownAtomNameWarning",
    "GpuNotAvailableWarning",
    "warn",
    "warn_once",
]
