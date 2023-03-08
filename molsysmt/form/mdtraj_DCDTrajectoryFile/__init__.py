form_name = 'mdtraj.DCDTrajectoryFile'
form_type = 'class'
form_info = ["", ""]

from .is_form import is_form

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures

_convert_to={
        'molsysmt.MolSys': _to_molsysmt_MolSys,
        'molsysmt.Structures': _to_molsysmt_Structures,
        }
