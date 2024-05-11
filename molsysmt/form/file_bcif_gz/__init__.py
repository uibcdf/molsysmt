form_name = 'file:bcif.gz'
form_type = 'file'
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
bonds_can_be_computed = True

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

from .download import download

from .to_mmcif_PdbxContainers_DataContainer import to_mmcif_PdbxContainers_DataContainer

_convert_to={
        'file:bcif.gz': extract,
        'mmcif.PdbxContainers_DataContainer': to_mmcif_PdbxContainers_DataContainer,
        }

