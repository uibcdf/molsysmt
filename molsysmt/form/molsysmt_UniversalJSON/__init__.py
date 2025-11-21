form_name = 'molsysmt.UniversalJSON'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
bonds_can_be_computed = False

from .is_form import is_form
from .attributes import attributes
from .has_attribute import has_attribute

from .get import *
from .copy import copy
from .extract import extract
from .append_structures import append_structures

from .to_molsysmt_UniversalJSON import to_molsysmt_UniversalJSON
from .to_molsysmt_MolSys import to_molsysmt_MolSys

_convert_to = {
    'molsysmt.UniversalJSON': to_molsysmt_UniversalJSON,
    'molsysmt.MolSys': to_molsysmt_MolSys,
}
