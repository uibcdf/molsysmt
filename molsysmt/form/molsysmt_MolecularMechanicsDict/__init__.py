form_name = 'molsysmt.MolecularMechanicsDict'
form_type = 'class'
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
#from .iterators import

from .to_molsysmt_MolecularMechanicsDict import to_molsysmt_MolecularMechanicsDict
from .to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics

_convert_to={
        'molsysmt.MolecularMechanicsDict': to_molsysmt_MolecularMechanicsDict,
        'molsysmt.MolecularMechanics': to_molsysmt_MolecularMechanics,
        }
