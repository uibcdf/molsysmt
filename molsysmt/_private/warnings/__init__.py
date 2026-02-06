"""Legacy warnings retained for compatibility.

Smonitor now owns message formatting via the catalog in `molsysmt/_private/smonitor`.
"""

from .user_molsysmt_warning import UserMolSysMTWarning
from .selection_warning import SelectionWarning
from .molsysmt_deprecation_warning import MolSysMTDeprecationWarning
from .cross_chain_covalent_bonds_warning import CrossChainCovalentBondsWarning
from .download_warning import DownloadWarning

from typing import Iterable, Type
import warnings

from smonitor.integrations import emit_from_catalog, merge_extra
from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, META

__all__ = ['UserMolSysMTWarning',
           'SelectionWarning',
           'MolSysMTDeprecationWarning',
           'CrossChainCovalentBondsWarning',
           'DownloadWarning',
           'warn',
           'warn_once']

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
                extra=merge_extra(META, {
                    "caller": None,
                    "message": str(message_or_warning),
                }),
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
                extra=merge_extra(META, {
                    "caller": None,
                    "message": msg,
                }),
            )
            return
        except Exception:
            pass
    warnings.warn(message_or_warning, cat, stacklevel=stacklevel)
