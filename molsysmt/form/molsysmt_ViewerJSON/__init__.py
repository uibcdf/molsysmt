from .to_molsysmt_ViewerJSON import to_molsysmt_ViewerJSON
from .to_molsysmt_MolSys import to_molsysmt_MolSys
form_name = 'molsysmt.ViewerJSON'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
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
    'get',
    'copy',
    'extract',
    'append_structures',
    'to_molsysmt_ViewerJSON',
    'to_molsysmt_MolSys',
    '_convert_to',
]

from .is_form import is_form
from .attributes import attributes
from .has_attribute import has_attribute

from .get_topological_attributes import *
from .get_structural_attributes import *
from .copy import copy
from .extract import extract
from .append_structures import append_structures


_convert_to = {
    'molsysmt.ViewerJSON': to_molsysmt_ViewerJSON,
    'molsysmt.MolSys': to_molsysmt_MolSys,
}
