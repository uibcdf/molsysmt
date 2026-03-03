form_name = 'openmm.GromacsTopFile'
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
from .iterators import TopologyIterator


_convert_to={
        'openmm.GromacsTopFile': 'to_openmm_GromacsTopFile',
        'openmm.Topology': 'to_openmm_Topology',
        'molsysmt.Topology': 'to_molsysmt_Topology',
        }
