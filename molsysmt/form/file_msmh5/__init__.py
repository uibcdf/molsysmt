form_name = 'file:msmh5'
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

from .to_molsysmt_MSMH5FileHandler import to_molsysmt_MSMH5FileHandler
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_Topology2 import to_molsysmt_Topology2
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_nglview_NGLWidget import to_nglview_NGLWidget

_convert_to={
        'file:msmh5': extract,
        'molsysmt.MSMH5FileHandler': to_molsysmt_MSMH5FileHandler,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.Topology2': to_molsysmt_Topology2,
        'molsysmt.Structures': to_molsysmt_Structures,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        }

