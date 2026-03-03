from .to_nglview_NGLWidget import to_nglview_NGLWidget
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_file_msmpk import to_file_msmpk
from .to_molsysmt_Topology import to_molsysmt_Topology
from .update_file import update_file

form_name = 'file:msmpk'
form_type = 'file'
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

from .update_file import update_file


_convert_to={
        'file:msmpk': to_file_msmpk,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.Structures': to_molsysmt_Structures,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        }

