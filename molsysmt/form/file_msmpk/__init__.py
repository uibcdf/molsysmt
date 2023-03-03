form_name = 'file:msmpk'
form_type = 'file'
form_info = ["", ""]

from .is_file_msmpk import is_file_msmpk

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_molsysmt_MolSys import to_molsysmt_MolSys 
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures 
from .to_nglview_NGLWidget import to_nglview_NGLWidget 

_dict_convert={
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.Structures': to_molsysmt_Structures,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        }

