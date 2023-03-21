form_name = 'molsysmt.MolecularMechanicsDict'
form_type = 'class'
form_info = ["", ""]

from .is_form import is_form

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .copy import copy
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
#from .iterators import

from .to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics

_convert_to={
        'molsysmt.MolecularMechanicsDict': extract,
        'molsysmt.MolecularMechanics': to_molsysmt_MolecularMechanics,
        }
