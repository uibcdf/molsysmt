form_name = 'pytraj.Trajectory'
form_type = 'class'
form_info = ["", ""]

from .is_pytraj_Trajectory import is_pytraj_Trajectory

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
from .to_pytraj_Topology import to_pytraj_Topology, _to_pytraj_Topology
from .to_nglview_NGLWidget import to_nglview_NGLWidget, _to_nglview_NGLWidget

_convert_to={
        'molsysmt.MolSys': _to_molsysmt_MolSys,
        'molsysmt.Topology': _to_molsysmt_Topology,
        'molsysmt.Structures': _to_molsysmt_Structures,
        'pytraj.Topology': _to_pytraj_Topology,
        'nglview.NGLWidget': _to_nglview_NGLWidget,
        }
