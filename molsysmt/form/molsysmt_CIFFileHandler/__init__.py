from .to_molsysmt_CIFFileHandler import to_molsysmt_CIFFileHandler
form_name = 'molsysmt.CIFFileHandler'
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
from .iterators import StructuresIterator, TopologyIterator

#
_convert_to={
        'molsysmt.CIFFileHandler': to_molsysmt_CIFFileHandler,
        #'MDAnalysis.Topology': to_MDAnalysis_Topology,
        }

