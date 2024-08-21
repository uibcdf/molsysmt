form_name = 'file:h5msm'
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
from .get_topological_attributes import *
from .get_structural_attributes import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_nglview_NGLWidget import to_nglview_NGLWidget
from .to_string_amino_acids_1 import to_string_amino_acids_1
from .to_string_amino_acids_3 import to_string_amino_acids_3

_convert_to={
    'file:h5msm': extract,
    'molsysmt.H5MSMFileHandler': to_molsysmt_H5MSMFileHandler,
    'molsysmt.MolSysOld': to_molsysmt_MolSysOld,
    'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
    'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
    'molsysmt.MolSys': to_molsysmt_MolSys,
    'molsysmt.Topology': to_molsysmt_Topology,
    'molsysmt.Structures': to_molsysmt_Structures,
    'nglview.NGLWidget': to_nglview_NGLWidget,
    'string:amino_acids_1': to_string_amino_acids_1,
    'string:amino_acids_3': to_string_amino_acids_3,
    }

