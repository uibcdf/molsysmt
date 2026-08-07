from molsysmt._private.argdigest import arg_digest

form_name = 'molsysmt.PDBFileHandler'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = 'molsysmt.Structures'
piped_any_attribute = None
bonds_are_explicit = True
bonds_can_be_computed = True

_convert_to = {
    'molsysmt.PDBFileHandler': 'to_molsysmt_PDBFileHandler',
    'molsysmt.Topology': 'to_molsysmt_Topology',
    'molsysmt.Structures': 'to_molsysmt_Structures',
    'molsysmt.MolSys': 'to_molsysmt_MolSys',
    'nglview.NGLWidget': 'to_nglview_NGLWidget',
}

from .to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_nglview_NGLWidget import to_nglview_NGLWidget

from .is_form import is_form
from .has_attribute import has_attribute
from . import iterators

from .attributes import attributes
from .extract import extract
from .copy import copy
from .add import add
from .merge import merge
from .append_structures import append_structures
from .get_topological_attributes import *
from .get_structural_attributes import *
from .set import *

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

@arg_digest(form=form_name)
def extract(item, selection='all', structure_indices='all', syntax='MolSysMT', 
            output_filename=None, copy_if_all=True, skip_digestion=False):
    from molsysmt.basic import extract as msm_extract
    return msm_extract(item, selection=selection, structure_indices=structure_indices, 
                       syntax=syntax, output_filename=output_filename, 
                       copy_if_all=copy_if_all, skip_digestion=True)
