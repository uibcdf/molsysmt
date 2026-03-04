from molsysmt._private.arg_digestion import arg_digest

form_name = 'molsysviewer.MolSysView'
form_type = 'class'
form_info = ["MolSysViewer visualization native object."]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
bonds_can_be_computed = True

_convert_to = {
    'molsysviewer.MolSysView': 'to_molsysviewer_MolSysView',
    'molsysmt.MolSys': 'to_molsysmt_MolSys',
}

from .is_form import is_form
from .has_attribute import has_attribute
from .attributes import attributes
from .extract import extract
from .append_structures import append_structures
from .copy import copy
from .get_topological_attributes import *
from .get_structural_attributes import *
from .get_mechanical_attributes import *

@arg_digest(form=form_name)
def get(item, element='system', selection='all', syntax='MolSysMT', structure_indices='all', 
        output_type='values', skip_digestion=False, **kwargs):
    from molsysmt.basic import get as msm_get
    return msm_get(item, element=element, selection=selection, syntax=syntax, 
                   structure_indices=structure_indices, output_type=output_type, 
                   skip_digestion=True, **kwargs)
