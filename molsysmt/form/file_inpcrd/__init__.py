form_name = 'file:inpcrd'
form_type = 'file'
form_info = ["AMBER ASCII restart/inpcrd file format",
             "https://ambermd.org/FileFormats.php#trajectory"]

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

from .to_openmm_AmberInpcrdFile import to_openmm_AmberInpcrdFile
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
from .to_molsysmt_Structures import to_molsysmt_Structures

_convert_to={
        'file:inpcrd': extract,
        'openmm.AmberInpcrdFile': to_openmm_AmberInpcrdFile,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        'molsysmt.Structures': to_molsysmt_Structures,
        }

