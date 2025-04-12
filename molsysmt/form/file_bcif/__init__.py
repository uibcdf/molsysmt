form_name = 'file:bcif'
form_type = 'file'
form_info = ["", ""]

piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = 'molsysmt.Structures'
piped_any_attribute = 'molsysmt.MolSys'
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
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures

_convert_to={
    'file:bcif': extract,
    'molsysmt.MolSys': to_molsysmt_MolSys,
    'molsysmt.Topology': to_molsysmt_Topology,
    'molsysmt.Structures': to_molsysmt_Structures,
    }

