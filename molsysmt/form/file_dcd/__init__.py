form_name = 'file:dcd'
form_type = 'file'
form_info = ["", ""]

from .is_file_dcd import is_file_dcd

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_mdtraj_DCDTrajectoryFile import to_mdtraj_DCDTrajectoryFile
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_MolSys import to_molsysmt_MolSys

_dict_convert={
        'mdtraj.DCDTrajectoryFile': to_mdtraj_DCDTrajectoryFile,
        'molsysmt.Structures': to_molsysmt_Structures,
        'molsysmt.MolSys': to_molsysmt_MolSys
        }

