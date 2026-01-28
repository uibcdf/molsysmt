"""
MolSysMT
This must be a short description of the project
"""

# versioningit
from ._version import __version__

def __print_version__():
    print("MolSysMT version " + __version__)

#__documentation_web__ = 'https://www.uibcdf.org/MolSysMT'
#__github_web__ = 'https://github.com/uibcdf/MolSysMT'
#__github_issues_web__ = __github_web__ + '/issues'

# Starting the modules
from . import config

config.setup_logging(level="WARNING", capture_warnings=True, simplify_warning_format=True)

from ._pyunitwizard import puw as pyunitwizard

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

# Adding molsysmt to nglview
#thirds.nglview.adding_molsysmt()

# Adding molsysmt to nglview (optional dependency)
try:
    from .thirds.nglview.patching_nglview import add_molsysmt_to_nglview
except Exception:  # pragma: no cover - optional dependency
    add_molsysmt_to_nglview = None
else:
    add_molsysmt_to_nglview()
    del(add_molsysmt_to_nglview)


# With the following list sphinx can document de methods in the api section without adding the
# module files names explicitly:

__all__ = []

