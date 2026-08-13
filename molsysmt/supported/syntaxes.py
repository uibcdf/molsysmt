"""Compatibility access to the directional selection-syntax registry.

New MolSysMT code imports :mod:`molsysmt.supported._syntaxes`. This module remains
available because ecosystem consumers historically imported the registry from here.
Python assigns an imported submodule to its parent package, so the small callable-module
adapter also preserves ``molsysmt.supported.syntaxes()`` after such an import.
"""

import sys
from types import ModuleType

from ._syntaxes import (
    lowercase_selection_syntaxes,
    lowercase_syntaxes,
    lowercase_translation_syntaxes,
    selection_syntaxes,
    syntax_capabilities,
    syntaxes,
    translation_syntaxes,
)


class _SyntaxCompatibilityModule(ModuleType):

    def __call__(self):
        from .supported import syntaxes as syntax_report

        return syntax_report()


sys.modules[__name__].__class__ = _SyntaxCompatibilityModule

__all__ = [
    'lowercase_selection_syntaxes',
    'lowercase_syntaxes',
    'lowercase_translation_syntaxes',
    'selection_syntaxes',
    'syntax_capabilities',
    'syntaxes',
    'translation_syntaxes',
]
