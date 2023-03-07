form_name = 'file:dcd'
form_type = 'file'
form_info = ["", ""]

from .is_form import is_form

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_mdtraj_DCDTrajectoryFile import to_mdtraj_DCDTrajectoryFile, _to_mdtraj_DCDTrajectoryFile
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures
from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys

_convert_to={
        'mdtraj.DCDTrajectoryFile': _to_mdtraj_DCDTrajectoryFile,
        'molsysmt.Structures': _to_molsysmt_Structures,
        'molsysmt.MolSys': _to_molsysmt_MolSys
        }

