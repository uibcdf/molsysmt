form_name = 'file:xtc'
form_type = 'file'
form_info = ["", ""]

from .is_file_xtc import is_file_xtc

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_mdtraj_XTCTrajectoryFile import to_mdtraj_XTCTrajectoryFile
from .to_molsysmt_Structures import to_molsysmt_Structures

