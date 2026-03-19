from .to_file_mdcrd import to_file_mdcrd
form_name = 'file:mdcrd'
form_type = 'file'
form_info = ["AMBER MDCRD coordinate/trajectory file format",
             "https://ambermd.org/FileFormats.php#trajectory"]

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
from .get_topological_attributes import *
from .get_structural_attributes import *
from .set import *
from .iterators import StructuresIterator


_convert_to={
        'file:mdcrd': to_file_mdcrd,
        }
