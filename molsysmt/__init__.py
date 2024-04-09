"""
MolSysMT
This must be a short description of the project
"""

# versioningit
from ._version import __version__

#__documentation_web__ = 'https://www.uibcdf.org/MolSysMT'
#__github_web__ = 'https://github.com/uibcdf/MolSysMT'
#__github_issues_web__ = __github_web__ + '/issues'

from . import config

from ._pyunitwizard import puw as pyunitwizard

from . import file

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
from . import molecular_dynamics
from . import hbonds
from . import thirds

from .systems import systems

# Adding molsysmt to nglview

thirds.nglview.adding_molsysmt()

# With the following list sphinx can document de methods in the api section without adding the
# module files names explicitly:

__all__ = []


