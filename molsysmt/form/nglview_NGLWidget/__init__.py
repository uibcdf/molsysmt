from molsysmt._private.argdigest import arg_digest

form_name = 'nglview.NGLWidget'
form_type = 'class'
form_info = [""]

piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = 'molsysmt.Structures'
piped_any_attribute = 'molsysmt.MolSys'
bonds_are_explicit = True
bonds_can_be_computed = True

_convert_to = {
    'nglview.NGLWidget': 'to_nglview_NGLWidget',
    'molsysmt.MolSys': 'to_molsysmt_MolSys',
    'molsysmt.Topology': 'to_molsysmt_Topology',
    'molsysmt.Structures': 'to_molsysmt_Structures',
    'openmm.Topology': 'to_openmm_Topology',
    'string:amino_acids_1': 'to_string_amino_acids_1',
    'string:amino_acids_3': 'to_string_amino_acids_3',
    'string:pdb_text': 'to_string_pdb_text',
}

from .is_form import is_form
from .has_attribute import has_attribute
from .attributes import attributes
from .extract import extract
from .add import add
from .append_structures import append_structures
from .copy import copy
from .merge import merge
from .iterators import *
from .get_topological_attributes import *
from .get_structural_attributes import *

@arg_digest(form=form_name)
def get(item, element='system', selection='all', syntax='MolSysMT', structure_indices='all', 
        output_type='values', skip_digestion=False, **kwargs):
    from molsysmt.basic import get as msm_get
    return msm_get(item, element=element, selection=selection, syntax=syntax, 
                   structure_indices=structure_indices, output_type=output_type, 
                   skip_digestion=True, **kwargs)

@arg_digest(form=form_name)
def set(item, element='system', selection='all', syntax='MolSysMT', structure_indices='all', 
        skip_digestion=False, **kwargs):
    from molsysmt.basic import set as msm_set
    return msm_set(item, element=element, selection=selection, syntax=syntax, 
                   structure_indices=structure_indices, skip_digestion=True, **kwargs)
