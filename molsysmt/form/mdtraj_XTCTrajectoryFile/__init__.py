form_name = 'mdtraj.XTCTrajectoryFile'
form_type = 'class'
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

from .to_molsysmt_Structures import to_molsysmt_Structures

_convert_to={
        'molsysmt.Structures': to_molsysmt_Structures,
        }
