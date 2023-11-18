form_name = 'file:xtc'
form_type = 'file'
form_info = ["", ""]

from .is_form import is_form

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .copy import copy
from .add import add
from .merge import merge
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator

from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_mdtraj_XTCTrajectoryFile import to_mdtraj_XTCTrajectoryFile
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld

_convert_to={
        'file:xtc': extract,
        'mdtraj.Trajectory': to_mdtraj_Trajectory,
        'mdtraj.XTCTrajectoryFile': to_mdtraj_XTCTrajectoryFile,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        }
