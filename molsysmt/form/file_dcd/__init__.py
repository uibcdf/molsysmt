form_name = 'file:dcd'
form_type = 'file'
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

from .to_mdtraj_DCDTrajectoryFile import to_mdtraj_DCDTrajectoryFile
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld

_convert_to={
        'file:dcd': extract,
        'mdtraj.DCDTrajectoryFile': to_mdtraj_DCDTrajectoryFile,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Structures': to_molsysmt_Structures,
        'molsysmt.MolSysOld': to_molsysmt_MolSysOld,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        }

