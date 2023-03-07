"""
MolSysMT
This must be a short description of the project
"""

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions

__documentation_web__ = 'https://www.uibcdf.org/MolSysMT'
__github_web__ = 'https://github.com/uibcdf/MolSysMT'
__github_issues_web__ = __github_web__ + '/issues'

from . import config

from ._pyunitwizard import puw as pyunitwizard

from . import file

from .basic import *
from . import basic

from . import form
from . import element

from . import topology
from . import structure
from . import build

#from . import help
from . import pbc
from . import physchem
from . import molecular_mechanics
from . import molecular_dynamics
from . import hbonds
from . import thirds
from .demo import demo


# Adding molsysmt to nglview

thirds.nglview.adding_molsysmt()

# With the following list sphinx can document de methods in the api section without adding the
# module files names explicitly:

__all__ = []


