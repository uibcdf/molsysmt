form_name = 'molsysmt.MolecularMechanics'
form_type = 'class'
form_info = ["", ""]

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

_convert_to={
        'molsysmt.MolecularMechanics': extract,
        'molsysmt.MolecularMechanicsDict': to_molsysmt_MolecularMechanicsDict,
        }
