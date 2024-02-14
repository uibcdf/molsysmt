form_name = 'nglview.NGLWidget'
form_type = 'class'
form_info = ["NGLView visualization native object", "http://nglviewer.org/nglview/latest/_modules/nglview/widget.html"]

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

from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
from .to_openmm_Topology import to_openmm_Topology
from .to_string_aminoacids1 import to_string_aminoacids1
from .to_string_aminoacids3 import to_string_aminoacids3
from .to_string_pdb_text import to_string_pdb_text

_convert_to={
        'nglview.NGLWidget': extract,
        'molsysmt.MolSysOld': to_molsysmt_MolSysOld,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        'openmm.Topology': to_openmm_Topology,
        'string:aminoacids1': to_string_aminoacids1,
        'string:aminoacids3': to_string_aminoacids3,
        'string:pdb_text': to_string_pdb_text,
        }
