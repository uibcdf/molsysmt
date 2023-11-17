form_name = 'molsysmt.Structures'
form_type = 'class'
form_info = ["", ""]

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

from .to_molsysmt_StructuresDict import to_molsysmt_StructuresDict
from .to_file_h5msm import to_file_h5msm
from .to_XYZ import to_XYZ

_convert_to={
        'molsysmt.Structures': extract,
        'molsysmt.StructuresDict': to_molsysmt_StructuresDict,
        'file:h5msm': to_file_h5msm,
        'XYZ': to_XYZ,
        }
