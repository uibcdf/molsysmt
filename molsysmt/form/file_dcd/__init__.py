form_name = 'file:dcd'
form_type = 'file'
form_info = ["", ""]

from .is_form import is_form

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .copy import copy
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator

from .to_mdtraj_DCDTrajectoryFile import to_mdtraj_DCDTrajectoryFile
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_MolSys import to_molsysmt_MolSys

_convert_to={
        'file:dcd': extract,
        'mdtraj.DCDTrajectoryFile': to_mdtraj_DCDTrajectoryFile,
        'molsysmt.Structures': to_molsysmt_Structures,
        'molsysmt.MolSys': to_molsysmt_MolSys
        }

