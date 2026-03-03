from .to_mdtraj_XTCTrajectoryFile import to_mdtraj_XTCTrajectoryFile
from .to_molsysmt_Structures import to_molsysmt_Structures
form_name = 'mdtraj.XTCTrajectoryFile'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None

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


_convert_to={
        'mdtraj.XTCTrajectoryFile': to_mdtraj_XTCTrajectoryFile,
        'molsysmt.Structures': to_molsysmt_Structures,
        }
