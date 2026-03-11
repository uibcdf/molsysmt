from .to_molsysmt_ViewerJSON import to_molsysmt_ViewerJSON
from .to_molsysmt_StructuresDict import to_molsysmt_StructuresDict
from .to_file_h5msm import to_file_h5msm
from .to_file_structures_yaml import to_file_structures_yaml
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_XYZ import to_XYZ
form_name = 'molsysmt.Structures'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = False
bonds_can_be_computed = False

from .is_form import is_form

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .copy import copy
from .add import add
from .merge import merge
from .append_structures import append_structures
from .get_topological_attributes import *
from .get_structural_attributes import *
from .set import *
from .iterators import StructuresIterator

_convert_to={
        'molsysmt.Structures': to_molsysmt_Structures,
        'file:h5msm': to_file_h5msm,
        'file:structures_yaml': to_file_structures_yaml,
        'molsysmt.StructuresDict': to_molsysmt_StructuresDict,
        'molsysmt.ViewerJSON': to_molsysmt_ViewerJSON,
        'XYZ': to_XYZ,
        }
