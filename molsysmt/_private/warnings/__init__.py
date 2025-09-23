from .user_molsysmt_warning import UserMolSysMTWarning
from .selection_warning import SelectionWarning
from .molsysmt_deprecation_warning import MolSysMTDeprecationWarning
from .cross_chain_covalent_bonds_warning import CrossChainCovalentBondsWarning
from .download_warning import DownloadWarning

from typing import Iterable, Type
import warnings

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
    warnings.warn(message_or_warning, cat, stacklevel=stacklevel)



