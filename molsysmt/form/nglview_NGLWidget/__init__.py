form_name = 'nglview.NGLWidget'
form_type = 'class'
form_info = ["NGLView visualization native object", "http://nglviewer.org/nglview/latest/_modules/nglview/widget.html"]

from .is_nglview_NGLWidget import is_nglview_NGLWidget

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
from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology
from .to_string_aminoacids1 import to_string_aminoacids1, _to_string_aminoacids1
from .to_string_aminoacids3 import to_string_aminoacids3, _to_string_aminoacids3
from .to_string_pdb_text import to_string_pdb_text, _to_string_pdb_text

