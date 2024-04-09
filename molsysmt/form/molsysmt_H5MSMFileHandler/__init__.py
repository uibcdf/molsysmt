form_name = 'molsysmt.H5MSMFileHandler'
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

from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
from .to_nglview_NGLWidget import to_nglview_NGLWidget

_convert_to={
        'molsysmt.H5MSMFileHandler': extract,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.Structures': to_molsysmt_Structures,
        'molsysmt.MolSysOld': to_molsysmt_MolSysOld,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        }

