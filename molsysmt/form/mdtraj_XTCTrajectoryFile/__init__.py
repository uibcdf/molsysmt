form_name = 'mdtraj.XTCTrajectoryFile'
form_type = 'class'
form_info = ["", ""]

from .is_mdtraj_XTCTrajectoryFile import is_mdtraj_XTCTrajectoryFile

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_molsysmt_Structures import to_molsysmt_Structures

