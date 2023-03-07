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

from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures
from .to_nglview_NGLWidget import to_nglview_NGLWidget, _to_nglview_NGLWidget 

_convert_to={
        'molsysmt.MolSys': _to_molsysmt_MolSys,
        'molsysmt.Topology': _to_molsysmt_Topology,
        'molsysmt.Structures': _to_molsysmt_Structures,
        'nglview.NGLWidget': _to_nglview_NGLWidget,
        }

