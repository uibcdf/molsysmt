form_name = 'molsysmt.Structures'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = False
bonds_can_be_computed = False

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

from .to_file_h5msm import to_file_h5msm
from .to_molsysmt_StructuresDict import to_molsysmt_StructuresDict
from .to_XYZ import to_XYZ

_convert_to={
        'molsysmt.Structures': extract,
        'file:h5msm': to_file_h5msm,
        'molsysmt.StructuresDict': to_molsysmt_StructuresDict,
        'XYZ': to_XYZ,
        }
