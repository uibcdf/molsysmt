form_name = 'file:cif'
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
from .iterators import StructuresIterator, TopologyIterator

from .to_molsysmt_CIFFileHandler import to_molsysmt_CIFFileHandler

_convert_to={
        'file:cif': extract,
        'molsysmt.CIFFileHandler': to_molsysmt_CIFFileHandler,
        }

