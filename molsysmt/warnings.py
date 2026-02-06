"""MolSysMT warnings backed by smonitor catalogs."""

from __future__ import annotations

from typing import Type
import warnings

from ._private.functions import caller_name
from smonitor.integrations import emit_from_catalog, merge_extra
from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, META
from ._private.smonitor_emit import message_from_catalog


class UserMolSysMTWarning(Warning):
    pass


class SelectionWarning(UserMolSysMTWarning):
    """Warnings related to selection strings and resolved subsets."""


class MolSysMTDeprecationWarning(DeprecationWarning):
    pass


class CrossChainCovalentBondsWarning(UserMolSysMTWarning):
    def __init__(self, molecular_system, atom_pairs):
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

        default_message = (
            f"{len(label_pairs_reported)} covalent bond(s) reported by the struct_conn table "
            f"between atoms belonging to different chains were added.\n"
            "Verify whether these cross-chain bonds are expected in your system.\n"
        )

        for label1, label2 in label_pairs_reported[:-1]:
            default_message += f"  - {label1}  <-->  {label2}\n"

        if label_pairs_reported:
            default_message += f"  - {label_pairs_reported[-1][0]}  <-->  {label_pairs_reported[-1][1]}"

        caller = caller_name()
        full_message = message_from_catalog(
            CATALOG["warnings"]["CrossChainCovalentBondsWarning"],
            extra={
                "caller": caller,
                "count": len(label_pairs_reported),
                "pairs": label_pairs_reported,
            },
            default_message=default_message,
        )

        super().__init__(full_message)


class DownloadWarning(UserMolSysMTWarning):
    """Warnings related to selection strings and resolved subsets."""


class NotDigestedArgumentWarning(Warning):
    def __init__(self, argument):
        default_message = f"The {argument} argument was not digested."

        full_message = message_from_catalog(
            CATALOG["warnings"]["NotDigestedArgumentWarning"],
            extra={"argument": argument},
            default_message=default_message,
        )

        super().__init__(full_message)


__all__ = [
    "UserMolSysMTWarning",
    "SelectionWarning",
    "MolSysMTDeprecationWarning",
    "CrossChainCovalentBondsWarning",
    "DownloadWarning",
    "NotDigestedArgumentWarning",
    "warn",
    "warn_once",
]


def warn(
    message_or_warning: str | Warning,
    category: Type[Warning] | None = None,
    *,
    stacklevel: int = 2,
) -> None:
    if isinstance(message_or_warning, Warning):
        cls_name = type(message_or_warning).__name__
    else:
        cls_name = (category or UserMolSysMTWarning).__name__
    if cls_name in CATALOG.get("warnings", {}):
        try:
            emit_from_catalog(
                CATALOG["warnings"][cls_name],
                package_root=PACKAGE_ROOT,
                extra=merge_extra(
                    META,
                    {
                        "caller": None,
                        "message": str(message_or_warning),
                    },
                ),
            )
            return
        except Exception:
            pass
    if isinstance(message_or_warning, Warning):
        warnings.warn(message_or_warning, stacklevel=stacklevel)
    else:
        warnings.warn(message_or_warning, category or UserMolSysMTWarning, stacklevel=stacklevel)


__WARNED_ONCE_CACHE__: set[tuple[Type[Warning], str]] = set()


def warn_once(
    message_or_warning: str | Warning,
    category: Type[Warning] | None = None,
    *,
    stacklevel: int = 2,
) -> None:
    if isinstance(message_or_warning, Warning):
        msg, cat = str(message_or_warning), type(message_or_warning)
    else:
        msg, cat = message_or_warning, category or UserMolSysMTWarning

    key = (cat, msg)
    if key in __WARNED_ONCE_CACHE__:
        return
    __WARNED_ONCE_CACHE__.add(key)
    cls_name = cat.__name__
    if cls_name in CATALOG.get("warnings", {}):
        try:
            emit_from_catalog(
                CATALOG["warnings"][cls_name],
                package_root=PACKAGE_ROOT,
                extra=merge_extra(
                    META,
                    {
                        "caller": None,
                        "message": msg,
                    },
                ),
            )
            return
        except Exception:
            pass
    warnings.warn(message_or_warning, cat, stacklevel=stacklevel)
