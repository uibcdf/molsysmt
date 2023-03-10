form_name = 'file:xtc'
form_type = 'file'
form_info = ["", ""]

from .is_form import is_form

from .attributes import attributes

from .extract import extract
from .copy import copy
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator

from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_mdtraj_XTCTrajectoryFile import to_mdtraj_XTCTrajectoryFile
from .to_molsysmt_Structures import to_molsysmt_Structures

_convert_to={
        'mdtraj.Trajectory': to_mdtraj_Trajectory,
        'mdtraj.XTCTrajectoryFile': to_mdtraj_XTCTrajectoryFile,
        'molsysmt.Structures': to_molsysmt_Structures,
        }
