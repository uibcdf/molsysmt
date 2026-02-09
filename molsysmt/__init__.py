"""
MolSysMT
This must be a short description of the project
"""

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

#__documentation_web__ = 'https://www.uibcdf.org/MolSysMT'
#__github_web__ = 'https://github.com/uibcdf/MolSysMT'
#__github_issues_web__ = __github_web__ + '/issues'

# Starting the modules
from . import config

config.setup_logging(level="WARNING", capture_warnings=True, simplify_warning_format=True)

from ._pyunitwizard import puw as pyunitwizard

from ._private.smonitor import (
    ArgumentError,
    ArgumentChoiceError,
    ArgumentLengthError,
    ArgumentConflictError,
    StructuralInconsistencyError,
    InternalAlgorithmError,
    IteratorError,
    LibraryNotFoundError,
    MolecularSystemNeededError,
    MolecularSystemsNeededError,
    NotCompatibleConversionError,
    NotImplementedConversionError,
    NotImplementedIteratorError,
    NotImplementedMethodError,
    NotSupportedFormError,
    NotSupportedSyntaxError,
    NotWithThisFormError,
    FileAlreadyHandledError,
    FileContentError,
    warn,
    warn_once,
)

from .basic import *
from . import basic

from . import form
from . import element
from . import attribute

from . import topology
from . import structure
from . import build

from . import supported
from . import pbc
from . import physchem
from . import molecular_mechanics
#from . import molecular_dynamics
from . import hbonds
from . import thirds

from .systems import systems
from .warmup_numba import warmup_numba

# NGLView patching is triggered lazily by the NGLView backend.


# With the following list sphinx can document de methods in the api section without adding the
# module files names explicitly:

__all__ = []
