"""
MolSysMT
This must be a short description of the project
"""

import importlib

# versioningit
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("molsysmt")
except PackageNotFoundError:
    # Package is not installed
    try:
        from ._version import __version__
    except ImportError:
        __version__ = "1.0.0+unknown"

from smonitor.integrations import ensure_configured as _ensure_smonitor_configured
from molsysmt._private.smonitor import PACKAGE_ROOT as _SMONITOR_PACKAGE_ROOT

_ensure_smonitor_configured(_SMONITOR_PACKAGE_ROOT)


# Central lazy-loading registry mapping public attribute/submodule names
# to their respective internal import submodules.
_LAZY_ATTRIBUTES = {
    # Submodules
    'configure': '.configure',
    'core': '.core',
    'basic': '.basic',
    'form': '.form',
    'element': '.element',
    'attribute': '.attribute',
    'topology': '.topology',
    'structure': '.structure',
    'build': '.build',
    'supported': '.supported',
    'pbc': '.pbc',
    'physchem': '.physchem',
    'molecular_mechanics': '.molecular_mechanics',
    'hbonds': '.hbonds',
    'third_party': '.third_party',
    'thirds': '.third_party',
    'systems': ('.systems', 'systems'),

    # pyunitwizard alias
    'pyunitwizard': ('._pyunitwizard', 'puw'),

    # Native classes
    'MolSysBuilder': ('.native', 'MolSysBuilder'),
    'MolSysDict': ('.native', 'MolSysDict'),
    'TopologyDict': ('.native', 'TopologyDict'),

    # Basic functions
    'is_a_molecular_system': ('.basic', 'is_a_molecular_system'),
    'are_multiple_molecular_systems': ('.basic', 'are_multiple_molecular_systems'),
    'has_attribute': ('.basic', 'has_attribute'),
    'where_is_attribute': ('.basic', 'where_is_attribute'),
    'get_attributes': ('.basic', 'get_attributes'),
    'get_label': ('.basic', 'get_label'),
    'get_form': ('.basic', 'get_form'),
    'select': ('.basic', 'select'),
    'convert': ('.basic', 'convert'),
    'ConversionIssue': ('.basic', 'ConversionIssue'),
    'ConversionReport': ('.basic', 'ConversionReport'),
    'copy': ('.basic', 'copy'),
    'extract': ('.basic', 'extract'),
    'get': ('.basic', 'get'),
    'set': ('.basic', 'set'),
    'info': ('.basic', 'info'),
    'remove': ('.basic', 'remove'),
    'merge': ('.basic', 'merge'),
    'add': ('.basic', 'add'),
    'concatenate_structures': ('.basic', 'concatenate_structures'),
    'append_structures': ('.basic', 'append_structures'),
    'is_composed_of': ('.basic', 'is_composed_of'),
    'contains': ('.basic', 'contains'),
    'compare': ('.basic', 'compare'),
    'view': ('.basic', 'view'),
    'Iterator': ('.basic', 'Iterator'),

    # SMonitor exceptions / helpers
    'ArgumentError': ('._private.smonitor', 'ArgumentError'),
    'ArgumentChoiceError': ('._private.smonitor', 'ArgumentChoiceError'),
    'ArgumentLengthError': ('._private.smonitor', 'ArgumentLengthError'),
    'ArgumentConflictError': ('._private.smonitor', 'ArgumentConflictError'),
    'StructuralInconsistencyError': ('._private.smonitor', 'StructuralInconsistencyError'),
    'InternalAlgorithmError': ('._private.smonitor', 'InternalAlgorithmError'),
    'IteratorError': ('._private.smonitor', 'IteratorError'),
    'LibraryNotFoundError': ('._private.smonitor', 'LibraryNotFoundError'),
    'MolecularSystemNeededError': ('._private.smonitor', 'MolecularSystemNeededError'),
    'MolecularSystemsNeededError': ('._private.smonitor', 'MolecularSystemsNeededError'),
    'MultipleMolecularSystemsError': ('._private.smonitor', 'MultipleMolecularSystemsError'),
    'MolecularSystemVerificationError': ('._private.smonitor', 'MolecularSystemVerificationError'),
    'NotCompatibleConversionError': ('._private.smonitor', 'NotCompatibleConversionError'),
    'NotImplementedConversionError': ('._private.smonitor', 'NotImplementedConversionError'),
    'NotImplementedIteratorError': ('._private.smonitor', 'NotImplementedIteratorError'),
    'NotImplementedMethodError': ('._private.smonitor', 'NotImplementedMethodError'),
    'NotSupportedFormError': ('._private.smonitor', 'NotSupportedFormError'),
    'NotSupportedSyntaxError': ('._private.smonitor', 'NotSupportedSyntaxError'),
    'NotWithThisFormError': ('._private.smonitor', 'NotWithThisFormError'),
    'FileAlreadyHandledError': ('._private.smonitor', 'FileAlreadyHandledError'),
    'FileContentError': ('._private.smonitor', 'FileContentError'),
    'warn': ('._private.smonitor', 'warn'),
    'warn_once': ('._private.smonitor', 'warn_once'),
}


def __getattr__(name: str):
    if name in _LAZY_ATTRIBUTES:
        target = _LAZY_ATTRIBUTES[name]
        if isinstance(target, str):
            # Target is a submodule to import lazily
            mod = importlib.import_module(target, __name__)
            globals()[name] = mod
            return mod
        elif isinstance(target, tuple):
            # Target is an attribute (function, class, exception) inside a submodule
            submod_path, attr_name = target
            mod = importlib.import_module(submod_path, __name__)
            val = getattr(mod, attr_name)
            globals()[name] = val
            return val

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(list(globals().keys()) + list(_LAZY_ATTRIBUTES.keys()))


__all__ = []
