form_name = 'file:h5msm'
form_type = 'file'
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
from .iterators import StructuresIterator, TopologyIterator

from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_MolSysNEW import to_molsysmt_MolSysNEW
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_TopologyNEW import to_molsysmt_TopologyNEW
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_StructuresNEW import to_molsysmt_StructuresNEW
from .to_nglview_NGLWidget import to_nglview_NGLWidget

_convert_to={
        'file:h5msm': extract,
        'molsysmt.H5MSMFileHandler': to_molsysmt_H5MSMFileHandler,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.MolSysNEW': to_molsysmt_MolSysNEW,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.TopologyNEW': to_molsysmt_TopologyNEW,
        'molsysmt.Structures': to_molsysmt_Structures,
        'molsysmt.StructuresNEW': to_molsysmt_StructuresNEW,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        }

