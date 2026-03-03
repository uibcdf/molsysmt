form_name = 'molsysviewer.MolSysView'
form_type = 'class'
form_info = ["MolSysViewer visualization native object", ""]

piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = 'molsysmt.Structures'
piped_any_attribute = 'molsysmt.MolSys'
bonds_are_explicit = True
bonds_can_be_computed = True

__all__ = [
    'form_name',
    'form_type',
    'form_info',
    'piped_topological_attribute',
    'piped_structural_attribute',
    'piped_any_attribute',
    'bonds_are_explicit',
    'bonds_can_be_computed',
    'is_form',
    'attributes',
    'has_attribute',
    'copy',
    'extract',
    'append_structures',
    'to_molsysviewer_MolSysView',
    'to_molsysmt_MolSys',
    '_convert_to',
]

from .is_form import is_form
from .attributes import attributes
from .has_attribute import has_attribute

from .copy import copy
from .extract import extract
from .append_structures import append_structures


from .get_topological_attributes import *
from .get_structural_attributes import *
from .get_mechanical_attributes import *

_convert_to = {
    'molsysviewer.MolSysView': 'to_molsysviewer_MolSysView',
    'molsysmt.MolSys': 'to_molsysmt_MolSys',
}
